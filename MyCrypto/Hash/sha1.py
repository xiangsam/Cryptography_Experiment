# -*- coding:utf-8 -*-
#! /usr/bin/python3

import hashlib#used to check the answer

class SHA1:
    """
    I try to imitate the function used in hashlib
    """
    def __init__(self):
        self._A = 0x67452301
        self._B = 0xEFCDAB89
        self._C = 0x98BADCFE
        self._D = 0x10325476
        self._E = 0xC3D2E1F0
        self._digest = b''
    
    def _lshift(self, x, step):
        """
        x is int
        """
        return ((x << step) | (x >> (32-step)))&0xffffffff

    def _process(self, block):
        M = [block[4*i:4*(i+1)] for i in range(64//4)]
        for i in range(16):
            M[i] = int.from_bytes(M[i],'big')
        for i in range(16, 80):
            M.append(self._lshift(M[i-3]^M[i-8]^M[i-14]^M[i-16],1))
        f1 = lambda b,c,d : (b & c) | (~b & d)
        f2 = lambda b,c,d : b^c^d
        f3 = lambda b,c,d : (b&c) | (b&d) | (c&d)
        f4 = lambda b,c,d : b^c^d
        A, B, C ,D, E = self._A, self._B, self._C, self._D, self._E
        for i in range(80):
            if i < 20:
                H0 = (self._lshift(A, 5)+f1(B,C,D)+E + M[i] + 0x5A827999)&0xffffffff
            elif i < 40:
                H0 = (self._lshift(A, 5)+f2(B,C,D)+E + M[i] + 0x6ED9EBA1)&0xffffffff
            elif i < 60:
                H0 = (self._lshift(A, 5)+f3(B,C,D)+E + M[i] + 0x8F1BBCDC)&0xffffffff
            else:
                H0 = (self._lshift(A, 5)+f4(B,C,D)+E + M[i] + 0xCA62C1D6)&0xffffffff
            E = D
            D = C
            C = self._lshift(B, 30)
            B = A
            A = H0
        return (A+self._A)&0xffffffff, (B+self._B)&0xffffffff, (C+self._C)&0xffffffff, (D+self._D)&0xffffffff, (E+self._E)&0xffffffff

    def update(self, data):
        """data is bytesStr"""
        assert isinstance(data, bytes)
        assert len(data) < 2**61 #the bits length of data should be less than 2^64
        dataLen = len(data)
        if dataLen % 64 <= 56:
            padLen = 56 - dataLen % 64
        else:
            padLen = 56 + 64 - dataLen % 64
        pad = 0b10000000
        if not padLen == 0:
            data += pad.to_bytes(padLen, 'little')
        data += (8*dataLen).to_bytes(8, 'big')
        block = [data[64*i:64*(i+1)] for i in range(len(data)//64)]
        for i, e in enumerate(block):
            if i == 0:
                A, B, C, D, E = self._process(e)
            else:
                A, B, C, D, E = self._process(e)
            self._A = A
            self._B = B
            self._C = C
            self._D = D
            self._E = E
        self._digest = b''.join([A.to_bytes(4,'big'),B.to_bytes(4, 'big'), C.to_bytes(4, 'big'),D.to_bytes(4,'big'),E.to_bytes(4,'big')])
        self._A = 0x67452301
        self._B = 0xEFCDAB89
        self._C = 0x98BADCFE
        self._D = 0x10325476
        self._E = 0xC3D2E1F0

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
    message = b'abd'
    s1 = SHA1()
    s1.update(message)
    print('message: ', message)
    print('hexDigest: ', s1.hexdigest())
