# -*- coding: utf-8 -*-
import sys

sys.path.append('../..')

from MyCrypto.util.matrix import Matrix
from MyCrypto.util.GF import GF
from MyCrypto.util.s2bs import i2bs, bs2i, s2bs

class GF28(GF):
    def __init__(self,value,order = 8):
        super().__init__(value, order)

class AES:

    def __init__(self, text, key):
        self.text = AES.getText(text)
        self.key = AES.getKey(key)
        self.roundKey = []
        #self.sbox = AES.getSBox()
        #self.inv_sbox = AES.getInv_SBox()
        self.sbox = Matrix([
                           [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                           [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                           [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
                           [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
                           [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
                           [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
                           [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
                           [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
                           [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
                           [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
                           [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
                           [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
                           [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
                           [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
                           [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
                           [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
                           ], GF28)
        self.inv_sbox = Matrix([
                               [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
                               [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
                               [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
                               [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
                               [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
                               [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
                               [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
                               [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
                               [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
                               [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
                               [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
                               [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
                               [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
                               [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
                               [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
                               [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d],
                               ], GF28)
        self.getRoundKey()
        self.c_mix = Matrix(
            [[0x02, 0x03, 0x01, 0x01], [0x01, 0x02, 0x03, 0x01],
             [0x01, 0x01, 0x02, 0x03], [0x03, 0x01, 0x01, 0x02]], GF28)
        self.invc_mix = Matrix(
            [[0x0e, 0x0b, 0x0d, 0x09], [0x09, 0x0e, 0x0b, 0x0d],
             [0x0d, 0x09, 0x0e, 0x0b], [0x0b, 0x0d, 0x09, 0x0e]], GF28)

    def sBoxShift(self, byte, inverse=False):
        byte = str(byte)
        if inverse:
            return self.inv_sbox[int(byte[0], 16), int(byte[1], 16)]
        return self.sbox[int(byte[0], 16), int(byte[1], 16)]

    def _gFun(self, word, rc):
        temp = [word[1], word[2], word[3], word[0]]
        temp2 = []
        ans = []
        for e in temp:
            temp2.append(self.sBoxShift(e))
        for a, b in zip(temp2, rc):
            ans.append(a + b)
        return ans

    def getRoundKey(self):
        words = []
        for i in range(4):
            words.append(self.key.getColumn(i))
        for i in range(4, 44):
            if i % 4 == 0:
                rc = [GF28(2)**(GF28(i // 4 - 1)), GF28(0), GF28(0), GF28(0)]
                words.append([
                    a + b
                    for a, b in zip(words[i - 4], self._gFun(words[i - 1], rc))
                ])
            else:
                words.append(
                    [a + b for a, b in zip(words[i - 4], words[i - 1])])
        for i in range(11):
            self.roundKey.append(
                Matrix([
                    words[4 * i], words[4 * i + 1], words[4 * i + 2],
                    words[4 * i + 3]
                ], GF28).transpose())

    def rowShift(self, mode='encrypt'):
        for i in range(1, 4):
            temp = self.text.getRow(i)
            if mode == 'decrypt':
                temp = [temp[(j - i) % 4] for j in range(4)]
            elif mode == 'encrypt':
                temp = [temp[(j + i) % 4] for j in range(4)]
            for j in range(4):
                self.text[i, j] = temp[j]

    def colMix(self, mode='encrypt'):
        if mode == 'encrypt':
            self.text = self.c_mix * self.text
        elif mode == 'decrypt':
            self.text = self.invc_mix * self.text

    def encrypt(self, bs=False):
        plain = self.text
        self.text = self.text + self.roundKey[0]
        for i in range(1, 11):
            #bytes substitution
            for r in range(4):
                for c in range(4):
                    self.text[r, c] = self.sBoxShift(self.text[r, c])
            self.rowShift()
            if not i == 10:
                self.colMix()
            self.text = self.text + self.roundKey[i]
        cypher = ''.join(
            [str(self.text[i, j]) for j in range(4) for i in range(4)])
        self.text = plain
        if bs:
            return i2bs(int(cypher,16),128)
        return cypher

    def decrypt(self, bs=False):
        cypher = self.text
        self.text = self.text + self.roundKey[10]
        for i in range(1, 11):
            self.rowShift('decrypt')
            for r in range(4):
                for c in range(4):
                    self.text[r, c] = self.sBoxShift(self.text[r, c], True)
            self.text = self.text + self.roundKey[10 - i]
            if not i == 10:
                self.colMix('decrypt')
        plain = ''.join(
            [str(self.text[i, j]) for j in range(4) for i in range(4)])
        self.text = cypher
        if bs:
            return i2bs(int(plain,16), 128)
        return plain

    def process(self,mode='encrypt'):
        """
        provide the same call method with SM4
        return binary string result
        """
        assert mode in ('encrypt', 'decrypt')
        if mode == 'encrypt':
            return self.encrypt(bs=True)
        else:
            return self.decrypt(bs=True)

    def getInjectPoint(self):
        plain = self.text
        self.text = self.text + self.roundKey[0]
        for i in range(1, 11):
            #bytes substitution
            for r in range(4):
                for c in range(4):
                    self.text[r, c] = self.sBoxShift(self.text[r, c])
            self.rowShift()
            if i == 9:
                break;
            if not i == 10:
                self.colMix()
            self.text = self.text + self.roundKey[i]
        ans = self.text
        self.text = plain
        return ans

    def getDiffCipher(self, text):
        plain = self.text
        if not isinstance(text, Matrix):
            self.text = AES.getText(text)
        else:
            self.text = text
        self.colMix()
        self.text = self.text + self.roundKey[9]
        for r in range(4):
            for c in range(4):
                self.text[r, c] = self.sBoxShift(self.text[r, c])
        self.rowShift()
        self.text = self.text + self.roundKey[10]
        ans = ''.join(
            [str(self.text[i, j]) for j in range(4) for i in range(4)])
        self.text = plain
        return ans


    @staticmethod
    def getText(text):
        '''
        convert text to textMatrix
        '''
        text = i2bs(text, 128)
        matrix = []
        for i, e in enumerate([text[8 * i:8 * (i + 1)] for i in range(16)]):
            if len(matrix) < 4:
                matrix.append([bs2i(e)])
            else:
                matrix[i % 4].append(bs2i(e))
        print(matrix)
        return Matrix(matrix, GF28)

    @staticmethod
    def getKey(key):
        '''
        convert key to keyMatrix
        '''
        key = i2bs(key, 128)
        matrix = []
        for i, e in enumerate([key[8 * i:8 * (i + 1)] for i in range(16)]):
            if len(matrix) < 4:
                matrix.append([bs2i(e)])
            else:
                matrix[i % 4].append(bs2i(e))
        return Matrix(matrix, GF28)

    @staticmethod
    def getSBox():
        s_matrix = [[(i * 16 + j) for j in range(16)] for i in range(16)]
        s_matrix = Matrix(s_matrix, GF28)
        a_matrix = [[1, 0, 0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 0, 1, 1, 1],
                    [1, 1, 1, 0, 0, 0, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1, 1]]
        a_matrix = Matrix(a_matrix, GF28)
        c_matrix = [[1], [1], [0], [0], [0], [1], [1], [0]]
        c_matrix = Matrix(c_matrix, GF28)
        for i in range(16):
            for j in range(16):
                temp = s_matrix[i, j].inverse()
                temp = int(str(temp), 16)
                b_matrix = []
                for k in range(8):
                    if (temp & (1 << k)) == (1 << k):
                        b_matrix.append([1])
                    else:
                        b_matrix.append([0])
                b_matrix = Matrix(b_matrix, GF28)
                b_matrix = a_matrix * b_matrix + c_matrix
                bs = ''.join([str(b_matrix[7 - i, 0])[1] for i in range(8)])
                s_matrix[i, j] = GF28(bs2i(bs))
        return s_matrix

    @staticmethod
    def getInv_SBox():
        invs_matrix = [[(i * 16 + j) for j in range(16)] for i in range(16)]
        invs_matrix = Matrix(invs_matrix, GF28)
        a_matrix = [[0, 0, 1, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0],
                    [0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 0, 1, 0, 0],
                    [0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0]]
        a_matrix = Matrix(a_matrix, GF28)
        c_matrix = [[1], [0], [1], [0], [0], [0], [0], [0]]
        c_matrix = Matrix(c_matrix, GF28)
        for i in range(16):
            for j in range(16):
                temp = invs_matrix[i, j]
                temp = int(str(temp), 16)
                b_matrix = []
                for k in range(8):
                    if (temp & (1 << k)) == (1 << k):
                        b_matrix.append([1])
                    else:
                        b_matrix.append([0])
                b_matrix = Matrix(b_matrix, GF28)
                b_matrix = a_matrix * b_matrix + c_matrix
                bs = ''.join([str(b_matrix[7 - i, 0])[1] for i in range(8)])
                invs_matrix[i, j] = GF28(bs2i(bs)).inverse()
        return invs_matrix


if __name__ == '__main__':
    p = AES(0x0123456789abcdeffedcba9876543210,
            0x0f1571c947d9e8590cb7add6af7f6798)
    c = AES(0xff0b844a0853bf7c6934ab4364148fb9,
            0x0f1571c947d9e8590cb7add6af7f6798)
    print('cypher: {}'.format(p.encrypt()))
    print('plaintext: {}'.format(c.decrypt()))
    print()

    p = AES(0x1b5e8b0f1bc78d238064826704830cdb,
            0x3475bd76fa040b73f521ffcd9de93f24)
    c = AES(0xfba4ec67020f1573ed28b47d7286d298,
            0x2b24424b9fed596659842a4d0b007c61)
    print('cypher: {}'.format(p.encrypt()) + '\n')
    print('plaintext: {}'.format(c.decrypt()))
    print(AES(0,0).encrypt())
    p = AES(0x3243F6A8885A308D313198A2E0370734,0x2b7e151628aed2a6abf7158809cf4f3c)
    print(p.roundKey)
