# -*- coding:utf-8 -*-
#! /usr/bin/python3

import sys
sys.path.append('../..')
from MyCrypto.Hash.sha1 import SHA1
from hashlib import sha1
from random import randint

class BirthdayAttack:
    def __init__(self, trueMessage, fakeMessage, crackBits, mode):
        self._trueMessage = trueMessage
        self._fakeMessage = fakeMessage
        assert crackBits % 2 == 0
        self._crackBits = crackBits
        self._tList, self._fList = BirthdayAttack.reshape(trueMessage, fakeMessage, crackBits)
        if not callable(mode):
            raise TypeError('mode: expect callable function')
        self._mode = mode
    
    def attack(self):
        """
        only test sha1 BirthdayAttack
        """
        num = len(self._tList)
        for i in range(num):
            hash1 = self._mode()
            hash1.update(self._tList[i])
            ans1 = hash1.hexdigest()
            ans1 = bin(int(ans1,16)).replace('0b','').rjust(160,'0')
            for j in range(num):
                hash2 = self._mode()
                hash2.update(self._fList[j])
                ans2 = hash2.hexdigest()
                ans2 = bin(int(ans2, 16)).replace('0b','').rjust(160, '0')
                if ans1[0:self._crackBits] == ans2[0:self._crackBits]:
                    return self._tList[i], self._fList[j]
        print('Fail!!!')
        return None

    @staticmethod
    def reshape(trueMessage, fakeMessage, crackBits):
        length = 2**(crackBits//2)
        tMLen = len(trueMessage)
        fMLen = len(fakeMessage)
        tList = [trueMessage]
        tLen = 1
        fList = [fakeMessage]
        fLen = 1
        while tLen < length:
            changePoint = randint(0, tMLen-1)
            changeLength = randint(1, length)
            temp = trueMessage[0:changePoint] + b' '*changeLength + trueMessage[changePoint:]
            if not temp in tList:
                tList.append(temp)
                tLen += 1
        while fLen < length:
            changePoint = randint(0, tMLen - 1)
            changeLength = randint(1, length)
            temp = fakeMessage[0:changePoint] + b' '*changeLength + fakeMessage[changePoint:]
            if not temp in fList:
                fList.append(temp)
                fLen += 1
        print('reshape ok')
        return tList, fList
        

if __name__ == '__main__':
    trueMessage = b'hello, world'
    fakeMessage = b'fuck, world'
    birthdayAttack = BirthdayAttack(trueMessage, fakeMessage,16, sha1)
    tM, fM = birthdayAttack.attack()
    print(tM)
    print(fM)
    sha  = sha1()
    sha.update(tM)
    print(sha.hexdigest())
    sha = sha1()
    sha.update(fM)
    print(sha.hexdigest())
