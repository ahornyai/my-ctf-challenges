from sage.all import *
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

# invalid curve attack, we can freely choose parameter b
# b=3 should be good (it has a subgroup with three elements)
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 3

E = EllipticCurve(GF(p), [a, b])
G = E.gens()[0]
q = E.order() // 3 # Lagrange's theorem :fire:

G1 = G*q

r = remote("localhost", 4141)#process(["python3", "../challenge/chall.py"])

r.sendline(str(G1[0]).encode())
r.sendline(str(G1[1]).encode())

r.recvuntil(b"iv = ")
iv = bytes.fromhex(r.recvline().decode())

r.recvuntil(b"ct = ")
ct = bytes.fromhex(r.recvline().decode())

# the size of the subgroup created by G1
for i in range(3):
    P = G1*i
    aes_key = sha256(b"Origin").digest()

    if not P.is_zero():
        aes_key = sha256(f"Point(x={P[0]}, y={P[1]})".encode()).digest()
    
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    
    try:
        print(unpad(cipher.decrypt(ct), 16).decode())
    except:
        pass