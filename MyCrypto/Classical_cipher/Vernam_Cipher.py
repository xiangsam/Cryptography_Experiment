# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys

sys.path.append('../..')
from MyCrypto.util.s2bs import s2bs, bs2s


def encrypt(fi_name, fo_name, k):
    print(len(k))
    c = ''
    list_c = []
    with open(fi_name, 'r') as f:
        p = f.read()
        p = s2bs(p)
        print(p)
        k = s2bs(k)
        k_len = len(k)
        print(k)
        for i, e in enumerate(p):
            k_i = i % k_len
            c_i = '0' if e == k[k_i] else '1'
            list_c.append(c_i)
        f.close()
    c = ''.join(list_c)
    f = open(fo_name, 'w')
    f.write(bs2s(c))
    f.close()


def decrypt(fi_name, fo_name, k):
    """
    the decrypt is the same with encrypt
    """
    encrypt(fi_name, fo_name, k)


if __name__ == '__main__':
    encrypt('input1.txt', 'output1.txt', 'Todayis20200308')
    encrypt('input2.txt', 'output2.txt', '12345abcde')
