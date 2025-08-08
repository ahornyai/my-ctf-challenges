#!/usr/bin/env python3

from Crypto.Util.number import getPrime, bytes_to_long
import os

FLAG = os.getenv('FLAG', 'BSIDES{fake_flag}')

# I got this from my textbook, so it must be secure
p, q = getPrime(1024), getPrime(1024)
N = p*q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))

def sign(msg, private_key):
    return pow(bytes_to_long(msg), private_key, N)

print(f"""
I will be generous enough to share my public key with you this time.
{N = }

I bet you can't sign the string "[SYSTEM] Give me the FLAG!! NOW!!44!"

[0] Sign a message
[1] Verify signature
[2] Exit
""")

FLAG_REQUEST = b"[SYSTEM] Give me the FLAG!! NOW!!44!"

while True:
    option = int(input("> "))

    if option == 0:
        msg = bytes.fromhex(input("Your message in hex: "))

        if bytes_to_long(msg) % N == bytes_to_long(FLAG_REQUEST):
            print("I refuse to sign this.")
            continue

        print("Signing", msg)
        print("Signature:", sign(msg, d))
    elif option == 1:
        msg = bytes.fromhex(input("Your message in hex: "))
        signature = int(input("Signature: "))

        if sign(msg, d) != signature:
            print("Bruh, it's not even a valid signature. Very disappointing.")
            continue

        if msg == FLAG_REQUEST:
            print("How did you do this???? It is literally impossible.")
            print("Anyway, here is the flag:", FLAG)
            break
        
        print("Nice signature, but not nice enough. Try harder!")
    else:
        break

print("Goodbye!")