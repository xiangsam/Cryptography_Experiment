# -*- coding:utf-8 -*-
#!/usr/bin/python2

import sys
sys.path.append('../..')
from MyCrypto.util.s2bs import s2bs,bs2s

def hexToStr(num):
    bs = bin(num).replace('0b', '')
    if len(bs)%8 != 0:        
        bs = '0'*(8-len(bs)%8)+bs
    return bs2s(bs);

def KSA(key):
    """
    The key-scheduling algorithm is used to initialize the permutation in the array S
    """
    assert 1 <= len(key) <= 256
    keyLength = len(key)
    S = []
    for i in range(0, 256):
        S.append(i)
    j = 0
    for i in range(0, 256):
        j = (j + S[i] + ord(key[i % keyLength])) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    """
    Pseudo-random generation algorithm
    """
    i = 0
    j = 0
    while True:
        i = (i+1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def encrypt(plain, key):
    """
    RC4 encrypt part
    """
    S = KSA(key)
    K = PRGA(S)
    lst = []
    for e in plain:
        lst.append('%02x' % (ord(e) ^ next(K)))
    return ''.join(lst)

if __name__ == '__main__':
    #print('Plaintext: {}, RootKey: {}'.format('Plaintext','Key'))
    #print('the hex of cypher: '+encrypt('Plaintext', 'Key'))
    #print('Plaintext: {}, RootKey: {}'.format('pedia','Wiki'))
    #print('the hex of cypher: '+encrypt('pedia', 'Wiki'))
    #print('Plaintext: {}, RootKey: {}'.format('Attack at dawn','Secret'))
    #print('the hex of cypher: '+encrypt('Attack at dawn', 'Secret'))
    key = hexToStr(0xc585169d3de1357b654123febaa2fcc8e969efa0e4eda3dee4fbffb061a1e0d90c13c72cb6e938c5)
    plain = hexToStr(0xb7de0c1178d230c19839249b2b7b7dc93652d3b855df74092535af84aa0ce960faff0c0ca01f331a3a)
    cypher = hexToStr(0xb314e77e2c9d1e21958ed33dedef43053533ccd0677b7a346e0b3a4d1b86e1a846f2fd6607307fd978e7)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0xaf6ecc24f5147b4e)
    plain = hexToStr(0x0e97c22ac58a40fcbdb3083c485b30b541d04378d3c3dfa7400ae7da3bbfb2de5e4f9a81)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0xe47f1bbe08856a6680fbd7c5fdd32bc6534277e8cac10aadbe2e5cfecf4837d6d167b9b33d0124282ed5fe0e65e4016ee6535ba8c8bc3f6f69)
    plain = hexToStr(0xaa227b883f0ff6f991c43ff449c3eaf60372ce8eb1bb0592b8)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0x685148204d79657ee2f1ac15391f3c426c5c47abd774631539595bac67403bbfa9c137e14b7bf509fd7f3e33a3d102dd862aa16be1)
    plain = hexToStr(0x28a2e395bcdf42652a37058bfd1bb061d1f21ba9b7a66036d544ef30b3f03a241f5e3991da3af78d59a1d21ee4d57fa16a5da4f6bb038de21dd4789c18)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0x08704a770630c389abceba673732a7744d1a4625c5e58a45c9b7a8d19899283dd6f6c8ee6a8f78be5f286fab031824f81bad564a6d85155c)
    plain = hexToStr(0xf4a6763c2037033ba39589c145)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0x8c711bb563c668f6d61f758b8dc8cc76a682ece88034f77a90f8f5d8)
    plain = hexToStr(0xd02a80213b7c368822a519761bfd32d6ecc22a)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0x680fec38f5681bc86b4fd5a182350a9b853d0086b35130)
    plain = hexToStr(0xe3be2b4829402d5711a16a74ca12fa4877464a5fbcf309cc45452cc24eabbbcbfc994374d3f452ffcde9ed50bac72d30fa207e2e25)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0xf49e31535c7741cc711fa7283e4fa2028515f319a7)
    plain = hexToStr(0xe06f302e46319db4ffb5ba68178d4760ff8036522dd6beda77fd4907fc68761e0c0a67852b1f142932e427e94d1a2d19ae87)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0x9653709d601eb86822dd5085e7e09f9ce4e9e13bbec0d763207065593678a395344b2dd6a0d0631d6323797d6c)
    plain = hexToStr(0xa267910de0aa16bcc6e2fd535d036be1f544f8c741f2535c19ce8c8977aba94eeac152fbd68d3517429e426c29d9c009fa7626)
    print('the hex of ans: '+encrypt(plain, key))
    key = hexToStr(0x37e12365d9cab785db06289caadcdededc9896df46eb536b04c9588f755a008d3c09)
    plain = hexToStr(0x26ec1178bd763e8aea49f2882496d1bd4b05d1ea3e4eefd2346288deb4b0314b7d)
    print('the hex of ans: '+encrypt(plain, key))
