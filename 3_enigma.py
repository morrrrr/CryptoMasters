import random
 
abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz."
n = len(abc)
 
def encrypt_rotor(lmb, a, m): # encrypt with the rotor
    b=(a+m)%n
    b=lmb[b]
    return (b-m)%n
 
def decrypt_rotor(lmb, a, m): # decrypt with the rotor
    b=(a+m)%n
    b=lmb.index(b)
    return (b-m)%n
 
def shift_rotors(shifts):
    i = 0
    shifts[i] += 1
    while shifts[i] >= n:
        shifts[i] = 0
 
        i += 1
 
        if(len(shifts) < i):
            shifts[i] += 1
        else:
            i = 0
    
    return shifts
 
def EncriptDecriptEnigma(rotors, keys, text, encript = True):
    newText = []
    shifts = list(keys) # dont forget to copy
 
    for m in text:
        # get index to ABC
        d = abc.index(m)
 
        # iterate over rotors
        rotors_keys = list(zip(rotors, shifts))
        # when decripting keys are reversed and different rotor funtion is used
        for rotor, s in rotors_keys if encript else reversed(rotors_keys):
            # encription indexes permutation array
            # decription finds which index was used
            func = encrypt_rotor if encript else decrypt_rotor
            # adjust index to rotor ABC permutation
            d = func(rotor, d, s)
 
        newText.append(abc[d])
 
        # shift first rotor by 1, if it is equal to lenght of ABC
        # set it to 0
        # and shift next rotor by 1
        shifts = shift_rotors(shifts)
    
    return newText
 
NUMBER_OF_ROTORS = 3  # tested with 1 and 111
 
# list of abc permutations
rotors = [ list(range(n)) for _ in range(NUMBER_OF_ROTORS) ]
 
# without shuffle it will be worthless
for r in rotors:
    random.shuffle(r)
 
# list of initial rotor positions
keys = [ random.randint(0, n) for i in range(len(rotors)) ]
 
for i, (r, k) in enumerate(zip(rotors, keys)):
    print(f"Rotor {i} permutation: {r}")
    print(f"Rotor {i} key: {k}")
 
message = "labai salta lauke. labai salta lauke. labai salta lauke. labai salta lauke. labai salta lauke. labai salta lauke. labai salta lauke. labai salta lauke."
cypher = EncriptDecriptEnigma(rotors, keys, message, encript=True)
 
print(f"Plain text: {message}")
print(f"Encripted text: {''.join(cypher)}")
 
decripted = EncriptDecriptEnigma(rotors, keys, cypher, encript=False)
print(f"Decripted text: {''.join(decripted)}")