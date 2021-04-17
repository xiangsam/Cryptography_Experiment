# -*- coding: utf-8 -*-

import random
import sys
sys.path.append('../..')
from MyCrypto.AES.aes import AES
from MyCrypto.util.matrix import Matrix
from MyCrypto.util.GF2 import GF2
from MyCrypto.util.s2bs import i2bs, bs2i
import random

def diffAnalysis(target):
    assert isinstance(target, AES)
    c_matrix = AES.getText(int('0x'+target.encrypt(),16))
    inject_matrix = target.getInjectPoint()
    ansKey10 = Matrix.zero(4,4,GF2)
    for i in range(4):
        X = [[],[],[],[]]
        times = Matrix([[0x02, 0x01, 0x01, 0x03]],GF2)
        while not 1 == len(X[0]) == len(X[1]) == len(X[2]) == len(X[3]):
            w = GF2(random.randint(0x01, 0xff))
            #w = GF2(0x2e)
            w_matrix = inject_matrix.copy()
            w_matrix[0, i] += w
            w_c_matrix = AES.getText(int('0x'+target.getDiffCipher(w_matrix),16))
            for j in range(4):
                if not len(X[j]) == 1:
                    index = getRowShiftIndex(j, i)
                    r = index[0]
                    c = index[1]
                    temp = []
                    for e in range(0xff+1):
                        e = GF2(e)
                        if target.sBoxShift(e + (times[0,j] * w)) == target.sBoxShift(e) + c_matrix[r, c]+w_c_matrix[r, c]:
                            temp.append(e)
                    if len(temp) == 0:
                        break
                    for t, e in enumerate(temp):
                        temp[t] = target.sBoxShift(e) + c_matrix[r,c]
                    if len(X[j]) == 0:
                        X[j] = temp
                    else:
                        X[j] = Intersection(X[j], temp)
                    if len(X[j]) == 1:
                        ansKey10[r, c] = X[j][0]
    return ansKey10

def recoverKey(target):
    Key10 = diffAnalysis(target)
    w = []
    for i in range(4):
        w.append(Key10.getColumn(i))
    for i in range(10):
        rc = [GF2(2)**GF2(9-i),GF2(0),GF2(0),GF2(0)]
        tempw = [0,0,0,0]
        for j in range(1,4):
            tempw[j] = [a+b for a,b in zip(w[4*i+j],w[4*i+j-1])]
        tempw[0] = [a+b for a,b in zip(w[4*i],target._gFun(tempw[3], rc))]
        for e in tempw:
            w.append(e)
    return Matrix([w[40],w[41],w[42],w[43]],GF2).transpose()

def Intersection(source, other):
    ans = []
    for e in source:
        if  e in other:
            ans.append(e)
    if len(ans) == 0:
        return source
    return ans
def getRowShiftIndex(r, c):
    if r == 0:
        return [r,c]
    if r == 1:
        return [r,(c-1)%4]
    if r == 2:
        return [r, (c-2)%4]
    if r == 3:
        return [r, (c-3)%4]
    print('wrong')
    return None

if __name__ == '__main__':
    target = AES(0x00112233445566778899aabbccddeeff,0x000102030405060708090a0b0c0d0e0f)
    print('True key is 0x%032x' % 0x000102030405060708090a0b0c0d0e0f )
    print('crack key is:')
    print(recoverKey(target))
    key = random.randint(0x10000000000000000000000000000000,0xffffffffffffffffffffffffffffffff)
    target = AES(0x00112233445566778899aabbccddeeff, key)
    crackKey = recoverKey(target)
    print('True key is 0x%032x' % key)
    print('crack key is:')
    print(crackKey)
