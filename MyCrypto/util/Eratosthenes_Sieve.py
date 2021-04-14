# -*- coding: utf-8 -*-
#!/usr/bin/python3
import numpy
import math
def Sieve(n):
    """initial version"""
    if n < 2:
        print("Can't find!!!")
    else:
        ans = []
        list = numpy.ones(n+1, dtype = bool)
        for i in range(2, int(math.sqrt(n))+1):
            if list[i] == list[0]:
                j = i * i #don't need to start at i * 2
                while j < n:
                    list[j] = b'0'
                    j = j+i
        for i in range(2, n+1):
            if list[i] == list[0]:
                ans.append(i)
    return ans

def Sieve2(n):
    """only create odd table"""
    if n < 2:
        print("Can't find!!!")
    else:
        ans = [2]
        size = (n-2)//2 if n%2 == 0 else (n-1)//2
        list = numpy.ones(size + 1, dtype = bool)
        print(size)
        for i in range(1, len(list)):
            if list[i] == True:
                odd = 2 * i + 1
                j = odd * odd
                base = (j-1) // 2
                while base <= size:
                    list[base] = False
                    j = j + odd * 2 # make sure j is odd
                    base = (j-1) // 2
        for i in range(1, len(list)):
            if list[i] == True:
                ans.append(2*i + 1)
    return ans

def Sieve3(n):
    """block sieve"""
    S = 1000000
    prime_size = int(math.sqrt(n))
    print(prime_size)
    f = open('output3', 'w')
    f.write(str(n)+'\n')
    base_list = numpy.ones(prime_size + 1, dtype = bool)
    prime_list = numpy.empty(1,dtype = int)
    prime_list[0] = 2
    for i in range(2, prime_size+1):
        if base_list[i] == True:
            if i != 2:
                prime_list = numpy.append(prime_list, i)
            j = i * i
            while j <= prime_size:
                base_list[j] = False
                j = j + i
    offset = 0
    num = 0 #the num of prime
    while offset * S <= n:
        print(str(offset)+'===>' + str(offset * S / n))
        block = numpy.ones(S, dtype = bool)
        if offset == 0:
            block[0] = False
            block[1] = False
        for p in prime_list:
            j = max(p, (offset * S + p - 1) // p) * p -offset * S #get the closest number of the multiple of p and get the index of it in block
            while j < S:
                block[j] = False
                j = j + p
        for i in range(S):
            if offset * S + i > n:
                break
            if block[i] == True:
                f.write(str(offset * S + i)+' ')
                num = num + 1
        offset = offset + 1
    f.write('\n')
    f.close()
    print(num)

if __name__ == '__main__':
    test = [2, 103, 10**4, 10**6]#4275117753
    '''
    with open('output1', 'w') as f:
        for e in test:
            f.write(str(e)+'\n')
            array = Sieve2(e)
            s = " ".join(str(x) for x in array)
            f.write(s+'\n')
    '''
    with open('output', 'w') as f:
        for e in test:
            f.write('\n' + str(e) + '\n')
            array = Sieve2(e)
            f.write('the num of primes is :' + str(len(array)) + '\n')
            s = " ".join(str(x) for x in array)
            f.write(s+'\n')
    #Sieve3(4275117753)
