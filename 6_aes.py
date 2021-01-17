import numpy as np
import sympy
import random
 
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz'
 
def string_to_int_blocks(_text, block_size):
    int_blocks = []
    for i in range(0, len(_text), block_size):
        block = _text[i:i+block_size]
 
        # append whitespaces to last block if it is shorter than 4
        if(len(block) < block_size):
            block += " "*(block_size-len(block))
 
        int_blocks.append([ALPHABET.index(m) for m in block])
    return int_blocks
 
def int_blocks_to_string(blocks):
    message = ""
 
    for block in blocks:
        message += "".join([ALPHABET[i] for i in block if i>0])
        
    return message
 
# Keys calc
def calculate_keys(key_matrix, a, b, p, iterations):
    keys = []
    key = key_matrix
    for _ in range(iterations):
        keys.append(key)
        key = next_key(key, a, b, p)
    return keys
 
def next_key(key, a, b, p):
    k1 = key[0] + sb_fun(key[3], a, b, p)
    k2 = key[1] + k1
    k3 = key[2] + k2
    k4 = key[3] + k3
    new_key = [k1, k2, k3, k4]
    return [x % p for x in new_key]
 
def inverse(mat, p):
    return np.linalg.inv(mat) % p
 
def Layer1(mat, a, b, p):
    return first_layer(mat, a, b, p)
 
def Layer1Inverse(mat3, a, b, p):
    return inv_first_layer(mat3, a, b, p)
 
def sb_fun(number, a, b, p):
    if number == 0:
        return b
    return a*sympy.mod_inverse(number, p) + b % p
 
def inv_sb_fun(number, a, b, p):
    r = (number - b) * sympy.mod_inverse(a, p)
    if r == 0:
        return 0
    return sympy.mod_inverse(r, p)
 
def inv_first_layer(matrix, a, b, p):
    return [inv_sb_fun(x, a, b, p) for x in matrix]
 
def first_layer(matrix, a, b, p):
    return [sb_fun(x, a, b, p) for x in matrix]
 
def Layer2(matrix):
    matrix[2], matrix[3] = matrix[3], matrix[2]
    return matrix
 
def Layer2Inverse(mat):
    return Layer2(mat)
 
def inv_matrix(matrix, p):
    m = matrix
    det = round(np.linalg.det(np.reshape(m, (2,2))))
    det_inv = sympy.mod_inverse(det, p)
    return list(map(lambda x : x * det_inv % p, [m[3], -m[1], -m[2], m[0]]))
 
def Layer3(matrix, t_matrix, p):
    t = t_matrix
    m1 = [matrix[0], matrix[2]]
    m2 = [matrix[1], matrix[3]]
    t = np.reshape(t,  (2,2))
    r1 = np.matmul(t, m1) % p
    r2 = np.matmul(t, m2) % p
    r = [r1[0], r2[0], r1[1], r2[1]]
    return r
 
def Layer3Inverse(mat, t, p):
    return Layer3(mat, inv_matrix(t, p), p)
 
def Layer4(mat, k, p):    
    return [(mat[i] + k[i]) % p for i in range(4)]
 
def Layer4Inverse(mat, k, p):    
    return [(mat[i] - k[i]) % p for i in range(4)]
 
def Encript(block, keys):   
    # iterate over generated keys 
    # execute each layers transformation
    for key in keys:        
        l1 = Layer1(block, a, b, p)
        l2 = Layer2(l1)
        l3 = Layer3(l2, T, p)
        l4 = Layer4(l3, key, p)
        block = l4
 
        # test reverse
        # l3_inv = Layer4Inverse(msg, key, p)
        # l2_inv = Layer3Inverse(l3_inv, T, p)
        # l1_inv = Layer2Inverse(l2_inv)
        # m_inv = Layer1Inverse(l1_inv, a, b, p)
        # decrypted = m_inv
    
    return block
 
def Decript(block, keys):
    # iterate over generated keys in reverse
    # apply transformation in reverse
    for key in reversed(keys):
        l3_inv = Layer4Inverse(block, key, p)
        l2_inv = Layer3Inverse(l3_inv, T, p)
        l1_inv = Layer2Inverse(l2_inv)
        m_inv = Layer1Inverse(l1_inv, a, b, p)
        block = m_inv
            
    return block
 
def EncriptAES(message, keys):
    # split message into blocks
    blocks = string_to_int_blocks(message, len(keys[0]))
    # iterate over each message block and encript it
    cypher = []
    for block in blocks:
        cypher.append(Encript(block, keys))
    return cypher
 
def DecriptAES(blocks, keys):
    # iterate over each cypher block and decript it
    message = []
    for block in blocks:
        message.append(Decript(block, keys))
    # reconstruct message
    return int_blocks_to_string(message)
 
 
#WORKS ONLY ON LINUX (WTF)
 
# parameters given in practical task
p = sympy.nextprime(317)
a, b = 13, 15
T = [1, 11, 31, 4]
K = [161, 126, 104, 287]
keys = calculate_keys(K,a,b,p,3)
 
message = "the quick brown fox jumps over the lazy dog"
print(f"Message: {message}")
 
cypher = EncriptAES(message, keys)
print(f"Cypher: {cypher}")
 
message = DecriptAES(cypher, keys)
print(f"Recovered: {message}")