# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys

sys.path.append('../..')
from MyCrypto.util.matrix import Matrix
from MyCrypto.util.gcd import gcd
from MyCrypto.util.inverse_mod import inverse_mod

table = [chr(ord('a') + i) for i in range(26)]


def crack(p, c, m_dim):
    """
    need plain-matrix is inversable
    """
    assert len(p) == len(c)
    assert len(p) % m_dim == 0
    mat_p = Matrix.zero(m_dim, m_dim)
    mat_c = Matrix.zero(m_dim, m_dim)
    for i in range(0, len(p) - m_dim**2 + 1, m_dim):
        for j in range(i, i + m_dim**2):
            row_i = (j - i) // m_dim
            col_i = (j - i) % m_dim
            mat_p[row_i, col_i] = table.index(p[j])
            mat_c[row_i, col_i] = table.index(c[j])
        if gcd(mat_p.det(), 26) != 1:  #search p matrix which is inversable
            continue
        det_inv = inverse_mod(mat_p.det(), 26)
        p_adj = mat_p.adjoint_matrix() % 26
        p_inv = p_adj * det_inv % 26
        k = p_inv * mat_c % 26
        return k
    return 'Oops!!Fail to crack with plain {} and cypher {}'.format(p, c)


if __name__ == '__main__':
    plain = 'youarepretty'
    cypher = 'kqoimjvdbokn'
    print('from plaintext {} and cypher {} we crack the key:\n{}'.format(
        plain, cypher, crack(plain, cypher, 2)))
    plain = 'youaresocute'
    cypher = 'ywwpcwsogfuk'
    print('from plaintext {} and cypher {} we crack the key:\n{}'.format(
        plain, cypher, crack(plain, cypher, 3)))
