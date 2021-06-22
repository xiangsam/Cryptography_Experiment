# -*- coding:utf-8 -*-
#!/usr/bin/python3

from Crypto.Util.number import getRandomNBitInteger,long_to_bytes, bytes_to_long

import sys
sys.path.append('../../..')
from MyCrypto.SM4.SM4_ATTACK.func import xor, rotl, get_uint32_be,\
        put_uint32_be, padding, unpadding, list_to_bytes, bytes_to_list
#the function xor has the same name with xor in pwnlib.......
from MyCrypto.SM4.SM4_ATTACK.sm4 import SM4_BOXES_TABLE, SM4_FK, SM4_CK,CryptSM4


class SM4DFA():
    def __init__(self):
        self._trueCyphers = []
        self._falseCyphers = []
    
    def reset(self):
        self._trueCyphers = []
        self._falseCyphers = []

    def update(self, trueCypher,falseCypher):
        self._trueCyphers.append(trueCypher)
        self._falseCyphers.append(falseCypher)
    
    def dfa(self, after_roundKey ,_round, target):
        key = []
        for k in range(256):#k is possible key
            for a, b in zip(self._trueCyphers, self._falseCyphers):
                trueCypher = SM4DFA._byte_to_words(a)
                falseCypher = SM4DFA._byte_to_words(b)
                trueCypher = SM4DFA._invR(trueCypher)
                falseCypher = SM4DFA._invR(falseCypher)
                if _round < 32:
                    for i in range(32-_round):
                        trueCypher = self.lookBack(after_roundKey,trueCypher, 32-i)
                        falseCypher = self.lookBack(after_roundKey,falseCypher, 32-i)
                tx1, tx2, tx3, tx4 = trueCypher
                fx1, fx2, fx3, fx4 = falseCypher

                out_diff = SM4DFA._invL(fx4 ^ tx4)
                in_diff = (tx1 ^ fx1) ^ (tx2 ^ fx2) ^ (tx3 ^ fx3)
                inv_put_uint32_be = lambda n:[((n)&0xff), ((n>>8)&0xff), ((n>>16)&0xff), ((n>>24)&0xff)]
                Sa = inv_put_uint32_be(out_diff)
                Sa = Sa[3-target]
                Sb = SM4_BOXES_TABLE[((fx3 ^ fx2 ^ fx1) >> (3-target) * 8) & 0xff ^ k] #Sbox output contains fault
                Sc = SM4_BOXES_TABLE[((fx3 ^ fx2 ^ fx1 ^ in_diff) >> (3-target) * 8) & 0xff ^ k] #Sbox output doesn't contain fault
                if Sa == Sb ^ Sc:
                    if not k in key:
                        key.append(k)
                        break
        return key
        

    def lookBack(self, after_roundKey,output, _round):#get the input of this round
        x1, x2, x3, x4 = output
        key = get_uint32_be(after_roundKey[32-_round])
        sboxIn = x1 ^ x2 ^ x3 ^ key
        sboxOut = [0,0,0,0]
        sboxIn = put_uint32_be(sboxIn)
        sboxOut[0] = SM4_BOXES_TABLE[sboxIn[0]]
        sboxOut[1] = SM4_BOXES_TABLE[sboxIn[1]]
        sboxOut[2] = SM4_BOXES_TABLE[sboxIn[2]]
        sboxOut[3] = SM4_BOXES_TABLE[sboxIn[3]]
        sboxOut = get_uint32_be(sboxOut)
        c = SM4DFA._L(sboxOut)
        x0 = x4 ^ c
        _input = x0, x1, x2, x3
        return _input
    
    @staticmethod
    def _invR(Y):#R is the inverse operation in the end
        return Y[::-1]
    
    @staticmethod
    def _byte_to_words(byteStr):
        x = bytes_to_long(byteStr)
        return [(x>>96) & 0xffffffff, (x>>64) & 0xffffffff, (x>>32) & 0xffffffff, x & 0xffffffff]
    @staticmethod
    def _L(B):
        return B ^ rotl(B, 2) ^ rotl(B,10) ^ rotl(B,18) ^ rotl(B, 24)

    @staticmethod
    def _invL(C):
        return C ^ rotl(C,2) ^ rotl(C,4) ^ rotl(C, 8) ^ rotl(C, 12) ^ rotl(C, 14)\
                ^ rotl(C, 16) ^ rotl(C, 18) ^ rotl(C, 22) ^ rotl(C, 24) ^ rotl(C, 30)

