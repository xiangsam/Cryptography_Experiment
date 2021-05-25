# -*- coding: utf-8 -*-
#!/usr/bin/python3


def s2bs(s):
    """
    binary string of ASCII code, make sure each character'length is 8
    """
    bs = ''
    for c in s:
        bc = bin(ord(c)).replace('0b', '').zfill(8)
        bs = bs + bc
    return bs


def bs2s(s):
    return ''.join([
        chr(i) for i in [
            int(b, 2)
            for b in [s[index:index + 8] for index in range(0, len(s), 8)]
        ]
    ])

def xor(*args):
    """
    a, b is binary string
    """
    assert len(args) > 1
    lst = []
    array = list(args)
    maxlen = max([len(e) for e in array])
    for i,e in enumerate(array):
        if len(e) < maxlen:
            #array[i] = '0'*(maxlen-len(e))+e
            array[i] = e.zfill(maxlen)
    for i in range(maxlen):
        temp = array[0][i]
        for e in array[1:]:
            if temp == e[i]:
                temp = '0'
            else:
                temp = '1'
        lst.append(temp)
    return ''.join(lst)
def 
def i2bs(num, length):
    """
    digit to binary string
    length is the length of binary string
    """
    bs = bin(num).replace('0b', '')
    #bs = '0'*(length - len(bs)) + bs
    bs = bs.zfill(length)
    return bs

def bs2i(bs):
    return int(bs, base=2)
if __name__ == '__main__':
    num = 0x0f1571c947d9e859
    s = i2bs(num, 64)
    print(s)
    print(bs2i(s))
    print('##########')
    print(xor('10001', '10010', '11'))
