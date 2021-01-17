A = 'abcdefghijklmnopqrstuvwxyz '
 
# UTILS
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        """
        find the gcd(a, b) with the simple euclidean algorithm:
            1. find the remainder when b is divided by a. (let's call it r) 
            2. if r = 0, gcd(a, b) = a. stop.
            3. otherwise, repeat step 1 with new values: b = a, a = r.
        """
        g, x1, y1 = egcd(b % a, a)
        """
        write the found gcd(a, b) as a linear combination of a and b (g = ax + by)
        this is done by recursively going back all the steps and updating x and y values.
        """
        x = y1 - (b // a) * x1
        y = x1
        return (g, x, y)
 
def exponentiation_by_squaring(base, exponent, modulus) : 
    # initialize the result to 1
    res = 1  
  
    # update base if it is more than or equal to modulus
    base = base % modulus  
 
    if base == 0: 
        return 0
 
    while exponent > 0 : 
 
        if exponent & 1 == 1:
            """
            if the exponent is odd:
                res = res * base 
                exponent = (exponent - 1) / 2
                base = base * base 
            """
            res = (res * base) % modulus 
            exponent = (exponent - 1) // 2      
            base = (base * base) % modulus 
        else:
            """
            if the exponent is even:
                exponent = exponent / 2
                base = base * base 
            """
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
 
 
# EXAMPLE AND DESCRIPTION
 
# GENERATING KEYS
"""choose two prime numbers"""
p, q = 502196563503983107029964037081, 1244319640274247145702661324591
n = p * q
phi_n = (p-1) * (q-1)
"""
choose the public key e that satisfies two conditions:
    1. e < phi_n
    2. gcd(e, phi_n) = 1
"""
e = 145682739 
"""
private key d is the inverse of e mod phi(n). can be computed using the extended euclidean algorithm.
"""
d = create_private_key(e, p, q)
 
# ENCRYPTION 
message = "tai yra labai slapta zinute"
"""
encryption is done by raising the original message to the power of e modulus n:
if x is the original message then the encrypted message y = x^e mod n
for big numbers can be computed using the fast exponentiation by squaring algorithm.
"""
encrypted = encrypt(no(message), n, e)
print("Encrypted message is ", encrypted)
 
# DECRYPTION
"""
decryption is done by raising the encrypted message to the power of d modulus n:
if y is the encrypted message then the decrypted message x = y^d mod n
for big numbers can be computed using the fast exponentiation by squaring algorithm.
"""
decrypted = text(decrypt(encrypted, n, d))
print("Decrypted message is ", decrypted)
 
 
# RSA SIGNATURE 
"""
message is signed by encrypting it with the private key (instead of the public one).
"""
signed = encrypt(no(message), n, d)
print("Message signature is ", signed)
 
"""
signature is verified by decrypting it with the public key and verifying the retrieved message.
"""
verify = text(decrypt(signed, n, e))
valid = True if verify == message else False
print("The signature is valid: ", valid)