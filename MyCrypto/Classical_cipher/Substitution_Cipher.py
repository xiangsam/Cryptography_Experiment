# -*- coding: utf-8 -*-
#!/usr/bin/python3
def encrypt(ptable, ctable, p):
    list_c = []
    for e in p:
        if e.isalpha():
            index = ptable.index(e.lower())
            list_c.append(ctable[index])
        else:
            list_c.append(e)
    c = ''.join(list_c)
    return c


def decrypt(ptable, ctable, c):
    list_p = []
    for e in c:
        if e.isalpha():
            index = ctable.index(e.lower())
            list_p.append(ptable[index])
        else:
            list_p.append(e)
    p = ''.join(list_p)
    return p


if __name__ == '__main__':
    plain = 'doyouwannatodance'
    cypher = 'youcanreallydance'
    m_ptable = 'abcdefghijklmnopqrstuvwxyz'
    m_ctable = 'qazwsxedcrfvtgbyhnujmiklop'
    print('the cypher of {} is {}'.format(plain, encrypt(m_ptable, m_ctable, plain)))
    print('the plaintext of {} is {}'.format(cypher, decrypt(m_ptable, m_ctable, cypher)))
