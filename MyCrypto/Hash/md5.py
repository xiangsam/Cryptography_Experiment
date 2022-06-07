'''
Author: Samrito
Date: 2022-06-06 21:42:03
LastEditors: Samrito
LastEditTime: 2022-06-07 00:03:10
'''
# -*- coding:utf-8 -*-
#! /usr/bin/python3

import math
import hashlib
from re import L  #used to check the answer


class MD5:
    """
    I try to imitate the function used in hashlib
    """

    def __init__(self):
        self._A = 0x67452301
        self._B = 0xefcdab89
        self._C = 0x98badcfe
        self._D = 0x10325476
        self._digest = b''
        self.K = [(int(4294967296 * abs(math.sin(i))) & 0xffffffff)
                  for i in range(1, 65)]
        self.s = [
            7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9,
            14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 4, 11, 16, 23, 4,
            11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15,
            21, 6, 10, 15, 21, 6, 10, 15, 21
        ]

    def _process(self, block):
        M = [block[4 * i:4 * (i + 1)] for i in range(64 // 4)]
        for i in range(16):
            M[i] = int.from_bytes(M[i], 'little')
        F = lambda x, y, z: ((x & y) | ((~x) & z))
        G = lambda x, y, z: ((x & z) | (y & (~z)))
        H = lambda x, y, z: (x ^ y ^ z)
        I = lambda x, y, z: (y ^ (x | (~z)))
        lshift = lambda x, n: (((x << n) | (x >>
                                            (32 - n))) & (0xffffffff))  #循环左移

        a, b, c, d = self._A, self._B, self._C, self._D
        for i in range(64):
            if i < 16:
                H0 = F(b, c, d) & 0xffffffff
                g = i
            elif i < 32:
                H0 = G(b, c, d) & 0xffffffff
                g = (5 * i + 1) % 16
            elif i < 48:
                H0 = H(b, c, d) & 0xffffffff
                g = (3 * i + 5) % 16
            else:
                H0 = I(b, c, d) & 0xffffffff
                g = (7 * i) % 16
            tmp = d
            d = c
            c = b
            tmp2 = (a + H0 + M[g] + self.K[i]) & 0xffffffff
            step = self.s[i]
            b = (b + lshift(tmp2, step)) & 0xffffffff
            a = tmp
        return (a + self._A) & 0xffffffff, (b + self._B) & 0xffffffff, (
            c + self._C) & 0xffffffff, (d + self._D) & 0xffffffff

    def update(self, data):
        """data is bytesStr"""
        assert isinstance(data, bytes)
        assert len(
            data) < 2**61  #the bits length of data should be less than 2^64
        dataLen = len(data)
        if dataLen % 64 <= 56:
            padLen = 56 - dataLen % 64
        else:
            padLen = 56 + 64 - dataLen % 64
        pad = 0b10000000
        if not padLen == 0:
            data += pad.to_bytes(padLen, 'little')  #数据填充
        data += (8 * dataLen).to_bytes(8, 'little')  #添加原始数据长度
        block = [data[64 * i:64 * (i + 1)] for i in range(len(data) // 64)]
        for e in block:
            A, B, C, D = self._process(e)
            self._A = A
            self._B = B
            self._C = C
            self._D = D

        self._digest = b''.join([
            self._A.to_bytes(4, 'little'),
            self._B.to_bytes(4, 'little'),
            self._C.to_bytes(4, 'little'),
            self._D.to_bytes(4, 'little')
        ])

        self._A = 0x67452301
        self._B = 0xEFCDAB89
        self._C = 0x98BADCFE
        self._D = 0x10325476

    def digest(self):
        return self._digest

    def hexdigest(self):
        return self._digest.hex()


if __name__ == '__main__':
    #  message1 = b'The quick brown fox jumps over the lazy dog'
    #  message2 = b'abcdef'
    #  sha1 = SHA1()
    #  sha1.update(message1)
    #  print(sha1.digest())
    #  sha1.update(message2)
    #  print(sha1.digest())
    #  sha1.update(message2)
    #  print(sha1.digest())

    #  s = hashlib.sha1()
    #  s.update(message2)
    #  print(s.digest())
    message = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    s1 = MD5()
    s1.update(message)
    print('message: ', message)
    print('hexDigest: ', s1.hexdigest())
    s2 = hashlib.md5()
    s2.update(message)
    print(s2.hexdigest())
