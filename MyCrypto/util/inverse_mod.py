# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys
sys.path.append("../..")
from MyCrypto.util import gcd
def inverse_mod(a, m):
    """get the inverse of a modual m"""
    assert isinstance(a, int)
    assert isinstance(m,int)
    d, p, q = gcd.exgcd(a, m)
    if d == 1:
        while p < 0:
            p += m 
        return p
    else:
        print("Wrong")
        return -1

if __name__ == '__main__':
    print(inverse_mod(5,9))
