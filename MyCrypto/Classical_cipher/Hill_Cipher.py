# -*- coding: utf-8 -*-
#!/bin/usr/python3
import sys

sys.path.append('../..')
from MyCrypto.util.matrix import Matrix
from MyCrypto.util.gcd import gcd
from MyCrypto.util.inverse_mod import inverse_mod

table = 'abcdefghijklmnopqrstuvwxyz'


def encrypt(p, k: Matrix):
    """
    no extension for p
    """
    assert k.isSquare
    assert len(p) % k.row == 0
    k_dim = k.row
    c = ''
    list_c = []
    mat = Matrix.zero(len(p) // k_dim, k_dim)
    for i, e in enumerate(p):
        r_index = i // k_dim
        c_index = i % k_dim
        mat[r_index, c_index] = table.index(e)
    out = (mat * k) % 26
    for i in range(len(p) // k_dim):
        for j in range(k_dim):
            list_c.append(table[out[i, j]])
    c = ''.join(list_c)
    return c


def decrypt(c, k: Matrix):
    """
    Hill cipher decrypt part
    """
    assert k.isSquare
    assert gcd(k.det(), 26) == 1  #makesure the Key matrix is inversable
    k_dim = k.row
    det_inv = inverse_mod(k.det(), 26)
    k_adj = k.adjoint_matrix() % 26
    k_inv = k_adj * det_inv % 26
    mat = Matrix.zero(len(c) // k_dim, k_dim)
    for i, e in enumerate(c):
        r_index = i // k_dim
        c_index = i % k_dim
        mat[r_index, c_index] = table.index(e)
    out = mat * k_inv % 26
    p = ''
    list_p = []
    for i in range(len(c) // k_dim):
        for j in range(k_dim):
            list_p.append(table[out[i, j]])
    p = ''.join(list_p)
    return p


if __name__ == '__main__':
    plaint = 'loveyourself'
    cypher = 'qweasdzxc'
    key = Matrix([[5, 8], [17, 3]])
    print('the cypher of {} is {}'.format(plaint, encrypt(plaint, key)))
    key = Matrix([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
    print('the plaintext of {} is {}'.format(cypher, decrypt(cypher, key)))
    key = Matrix([[9,4],[5,7]])
