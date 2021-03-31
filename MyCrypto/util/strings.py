#-*- coding:utf-8 -*-

def s2n(s):
    """
    String to number
    """
    if not len(s):
        return 0
    return int(s.encode('hex'), 16)

def n2s(n):
    """
    Number to String
    """
    s = hex(n)[2:].rstrip('L')
    if len(s) % 2 != 0:
        s = '0' + s
    return s.decode('hex')
