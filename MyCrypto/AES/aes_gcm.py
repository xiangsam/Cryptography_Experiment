# -*- coding:utf-8 -*-
#!/usr/bin/python3

import sys
sys.path.append('../..')
from MyCrypto.AES.aes import AES
from MyCrypto.util.s2bs import s2bs, bs2i, bs2s, i2bs,xor
from MyCrypto.util.GF import GF

class GF2_128(GF):
    def __init__(self, data, order = 128):
        super().__init__(data, order)

class GCM:
    def __init__(self,text,key,IV,A,T = None):
        self.lenP, self.text = GCM.getText(text)
        self.key = key
        self.IV = IV
        self.A = A
        self.T = T

    def encrypt(self):
        H = int(AES(0, self.key).encrypt(),16)
        print('H: {}'.format(hex(H)))
        Y0 = 0
        if len(self.IV) == 24:
            Y0 = int(self.IV+'0'*7+'1',16)
        else:
            lenT = 0
            temp = bin(int(self.IV,16)).replace('0b','').zfill(len(self.IV) * 4)
            if len(temp) % 128 == 0:#convert IV to binary string list
                lenT = len(temp) // 128
            else:
                lenT = len(temp) // 128 + 1
            Y0 = self.GHASH(H, None, [temp[128*i:128*(i+1)] for i in range(lenT)])
        Y = [Y0]
        for i in range(len(self.text)+1): #get Yi
            if i == 0:
                Y[0] == Y0
                print('Y{}: '.format(str(i))+hex(Y[i]))
            else:
                Y.append(GCM.incr(Y[i-1]))
                print('Y{}: '.format(str(i))+hex(Y[i]))
        C = []
        P = [bin(int(e,16)).replace('0b','').zfill(len(e)*4) for e in self.text]
        for i in range(len(self.text)-1):
            C.append(xor(P[i], i2bs(int(AES(Y[i+1],self.key).encrypt(), 16),128)))
        u = len(self.text[-1]) * 4
        C.append(xor(P[-1], i2bs(int(AES(Y[-1],self.key).encrypt(),16),128)[0:u]))
        X = self.GHASH(H, self.A, C)
        print('C is {}'.format(hex(int(''.join(C),2)).replace('0x','').zfill(len(C)*32)))
        print('T is '+hex(int(xor(i2bs(X,128),i2bs(int(AES(Y[0],self.key).encrypt(),16),128)),2)))

    def decrypt(self):
        H = int(AES(0, self.key).encrypt(),16)
        print('H: {}'.format(hex(H)))
        Y0 = 0
        if len(self.IV) == 24:
            Y0 = int(self.IV+'0'*7+'1',16)
        else:
            lenT = 0
            temp = bin(int(self.IV,16)).replace('0b','').zfill(len(self.IV) * 4)
            if len(temp) % 128 == 0:
                lenT = len(temp) // 128
            else:
                lenT = len(temp) // 128 + 1
            Y0 = self.GHASH(H, None, [temp[128*i:128*(i+1)] for i in range(lenT)])
        Y = [Y0]
        C = [bin(int(e,16)).replace('0b','').zfill(len(e)*4) for e in self.text]
        X = self.GHASH(H, self.A, C)
        T = int(xor(i2bs(X,128),i2bs(int(AES(Y[0],self.key).encrypt(),16),128)),2)
        if not T == self.T:
            print('INVLID')
            return
        for i in range(len(self.text)+1):
            if i == 0:
                Y[0] == Y0
                print('Y{}: '.format(str(i))+hex(Y[i]))
            else:
                Y.append(GCM.incr(Y[i-1]))
                print('Y{}: '.format(str(i))+hex(Y[i]))
        P = []
        for i in range(len(self.text)-1):
            P.append(xor(C[i], i2bs(int(AES(Y[i+1],self.key).encrypt(), 16),128)))
        u = len(self.text[-1]) * 4
        P.append(xor(C[-1], i2bs(int(AES(Y[-1],self.key).encrypt(),16),128)[0:u]))
        print('The T is matched')
        print('P is {}'.format(hex(int(''.join(P),2)).replace('0x','').zfill(len(P)*32)))


    @staticmethod
    def getText(text):
        lenT = 0
        if len(text) % 32 == 0:
            lenT = len(text) // 32
        else:
            lenT = len(text) // 32 + 1
        lst = [text[32*i:32*(i+1)] for i in range(lenT)]
        return len(text)*4, lst

    @staticmethod
    def incr(Y):
        Yi = Y>>32
        Yj = Y & 0xffffffff
        Yj = (Yj + 1) & 0xffffffff
        return (Yi << 32) + Yj

    def GHASH(self,H,A,C):
        if A == None:
            A = ''
        else:
            A = bin(int(A,16)).replace('0b','').zfill(len(A)*4)
        H = bin(H).replace('0b','').zfill(128)
        H = int(H[::-1],2)
        X = [0]
        lenA = 0
        lenC = len(C)
        if len(A) % 128 == 0:
            lenA = len(A) // 128
        else:
            lenA = len(A) // 128 + 1
        lstA = [A[128*i:128*(i+1)] for i in range(lenA)]
        m = lenA
        n = lenC
        u = len(C[-1])
        for i in range(m+n+2):
            addPart = 0
            if i == 0:
                X[i] = 0
                continue
            elif 1 <= i <= m-1:
                addPart = GF2_128(X[i-1]) + GF2_128(int(lstA[i-1],2))
            elif i == m:
                addPart = GF2_128(X[i-1]) + GF2_128(int(lstA[i-1].ljust(128,'0'),2))
            elif m+1 <= i <= m+n-1:
                addPart = GF2_128(X[i-1]) + GF2_128(int(C[i-m-1],2))
            elif i == m+n:
                addPart = GF2_128(X[i-1]) + GF2_128(int(C[i-m-1].ljust(128,'0'),2))
            elif i == m+n+1:
                addPart = GF2_128(X[i-1]) + GF2_128(((len(A) & 0xffffffffffffffff)<<64)+((lenC-1)*128+u & 0xffffffffffffffff))
            addPart = bin(addPart.value).replace('0b','').zfill(128)
            addPart = int(addPart[::-1],2)
            ans = (GF2_128(addPart) * GF2_128(H)).value
            ans = bin(ans).replace('0b','').zfill(128)
            ans = int(ans[::-1],2)
            X.append(ans)
            print('X{}: '.format(str(i)) + hex(X[i]))
        return X[m+n+1]


