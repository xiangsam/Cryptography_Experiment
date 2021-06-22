'''
used to test the output data type
'''
from pwn import *
from Crypto.Util.number import getRandomNBitInteger,long_to_bytes
p = remote('0.0.0.0', 12345)
context.log_level = 'debug'
p.recvuntil('> ')
p.sendline('1')
pt = getRandomNBitInteger(128)
pt = hex(pt)[2:].zfill(32)
print('pt is ', pt)
p.recvuntil('your plaintext in hex')
p.sendline(pt)
p.recvuntil('your ciphertext in hex:')
ct = p.recvuntil('\n')[:-1]
print(ct)
print(ct.__class__)
print(int(ct, 16))
print(long_to_bytes(int(ct,16))[:16])
print(len(long_to_bytes(int(ct,16))))#有16个填充字节
p.interactive()

