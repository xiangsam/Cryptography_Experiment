# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys

sys.path.append('../..')

from MyCrypto.util.inverse_mod import inverse_mod
from MyCrypto.util.gcd import gcd

table = 'abcdefghijklmnopqrstuvwxyz'


def encrypt(p, k, b):
    """
    @p: string
    @return: c = (k * p + b) mod 26
    """
    if gcd(k, 26) != 1:
        print('Warning, check you k')
    list_c = []
    for e in p:
        if e.isalpha():
            index = table.index(e.lower())
            n_index = (index * k + b) % 26
            list_c.append(table[n_index])
        else:
            list_c.append(e)
    c = ''.join(list_c)
    return c


def decrypt(c, k, b):
    """
    @c: string
    @return: p = (c - b) / k mod 26
    """
    if gcd(k, 26) != 1:
        print('Erroe, the gcd of k and 26 is not 1')
        return None
    list_p = []
    for e in c:
        if e.isalpha():
            index = table.index(e.lower())
            n_index = ((index - b) % 26 * inverse_mod(k, 26)) % 26
            list_p.append(table[n_index])
        else:
            list_p.append(e)
    p = ''.join(list_p)
    return p


if __name__ == '__main__':
    plain = 'cryptography'
    print('the cypher of {} is {}'.format(plain, encrypt(plain, 7, 10)))
    plain = 'seeyoutomorrow'
    print('the cypher of {} is {}'.format(plain, encrypt(plain, 9, 13)))
    cypher = 'thisisciphertext'
    print('the plaintexe of {} is {}'.format(cypher, decrypt(cypher, 15, 20)))
    plain = 'abcdef'
    print('the cypher of {} is {}'.format(plain, encrypt(plain, 2, 1)))
