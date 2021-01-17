import random
from sympy import nextprime
 
A = 'abcdefghijklmnopqrstuvwxyz '
 
# UTILS
def gcd(a, b):
    if a == 0:
        return b
    else:
        return gcd(b % a, a)
 
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x1, y1 = egcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return (g, x, y)
 
def exponentiation_by_squaring(base, exponent, modulus) : 
    res = 1  
  
    base = base % modulus  
 
    if base == 0: 
        return 0
 
    while exponent > 0 : 
 
        if exponent & 1 == 1:
            res = (res * base) % modulus 
            exponent = (exponent - 1) // 2      
            base = (base * base) % modulus 
        else:
            exponent = exponent // 2     
            base = (base * base) % modulus 
     
    return res 
 
def text(M):
    n = int(M)
    text = ''
    while n > 0:
        ind = n % 100
        ind = ind-1
        if (ind >= 0) & (ind < len(A)):
            text += A[ind]
            n = (n-ind+1)//100
        else:
            text += '?'
            n = (n-ind+1)//100
    return text[::-1]
 
def no(text):
    t = ''
    for r in text:
        if r in A:
            ind = A.index(r) + 1
            if ind < 10:
                t = t + '0' + str(ind)
            else:
                t = t + str(ind)
    return int(t, 10)
 
def get_coprime(n):
    r = 1000
    while gcd(r, n) is not 1:
        r = random.randint(r, n)
    return r
 
def check_coprime(p, n):
    if not gcd(p, n) == 1:
        raise Exception("numbers are not coprime.")
 
# RSA 
def create_private_key(e, p, q):
    phi = (p-1)*(q-1)
    g, d, y = egcd(e, phi)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return d % phi
 
def decrypt(y, n, d):
    x = exponentiation_by_squaring(y, d, n)
    return x
 
def encrypt(m, n, e):
    c = exponentiation_by_squaring(m, e, n)
    return c
 
def blind(m, r, e, n):
    m2 = (m * exponentiation_by_squaring(r, e, n)) % n
    return m2    
 
def blind_sign(blind, d, n):
    b = exponentiation_by_squaring(blind, d, n)
    return b  
 
def retrieve_signature(s_blind, r, n):
    g, r_inv, y = egcd(r, n)
    r_inv = r_inv%n
    s = (s_blind * r_inv) % n 
    return s
 
# EXAMPLE AND DESCRIPTION
"""
Blind signature is used when the contents of the message 
should be kept secret from the signing authority. Used in election systems,
digital cash schemes, etc.
"""
message = "as balsuoju uz brazauska"
message_no = no(message)
 
# CONSTRUCT RSA
"""choose two prime numbers"""
p = nextprime(message_no)
q = nextprime(p)
n = p * q
phi_n = (p-1) * (q-1)
"""
choose the public key e that satisfies two conditions:
    1. e < phi_n
    2. gcd(e, phi_n) = 1
"""
e = get_coprime(phi_n)
"""
private key d is the inverse of e mod phi_n. can be computed using the extended euclidean algorithm.
"""
d = create_private_key(e, p, q)
 
# BLIND SIGNATURE 
 
"""
Message author chooses a random blinding factor which is coprime with n (it means that an inverse of r exists in modulus n).
"""
r = get_coprime(n)
 
"""
Message author blinds the message using the blinding factor:
    m' = m * r^e (mod n)
"""
blinded = blind(message_no, r, e, n)
 
"""
The blinded message is sent to the signing authority which calculates the blinded signature as follows:
    s' = (m')^d (mod n) 
"""
s_blind = blind_sign(blinded, d, n)
 
"""
The sent message is sent back to the message author who can remove the blinding factor and retrieve the message:
    s = s' * r^-1 (mod n)
"""
signature = retrieve_signature(s_blind, r, n)
print("Message signature is ", signature)
 
"""
Blind signature is verified the same way as the regular rsa signature: 
    decrypted with the public key and verified against the message.
"""
verify = text(decrypt(signature, n, e))
valid = True if verify == message else False
print("The signature is valid: ", valid)