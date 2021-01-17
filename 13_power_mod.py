"""
Fast exponentiation by squaring algorithm:
    1. Initialize the result to 1
    2. If the exponent is 0, return the result. stop.
    3. If the exponent is even, update values to:
            result = result * base
            exponent = exponent / 2
            base = base * base
        and repeat from the step 2. 
    4. If the exponent is odd, update values to:
            exponent = (exponent - 1) / 2
            base = base * base
        and repeat from the step 2. 
"""
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
 
# example
x = 5
y = 314
p = 3154
print("{}^{} mod {} = {}".format(x, y, p, exponentiation_by_squaring(x, y, p)))