# -*- coding:utf-8 -*-
#! /usr/bin/python3

import sys
sys.path.append('../..')
from MyCrypto.Hash.sha1 import SHA1

class HMAC:
    def __init__(self, key, msg, mode):
        if not isinstance(key, bytes):
            raise TypeError("key: expected bytes, but got %r" % type(key).__name__)
        if not isinstance(msg, bytes):
            raise TypeError("msg: expected bytes, but got %r" % type(msg).__name__)
        if not callable(mode):
            raise TypeError('the arg mode is not callable function')
        self._key = key
        self._msg = msg
        self._mode = mode
        self.blocksize = 64 # 512-bit HMAC; can be changed in subclasses.
        self._digest = b''
        self._getdigest()
        
    def _getdigest(self):
        k = self._key
        ipad = b'\x36' * self.blocksize
        opad = b'\x5c' * self.blocksize
        mode = self._mode()
        if len(k) > self.blocksize:
            mode.update(k)
            k = mode.digest()
        k = k + b'\x00'*(self.blocksize - len(k))
        inner = []
        for i, j in zip(k, ipad):
            inner.append((i^j).to_bytes(1, 'big'))
        inner = b''.join(inner)
        inner += self._msg
        mode.update(inner)
        inner = mode.digest()
        outer = []
        for i, j in zip(k, opad):
            outer.append((i ^ j).to_bytes(1, 'big'))
        outer = b''.join(outer) + inner
        mode.update(outer)
        self._digest = mode.digest()

    def digest(self):
        return self._digest
    
    def hexdigest(self):
        return self._digest.hex()


if __name__ == '__main__':
    #  message = b'Hello, world!'
    #  key = b'secret'
    #  hmac = HMAC(key, message, SHA1)
    #  print(hmac.hexdigest())
    message = b'Sample message for keylen<blocklen'
    key = bytes.fromhex('000102030405060708090A0B0C0D0E0F10111213')
    hmac = HMAC(key, message, SHA1)
    print('msg: ', message)
    print('key: ', key)
    print('hexdigest: ', hmac.hexdigest())
