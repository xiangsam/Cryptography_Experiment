# -*- coding:utf-8 -*-
#!/usr/bin/python3

import sys
sys.path.append('../..')
from hashlib import sha512
from MyCrypto.ECC.ecc import ECC,n2s, s2n
from MyCrypto.util.PF import PF
from random import randint
import math
from gmssl.sm3 import sm3_hash

class SM2:
    def __init__(self, n,G, dk):
        """
        dk is private Key
        """
        self.v = 256
        self.n = n
        self.G = G
        self.dk = dk
        self.pubK = self.dk * self.G
        self.byteLen = math.ceil(math.ceil(math.log2(self.G.field().modulo))/8)

    def encrypt(self, M):
        while True:
            #k = randint(1, self.n - 1)
            k = 0x384F30353073AEECE7A1654330A96204D37982A3E15B2CB5
            C1 = k * self.G
            byteC1 = C1.pointToByteStr()
            print('encrypt byteC1:',byteC1)
            p2 = k * self.pubK
            x2 = p2.x.value.to_bytes(self.byteLen, 'big')
            y2 = p2.y.value.to_bytes(self.byteLen, 'big')
            t = SM2.KDF(x2+y2, len(M) * 8)
            #t = n2s(0x046B04A9ADF53B389B9E2AAFB47D90F4D08978)
            print('t:', t)
            if s2n(t) == 0:
                continue
            byteM = M.encode('utf-8')
            byteC2 = b''
            for i, j in zip(byteM, t):
                tmp = i ^ j
                if tmp == 0:
                    byteC2 += b'\x00'
                else:
                    byteC2 += n2s(tmp)
            print('encrypt byteC2:',byteC2)
            byteC3 = SM2.HASH(x2+byteM + y2)
            print('encrypt byteC3:',byteC3)
            return byteC1 + byteC3 + byteC2
    
    def decrypt(self, C):
        byteC1, C = C[:2*self.byteLen + 1],C[2*self.byteLen + 1:]
        byteC3, byteC2 = C[:256//8], C[256//8:]
        C1 = self.G.bytestrToPoint(byteC1)
        p2 = self.dk * C1
        x2 = p2.x.value.to_bytes(self.byteLen, 'big')
        y2 = p2.y.value.to_bytes(self.byteLen, 'big')
        t = SM2.KDF(x2+y2, len(byteC2) * 8)
        M = b''
        for i, j in zip(byteC2, t):
            tmp = i ^ j
            if tmp == 0:
                M += b'\x00'
            else:
                M += n2s(tmp)
        u = SM2.HASH(x2+M+y2)
        if not u == byteC3:
            raise Exception
        return M.decode('utf-8')

    
    @staticmethod
    def HASH(byteStr):
        #  s = sha512()
        #  s.update(byteStr)
        #  return s.digest()
        msg = [i for i in byteStr]
        ans = sm3_hash(msg)
        return bytes.fromhex(ans)

    @staticmethod
    def KDF(Z, klen):
        """
        Z is bytes string
        klen is bits length
        """
        assert klen % 8 == 0
        klen = klen // 8
        ct = 0x00000001
        t = b''
        for i in range(math.ceil(klen/(256//8))):
            t += SM2.HASH(Z+ct.to_bytes(4, 'big'))
            ct += 1
        return t[:klen]
            


if __name__ == '__main__':
    a = 0xBB8E5E8FBC115E139FE6A814FE48AAA6F0ADA1AA5DF91985
    b = 0x1854BEBDC31B21B7AEFC80AB0ECD10D5B1B3308E6DBF11C1
    p = 0xBDB6F4FE3E8B1D9E0DA8C0D46F4C318CEFE4AFE3B6B8551F
    x = 0x4AD5F7048DE709AD51236DE65E4D4B482C836DC6E4106640
    y = 0x02BB3A02D4AAADACAE24817A4CA3A1B014B5270432DB27D2
    class PF_p(PF):
        def __init__(self, value=0, modulo=p):
            super().__init__(value, modulo)
    G = ECC(a, b, PF_p, x, y, False)
    n = 0xBDB6F4FE3E8B1D9E0DA8C0D40FC962195DFAE76F56564677
    dk = 0x58892B807074F53FBF67288A1DFAA1AC313455FE60355AFD
    sm2 = SM2(n, G, dk)
    print('publik key x:' , hex(sm2.pubK.x.value))
    print('public key y:' ,hex(sm2.pubK.y.value))
    M = 'encryption standard'
    print('message is:',M)
    ans = sm2.encrypt(M)
    print('decrypt message is:',sm2.decrypt(ans))
