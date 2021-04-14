# -*- coding: utf-8 -*-
#!/usr/bin/python3


def encrypt(n, p):
    """
    simple Rail_Fence_Cipher encrypt
    no limit in p'length
    """
    p_len = len(p)
    L = []
    assert n < p_len  #make sure the cypher is different from the plaintext
    for i, e in enumerate(p):
        row_i = i % n
        if len(L) < row_i + 1:
            l = []
            l.append(e)
            L.append(l)
        else:
            L[row_i].append(e)
    list_c = []
    for l in L:
        for e in l:
            list_c.append(e)
    c = ''.join(list_c)
    return c


def decrypt(n, c):
    """
    know the rows, and decrypt
    """
    L = []
    r_len = len(c) // n if len(c) % n == 0 else len(c) // n + 1
    for i, e in enumerate(c):
        row_i = i // r_len
        col_i = i % r_len
        if col_i == 0:
            l = []
            l.append(e)
            L.append(l)
        else:
            L[row_i].append(e)
    list_p = []
    for i in range(r_len):
        list_p.append(L[0][i])
        for r in range(1, n):
            if i < len(L[r]):
                list_p.append(L[r][i])
    p = ''.join(list_p)
    return p


if __name__ == '__main__':
    plain = 'whateverisworthdoingisworthdoingwell'
    print('the cypher of {} is {}'.format(plain, encrypt(3, plain)))
    cypher = 'hatimriprathnelhelhsoemotntawat'
    print('the plaintext of {} is {}'.format(cypher, decrypt(2, cypher)))
