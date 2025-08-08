from sage.all import *

p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC

for b in range(100):
    try:
        E = EllipticCurve(GF(p), [a, b])
        
        if E.order() % 2 == 0:
            print("good curve!", E)
    except:
        pass
