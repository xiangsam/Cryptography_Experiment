# -*- coding:utf-8 -*-
#! /usr/bin/python3

import sys
sys.path.append('../..')
from MyCrypto.util.pow_modual import quickPow
from MyCrypto.util.gcd import gcd
from MyCrypto.util.inverse_mod import inverse_mod
from MyCrypto.Hash.sha1 import SHA1

from random import randint

class ElGamal_DSA:
    def __init__(self, q, a):
        self._a = a
        assert q > 2
        self._q = q
    
    def genKey(self):
        priK = randint(2, self._q-1)
        pubK = quickPow(self._a, priK, self._q)
        return priK, pubK

    def sign(self, message, priK):
        sha = SHA1()
        sha.update(message)
        m = int.from_bytes(sha.digest(), 'big') % self._q
        k = 0
        while k == 0:
            tk = randint(1, self._q-1)
            if gcd(tk, self._q -1) == 1:
                k = tk
        S1 = quickPow(self._a, k, self._q)
        inv_k = inverse_mod(k, self._q -1)
        S2 = (inv_k * (m-priK * S1) ) % (self._q - 1)
        return S1, S2

    def verify(self, message ,sign, pubK):
        S1, S2 = sign
        sha = SHA1()
        sha.update(message)
        m = int.from_bytes(sha.digest(), 'big') % self._q
        V1 = quickPow(self._a, m, self._q)
        V2 = (quickPow(pubK, S1, self._q)*quickPow(S1, S2, self._q)) % self._q
        return V1 == V2

if __name__ == '__main__':
    dsa = ElGamal_DSA(19, 10)
    priK, pubK = dsa.genKey()
    message = b'dsallo'
    print('private Key: ', priK)
    print('public Key: ', pubK)
    sign = dsa.sign(message, priK)
    print('digital sign: ', sign)
    print('if receive message: ', message)
    print('sign verified? ', dsa.verify(message, sign, pubK))
    message = message + b'w'
    print('if receive message: ', message)
    print('sign verified? ', dsa.verify(message, sign, pubK))
