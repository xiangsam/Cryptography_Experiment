# -*- coding: utf-8 -*-
#!/usr/bin/python2

import sys
sys.path.append('../..')
from MyCrypto.util.s2bs import s2bs, bs2s, i2bs, xor
from MyCrypto.SM4.sm4 import SM4

def readFile(filename):
    with open(filename,'rb') as f:
        while True:
            data = f.read(16)
            if not data:
                break
            yield data

def padding(data):
    """
    use PKCS7 mode to padding
    """
    assert len(data)<16
    padlen = 16-len(data)
    data += chr(padlen)*padlen
    return data

def rmpadding(data):
    """
    padding mode is PKCS7
    """
    assert len(data) == 16
    padlen = ord(data[-1])
    return data[0:-padlen]

def ECB(cipher_func,inputf, outputf, mode = 'encrypt'):
    assert mode in ('encrypt', 'decrypt')
    anslst = []
    for e in readFile(inputf):
        if mode == 'encrypt' and len(e) < 16:
            e = padding(e)
        data = s2bs(e)
        out = cipher_func(int(data,2), 0x0123456789abcdeffedcba9876543210).process(mode)
        out = bs2s(out)
        anslst.append(out)
    if mode == 'decrypt':
        anslst[-1] = rmpadding(anslst[-1])
    ans = ''.join(anslst)
    with open(outputf,'wb') as f:
        f.write(ans)

def CBC(cipher_func, inputf, outputf,mode = 'encrypt'):
    assert mode in ('encrypt', 'decrypt')
    anslst = []
    IV = i2bs(0x0123456789abcdeffedcba9876543210,128)
    laste = ''
    for i, e in enumerate(readFile(inputf)):
        if mode == 'encrypt':
            if len(e) < 16:
                e = padding(e)
            data = s2bs(e)
            if i == 0:
                data = xor(data, IV)
            else:
                data = xor(data, s2bs(anslst[-1]))
            out = cipher_func(int(data,2), 0x0123456789abcdeffedcba9876543210).process(mode)
            out = bs2s(out)
            anslst.append(out)
        else:
            data = s2bs(e)
            out = cipher_func(int(data,2), 0x0123456789abcdeffedcba9876543210).process(mode)
            if i == 0:
                out = xor(out, IV)
            else:
                out = xor(out, laste)
            out = bs2s(out)
            anslst.append(out)
        laste = s2bs(e)
    if mode == 'decrypt':
        anslst[-1] =  rmpadding(anslst[-1])
    ans = ''.join(anslst)
    with open(outputf,'wb') as f:
        f.write(ans)

def CTR(cipher_func, inputf, outputf, mode = 'encrypt'):
    assert mode in ('encrypt', 'decrypt')
    anslst = []
    IV = 0x0123456789abcdeffedcba9876543210
    for i, e in enumerate(readFile(inputf)):
        data = s2bs(e)
        temp = (IV+i) % 0xffffffffffffffffffffffffffffffff
        out = cipher_func(temp, 0x0123456789abcdeffedcba9876543210).process()
        out = out[0:len(data)]
        out = xor(data, out)
        anslst.append(bs2s(out))
    ans = ''.join(anslst)
    with open(outputf, 'wb') as f:
        f.write(ans)

if __name__=='__main__':
    ECB(SM4,'message', 'ecb')
    ECB(SM4,'ecb', 'message_ecb', 'decrypt')
    CBC(SM4,'message', 'cbc')
    CBC(SM4,'cbc', 'message_cbc', 'decrypt')
    CTR(SM4,'message', 'ctr')
    CTR(SM4,'ctr', 'message_ctr', 'decrypt')
