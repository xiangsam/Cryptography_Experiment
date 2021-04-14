# -*- coding: utf-8 -*-
import sys

sys.path.append('../..')
from MyCrypto.Classical_cipher.Shift_Cipher import  decrypt

table = 'abcdefghijklmnopqrstuvwxyz'


def countWords(article):
    """
    Count the number of letters
    """
    num = 0
    with open(article, 'r') as f:
        for line in f:
            for e in line:
                if e.isalpha:
                    num = num + 1
        f.close()
    return num


def getExpectTimes(articlen):
    expect_list = [
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
        0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
        0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
        0.01974, 0.00074
    ]
    for i, e in enumerate(expect_list):
        expect_list[i] = e * articlen
    return expect_list


def getScore(dic, expect_list, article, k):
    """
    k is guessed key for shift cipher
    """
    actual_list = [0 for i in range(26)]
    with open(article, 'r') as f:
        content_s = f.read()
        content_ns = decrypt(content_s, k)
        for e in content_ns:
            if e.isalpha():
                actual_list[table.index(e.lower())] += 1
        score = 0
        content_ns = 'The Key: {}\n'.format(k) + content_ns
        for a, b in zip(actual_list, expect_list):
            score += (a - b)**2 / b
        dic[content_ns] = score
        f.close()
    return dic

if __name__ == '__main__':
    articl_len = countWords('Shift_Plaintext')
    expect = getExpectTimes(articl_len)
    dic = {}
    for key in range(26):
        getScore(dic, expect, 'Shift_Plaintext', key)
    for e in sorted(dic.items(), key=lambda x:x[1]):
        print('the score is {}\n {}'.format(e[1], e[0]))
