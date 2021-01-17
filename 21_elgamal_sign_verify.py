import random
 
 
def gen_key(q):
    key = random.randint(1, q)
    while gcd(q, key) != 1:
        key = random.randint(1, q)
 
    return key
 
 
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)
 
 
def verify_signature(p, g, y, text, r, s):
    left = pow(g, text, p)
    right = (pow(y, r, p) * pow(r, s, p)) % p
    return left == right
 
 
def elgamal_sign_verify():
    # Signature generation
    # Let's say we have a public key [p, g, y] in normal literature, [p, alpha, beta] in Vilius world
    # [p, g, y] = [p, alpha, beta] = [12016012609141909200527091927191118250205120747, 14, 4694855255638262945852818492660822341263525248]
    # # and private key x = 6008006304570954600263545963595559912787238624
    # x = 6008006304570954600263545963595559912787238624
    #
    # # Select the text, translate it into a number
    [p, g, y] = [2820179, 22, 1198978]
    [x] = [632226]
    text = 1231
 
    # find k, such that 0 < k < p - 1 and gcd(k, p - 1) = 1
    k = gen_key(p - 1)
    print('k', k)
    assert(gcd(k, p - 1) == 1)
    assert(0 < k < p - 1)
    # compute r pow(g, k, p)
    r = pow(g, k, p)
 
    # now the workaround part, due me not being smart, just copy the output in between the lines to sage and run it
    # there, then replace the 87th line with the sage output
    print('---------------')
    print('[text, x, r, k, p]=', [text, x, r, k, p])
    print('s = ((text - x * r) / k) % (p - 1)')
    print("print('[r, s] =', [r, s])")
    print('------------')
 
    # replace this line with sage output
    [r, s] = [2562751, 143827]
 
    assert(s != 0)
    assert(0 < r < p)
    assert(0 < s < p - 1)
 
    signature = [r, s]
    print(signature)
 
    print(verify_signature(p, g, y, text, r, s))
 
elgamal_sign_verify()