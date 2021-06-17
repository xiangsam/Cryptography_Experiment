/*only linux supported*/
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/time.h>

#include "aes_data.h"

#define gFun(w)                                               \
  ((S[(w >> 16) & 0xff] << 24) + (S[(w >> 8) & 0xff] << 16) + \
   (S[w & 0xff] << 8) + (S[(w >> 24) & 0xff]))
#define TeChange(r, roundKey, i)                                               \
  r[0] = Te0[s[0]] ^ Te1[s[5]] ^ Te2[s[10]] ^ Te3[s[15]] ^ roundKey[4 * i];    \
  r[1] = Te0[s[4]] ^ Te1[s[9]] ^ Te2[s[14]] ^ Te3[s[3]] ^ roundKey[4 * i + 1]; \
  r[2] = Te0[s[8]] ^ Te1[s[13]] ^ Te2[s[2]] ^ Te3[s[7]] ^ roundKey[4 * i + 2]; \
  r[3] = Te0[s[12]] ^ Te1[s[1]] ^ Te2[s[6]] ^ Te3[s[11]] ^ roundKey[4 * i + 3];

#define TdChange(r, roundKey, i)                                               \
  r[0] = Td0[s[0]] ^ Td1[s[13]] ^ Td2[s[10]] ^ Td3[s[7]] ^ roundKey[4 * i];    \
  r[1] =                                                                       \
      Td0[s[4]] ^ Td1[s[1]] ^ Td2[s[14]] ^ Td3[s[11]] ^ roundKey[4 * i + 1];   \
  r[2] = Td0[s[8]] ^ Td1[s[5]] ^ Td2[s[2]] ^ Td3[s[15]] ^ roundKey[4 * i + 2]; \
  r[3] = Td0[s[12]] ^ Td1[s[9]] ^ Td2[s[6]] ^ Td3[s[3]] ^ roundKey[4 * i + 3];

#define wordsToBytes(s, r, j)         \
  s[4 * j] = (r[j] >> 24) & 0xff;     \
  s[4 * j + 1] = (r[j] >> 16) & 0xff; \
  s[4 * j + 2] = (r[j] >> 8) & 0xff;  \
  s[4 * j + 3] = r[j] & 0xff;

void getRoundKey(uint32_t roundKey[], uint8_t key[]) {
  for (int i = 0; i < 4; ++i) {
    roundKey[i] = (key[4 * i] << 24) + (key[4 * i + 1] << 16) +
                  (key[4 * i + 2] << 8) + (key[4 * i + 3]);
  }
  uint32_t *ptr = roundKey;
  for (int i = 0; i < 10; ++i) {
    ptr[4] = ptr[0] ^ gFun(ptr[3]) ^ rcon[i];
    ptr[5] = ptr[1] ^ ptr[4];
    ptr[6] = ptr[2] ^ ptr[5];
    ptr[7] = ptr[3] ^ ptr[6];
    ptr += 4;
  }
  return;
}
void encrypt(uint8_t block[], uint32_t roundKey[]) {
  uint8_t s[16];
  uint32_t r[4];
  for (int i = 0; i < 4; ++i) {
    s[4 * i] = block[4 * i] ^ ((roundKey[i] >> 24) & 0xff);
    s[4 * i + 1] = block[4 * i + 1] ^ ((roundKey[i] >> 16) & 0xff);
    s[4 * i + 2] = block[4 * i + 2] ^ ((roundKey[i] >> 8) & 0xff);
    s[4 * i + 3] = block[4 * i + 3] ^ ((roundKey[i]) & 0xff);
  }
  for (int i = 1; i < 10; ++i) {
    TeChange(r, roundKey, i);
    for (int j = 0; j < 4; ++j) {
      wordsToBytes(s, r, j);
    }
  }
  for (int i = 0; i < 4; ++i) {
    block[4 * i] = S[s[4 * i]] ^ ((roundKey[40 + i] >> 24) & 0xff);
    block[4 * i + 1] =
        S[s[(4 * (i + 1) + 1) % 16]] ^ ((roundKey[40 + i] >> 16) & 0xff);
    block[4 * i + 2] =
        S[s[(4 * (i + 2) + 2) % 16]] ^ ((roundKey[40 + i] >> 8) & 0xff);
    block[4 * i + 3] =
        S[s[(4 * (i + 3) + 3) % 16]] ^ ((roundKey[40 + i]) & 0xff);
  }
  return;
}
void decrypt(uint8_t block[], uint32_t roundKey[]) {
  uint8_t s[16];
  uint32_t r[4];
  for (int i = 0; i < 4; ++i) {
    s[4 * i] = block[4 * i] ^ ((roundKey[40 + i] >> 24) & 0xff);
    s[4 * i + 1] = block[4 * i + 1] ^ ((roundKey[40 + i] >> 16) & 0xff);
    s[4 * i + 2] = block[4 * i + 2] ^ ((roundKey[40 + i] >> 8) & 0xff);
    s[4 * i + 3] = block[4 * i + 3] ^ ((roundKey[40 + i]) & 0xff);
  }
  for (int i = 9; i > 0; --i) {
    TdChange(r, roundKey, i);
    for (int j = 0; j < 4; ++j) {
      wordsToBytes(s, r, j);
    }
  }
  for (int i = 0; i < 4; ++i) {
    block[4 * i] = inv_S[s[4 * i]] ^ ((roundKey[i] >> 24) & 0xff);
    block[4 * i + 1] =
        inv_S[s[(4 * (i + 3) + 1) % 16]] ^ ((roundKey[i] >> 16) & 0xff);
    block[4 * i + 2] =
        inv_S[s[(4 * (i + 2) + 2) % 16]] ^ ((roundKey[i] >> 8) & 0xff);
    block[4 * i + 3] =
        inv_S[s[(4 * (i + 1) + 3) % 16]] ^ ((roundKey[i]) & 0xff);
  }
  return;
}

