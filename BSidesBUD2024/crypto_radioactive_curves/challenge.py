#!/usr/bin/env python3

"""
pip install pycryptodome
pip install fastecdsa
"""

from Crypto.Util.number import bytes_to_long
from fastecdsa.curve import P256
import random
import os

FLAG = bytes_to_long(os.getenv('FLAG', 'BSIDES{fake_flag}').encode())
G = P256.G
output = open("samples.txt", "w")

# Just to make sure the challenge is solvable
assert FLAG.bit_length() < 255

# Radioactivity destroys the results 90% of the time. :(
for i in range(1000):
    if random.randint(0, 9) == 0:
        point = FLAG * G
    else:
        # Radioactivity loves to flip bits
        radioactivity = 1 << random.randint(0, FLAG.bit_length() - 1)
        point = (FLAG ^ radioactivity) * G
    
    output.write(f"{point.x} {point.y}\n")
