# -*- coding:utf-8 -*-
class GF:
    def __init__(self, value,  order=0):
        if isinstance(value, GF):
            value = value.value
        assert isinstance(value, int)
        self.value = value
        self.order = order
        if order == 0:
            self.modulo = 0
        elif order == 8:
            self.modulo = 0x11b #Primitive polynomial is x^8 + x^4 + x^3 + x + 1
        elif order == 128:
            self.modulo = 0x100000000000000000000000000000087
        else:
            raise Exception

    def __call__(self, value=None,order=None):#need for subclass
        if value is None:
            value = self.value
        if order == None:
            order = self.order
        return self.__class__(value, order)
    def __repr__(self):
        return '%02x' % (self.value)
    __str__ = __repr__
    def  __hash__(self):
        return self.value
    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, self.__class__) and self.order == other.order:
            return self.value == other.value
        else:
            raise Exception

    def __add__(self, other):
        """add in GF(2^order)"""
        assert isinstance(other, self.__class__) and self.order == other.order 
        return self((self.value)^(other.value), self.order)
    def __sub__(self, other):
        """sub in GF(2^order)"""
        assert isinstance(other, self.__class__) and self.order == other.order 
        return self((self.value)^(other.value), self.order)
    def __mul__(self, other):
        """mul in GF(2^order)"""
        assert isinstance(other, self.__class__) and self.order == other.order and self.order != 0
        temp = self.value
        res = (other.value & 1) * temp
        for i in range(1, self.order):
            if temp & (1 << (self.order -1)):# simple shift in GF(2^order)
                temp = (temp << 1) ^ self.modulo
            else:
                temp = temp << 1
            res ^= (((other.value >> i) & 1) * temp) #if now the bit is 1, then add
        return self(res, self.order)
    def __pow__(self, power):
        """pow in GF(2^order)"""
        if isinstance(power, self.__class__):
            power = power.value
        assert isinstance(power , int) and power >= -1
        if power == -1:
            return self.inverse()
        d = self(1, self.order)
        while power > 0:
            if power % 2  == 1:
                d = d * self
                power = (power-1) // 2
            else:
                power = power // 2
            self = self * self
        return d
    def __mod__(self, other):
        """the Division with remainder in GF(2)"""
        assert isinstance(other, self.__class__)
        if self.degree < other.degree:
            return self
        else:
            dif = self.degree - other.degree
            a = self.value
            b = other.value
            a = a ^ (b << dif)
            r = self(a,self.order) % self(b,self.order)
            return r
    def __truediv__(self, other):
        """Division in GF(2^order)"""
        assert isinstance(other, self.__class__) and self.order == other.order
        return self * other.inverse()
    def __floordiv__(self, other):
        """the Division with remainder in GF(2), use //"""
        assert isinstance(other, self.__class__)
        if self.degree < other.degree:
            return self(0,self.order)
        else:
            dif = self.degree - other.degree
            a = self.value
            b = other.value
            a = a ^ (b << dif)
            q = self(a,self.order) // self(b,self.order)
            return self((1<<dif) | q.value,self.order)
    
    def inverse(self):
        """get the inv in GF(2^order)"""
        if self.value == 0:
            return self(0, self.order)
        else:
            for i in range(1, 256):
                mul = self * self(i, self.order)
                if mul.value == 1:
                    return self(i, self.order)
    def inverse2(self):
        if self.value == 0:
            return self(0,self.order)
        else:
            x, y, d = GF.exgcd(self, self(self.modulo,self.order))
            return self(x.value, self.order)    
    
    @staticmethod
    def gcd(a, b):
        """gcd  in  GF(2)"""
        if b.value == 0:
            return a
        else:
            return GF.gcd(b, a%b)
    @staticmethod
    def exgcd(a, b):
        """x * a + y * b == gcd(a,b)"""
        if b.value == 0:
            return a(1,a.order), a(0,a.order), a
        else:
            x1, y1, d = GF.exgcd(b, a % b)
            x, y = y1, x1 - (a // b) * y1
            return x, y, d
            
    @staticmethod
    def Pri_poly(n):
        """get the primitive polynomial of GF(2), the degree is n"""
        m = GF((1 << (2**n - 1)) | 1)
        for p_i in range(1<<n, 1<<(n+1)):
            p = GF(p_i)
            for k_i in range(2, p_i):
                k = GF(k_i)
                if (p % k).value == 0:
                    k_i = -1
                    break
            if k_i != -1: #p is irreducible polynomial
                if (m % p).value == 0:
                    for j in range(1, 2**n - 1):
                        q = GF((1<<(j)) | 1)
                        if (q % p).value == 0:
                            j = -1
                            break
                    if j != -1:
                        print(p)
    @property
    def degree(self):
        if self.value == 0:
            return -1
        else:
            return self.value.bit_length()

if __name__ == '__main__':
    #part one
    a = [0x89, 0xaf, 0x35]
    b = [0x4d, 0x3b, 0xc6]
    for i in range(len(a)):
        aa = GF(a[i],8)
        bb = GF(b[i],8)
        print('a+b:{} a-b:{}'.format(aa+bb, aa-bb))
    a = [0xce, 0x70, 0x00]
    b = [0xf1, 0x99, 0xa4]
    for i in range(len(a)):
        aa = GF(a[i],8)
        bb = GF(b[i],8)
        print('a*b:{}'.format(aa * bb))
    a = [0xde, 0x8c, 0x3e]
    b = [0xc6, 0x0a, 0xa4]
    for i in range(len(a)):
        aa = GF(a[i],8)
        bb = GF(b[i],8)
        print('a/b:{}'.format(aa // bb))
    
    #part two
    print()
    a = [0x89, 0x3e, 0x19, 0xba]
    b = [18829, 28928, 26460, 13563]
    for i in range(len(a)):
        aa = GF(a[i],8)
        bb = GF(b[i],8)
        print('a^b:{}'.format(aa**bb))
    
    #part three
    print()
    a = [0x75, 0xac, 0xf8, 0x48]
    b = [0x35, 0x59, 0x2e, 0x99]
    for i in range(len(a)):
        aa = GF(a[i],8)
        bb = GF(b[i],8)
        print(GF.exgcd(aa, bb))
    
    #part four
    print()
    a = [0x8c, 0xbe, 0x01, 0x2d]
    for i in a:
        aa = GF(i,8)
        print('The inverse of {} is：{}'.format(hex(i), aa.inverse()))

    #part five
    print()
    GF.Pri_poly(8)


    print('#####')
    print(GF(0x1c, 8).inverse())
    print(GF(0x1c,8).inverse2())
