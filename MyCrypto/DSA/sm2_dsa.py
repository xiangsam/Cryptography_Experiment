# -*- coding:utf-8 -*-
#!/usr/bin/python3

import sys
sys.path.append('../..')
from hashlib import sha512
from MyCrypto.ECC.ecc import ECC,n2s, s2n
from MyCrypto.util.PF import PF
from MyCrypto.util.inverse_mod import inverse_mod
from random import randint
import math
from gmssl.sm3 import sm3_hash


class SM2_DSA:
    def __init__(self, n,G, dk, ID):
        """
        dk is private Key
        """
        self.v = 256
        self.n = n
        self.G = G
        self.dk = dk
        self.pubK = self.dk * self.G
        self.byteLen = math.ceil(math.ceil(math.log2(self.G.field().modulo))/8)
        self._ID = ID
        self._ENTL = len(self._ID)*8
        self.Z = self.getZ()

    def sign(self, message):
        M = self.Z + message
        e = int.from_bytes(SM2_DSA.HASH(M), 'big')
        while True:
            #k = randint(1, self.n-1)
            k = 0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F
            point = k * self.G
            x1 = point.x.value
            r = (e+x1) % self.n
            s = (inverse_mod(1+self.dk, self.n) * ((k-r * self.dk) % self.n)) % self.n
            if r != 0 and r+k != self.n and s != 0:
                return n2s(r), n2s(s)
             
    def verify(self, message, sign):
        r , s = sign
        r = int.from_bytes(r, 'big')
        s = int.from_bytes(s, 'big')
        if not 1 <= r <= self.n-1:
            return False
        if not 1 <= s <= self.n-1:
            return False
        e = int.from_bytes(SM2_DSA.HASH(self.Z+message), 'big')
        t = (r + s) % self.n
        if t == 0:
            return False
        point = s*self.G + t * self.pubK
        x1 = point.x.value
        R = (e + x1) % self.n
        if R == r:
            return True
        return False


    def getZ(self):
        byteStr = self._ENTL.to_bytes(2, 'big') + self._ID
        byteStr += n2s(self.G.a.value) + n2s(self.G.b.value) + self.G.pointToByteStr()[1:] + self.pubK.pointToByteStr()[1:]
        return SM2_DSA.HASH(byteStr)

    @staticmethod
    def HASH(byteStr):
        #  s = sha512()
        #  s.update(byteStr)
        #  return s.digest()
        msg = [i for i in byteStr]
        ans = sm3_hash(msg)
        return bytes.fromhex(ans)

if __name__ == '__main__':
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    x = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    class PF_p(PF):
        def __init__(self, value=0, modulo = p):
            super().__init__(value, modulo)
    G = ECC(a,b,PF_p, x,y,False)
    dk = 0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263
    ID = b'ALICE123@YAHOO.COM'
    dsa = SM2_DSA(n, G, dk,ID)
    message = b'message digest'
    sign = dsa.sign(message)
    print('Za: ', dsa.Z)
    print('sign: ', sign)
    print('if receive message: ', message)
    print('verified? ', dsa.verify(message, sign))
    message += b'w'
    print('if receive message: ', message)
    print('verified? ', dsa.verify(message, sign))
