#include "aes_data.h"
#include <stdio.h>
uint8_t GF2_8_mul(uint8_t a, uint8_t b) {
  /*The primitive polynomial is x^8 + x^4 + x^3 + x + 1*/
  uint8_t ans = 0;
  for (int i = 0; i < 8; ++i) {
    if (a & 0x01) {
      ans ^= b;
    }
    int flag = (b & 0x80);
    b = b << 1;
    if (flag) {
      b ^= 0x1b; /*x^8 -> x^4 + x^3 + x + 1*/
    }
    a = a >> 1;
  }
  return ans;
}

void getTe(uint8_t S[]) {
  int count = 0;
  for (int j = 0; j < 256; ++j) {
    uint8_t input = (j & 0xff);
    printf("0x%08x, ", (uint32_t)((GF2_8_mul(0x1u, S[input]) << 24) +
                                  (GF2_8_mul(0x1u, S[input]) << 16) +
                                  (GF2_8_mul(0x3u, S[input]) << 8) +
                                  (GF2_8_mul(0x2u, S[input]))));
    count++;
    if (count == 17) {
      printf("\n");
      count = 0;
    }
  }
}
int main(){
	getTe(S);
}
