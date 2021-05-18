# -*- coding: utf-8 -*-

class GF2:
    """
    the polynomial is x^8 + x^4 + x^3 + x^1 + x^0
    """
    def __init__(self, value):
        if isinstance(value, GF2):
            self.value = value.value
        else:
            self.value = value
    def getValue(self):
        return self.value
    def __str__(self):
        return '%02x' % (self.value)
    __repr__ = __str__
    def __iter__(self):
        return self
    def __eq__(self, other):
        return self.value == other.value
    def __hash__(self):
        return self.value
    def __next__(self):
        return self
    def __add__(self, other):
        return GF2(self.value ^ other.value)
    def __sub__(self, other):
        return GF2(self.value ^ other.value)
    def __mul__(self, other):
        """in GF(2^8)"""
        a = self.value
        b = other.value
        ans = 0
        for i in range(8):
            if b & 1 == 1:
                ans = ans ^ a
            overl = a & 0x80
            a = (a << 1) & 0xff
            if overl == 0x80:
                a = a ^ 0x1b
            b = b >> 1
        return GF2(ans)
    def __floordiv__(self, other):
        """the Division with remainder in GF(2), use //"""
        if self.degree < other.degree:
            return GF2(0)
        else:
            dif = self.degree - other.degree
            a = self.value
            b = other.value
            a = a ^ (b << dif)
            q = GF2(a) // GF2(b)
            return GF2((1<<dif) | q.value)
    def __truediv__(self, other):
        """the Division in GF(2^8), use /"""
        return self * other.inverse()
    def __mod__(self, other):
        """the Division with remainder in GF(2)"""
        if self.degree < other.degree:
            return self
        else:
            dif = self.degree - other.degree
            a = self.value
            b = other.value
            a = a ^ (b << dif)
            r = GF2(a) % GF2(b)
            return r
    def __pow__(self, other):
        d = GF2(1)
        n = other.value
        while n > 0:
            if n % 2  == 1:
                d = d * self
                n = (n-1) // 2
            else:
                n = n // 2
            self = self * self
        return d
    def inverse(self):
        if self.value == 0:
            return GF2(0)
        else:
            for i in range(1, 256):
                mul = self * GF2(i)
                if mul.value == 1:
                    return GF2(i)
    def inverse2(self):
        if self.value == 0:
            return GF2(0)
        else:
            x, y, d = GF2.exgcd(self, GF2(0x11b))
            return x

    @staticmethod
    def gcd(a, b):
        if b.value == 0:
            return a
        else:
            return GF2.gcd(b, a%b)
    @staticmethod
    def exgcd(a, b):
        """x * a + y * b == gcd(a,b)"""
        if b.value == 0:
            return GF2(1), GF2(0), a
        else:
            x1, y1, d = GF2.exgcd(b, a % b)
            x, y = y1, x1 - (a // b) * y1
            return x, y, d
            
    @staticmethod
    def Pri_poly(n):
        """get the primitive polynomial of GF(2), the degree is n"""
        m = GF2((1 << (2**n - 1)) | 1)
        for p_i in range(1<<n, 1<<(n+1)):
            p = GF2(p_i)
            for k_i in range(2, p_i):
                k = GF2(k_i)
                if (p % k).value == 0:
                    k_i = -1
                    break
            if k_i != -1: #p is irreducible polynomial
                if (m % p).value == 0:
                    for j in range(1, 2**n - 1):
                        q = GF2((1<<(j)) | 1)
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
        aa = GF2(a[i])
        bb = GF2(b[i])
        print('a+b:{} a-b:{}'.format(aa+bb, aa-bb))
    a = [0xce, 0x70, 0x00]
    b = [0xf1, 0x99, 0xa4]
    for i in range(len(a)):
        aa = GF2(a[i])
        bb = GF2(b[i])
        print('a*b:{}'.format(aa * bb))
    a = [0xde, 0x8c, 0x3e]
    b = [0xc6, 0x0a, 0xa4]
    for i in range(len(a)):
        aa = GF2(a[i])
        bb = GF2(b[i])
        print('a/b:{}'.format(aa // bb))
    
    #part two
    print()
    a = [0x89, 0x3e, 0x19, 0xba]
    b = [18829, 28928, 26460, 13563]
    for i in range(len(a)):
        aa = GF2(a[i])
        bb = GF2(b[i])
        print('a^b:{}'.format(aa**bb))
    
    #part three
    print()
    a = [0x75, 0xac, 0xf8, 0x48]
    b = [0x35, 0x59, 0x2e, 0x99]
    for i in range(len(a)):
        aa = GF2(a[i])
        bb = GF2(b[i])
        print(GF2.exgcd(aa, bb))
    
    #part four
    print()
    a = [0x8c, 0xbe, 0x01, 0x2d]
    for i in a:
        aa = GF2(i)
        print('The inverse of {} is：{}'.format(hex(i), aa.inverse()))

    #part five
    print()
    GF2.Pri_poly(8)


    print('#####')
    print(GF2(0x1c).inverse())
    print(GF2(0x1c).inverse2())
