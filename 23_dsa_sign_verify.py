# Sorry, this one is in Sage - DSA
# Create keys
p = next_prime(209291249113126)
#p = 209291249113159
g = primitive_root(p)
q = factor(p - 1)[-1][0]
a = next_prime(randint(0, q - 1))
#a_pr = randint(0, q - 1)
alpha = power_mod(g, (p - 1) // q, p)
beta = power_mod(alpha, a, p)
 
K_priv = [a]
K_pub = [p, q, alpha, beta]
print('K_pub = [p, q, alpha, beta] =', K_pub)
print('K_priv = [a] =', K_priv)
#K_pub = [209291249113159, 10870013977, 10929243831572, 82083813141070]
 
# Sign
k = randint(1, q)
text_to_sign = 1093119 
 
gama = power_mod(alpha, k, p) % q
delta = ((text_to_sign + a * gama) / k) % q
Signature = [gama, delta]
 
print('text_to_sign = ', text_to_sign)
print('Signature = [gama, delta] =', Signature)
 
# Verify
e1 = text_to_sign / delta % q
e2 = gama / delta % q
gama_verify = power_mod(alpha, e1, p) * power_mod(beta, e2, p) % p % q
 
print('Signature verified') if gama_verify == gama else print('Signature not verified')