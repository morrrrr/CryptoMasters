import math
from sympy import nextprime
 
# UTILS
def exponentiation_by_squaring(base, exponent) : 
    res = 1  
    while exponent > 0 : 
        if exponent & 1 == 1:
            res = (res * base) 
            exponent = (exponent - 1) // 2      
            base = (base * base) 
        else:
            exponent = exponent // 2     
            base = (base * base) 
     
    return res 
 
def non_trivial_divisors(n):
    divs = []
    
    for i in range(2,int(math.sqrt(n))+1):
        if n%i == 0:
            divs.append(i)
            divs.append(int(n/i))
 
    return list(set(divs))
 
def is_generating_element(g, N):
    result = True
    for div in non_trivial_divisors(N-1):
        if(pow(g,div) % N == 1):
            result = False
            break
 
    return result
 
def generating_element(mod):
    for i in range(2, mod):
        if is_generating_element(i, mod):
            return i
 
# EXAMPLE AND DESCRIPTION
"""
Diffie-Hellman key exchange is a method of securely exchanging cryptographic
keys over a public channel. The simplest and the original implementation of the protocol uses the 
multiplicative group of integers modulo p, where p is prime, and g is a primitive root modulo p.
"""
 
"""alice and bob choose a public prime number and its primitive root"""
p = nextprime(1000)
g = generating_element(p)
 
"""alice picks a random private u, computes ya = g^u and sends it to bob"""
u = 17
ya = exponentiation_by_squaring(g, u)
 
"""bob picks a random private v, computes yb = g^v and sends it to alice"""
v = 28
yb = exponentiation_by_squaring(g, v)
 
"""both compute the common secret key"""
ka = exponentiation_by_squaring(yb, u)
kb = exponentiation_by_squaring(ya, v)
 
print("Alice and Bob secret keys match ", ka == kb)
print("The secret common key is ", ka)