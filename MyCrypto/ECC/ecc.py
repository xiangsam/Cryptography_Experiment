# -*- coding:utf-8 -*-
#!/usr/bin/python3

import math
from random import randint

def s2n(s):
    return int.from_bytes(s, 'big')
def n2s(n):
    nbits = n.bit_length()
    nbytes = (nbits + 7) >> 3
    return n.to_bytes(nbytes, 'big')
class ECC:
    """
    y^2 = x^3 + a*x + b(mod p), (x, y) belong Zp*Zp
    """
    def __init__(self, a, b, field, x, y, isIdentity=False):
        if not (isinstance(a, field) and isinstance(b, field)):
            a, b = field(a), field(b)
        assert field(4)*a**3 + field(27)*b**2 != field(0)
        if not isIdentity:# P is not O
            if not (isinstance(x, field) and isinstance(y, field)):
                x, y = field(x), field(y)
            assert y**2 == x**3 + a * x + b#make sure the point is in the ECC
        self.a = a
        self.b = b
        self.field = field
        self.x = x
        self.y = y
        self.isIdentity = isIdentity

    def __call__(self, a=None,b=None,field=None, x=None, y=None, isIdentity=None):
        if a is None:
            a = self.a
        if b is None:
            b = self.b
        if field is None:
            field = self.field
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if isIdentity is None:
            isIdentity = self.isIdentity
        return self.__class__(a,b,field, x, y, isIdentity)

    def __repr__(self):
        if self.isIdentity:
            return 'Identity element'
        return '({},{})'.format(self.x, self.y)
    __str__ = __repr__

    def __neg__(self):
        if self.isIdentity:
            return self()
        return self(x=self.x, y = -self.y)

    def __eq__(self, other):
        assert isinstance(other, self.__class__) and other.field == self.field
        assert self.a == other.a and self.b == other.b #make sure self and other belong to the same abel group
        if self.isIdentity or other.isIdentity:
            return self.isIdentity and other.isIdentity
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        assert isinstance(other, self.__class__) and other.field == self.field
        assert self.a == other.a and self.b == other.b #make sure self and other belong to the same abel group
        #P+O = O+P = P
        if self.isIdentity:
            return other()
        if other.isIdentity:
            return self()
        if self == other:#P3 = P+P
            k = (self.field(3) * self.x * self.x + self.a)/(self.field(2)*self.y)#k is slope
        else:#P3 = P1+P2
            k = (other.y - self.y)/(other.x - self.x)
        x3 = k*k - self.x - other.x
        y3 = k*(self.x - x3) - self.y
        return self(x=x3, y=y3)

    def __sub__(self, other):
        assert isinstance(other, self.__class__) and other.field == self.field
        assert self.a == other.a and self.b == other.b #make sure self and other belong to the same abel group
        return self+(-other)

    def __mul__(self, k):#二进制展开法
        assert isinstance(k, int)
        Q = self(isIdentity=True)
        lst = list(bin(k).replace('0b', ''))
        while len(lst):
            Q = Q + Q
            if lst.pop(0) == '1':
                Q = Q + self
        return Q

    def __rmul__(self, k):
        assert isinstance(k, int)
        return self * k

    def getG(self):
        """
        get one point in ECC(a, b, Fp)
        """
        while(True):
            x = randint(0, self.field(0).modulo -1)
            x = self.field(x)
            alpha = x**3 + self.a*x+self.b
            if alpha.value == 0:
                return self(x=x.value, y=0,isIdentity=False)
            else:
                if alpha.sqrt() is None:
                    continue
                return self(x = x.value, y = alpha.sqrt()[0].value, isIdentity=False)


    def bytestrToPoint(self,  s):
        assert len(s) % 2 == 1#no compress method
        PC, X1, Y1 = s[0], s[1:(len(s)-1)//2+1], s[(len(s)-1)//2+1:]
        if PC == 0x00:
            return self(isIdentity=True)
        if not PC == 0x04:
            raise Exception
        xp = self.field(s2n(X1)) 
        yp = self.field(s2n(Y1))
        return self(x = xp, y = yp, isIdentity=False) 

    def pointToByteStr(self):
        assert self.isIdentity is False
        q = self.field().modulo
        l = math.ceil(math.ceil(math.log2(q))/8) 
        xp = self.x.value
        yp = self.y.value
        X1 = xp.to_bytes(l, 'big')
        Y1 = yp.to_bytes(l, 'big')
        PC = b'\x04'
        return b''.join([PC, X1, Y1])


if __name__ == '__main__':
    import sys 
    sys.path.append('../..')
    from MyCrypto.util.PF import PF
    class PF_11(PF):
        def __init__(self, value=0, modulo=11):
            super().__init__(value, modulo)
    p = ECC(1, 6, PF_11, 2, 7, False)
    print('p is %s' %p)
    print('test bytestrToPoint and the pointToByteStr: %s' % p.bytestrToPoint(p.pointToByteStr()))
    #print(p.strToPoint())
    for i in range(2, 13):
        print('[{}]p is {}'.format(str(i),str(i * p)))
