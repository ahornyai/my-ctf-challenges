#!/usr/bin/env python3

import os
from ecc import *
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = os.getenv("FLAG", "bsides{fake_flag}").encode()

Ax = int(input("What's your public key? (x coordinate): "))
Ay = int(input("What's your public key? (y coordinate): "))

if Ax % P256.p == 0 or Ay % P256.p == 0:
    print("nice try :)")
    exit()

secret_key = int(os.urandom(32).hex(), 16)

A = Point(Ax, Ay)
B = ecc_mul(G, secret_key, P256)

print("Oops, I forgot to send Bob's public key, now guess the shared key...")

# good luck
shared_key = ecc_mul(A, secret_key, P256)
aes_key = sha256(str(shared_key).encode()).digest()
iv = os.urandom(16)

cipher = AES.new(aes_key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(FLAG, 16))

print("iv =", iv.hex())
print("ct =", ct.hex())