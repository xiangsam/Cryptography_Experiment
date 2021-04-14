# -*- coding: utf-8 -*-
#!/usr/bin/python3
table = 'abcdefghijklmnopqrstuvwxyz'


def encrypt(p, k):
    """
    @p: p is a string
    """
    list_c = []
    key_len = len(k)
    for i, e in enumerate(p):
        t_index = table.index(e)
        k_index = i % key_len
        t_index = (t_index + table.index(k[k_index])) % 26
        list_c.append(table[t_index])
    c = ''.join(list_c)
    return c


def decrypt(c, k):
    """
    @c: c is a string
    """
    list_p = []
    key_len = len(k)
    for i, e in enumerate(c):
        t_index = table.index(e)
        k_index = i % key_len
        t_index = (t_index - table.index(k[k_index])) % 26
        list_p.append(table[t_index])
    p = ''.join(list_p)
    return p


if __name__ == '__main__':
    key = 'interesting'
    plain = 'zhonghuaminzuweidafuxing'
    print('the cypher of {} is {}'.format(plain, encrypt(plain, key)))
    key = 'boring'
    cypher = 'kqjyhynruwnadzmk'
    print('the plaintext of {} is {}'.format(cypher, decrypt(cypher, key)))
