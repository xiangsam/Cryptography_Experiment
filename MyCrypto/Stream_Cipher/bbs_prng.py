# -*- coding:utf-8 -*-

import sys
sys.path.append('../..')
from MyCrypto.util.Miler_Rabin import Miler_Rabin
from MyCrypto.util.gcd import gcd
from MyCrypto.util.pow_modual import quickPow

def getPrimeNumber(base):
    suspect = base + (3 - base % 4)
    while True:
        if Miler_Rabin(suspect):
            return suspect
        else:
            suspect += 4

def BBS(seed, length):
    p = getPrimeNumber(2^12)
    q = 0
    temp = p+1
    while True:
        temp = getPrimeNumber(temp)
        if gcd(seed, temp * p) == 1:
            q = temp
            break
    n = p * q
    n = 192649
    X = quickPow(seed, 2, n)
    B = []
    for i in range(1, length+1):
        X = quickPow(X, 2, n)
        B.append(X % 2)
    return B

if __name__ == '__main__':
    print(BBS(101355, 20))
