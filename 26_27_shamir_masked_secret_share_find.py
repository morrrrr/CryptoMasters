from sympy import nextprime, isprime
from math import gcd, sqrt
import random
 
def coprime(a, b):
    return gcd(a, b) == 1
 
### Helper to compute find generating elements (more info in exam task #15)
def non_trivial_divisors(n):
    divs = []
    for i in range(2,int(sqrt(n))+1):
        if n%i == 0:
            divs.append(i)
            divs.append(int(n/i))
 
    return list(set(divs))
 
### Helper to compute find generating elements (more info in exam task #15)
def is_generating_element(g, N):
    result = True
    for div in non_trivial_divisors(N-1):
        if(pow(g,div) % N == 1):
            result = False
            break
    return result
    
### Helper to compute find generating elements (more info in exam task #15)
def get_generating_element(mod):
    for i in range(2, mod):
        if is_generating_element(i, mod):
            return i
    return -1
 
# compute polynomial function using its coeficients x
def InterpolatePolynomial(x, z, t, p, q):
    S = 1
    for j in range(t):
 
        skaitiklis = 1  #up
        vardiklis = 1 #down
        # b = 1
 
        for k in range(t):
            if(k == j):
                continue
            
            # b = (x[k] / (x[k] - x[j])) % q
            skaitiklis *= x[k]
            vardiklis *= (x[k] - x[j])
 
        b = (skaitiklis / vardiklis) % q
        S *= pow(z[j], b)
 
    return S % p
 
# NOTE: this polynomial differs from the one without a mask
# f(x) = a[0] + a[1]*x^1 + a[2]*x^2 + ...
def ComputePolynomial(x, A):
    ax = A[0]    
    for i in range(1, len(A)):
        ax += A[i] * pow(x,i)
    return ax
 
def ShamirShareMaskedSecret(shares, threshold):
    p = nextprime(shares**3) # p should prime be bigger than the secret
 
    # choose q that    
    # q is prime
    # q|p-1
    # q >= n+1
    for q in range(shares+1, p):        
        if(isprime(q) and is_generating_element(q, p)):
            break
 
    # choose random x and a value that will be used to compute polynomial function        
    # choose non duplicating values
    X = random.sample(range(1, q), shares)
    A = random.sample(range(1, q), threshold)
 
    # Dealers pick g
    # g in generating element
    g = get_generating_element(p)
    g = pow(g, q)
 
    # compute each share with specific x
    S = [ComputePolynomial(x, A) for x in X]
 
    # k is the secret
    k = pow(g, A[0], p)
 
    return k, p, q, g, X, A, S
 
def ComputeMaskedShares(S, p, g):
    # Using g, the public X and private S
    # participants compute they masked S 
    # and then can give it to dealer
    # masked = (g**s)%p
    maskedS = [pow(g, s, p) for s in S]
    return maskedS
 
# X - public polynomial x
# threshold - minimum number of shares
# p - public prime number
# q - public prime number
def ShamirFindMaskedSecret(X, maskedShares, threshold, p, q):
    return InterpolatePolynomial(X, maskedShares, threshold, p, q)
 
 
 
shares = 5
threshold = 1 # does not work with bigger t :/
 
k, p, q, g, X, A, S = ShamirShareMaskedSecret(shares, threshold)
print(f"Shared secret: {k}")
print(f"Public prime: {p}")
print(f"Public second prime: {q}")
print(f"Generating element: {g}")
print(f"Public X: {X}")
print(f"Private Shares: {S}")
 
maskedShares = ComputeMaskedShares(S, p, g)
print(f"Masked shares: {maskedShares}")
 
revealedSecret = ShamirFindMaskedSecret(X, maskedShares, threshold, p, q)
print(f"Revealed secret: {revealedSecret}")