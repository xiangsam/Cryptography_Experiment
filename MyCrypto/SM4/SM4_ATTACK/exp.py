# -*- coding:utf-8 -*-
#! /usr/bin/python3

from pwn import *
from Crypto.Util.number import getRandomNBitInteger,long_to_bytes, bytes_to_long

import sys
sys.path.append('../../..')
from MyCrypto.SM4.SM4_ATTACK.func import xor, rotl, get_uint32_be,\
        put_uint32_be, padding, unpadding, list_to_bytes, bytes_to_list
#the function xor has the same name with xor in pwnlib.......
from MyCrypto.SM4.SM4_ATTACK.sm4 import SM4_BOXES_TABLE, SM4_FK, SM4_CK,CryptSM4
from MyCrypto.SM4.SM4_ATTACK.sm4_dfa import SM4DFA

def encrypt1(p,pt):
    p.recvuntil('> ')
    p.sendline('1')
    p.recvuntil('your plaintext in hex')
    p.sendline(pt)
    p.recvuntil('your ciphertext in hex:')
    ct = p.recvuntil('\n')[:-1]
    return ct

def encrypt2(p, pt, r, f, place):
    p.recvuntil('> ')
    p.sendline('2')
    p.recvuntil('your plaintext in hex')
    p.sendline(pt)
    p.recvuntil('give me the value of r f p')
    payload  = str(r) + ' ' + str(f) + ' ' + str(place)
    p.sendline(payload)
    p.recvuntil('your ciphertext in hex:')
    ct = p.recvuntil('\n')[:-1]
    return ct

def decrypt(p, ct, key):
    p.recvuntil('> ')
    p.sendline('3')
    p.recvuntil('your key in hex')
    p.sendline(key)
    p.recvuntil('your ciphertext in hex')
    p.sendline(ct)
    p.recvuntil('your plaintext in hex:')
    pt = p.recvuntil('\n')[:-1]
    return pt

def injectByte(p, target, _round, roundKey,injectTimes):
    lastRound = False
    if _round == 32:
        lastRound = True
        _round = 31
    sm4dfa = SM4DFA()
    if lastRound == False:
        place = 4 + target #in x0, x1, x2,x3, we choose inject x1
    else:
        place = target
    f = randint(1, 0xff) #the injected fault
    for i in range(injectTimes):
        pt = getRandomNBitInteger(128)
        pt = hex(pt).replace('0x','').zfill(32)
        ct1 = long_to_bytes(int(encrypt1(p, pt), 16))[:16] #the ct has 32 bytes, the last 16 bytes are from padding
        ct2 = long_to_bytes(int(encrypt2(p, pt, _round, f, place), 16))[:16]
        sm4dfa.update(ct1,ct2)
    if lastRound == True:
        set1 = set(sm4dfa.dfa(roundKey,32,target))
    else:
        set1 = set(sm4dfa.dfa(roundKey, _round, target))
    
    sm4dfa.reset()
    f = randint(1, 0xff) #the injected fault
    for i in range(injectTimes):
        pt = getRandomNBitInteger(128)
        pt = hex(pt).replace('0x','').zfill(32)
        ct1 = long_to_bytes(int(encrypt1(p, pt), 16))[:16] #the ct has 32 bytes, the last 16 bytes are from padding
        ct2 = long_to_bytes(int(encrypt2(p, pt, _round, f, place), 16))[:16]
        sm4dfa.update(ct1,ct2)
    if lastRound == True:
        set2 = set(sm4dfa.dfa(roundKey, 32, target))
    else:
        set2 = set(sm4dfa.dfa(roundKey, _round, target))
    ans = list(set1&set2)
    return ans[0]

def attackRoundKey(p,_round,roundKey):
    keys = []
    for i in range(4):
        print('attack the %dth bytes...' % i)
        key = injectByte(p, i, _round, roundKey,3)
        keys.append(key)
    return keys

def resumeRoundKey(roundKey):#resume all roundKey from the last 4 rounds
    _roundKey = [0]*32 + roundKey[::-1]
    for i in range(31,-1,-1):
        _roundKey[i] = _roundKey[i+4] ^ CryptSM4._round_key(_roundKey[i+1]^_roundKey[i+2]^_roundKey[i+3]^SM4_CK[i])
    MK = xor(_roundKey[0:4], SM4_FK[0:4])
    f = lambda key_data:(key_data[0] << 96) | (key_data[1] << 64) | (key_data[2] << 32) | (key_data[3])
    return long_to_bytes(f(MK))

p = remote('10.212.25.14',23367)
p.recvuntil('your flag is\n')
enc_flag = p.recvuntil('\n')[:-1]
roundKey = []
for i in range(32,28,-1):
    if i == 32:
        print('inject round: 32(31)')
    else:
        print('inject round: ', i)
    keys = attackRoundKey(p, i,roundKey)
    print('attacked RoundKey: ', keys)
    roundKey.append(keys)
roundKey = [get_uint32_be(e) for e in roundKey]
attack_key = resumeRoundKey(roundKey)
attack_key = hex(bytes_to_long(attack_key))[2:].zfill(32)
print("attacked key : ",attack_key)
flag = decrypt(p,enc_flag,attack_key)
flag = long_to_bytes(int(flag.decode("utf-8"),16))
print('attacked flag : ',flag)
p.interactive()
