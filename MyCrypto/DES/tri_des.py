#!/usr/bin/python2

import sys

sys.path.append('../..')
from MyCrypto.util.s2bs import i2bs, bs2i


class DES:

    def __init__(self, text, key):
        self.key = i2bs(key, 128)
        self.key1 = self.key[0:64]
        self.key2 = self.key[64:]
        self.text = i2bs(text, 64)
        self.Key_28 = []
        self.ip_table = [
            58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62,
            54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49,
            41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37,
            29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
        ]
        self.ip_inv_table = [
            40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6,
            46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44,
            12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10,
            50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
        ]
        self.e_table = [
            32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13,
            14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24,
            25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
        ]
        self.p_table = [
            16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8,
            24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
        ]
        self.sbox = [
                     [
                         14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
                         0, 15, 7, 4,14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
                         4, 1, 14, 8, 13, 6, 2, 11,15, 12, 9, 7, 3, 10, 5, 0,
                         15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14,10, 0, 6, 13
                     ],
                     [
                         15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
                         3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
                         0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
                         13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
                     ],
                     [
                         10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
                         13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
                         13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
                         1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
                     ],
                     [
                         7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
                         13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
                         10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
                         3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
                     ],
                     [
                         2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
                         14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
                         4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
                         11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
                     ],
                     [
                         12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
                         10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
                         9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
                         4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
                     ],
                     [
                         4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
                         13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
                         1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
                         6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
                     ],
                     [
                         13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
                         1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
                         7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
                         2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
                     ]]
        self.pc1_table = [
            57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51,
            43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28,
            20, 12, 4
        ]
        self.pc2_table = [
            14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33,
            48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
        ]
        self.shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def getRoundKey(self, keySelect = 1):
        self.Key_28 = []
        key = ''
        if keySelect == 1:
            key = self.key1
        elif keySelect == 2:
            key = self.key2
        else:
            print('wrong keySelect')
            return None
        key = DES.tableShift(key, self.pc1_table)
        lkey = key[0:28]
        rkey = key[28:]
        for i in range(16):
            lkey = DES.circle_lshift(lkey, self.shift_table[i])
            rkey = DES.circle_lshift(rkey, self.shift_table[i])
            self.Key_28.append(DES.tableShift(lkey+rkey, self.pc2_table))
        return

    def F(self, dest, seq):
        e_dest = DES.tableShift(dest, self.e_table)
        xorans = DES.xor(e_dest, self.Key_28[seq])
        sboxans = DES.SboxShift(xorans, self.sbox)
        return DES.tableShift(sboxans, self.p_table)

    def process(self, mode='encrypt', selectKey = 1):
        self.getRoundKey(selectKey)
        text = self.text
        ip_text = DES.tableShift(text, self.ip_table)
        ltext = ip_text[0:32]
        rtext = ip_text[32:]
        if mode == 'encrypt':
            for i in range(16):
                temp = rtext
                rtext = DES.xor(ltext, self.F(rtext, i))
                ltext = temp
        elif mode == 'decrypt':
            for i in range(16):
                temp = rtext
                rtext = DES.xor(ltext, self.F(rtext, 15-i))
                ltext = temp
        else:
            print('Error Mode')
            return
        ans = rtext + ltext
        ans = DES.tableShift(ans, self.ip_inv_table)
        return ans

    def tri_process(self, mode='encrypt'):
        if mode == 'encrypt':
            self.text = self.process('encrypt', 1)
            self.text = self.process('decrypt', 2)
            self.text = self.process('encrypt', 1)
        elif mode == 'decrypt':
            self.text = self.process('decrypt', 1)
            self.text = self.process('encrypt', 2)
            self.text = self.process('decrypt', 1)
        else:
            print('wrong mode')
            return None
        return '0x%016x' % bs2i(self.text)

    @staticmethod
    def SboxShift(dest, Sbox):
        d_out = ''
        for i in range(8):
            d_in = dest[6*i:6*(i+1)]
            s_box = Sbox[i]
            row = int(d_in[0])*2 + int(d_in[5])
            col = int(d_in[1:5] ,2)
            d_out += i2bs(s_box[row * 16 + col], 4)
        return d_out
    @staticmethod
    def xor(a, b):
        l = []
        for i, j in zip(a, b):
            if i == j:
                l.append('0')
            else:
                l.append('1')
        return ''.join(l)
    @staticmethod
    def tableShift(dest, table):
        ans = []
        for e in table:
            ans.append(dest[e - 1])
        return ''.join(ans)

    @staticmethod
    def circle_lshift(dest, shiftbit):
        return dest[shiftbit:] + dest[0:shiftbit]

if __name__ == '__main__':
    test_p = DES(0x0bae3b9e42415649, 0x05261d3824311a20300935393c0d100b)
    test_c = DES(0x3fcf306caa460b1e, 0x05261d3824311a20300935393c0d100b)
    print('cypher: {}'.format(test_p.tri_process()))
    print('plaintext: {}\n'.format(test_c.tri_process('decrypt')))
    test_p = DES(0x67117cf2c11bfc09, 0x1c10372a2832002b3325340136002c35)
    test_c = DES(0x78a22441bd78c3dd, 0x1c10372a2832002b3325340136002c35)
    print('cypher: {}'.format(test_p.tri_process()))
    print('plaintext: {}\n'.format(test_c.tri_process('decrypt')))
    test_p = DES(0xf596506e738538b8, 0x12071c241a0a0f0804292a380c341f03)
    print('cypher: {}\n'.format(test_p.tri_process()))
    test_c = DES(0x2b2cefbc99f91153, 0x1d81b63cf3a645139c6f1460f2ec2638)
    print('plaintext: {}\n'.format(test_c.tri_process('decrypt')))
