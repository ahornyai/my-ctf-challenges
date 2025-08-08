from pwn import *

r = remote("localhost", 1234)#process(["python3", "../challenge.py"])

a = int(r.recvline().split(b"=")[1].decode())
c = int(r.recvline().split(b"=")[1].decode())
m = int(r.recvline().split(b"=")[1].decode())

"""
s_2 = a*s_1 + c (mod m)

s_1 = a*s_1 + c (mod p)
s_1 - a*s_1 = c (mod m)
s_1*(1-a) = c (mod m)
s_1 = c*(1-a)^-1 (mod m)
"""
s = (c*pow(1-a, -1, m)) % m

r.sendline(str(s).encode())
r.recvuntil(b"=")

known_pt = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit."
known_ct = bytes.fromhex(r.recvline().split(b" ")[1].decode())
r.recvuntil(b"=")

flag_ct = bytes.fromhex(r.recvline().split(b" ")[1].decode())

print(xor(xor(known_ct, known_pt), flag_ct, cut='min').decode())