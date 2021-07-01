# -*- coding:utf-8 -*-
#! /usr/bin/python3

from Crypto.Util.number import getPrime 
import math
import sys
from random import randbytes
sys.path.append('../..')
from MyCrypto.Hash.sha1 import SHA1
from MyCrypto.util.inverse_mod import inverse_mod
from MyCrypto.util.pow_modual import quickPow

class RSA_PSS:
    def __init__(self, p, q):
        """
        p, q is primeNumber, n is the modulo of RSA
        """
        self._hlen = 20
        self._slen = self._hlen
        self._n = p * q
        self._phin = (p-1)*(q-1)
        self._bc = b'\xbc'

    def genKey(self):
        pubK = 65537
        phi_n = self._phin
        priK = inverse_mod(pubK, phi_n)
        return priK, pubK

    def sign(self, message:bytes, emBits, priK):
        #get EM
        Hash = SHA1()
        emLen = math.ceil(emBits / 8)
        pad1 = b'\x00' * 8
        one = 1
        pad2 = one.to_bytes(emLen - self._slen - self._hlen - 2,'big')
        #pad2 = one.to_bytes(emLen - self._slen - self._hlen - 1,'big')
        Hash.update(message)
        mHash = Hash.digest()
        salt = randbytes(self._slen)
        M = b''.join([pad1, mHash, salt])
        Hash.update(M)
        H = Hash.digest()
        DB = b''.join([pad2, salt])
        dbMask = self.MGF(H, emLen-self._hlen - 1)
        maskedDB = int.from_bytes(DB, 'big') ^ int.from_bytes(dbMask, 'big')
        maskedDB = maskedDB.to_bytes(max(len(DB), len(dbMask)), 'big')
        temp = maskedDB[0]
        maskedDB = maskedDB[1:]
        temp = ((temp<<(8*emLen-emBits)) & 0xff) >> (8*emLen - emBits)
        temp = temp.to_bytes(1, 'big')
        maskedDB = temp + maskedDB
        EM = b''.join([maskedDB, H, self._bc])
        #get sign
        m = int.from_bytes(EM, 'big')
        s = quickPow(m, priK, self._n)
        k = (self._n.bit_length()+7)>>3
        return s.to_bytes(k,'big')

    def verify(self, message:bytes, sign, emBits, pubK):
        emLen = math.ceil(emBits / 8)
        #get EM
        s = int.from_bytes(sign, 'big')
        m = quickPow(s, pubK, self._n)
        EM = m.to_bytes(emLen, 'big')

        #EM verify
        Hash = SHA1()
        pad1 = b'\x00' * 8
        one = 1
        pad2 = one.to_bytes(emLen - self._slen - self._hlen - 2,'big')
        #pad2 = one.to_bytes(emLen - self._slen - self._hlen - 1,'big')
        Hash.update(message)
        mHash = Hash.digest()
        if emLen < self._hlen + self._slen + 2:
            return False
        if EM[-1:] != self._bc:
            return False
        maskedDB = EM[:emLen - self._hlen - 1]
        H = EM[emLen-self._hlen - 1:-1]
        temp = maskedDB[0]
        tempmask = (0xff >> (8 - 8*emLen + emBits)) << (8 - 8*emLen + emBits)
        if (temp & tempmask) != 0:
            return False
        dbMask = self.MGF(H, emLen - self._hlen - 1)
        DB = int.from_bytes(maskedDB, 'big') ^ int.from_bytes(dbMask, 'big')
        DB = DB.to_bytes(max(len(dbMask), len(maskedDB)), 'big')
        temp = DB[0]
        DB = DB[1:]
        temp = ((temp<<(8*emLen-emBits)) & 0xff) >> (8*emLen - emBits)
        temp = temp.to_bytes(1, 'big')
        DB = temp + DB
        if int.from_bytes(DB[:emLen-self._hlen - self._slen - 1], 'big') != int.from_bytes(pad2,'big'):
            return False
        salt = DB[-self._slen:]
        M = b''.join([pad1, mHash, salt])
        Hash.update(M)
        HH = Hash.digest()
        if H == HH:
            return True
        return False

    def MGF(self, X, maskLen):
        T = b''
        Hash = SHA1()
        k = math.ceil(maskLen / self._hlen) - 1
        for counter in range(k+1):
            Hash.update(X+counter.to_bytes(4, 'big'))
            T = T + Hash.digest()
        return T[0:maskLen]

if __name__ == '__main__':
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        n = p * q
        if n.bit_length() == 2048:
            break
    print('p: ', p)
    print('q: ', q)
    print('n: ', n)
    emBits = n.bit_length()-1
    dsa = RSA_PSS(p, q)
    message = b'hello,world'
    priK, pubK = dsa.genKey()
    sign = dsa.sign(message, emBits,priK)
    print('sign: ', sign)
    print('if receive message: ', message)
    print('verified? ', dsa.verify(message, sign, emBits, pubK))
    message += b'w'
    print('if receive message: ', message)
    print('verified? ', dsa.verify(message, sign, emBits, pubK))
