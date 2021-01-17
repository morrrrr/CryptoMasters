from math import sqrt
from random import randint
from sympy import nextprime
 
 
# trivial divisors of n
# is 1, -1, n, -n
# because every number will divide be 1 and by itself
# non trivial divisors are all other ones
def non_trivial_divisors(n):
    divs = []
 
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            divs.append(int(n / i))
 
    return list(set(divs))
 
 
def is_generating_element(g, N):
    result = True
 
    # tikriname ar su visais netrivialiais dalikliais x
    # islaikoma savybe g^x != 1 mod(N)
    for div in non_trivial_divisors(N - 1):
        if (pow(g, div) % N == 1):
            result = False
            break
 
    return result
 
 
# cikline grupe yra G = {g^0, g^1, g^2 ... g^N-1}
# N - ciklines grupes elementu skaicius
# g - generuojantis elementas
# turint moduli galima rasti ne viena cikline grupe
# paprasciausia yra iteruoti per visus skaicius
# ir tikrinti ar su elementu imanoma cikline grupe
def find_generating_element(mod, min = 1):
    for i in range(min, mod):
        if is_generating_element(i, mod):
            return i
    return -1
#------------------
 
 
def schnorr_demo():
    text = 11231231
    print('Text to sing:', text)
 
    # Generate keys
    q = nextprime(999999)
    g = find_generating_element(q, 50)
    print('Public parameters [q, g] =', [q, g])
 
    # x - private key, y - public key
    x = randint(1, q)
    y = pow(g, x, q)
    print('Private key x =', x)
    print('Public key y =', y)
 
    # Sign
    # very important part - random, one time use k, then calculate r
    k = randint(1, q)
    r = pow(g, k, q)
 
    # e = hash(text || r), but for the sake of simplicity no hashing is done
    e = text + r
    s = k - x * e
    # signature = [e, s]
    print('Signature [e, s] =', [e, s])
 
    # Verify
    r_verify = (pow(g, s, q) * pow(y, e, q)) % q
    e_verify = text + r_verify
 
    print('Signature verified') if e == e_verify else print('Signature not verified')
 
 
schnorr_demo()