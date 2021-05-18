# -*- coding: utf-8 -*-

import sys
sys.path.append('../..')
from MyCrypto.AES.aes import AES, GF28
from MyCrypto.util.matrix import Matrix
from MyCrypto.util.s2bs import i2bs, bs2i
import random

def diffAnalysis(target):
    assert isinstance(target, AES)
    c_matrix = AES.getText(int('0x'+target.encrypt(),16))
    inject_matrix = target.getInjectPoint()
    ansKey10 = Matrix.zero(4,4,GF28)
    for i in range(4):
        X = [[],[],[],[]]
        times = Matrix([[0x02, 0x01, 0x01, 0x03]],GF28)
        while not 1 == len(X[0]) == len(X[1]) == len(X[2]) == len(X[3]):
            w = random.randint(0x1, 0xff) #this wrong is unvisitable
            w = GF28(w)
            w_matrix = inject_matrix.copy()
            w_matrix[0, i] += w
            w_c_matrix = AES.getText(int('0x'+target.getDiffCipher(w_matrix),16))
            temp = [{},{},{},{}]
            # get the set of {ww: [e]}(ww is possible wrong and the list of e is the corresponding X)
            for j in range(4):
                index = getRowShiftIndex(j, i)
                r = index[0]
                c = index[1]
                for ww in range(0xff+1):
                    ww = GF28(ww)
                    for e in range(0xff+1):
                        e = GF28(e)
                        if target.sBoxShift(e + (times[0,j] * ww)) == target.sBoxShift(e) + c_matrix[r, c]+w_c_matrix[r, c]:
                            if not ww in temp[j].keys():
                                temp[j][ww] = [e]
                            else:
                                temp[j][ww].append(e)
            tempX = [[],[],[],[]]
            # only if possible wrong ww has correspongding X for all temp[0] to temp[3], it is true possible wrong
            # then merge the possible X for this injection
            for e in range(0xff+1):
                e = GF28(e)
                if not e in temp[0] or not e in temp[1] or not e in temp[2] or not e in temp[3]:
                    continue
                if  len(temp[0][e]) == 0 or len(temp[1][e]) == 0 or len(temp[2][e]) == 0 or len(temp[3][e]) == 0:
                    continue
                else:
                    for j in range(4):
                        index = getRowShiftIndex(j, i)
                        r = index[0]
                        c = index[1]
                        for t, tt in enumerate(temp[j][e]):
                            temp[j][e][t] = target.sBoxShift(tt) + c_matrix[r,c]
                        for t in temp[j][e]:
                            if not t in tempX[j]:
                                tempX[j].append(t)
            # after some times of injecting, we can get the final Key of 10th round
            for j in range(4):
                index = getRowShiftIndex(j, i)
                r = index[0]
                c = index[1]
                if len(X[j]) == 0:
                    X[j] = tempX[j]
                else:
                    X[j] = Intersection(X[j], tempX[j])
                print('{}  {}---------'.format(r, c)+str(X[j]))
                if len(X[j]) == 1:
                    ansKey10[r, c] = X[j][0]
                    print(ansKey10)
    return ansKey10

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

def recoverKey(target):
    Key10 = diffAnalysis(target)
    w = []
    for i in range(4):
        w.append(Key10.getColumn(i))
    for i in range(10):
        rc = [GF28(2)**GF28(9-i),GF28(0),GF28(0),GF28(0)]
        tempw = [0,0,0,0]
        for j in range(1,4):
            tempw[j] = [a+b for a,b in zip(w[4*i+j],w[4*i+j-1])]
        tempw[0] = [a+b for a,b in zip(w[4*i],target._gFun(tempw[3], rc))]
        for e in tempw:
            w.append(e)
    return Matrix([w[40],w[41],w[42],w[43]],GF28).transpose()

if __name__ == '__main__':
    target = AES(0x00112233445566778899aabbccddeeff,0x000102030405060708090a0b0c0d0e0f)
    print(target.key)
    print(recoverKey(target))
