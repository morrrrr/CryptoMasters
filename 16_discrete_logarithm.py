import math
 
# meet in the middle algorithm
# input
# a - cycle group generating element {g}
# b - cycle group element {g^n}
# p - mod
# output
# n - cycle group element b order
def baby_steps_giant_steps(a,b,p):
    N = 1 + int(math.sqrt(p))
 
    #initialize baby_steps table
    baby_steps = {}
    baby_step = 1
    for r in range(N+1):
        baby_steps[baby_step] = r
        baby_step = baby_step * a % p
 
    #now take the giant steps
    giant_stride = pow(a, (p-2)*N, p)
    giant_step = b
    for q in range(N+1):
        if giant_step in baby_steps:
            return q*N + baby_steps[giant_step]
        else:
            giant_step = giant_step * giant_stride % p
 
    return "No Match"
 
a = 100001
b = 54696545758787
p = 70606432933607
 
x = pow(a,b,p)
 
found_b = baby_steps_giant_steps(a, x, p) #takes around 6 seconds
print(found_b)