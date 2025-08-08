from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

FLAG_REQUEST = b"[SYSTEM] Give me the FLAG!! NOW!!44!"

p = remote("localhost", 4141)#process("./server.py")

def sign_as_user(msg):
    p.sendlineafter(b">", b"0")
    p.sendlineafter(b"Your message in hex:", msg.hex().encode())
    p.recvuntil(b"Signature:")

    return int(p.recvline())

# get the public key
p.recvuntil(b"N =")
N = int(p.recvline())
forged_signature = 1

# 3 is a prime factor of the flag request
for f in [bytes_to_long(FLAG_REQUEST)//3, 3]:
    forged_signature *= sign_as_user(long_to_bytes(f))
    forged_signature %= N

p.sendlineafter(b">", b"1")
p.sendlineafter(b"Your message in hex:", FLAG_REQUEST.hex().encode())
p.sendlineafter(b"Signature:", str(forged_signature).encode())
p.recvuntil(b"Anyway, here is the flag: ")

print(p.recvline().strip().decode())