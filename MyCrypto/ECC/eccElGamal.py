# -*- coding:utf-8 -*-
#!/usr/bin/python3

import sys
sys.path.append('../..')
from MyCrypto.ECC.ecc import ECC
from MyCrypto.util.PF import PF
from random import randint

class ElGamal:
    def __init__(self, G, n):
        self.G = G
        self.n = n #private key

    def getPubKey(self):
        return self.n * self.G

    def encrypt(self, pm, pk):
        #k = randint(1, self.n)
        x = self.G(isIdentity=True)
        while x.isIdentity:#make sure k * pk is point of ECC and not ZERO
            k = randint(1, self.n-1)
            x = k * pk
        return (k*self.G, pm+x)

    def decrypt(self, c):
        return c[1] -self.n *  c[0]

if __name__ == '__main__':
    class PF_p(PF):
        def __init__(self, value, modulo=6277101735386680763835789423207666416083908700390324961279):
            super().__init__(value, modulo)

    G = ECC(-3, 2455155546008943817740293915197451784769108058161191238065, PF_p, 602046282375688656758213480587526111916698976636884684818,174050332293622031404857552280219410364023488927386650641,False)
    elgamalA = ElGamal(G, 963733050849230262168000691203)
    elgamalB = ElGamal(G, 273065013239976945911310331771)
    print(G.getG())
    #Pa = elgamalA.getPubKey()
    #Pb = elgamalB.getPubKey()
    #print('Public Key: ' )
    #print('A: {}'.format(str(Pa)))
    #print('B: {}'.format(str(Pb)))
    Pa = G(x = 4535708181192800030922425040161683059768487875080759471914, y = -1061575060680846108649238340040410272066486614691829051119)
    Pb = G(x = 15051890357046942792346514451227979111717518527499676907, y = 5515597659079030185293133062027700068886157516430489991452)
    Pm = G(x = 2594161300049362469169638638781986485403377947559889224556, y = -915731655498392811604767074090214190962897463083669095347)
    Pc = elgamalA.encrypt(Pm, Pa)
    print('Pm is %s' % Pm)
    print('Pc is :',end=' ')
    print(Pc)
    print('From Pc decrypt Pm is %s' % elgamalA.decrypt(Pc))
