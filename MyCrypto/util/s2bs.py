#!/usr/bin/python3


def s2bs(s):
    """
    binary string of ASCII code, make sure each character'length is 8
    """
    bs = ''
    for c in s:
        bc = bin(ord(c)).replace('0b', '')
        bc = '0' * (8 - len(bc)) + bc
        bs = bs + bc
    return bs


def bs2s(s):
    return ''.join([
        chr(i) for i in [
            int(b, 2)
            for b in [s[index:index + 8] for index in range(0, len(s), 8)]
        ]
    ])

def i2bs(num, length):
    """
    digit to binary string
    length is the length of binary string
    """
    bs = bin(num).replace('0b', '')
    bs = '0'*(length - len(bs)) + bs
    return bs

def bs2i(bs):
    return int(bs, base=2)
if __name__ == '__main__':
    num = 0x0f1571c947d9e859
    s = i2bs(num, 64)
    print(s)
    print(bs2i(s))
