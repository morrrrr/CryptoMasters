from sympy import nextprime
import random
 
# compute polynomial function using its coeficients x
def LagrangeInterpolatingPolynomial(x, s, t, p):
    S = 0
    for i in range(t):
 
        skaitiklis = 1  #up
        vardiklis = 1 #down
        
        for k in range(t):
            if(k == i):
                continue
 
            skaitiklis *= x[k]
            vardiklis *= (x[k] - x[i])
        
        S += s[i] * (skaitiklis/vardiklis)
    
    result = S % p
    return round(result)
 
# f(x) = a[0]*x^1 + a[1]*x^2 + a[2]*x^3 + ...
def ComputePolynomial(x, A):
    ax = 0
    # compute polynomial function using all coeficients a
    for i, a in enumerate(A):
        ax += a * x**(i+1)
    return ax
 
def ShamirShareSecret(secret, shares, threshold):
    p = nextprime(secret**shares) # p should prime be bigger than the secret
 
    # choose random x and a value that will be used to compute polynomial function        
    # choose non duplicating values
    X = random.sample(range(1, 100), shares)
    A = random.sample(range(1, 100), threshold-1)
    
    S = []    
    for x in X:
        # compute one share with specific x
        # S + polynomial
        sh = secret + ComputePolynomial(x, A)
        S.append(sh % p)
 
    return p, X, A, S
 
# X - dealers private x values that were used to calculate shares
# S - shares
# threshold - minimum number of shares
# prime - public prime number
def ShamirFindSecret(X, S, threshold, prime):
    secret = LagrangeInterpolatingPolynomial(X, S, threshold, prime)
 
    # if there is enough shares
    # we will compute correct secret
    secret2 = LagrangeInterpolatingPolynomial(X[:threshold], S[:threshold], threshold, prime)
 
    # this should fail
    # because there is not enough shares
    secret3 = LagrangeInterpolatingPolynomial(X[:threshold-1], S[:threshold-1], threshold-1, prime)
 
    if(secret == secret2 and secret != secret3):
        print("Secret found")
 
    return secret
 
 
shares = 10
threshold = 6
secret = 1234567
 
print(f"Secret: {secret}")
 
p, X, A, S = ShamirShareSecret(secret, shares, threshold)
print(f"Public prime: {p}")
# print(f"X: {X}")
# print(f"A: {A}")
print(f"Shares: {S}")
 
revealedSecret = ShamirFindSecret(X, S, threshold, p)
print(f"Revealed secret: {revealedSecret}")