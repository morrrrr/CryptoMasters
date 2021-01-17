import random
from sympy import nextprime
 
# -------------------------- utils
 
import math
 
 
# trivial divisors of n
# is 1, -1, n, -n
# because every number will divide be 1 and by itself
# non trivial divisors are all other ones
def non_trivial_divisors(n):
    divs = []
 
    for i in range(2, int(math.sqrt(n)) + 1):
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
def generating_elements(mod, min = 1):
    elements = []
 
    for i in range(min, mod):
        if is_generating_element(i, mod):
            print('found one!')
            elements.append(i)
            return elements
 
    return elements
#------------------
 
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)
 
    # Generating large random numbers
 
 
def gen_key(q):
    key = random.randint(2, q)
    while gcd(q, key) != 1:
        key = random.randint(2, q)
 
    return key
 
 
# Asymmetric encryption
# uses [q, h, g] - the public key
def encrypt(msg, q, h, g):
    # randomly select an integer k, must be done every time and kept private for the sender
    k = gen_key(q)  # Private key for sender
    # calculate s = pow(h, k, q)
    s = pow(h, k, q)
    # calculate c1 = pow(g, k, q)
    c1 = pow(g, k, q)
 
    # compute c2 = s * msg
    c2 = s * msg
 
    # the ciphertext is c1, c2
    return c1, c2
 
 
def decrypt(c2, c1, key, q):
    h = pow(c1, key, q)
    dr_msg = c2 // h
 
    return dr_msg
 
 
def elgamal_demo():
    # Vilius šitą vadina p, arba jį duos arba pasirenki random didelį
    # a large prime
    p = nextprime(random.randint(3000, 3000000))
    # a generating element of the group if integers modulo p
    [g] = generating_elements(p, 20)
    print('g:', g)
 
    # find private key, any random integer less than p - 1
    key = random.randint(1, p - 1)
 
    # compute y = pow(g, a, q)
    y = pow(g, key, p)
 
    # so the public key = [q, g, h] = [p, g, y]; private key = [key] = [x]
    public_key = [p, g, y]
    private_key = [key]
    print('public_key = [p, g, y] = ', public_key)
    print('private_key = [key] = ', private_key)
 
    # tekstas: paskaita ivyks = 1601191101092001270922251119
    # using already converted message to a number for the sake of simplicity
    tekstas = 1601191101092001270922251119
    print("Original Message :", tekstas)
 
    # ciphertext = [c1, c2], that can be decrypted using the private key
    c1, c2 = encrypt(tekstas, p, y, g)
 
    decrypted_msg = decrypt(c2, c1, key, p)
    print("Decrypted Message :", decrypted_msg)
    print('Success: ', decrypted_msg == tekstas)
 
elgamal_demo()