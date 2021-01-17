import numpy as np
import random
from math import gcd
 
def coprime(a, b):
    return gcd(a, b) == 1
 
def modInverse(a, m): 
    a = a % m 
    for x in range(1, m): 
        if ((a * x) % m == 1): 
            return x 
    return 1
 
def int2bin(integer, digits):
    if integer >= 0:
        return bin(integer)[2:].zfill(digits)
    else:
        return bin(2**digits + integer)[2:]
 
def toBin(n, digits):
    bits = int2bin(n, digits)
    return np.array(list(bits), dtype=int)
 
def bin2Int(arr):
    return int("".join(str(x) for x in arr), 2)
 
def IsSuperIncreasing(weights):
    L = np.cumsum(weights)
    return all(x<y for x, y in zip(L, weights[1:]))
 
# create super increasing number list
# where each integer is bigger that the sum of integers before it
# weights[i] > sum(weights[:i])
def CreateSuperIncreasingWeightSystem(n):
    weights = np.zeros(n, dtype=np.int)
 
    sum = 0
    for i in range(n):
        weights[i] = sum + random.randint(1, 10)
        sum += weights[i]
 
    # simple check
    if not IsSuperIncreasing(weights):
        return -1
 
    return weights
 
# Solving super-increasing knapsack
# using original weights and the sum of binary message weights
# find original binary message
def solve(W,m): # W system of weights, m - knapsack weight
    M=m; spr=[]
    for i, w in enumerate(reversed(W)):
        if w<=M:
            spr=[len(W)-i-1]+spr
            M=M-w
    return spr
 
def EncriptKnapsack(message, weights, p, s):
    n = len(weights)
    messageBin = toBin(message, n)
 
    sInv = modInverse(s, p)
    # public key is product of private weights and private s
    publickey = [w*sInv for w in weights]
 
    # messageBin is like a mask for weight vector
    # after multiplication we get binary message that is represented with weight instead of 1's and 0's
    cypher = np.sum(messageBin * np.array(publickey))
 
    return cypher, publickey
 
def DecriptKnapsack(cypher, weights, p, s):
    # inverted cypher value is the sum of private weights insted of public weights
    cInv = cypher * s % p
    X = solve(weights, cInv)
        
    revealedBin = np.zeros(len(weights), dtype=int)
    # revealed indexes point to original message ones
    revealedBin[X] = 1
    message = bin2Int(revealedBin)
 
    return message
 
message = 420 # 0001 1010 0100
n = 9 # n bits have to be enough to store the message
weights = CreateSuperIncreasingWeightSystem(n)
 
# p has to be bigger than sum of weights
p = np.sum(weights) + random.randint(1, 100)
 
# choose s that is coprime to p
for s in range(2, p):
    if coprime(p, s):
        break
 
print(f"Message: {message}")
cypher, publickey = EncriptKnapsack(message, weights, p, s)
 
print(f"Public P: {p}")
print(f"Private S: {s}")
print(f"Private Weights: {weights}")
print(f"Public key: {publickey}")
print(f"Cypher: {cypher}")
 
revealedMsg = DecriptKnapsack(cypher, weights, p, s)
print(f"Revealed message: {revealedMsg}")