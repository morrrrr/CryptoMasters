import math
 
# trivial divisors of n
# is 1, -1, n, -n
# because every number will divide be 1 and by itself
# non trivial divisors are all other ones
def non_trivial_divisors(n):
    divs = []
    
    for i in range(2,int(math.sqrt(n))+1):
        if n%i == 0:
            divs.append(i)
            divs.append(int(n/i))
 
    return list(set(divs))
 
def is_generating_element(g, N):
    result = True
 
    # tikriname ar su visais netrivialiais dalikliais x
    # islaikoma savybe g^x != 1 mod(N)
    for div in non_trivial_divisors(N-1):
        if(pow(g,div) % N == 1):
            result = False
            break
 
    return result
 
# cikline grupe yra G = {g^0, g^1, g^2 ... g^N-1}
# N - ciklines grupes elementu skaicius
# g - generuojantis elementas
# turint moduli galima rasti ne viena cikline grupe
# paprasciausia yra iteruoti per visus skaicius
# ir tikrinti ar su elementu imanoma cikline grupe
def generating_elements(mod):
    elements = []
 
    for i in range(2, mod):
        if is_generating_element(i, mod):
            elements.append(i)
 
    return elements
 
def GetCycleGroup(gen_element, mod, elements):
    return [pow(gen_element,i,mod) for i in range(elements)]
 
 
# Tests
print(is_generating_element(2,7)) # false
print(is_generating_element(3,7)) # true
print(generating_elements(9)) # 2,3,4,5,6,7
 
# use generating element to get list of numbers
# that have repeating pattern
print(GetCycleGroup(2, 9, elements = 20))
# [1, 2, 4, 8, 7, 5, 
#  1, 2, 4, 8, 7, 5, 
#  1, 2, 4, 8, 7, 5, 
#  1, 2]
 
print(GetCycleGroup(7, 9, elements = 20))
# [1, 7, 4, 1, 7, 4, 1, 7, 4, 1, 7, 4, 1, 7, 4, 1, 7, 4, 1, 7]