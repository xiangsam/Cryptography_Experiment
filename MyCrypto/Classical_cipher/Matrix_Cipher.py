# -*- coding: utf-8 -*-
#!/usr/bin/python3

table = [chr(ord('a') + i) for i in range(26)]


def encrypt(p, k):
    """
    make sure the p'length % k'length = 0
    the rows of matrix is dependent on k'length
    """
    L = []
    k_len = len(k)
    assert len(p) % k_len == 0
    for i, e in enumerate(p):
        row_i = i // k_len
        col_i = i % k_len
        if col_i == 0:
            l = []
            l.append(e)
            L.append(l)
        else:
            L[row_i].append(e)
    list_c = []
    for i in range(k_len):
        j = k.index(str(i + 1))
        for e in L:
            list_c.append(e[j])
    c = ''.join(list_c)
    return c


def decrypt(c, k):
    assert len(c) % len(k) == 0
    k_len = len(k)
    row = len(c) // k_len
    L = [[0 for j in range(k_len)] for i in range(len(c) // k_len)]
    for i, e in enumerate(c):
        row_i = i % row
        col_i = int(k.index(str(i // row + 1)))
        L[row_i][col_i] = e
    list_p = []
    for l in L:
        for e in l:
            list_p.append(e)
    p = ''.join(list_p)
    return p


if __name__ == '__main__':
    plain = 'tobeornottobethatisaquestion'
    cypher = 'obestdnfhhmoeaaohleywsdloreb'
    key = '6234517'
    print('the cypher of {} is {}'.format(plain, encrypt(plain, key)))
    key = '7345261'
    print('the plaintext of {} is {}'.format(cypher, decrypt(cypher, key)))
