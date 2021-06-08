# -*- coding:utf-8 -*-
#! /usr/bin/python3

import sys
sys.path.append('../..')
from MyCrypto.ECC.ecc import ECC
from MyCrypto.util.PF import PF

class DH:
    """
    Diffie-Hellman key exchange with ECC 
    """
    def __init__(self, G, n):
        """
        n is private key
        """
        assert isinstance(G, ECC)
        self.G = G
        self.n = n

    def getPubKey(self):
        return self.n * self.G

    def getShareKey(self, pk):
        assert isinstance(pk, self.G.__class__)
        return self.n * pk

if __name__ == '__main__':
    class PF_211(PF):
        def __init__(self, value, modulo=211):
            super().__init__(value, modulo)
    G = ECC(0, -4, PF_211, 2,2,False)
    dhA = DH(G, 121)
    dhB = DH(G, 203)
    Pa = dhA.getPubKey()
    Pb = dhB.getPubKey()
    print('The public Key of A: %s' %  Pa)
    print('The public Key of B: %s' % Pb)
    print('The shareKey A gets is %s' % dhA.getShareKey(Pb))
    print('The shareKey B gets is %s' % dhB.getShareKey(Pa))
