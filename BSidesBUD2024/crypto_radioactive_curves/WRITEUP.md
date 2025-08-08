# Writeup

The given code generates 1000 samples of the result flag * G, where the flag is a scalar. G is the generator point of the [P256](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186-draft.pdf#page=24) elliptic curve.

However, 90% of these samples are faulty. They have one bitflip. Let's take a look at a small example.

$flag_0  * G = 11001010_2 * G$


$flag_1 * G = 11000010_2 * G$

The original flag is $flag_0$ and the bit-flipped flag is $flag_1$. Our job is to determine the flipped bit from the values of $flag_0 * G$ and $flag_1 * G$. We can't take the elliptic curve discrete logarithm in the original challenge, because the flag is probably a large number. However, since the addition of points over an elliptic curve is a group operation, we can freely subtract these points from each other.

$flag_0 * G - flag_1 * G = (flag_0 - flag_1) * G = 1000_2 * G = 2^3 * G$

We can observe that after subtracting a faulty sample from a good sample we always get a power of two multiplied by the generator point. If the original value of the flipped bit was 1, we get a positive number. Otherwise, we get a negative.

Now the only question is how can we determine the value of the original point that doesn't contain any bit flips? Well, it's pretty easy, because 10% of the generated points are like this, so there is a large chance that this will be the most common point.

Let's precompute all points from $2^0 * G$ to $2^{254} * G$ at the start of our solving script to speed up the comparison.

```python
from fastecdsa.curve import P256

G = P256.G
precompute = [2**i * G for i in range(255)]
```

Let's write the recover bit logic:
```python
def recover_bit(reference, radioactive):
    diff = reference - radioactive

    for i in range(255):
        if precompute[i] == diff:
            return (i, "1")
        elif precompute[i] == -diff:
            return (i, "0")
    
    return None
```

After putting this all together we can get the flag back without solving the elliptic curve discrete logarithm problem.

[Full solution script](sol.py)

Flag: `BSIDES{r4d1o4cT1v3_3CC}`