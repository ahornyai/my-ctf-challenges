from collections import namedtuple

Point = namedtuple("Point", "x y")
Curve = namedtuple("Curve", "p a b G")

O = "Origin"

p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
G = Point(0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296, 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5)
P256 = Curve(p, a, b, G)

def point_inv(P, C):
    if P == O:
        return P

    return Point(P.x, -P.y % C.p)

def point_add(P, Q, C):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inv(P, C):
        return O
    else:
        if P == Q:
            lam = (3 * P.x**2 + C.a) * pow(2 * P.y, -1, C.p)
            lam %= C.p
        else:
            lam = (Q.y - P.y) * pow((Q.x - P.x), -1, C.p)
            lam %= p
    
    Rx = (lam**2 - P.x - Q.x) % C.p
    Ry = (lam * (P.x - Rx) - P.y) % C.p
    
    return Point(Rx, Ry)

def ecc_mul(P, n, C):
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_add(R, Q, C)
        Q = point_add(Q, Q, C)
        n = n // 2
    return R
