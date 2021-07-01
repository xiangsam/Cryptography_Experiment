# -*- coding:utf-8 -*-
#! /usr/bin/python3

import sys
sys.path.append('../..')
from MyCrypto.util.inverse_mod import inverse_mod
from MyCrypto.util.pow_modual import quickPow
from MyCrypto.Hash.sha1 import SHA1

from random import randint
from Crypto.Util.number import getPrime

def n2s(n):
    nbits = n.bit_length()
    nbytes = (nbits + 7) >> 3
    return n.to_bytes(nbytes, 'big')

class Schnorr_DSA:
    def __init__(self, p, q, a):
        assert (p-1) % q == 0
        assert quickPow(a, q, p) == 1
        self._p = p
        self._q = q
        self._a = a

    def genKey(self):
        '''
        return (priK, pubK)
        '''
        priK = randint(1, self._q - 1)
        pubK = inverse_mod(quickPow(self._a, priK, self._p),self._p)
        return priK, pubK

    def sign(self, message, priK):
        assert isinstance(message, bytes)
        r = randint(1, self._q-1)
        x = quickPow(self._a, r, self._p)
        sha = SHA1()
        sha.update(message+n2s(x))
        e = int.from_bytes(sha.digest(), 'big')
        y = (r + priK * e) % self._q
        return e, y

    def verify(self, message, sign, pubK):
        e, y = sign
        xx = (quickPow(self._a, y, self._p) * quickPow(pubK, e, self._p))%self._p
        sha = SHA1()
        sha.update(message + n2s(xx))
        if e == int.from_bytes(sha.digest(), 'big'):
            return True
        return False


if __name__ == '__main__':
    dsa = Schnorr_DSA(19, 3,1 )
    message = b'hello'
    priK, pubK = dsa.genKey()
    print('priK: ', priK)
    print('pubK: ', pubK)
    sign = dsa.sign(message, priK)
    print('digital sign: ', sign)
    print('if receive message: ', message)
    print('verify result: ', dsa.verify(message, sign, pubK))
    message += b'w'
    print('if receive message: ', message)
    print('verify result: ', dsa.verify(message, sign, pubK))