if __name__ == '__main__':
    print('##### Encrypt Part #####')
    print('\nTest Case 2\n')
    GCM('00000000000000000000000000000000',0,'000000000000000000000000',None).encrypt()
    print('\nTest Case 3\n')
    GCM('d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255', 0xfeffe9928665731c6d6a8f9467308308, 'cafebabefacedbaddecaf888',None).encrypt()
    print('\nTest Case 4\n')
    GCM('d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39', 0xfeffe9928665731c6d6a8f9467308308, 'cafebabefacedbaddecaf888','feedfacedeadbeeffeedfacedeadbeefabaddad2').encrypt()
    print('\nTest Case 5\n')
    GCM('d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39', 0xfeffe9928665731c6d6a8f9467308308, 'cafebabefacedbad','feedfacedeadbeeffeedfacedeadbeefabaddad2').encrypt()
    print('\nTest Case 6\n')
    GCM('d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39', 0xfeffe9928665731c6d6a8f9467308308, '9313225df88406e555909c5aff5269aa6a7a9538534f7da1e4c303d2a318a728c3c0c95156809539fcf0e2429a6b525416aedbf5a0de6a57a637b39b','feedfacedeadbeeffeedfacedeadbeefabaddad2').encrypt()
    print('\n\n##### Decrypt Part #####')
    print('\nTest Case 2\n')
    GCM('0388dace60b6a392f328c2b971b2fe78',0,'000000000000000000000000',None,0xab6e47d42cec13bdf53a67b21257bddf).decrypt()
    print('\nTest Case 3\n')
    GCM('42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091473f5985', 0xfeffe9928665731c6d6a8f9467308308, 'cafebabefacedbaddecaf888',None,0x4d5c2af327cd64a62cf35abd2ba6fab4).decrypt()
    print('\nTest Case 4\n')
    GCM('42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091', 0xfeffe9928665731c6d6a8f9467308308, 'cafebabefacedbaddecaf888','feedfacedeadbeeffeedfacedeadbeefabaddad2',0x5bc94fbc3221a5db94fae95ae7121a47).decrypt()
    print('\nTest Case 5\n')
    GCM('61353b4c2806934a777ff51fa22a4755699b2a714fcdc6f83766e5f97b6c742373806900e49f24b22b097544d4896b424989b5e1ebac0f07c23f4598', 0xfeffe9928665731c6d6a8f9467308308, 'cafebabefacedbad','feedfacedeadbeeffeedfacedeadbeefabaddad2',0x3612d2e79e3b0785561be14aaca2fccb).decrypt()
    print('\nTest Case 6\n')
    GCM('8ce24998625615b603a033aca13fb894be9112a5c3a211a8ba262a3cca7e2ca701e4a9a4fba43c90ccdcb281d48c7c6fd62875d2aca417034c34aee5', 0xfeffe9928665731c6d6a8f9467308308, '9313225df88406e555909c5aff5269aa6a7a9538534f7da1e4c303d2a318a728c3c0c95156809539fcf0e2429a6b525416aedbf5a0de6a57a637b39b','feedfacedeadbeeffeedfacedeadbeefabaddad2',0x619cc5aefffe0bfa462af43c1699d050).decrypt()
