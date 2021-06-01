# -*- coding:utf-8 -*-
#!/usr/bin/python3

import sys
sys.path.append('../..')
from MyCrypto.util.Miler_Rabin import isPrime 
from MyCrypto.util.inverse_mod import inverse_mod

class PF:
    """
    prime field GF(p)
    """
    def __init__(self, value, modulo):
        #assert isPrime(modulo)
        assert isinstance(value, int) and isinstance(modulo, int)
        self.value = value % modulo
        self.modulo = modulo

    def __call__(self, value=None, modulo=None):
        if value == None:
            value = self.value
        if modulo == None:
            modulo = self.modulo
        return self.__class__(value, modulo)

    def __repr__(self):
        return str(self.value)
    __str__ = __repr__

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, self.__class__):
            return self.value == other.value
        raise Exception

    def __neg__(self):
        return self(-self.value)

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        return self(self.value + other.value)

    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        return self(self.value - other.value)

    def __mul__(self, other):
        assert isinstance(other, self.__class__)
        return self(self.value * other.value)

    def __truediv__(self, other):
        assert isinstance(other, self.__class__)
        return self * other.inverse()

    def __pow__(self, power):
        if isinstance(power, self.__class__):
            power = power.value
        assert isinstance(power , int) and power >= -1
        if power == -1:
            return self.inverse()
        d = self(1)
        while power > 0:
            if power % 2  == 1:
                d = d * self
                power = (power-1) // 2
            else:
                power = power // 2
            self = self * self
        return d

    def sqrt(self):
        """
        only work if  modulo % 4 == 3 or modulo % 8 == 5
        """
        if self.value == 0:
            return self(0)
        if self.modulo % 4 == 3:
            u = (self.modulo - 3) // 4
            y = self**(u+1)
            z = y ** 2
            if z == self:
                return (y, -y)
            return None
        if self.modulo % 8 == 5:
            u = (self.modulo - 5) // 8
            y = self**(self(value=2)*u+self(value=1))
            z = y**2
            if z == self:
                return(y, -y)
            return None
        return None

    def inverse(self):
        a = self.value
        m = self.modulo
        a_inv = inverse_mod(a, m)
        return self(a_inv)

if __name__ == '__main__':
    a = PF(3, 23)
    b = PF(5, 23)
    print('a', a)
    print('-a', -a)
    print('b', b)
    print('a+b', a+b)
    print('a-b', a-b)
    print('a*b', a*b)
    print('a/b', a/b)
    print('a/a', a/a)
    print('a^3', a**3)
    print('a^-1', a**-1)
    print('a^1/2', a.sqrt())
