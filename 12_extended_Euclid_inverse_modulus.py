"""
Returns (g, x, y) such that g = gcd(a, b) and g = ax + by. 
If gcd(a, b) = 1 then x is an inverse of a mod b. 
"""
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
 
"""
Finds the inverse of a mod n using the extended euclidean algorithm.
"""
def modinv(a, n):
    g, x, y = egcd(a, n)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % n
 
# example
a = 123
b = 3797287661786431
print("{}^-1 mod {} = {}".format(a, b, modinv(a, b)))