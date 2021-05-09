# -*- coding:utf-8 -*-
#!/usr/bin/python2

import sys
sys.path.append('../..')
from MyCrypto.util.s2bs import s2bs,bs2s

def KSA(key):
    """
    The key-scheduling algorithm is used to initialize the permutation in the array S
    """
    assert 1 <= len(key) <= 256
    keyLength = len(key)
    S = []
    for i in range(0, 256):
        S.append(i)
    j = 0
    for i in range(0, 256):
        j = (j + S[i] + ord(key[i % keyLength])) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    """
    Pseudo-random generation algorithm
    """
    i = 0
    j = 0
    while True:
        i = (i+1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def encrypt(plain, key):
    """
    RC4 encrypt part
    """
    S = KSA(key)
    K = PRGA(S)
    lst = []
    for e in plain:
        lst.append('%02x' % (ord(e) ^ next(K)))
    return ''.join(lst)

if __name__ == '__main__':
    print('Plaintext: {}, RootKey: {}'.format('Plaintext','Key'))
    print('the hex of cypher: '+encrypt('Plaintext', 'Key'))
    print('Plaintext: {}, RootKey: {}'.format('pedia','Wiki'))
    print('the hex of cypher: '+encrypt('pedia', 'Wiki'))
    print('Plaintext: {}, RootKey: {}'.format('Attack at dawn','Secret'))
    print('the hex of cypher: '+encrypt('Attack at dawn', 'Secret'))
