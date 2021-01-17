import random 
import math
from sympy import nextprime
 
# UTILS
 
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
 
def baby_steps_giant_steps(a,b,p):
    N = 1 + int(math.sqrt(p))
 
    baby_steps = {}
    baby_step = 1
    for r in range(N+1):
        baby_steps[baby_step] = r
        baby_step = baby_step * a % p
 
    giant_stride = pow(a, (p-2)*N, p)
    giant_step = b
    for q in range(N+1):
        if giant_step in baby_steps:
            return q*N + baby_steps[giant_step]
        else:
            giant_step = giant_step * giant_stride % p
 
    return "No Match"
 
# ZERO KNOWLEDGE PROOF PROTOCOL FOR DISCRETE LOGARITHM 
 
"""
Zero-knowledge proof protocol is a method by which one party (the prover) 
can prove to another party (the verifier) 
that they know a value x, 
without conveying any information apart from the fact that they know the value x.
"""
 
# common knowledge: prime number p, its generating element g and y
p = nextprime(1000)
g = generating_element(p)
y = random.randint(1, 1000)
 
# the prover knows the value of x such that y = g^x (mod p)
x = baby_steps_giant_steps(g, y, p)
 
# check discrete log
if not pow(g, x, p) == y%p:
    raise Exception("discrete log calculated incorrectly.")
 
# 1. the prover P randomly chooses r and computes t = g^r (mod p) 
# and sends it to V
r = random.randint(1, 1000)
t = pow(g, r, p)
 
# 2. V chooses a random c and sends to P
c = random.randint(1, 1000)
 
# 3. P computes s = r + c*x (mod p-1) and sends to V
s = (r + c*x) % (p-1) 
 
# 4. V checks whether g^s = t * y^c (mod p)
verify = pow(g, s, p) == t * pow(y, c, p) % p
print("The knowledge is proven ", verify)