# -*- coding: utf-8 -*-
#!/usr/bin/python3
import random
import sys
sys.path.append('../..')

from MyCrypto.util.pow_modual import quickPow
from MyCrypto.util.gcd import gcd
def Miler_Rabin(n):
    """
    Miller–Rabin primality test
    if the number is Prime number, then return True.
    """
    test_time = 100
    if n % 2 == 0:
        #print("Composite number")
        return False
    else:
        tmp = n-1
        k = 0
        while(tmp %2 == 0):
            tmp = tmp // 2
            k  = k + 1
        q = (n-1)// (2**k)
        assert(2**k * q == n-1)
        for i in range(test_time):
            a = random.randint(2, n-2)
            if(quickPow(a, q, n) == 1):
                continue
            for j in range(0,k):
                if quickPow(a,(2**j) * q, n) == n-1:
                    j = -1
                    break
            if j != -1:
                #print('Composite number')
                return False
        #print("Prime number")
        return True

def isPrime(n):
    return Miler_Rabin(n)

if __name__ == '__main__':
    n = [1000023, 1000033, 100160063, 1500450271, 1494462659429290047815067355171411187560751791530,
         22490812876539885046336053040043361022772062226905764414319531416752624982967181455912526153033030222985778230314070837549143068021815197910334221004333099,
         173114538715442253801652636578504897235814058376012019984132280493073144140873423822066926533851768593567972986030786930865304524765873917291156820356593465395949615668311730524585862713216977118030162614331116320577533153712280997129347743623082819252354000224098702300466561157715990374851814717133985999661
        ]
    for num in n:
        print(num)
        Miler_Rabin(num)