double aesEncryptECB(uint8_t plain[], uint8_t key[]) {
  struct timeval start, end;
  uint32_t roundKey[44];
  uint32_t plainLen = strlen(plain);
  uint32_t padLen = 16u - plainLen % 16u;
  uint8_t pad[17];
  pad[16] = '\0';
  memset(pad, (uint8_t)(padLen & 0xff), padLen);
  if (padLen < 16) memset(pad + padLen, '\0', 16 - padLen);
  strcat(plain, pad);
  int i = 0;
  gettimeofday(&start, 0);
  getRoundKey(roundKey, key);
  while (*(plain + 16 * i) != '\0') {
    encrypt(plain + 16 * i, roundKey);
    /* for(int j = 0; j < 16; ++j) */
    /* printf("%02x", plain[j+16*i]); */
    i += 1;
  }
  gettimeofday(&end, 0);
  double timeused =
      1000000 * (end.tv_sec - start.tv_sec) + end.tv_usec - start.tv_usec;
  return timeused;
}
double aesDecrypeECB(uint8_t cypher[], uint8_t key[]) {
  struct timeval start, end;
  uint32_t roundKey[44];
  gettimeofday(&start, 0);
  getRoundKey(roundKey, key);
  for (int i = 4; i < 40; ++i) {
    roundKey[i] = Td0[S[(roundKey[i] >> 24) & 0xff]] ^
                  Td1[S[(roundKey[i] >> 16) & 0xff]] ^
                  Td2[S[(roundKey[i] >> 8) & 0xff]] ^
                  Td3[S[(roundKey[i]) & 0xff]];
  }
  int i = 0;
  while (*(cypher + 16 * i) != '\0') {
    decrypt(cypher + 16 * i, roundKey);
    /* for(int j = 0; j < 16; ++j){
             printf("%c", cypher[j+16*i]);
     } */
    i += 1;
  }
  gettimeofday(&end, 0);
  double timeused =
      1000000 * (end.tv_sec - start.tv_sec) + end.tv_usec - start.tv_usec;
  return timeused;
}
int main(int argv, char *argc[]) {
  uint8_t key[16] = {0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
                     0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c};
  // uint8_t plain[16] = {0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31,
  // 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34}; uint8_t cypher[16] = {0x39, 0x25,
  // 0x84, 0x1D, 0x02, 0xDC, 0x09, 0xFB, 0xDC, 0x11, 0x85, 0x97, 0x19, 0x6A,
  // 0x0B, 0x32}; encrypt(plain,key); decrypt(cypher, key);
  struct stat statbuff;
  stat("test", &statbuff);
  int bitSize = 8 * statbuff.st_size;
  double encryptTime = 0;
  double decryptTime = 0;
  for (int i = 0; i < 20000; ++i) {
    FILE *f = fopen("test", "r");
    char plain[200000];
    fgets(plain, 100000, f);
    /* puts(plain); */
    uint8_t *message;
    if (strlen(plain) % 16 != 0)
      message = (uint8_t *)malloc(sizeof(uint8_t) *
                                  (strlen(plain) + strlen(plain) % 16));
    else
      message = (uint8_t *)malloc(sizeof(uint8_t) * (strlen(plain) + 16));
    strcpy(message, plain);
    encryptTime += aesEncryptECB(message, key);
    decryptTime += aesDecrypeECB(message, key);
    free(message);
    fclose(f);
  }
  encryptTime /= 20000;
  decryptTime /= 20000;
  printf("encrypt speed: %lf Mbits/s\n",
         (bitSize / encryptTime) * 1000000 / (1024 * 1024));
  printf("decrypt speed: %lf Mbits/s\n",
         (bitSize / decryptTime) * 1000000 / (1024 * 1024));
  return 0;
}
