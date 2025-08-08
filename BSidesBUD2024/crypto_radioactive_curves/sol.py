from fastecdsa.curve import P256
from fastecdsa.point import Point
from Crypto.Util.number import long_to_bytes

G = P256.G

samples = []
precompute = [2**i * G for i in range(255)]

for sample in open("original_samples.txt").readlines():
    x,y = sample.strip().split()
    
    samples.append((int(x), int(y)))

def recover_bit(reference, faulty):
    diff = reference - faulty

    for i in range(255):
        if precompute[i] == diff:
            return (i, "1")
        elif precompute[i] == -diff:
            return (i, "0")
    
    return None

# the most common element
original_flag = max(set(samples), key=samples.count)
flag_point = Point(*original_flag)
flag_bits = [None] * 183

# remove duplicates
samples = set(samples)

# recovery
for sample in samples:
    if sample == original_flag:
        continue

    sample_point = Point(*sample)
    (pos, value) = recover_bit(flag_point, sample_point)

    flag_bits[pos] = value

flag_bits.reverse()

print(long_to_bytes(int("".join(flag_bits), 2)).decode())
