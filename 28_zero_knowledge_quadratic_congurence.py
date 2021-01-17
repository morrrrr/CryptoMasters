import random 
# whh is the quadratic congruence?
# the solution x of x^2 ≡ c (mod n) (can have multiple solutions)
 
# ZERO KNOWLEDGE PROOF PROTOCOL FOR QUADRATIC CONGRUENCES
"""
Zero-knowledge proof protocol is a method by which one party (the prover) 
can prove to another party (the verifier) 
that they know a value x, 
without conveying any information apart from the fact that they know the value x.
"""
 
# common (public) knowledge is c and n of the x^2 ≡ c (mod n) congruence
c = 145
n = 516
 
# the prover knows the solution x and tries to prove this knowledge to the verifier 
# without revealing the solution itself
x = 305
 
# 1. the prover P randomly chooses r and sends y = r^2 (mod n) to the verifier V
r = random.randint(1, 100)
y = pow(r, 2, n)
 
# 2. V randomly chooses i from {0, 1} and sends it to P
i = random.randint(0, 1)
 
# 3. P computes z = x^i * r (mod n) and sends to V
z = pow(x, i, n) * r % n
 
# 4. V checks whether z^2 = c^i * y (mod n)
verify = pow(z, 2, n) == pow(c, i, n) * y % n 
print("The knowledge is proven ", verify)