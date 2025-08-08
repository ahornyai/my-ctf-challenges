#!/usr/bin/env python3

from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
import os

FLAG = os.getenv("FLAG", "bsides{fake_flag}").encode()

class LCG:

    def __init__(self, s, a, c, m):
        self.s = s
        self.a = a
        self.c = c
        self.m = m
    
    def next(self):
        self.s = (self.a * self.s + self.c) % self.m
        return self.s

a = getPrime(96)
c = getPrime(96)
m = getPrime(96)

print(f"{a = }")
print(f"{c = }")
print(f"{m = }")

s0 = int(input("seed? "))

# lcg -> performance 🚀
nonce_lcg = LCG(s0, a, c, m)
key = os.urandom(16)

def encrypt(pt, key, nonce):
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    
    return cipher.encrypt_and_digest(pt)

ct1, t1 = encrypt(b"Lorem ipsum dolor sit amet, consectetur adipiscing elit.", key, int.to_bytes(nonce_lcg.next(), 12))
ct2, t2 = encrypt(FLAG, key, int.to_bytes(nonce_lcg.next(), 12))

print("ciphertext1, tag1 =", ct1.hex(), t1.hex())
print("ciphertext2, tag2 =", ct2.hex(), t2.hex())
