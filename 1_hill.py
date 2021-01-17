# Hill cipher is a polygraphic substitution cipher based on linear algebra.Each letter is represented by a number modulo 26. Often the simple scheme A = 0, B = 1, …, Z = 25 is used, but this is not an essential feature of the cipher. To encrypt a message, each block of n letters (considered as an n-component vector) is multiplied by an invertible n × n matrix, against modulus 26. To decrypt the message, each block is multiplied by the inverse of the matrix used for encryption.
#
# The matrix used for encryption is the cipher key, and it should be chosen randomly from the set of invertible n × n matrices (modulo 26).
 
# https://www.geeksforgeeks.org/hill-cipher/
 
import numpy as np
 
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_LEN = len(ALPHABET)
BLOCK_LENGTH = 3
 
 
def char_to_int(char, abc=ALPHABET):
    return abc.find(char)
 
 
def int_to_char(_int, abc=ALPHABET):
    return abc[_int] if 0 <= _int < len(abc) else ''
 
 
def sanitize_input(str_input):
    clean_input = ''
    for letter in str_input.upper():
        if letter in ALPHABET:
            clean_input += letter
    return clean_input
 
 
def chop_string_into_blocks(str_input, n=BLOCK_LENGTH):
    res = []
    padded = 0
    for i in range(len(str_input) // n + 1):
        single_block = []
        for j in range(n):
            if i * n + j < len(str_input):
                single_block.append(str_input[i * n + j])
            else:
                single_block.append(ALPHABET[padded])
                padded += 1
        res.append(single_block)
    return res
 
 
def chopped_input_to_array_of_modulus_int_vectors(chopped_input):
    res = []
    for chop in chopped_input:
        vector = np.array([char_to_int(x) for x in chop])
        res.append(vector)
    return res
 
 
def generate_key_matrix(str_key, n=BLOCK_LENGTH):
    clean_str_key = sanitize_input(str_key)
    res = []
    padded = 0
    for i in range(n):
        single_line = []
        for j in range(n):
            if i * n + j < len(clean_str_key):
                single_line.append(char_to_int(clean_str_key[i * n + j]))
            else:
                single_line.append(padded)
                padded += 1
        res.append(np.array(single_line))
    return np.array(res)
 
 
def vectors_to_text(encrypted_vectors):
    ciphertext = ''
    for encr_vector in encrypted_vectors:
        for encr_symbol in encr_vector:
            ciphertext += int_to_char(encr_symbol)
    return ciphertext
 
 
def multiply_array_of_vectors_by_matrix_in_modulus(vectors, matrix):
    return [np.dot(x, matrix) % ALPHABET_LEN for x in vectors]
 
 
# ################################################################ modular matrix inverse, taken from stackoverflow
def modMatInv(A, p):  # Finds the inverse of matrix A mod p
    n = len(A)
    A = np.matrix(A)
    adj = np.zeros(shape=(n, n))
    for i in range(0, n):
        for j in range(0, n):
            adj[i][j] = ((-1) ** (i + j) * int(round(np.linalg.det(minor(A, j, i))))) % p
    return ((modInv(int(round(np.linalg.det(A))), p) * adj) % p).astype(int)
 
 
def modInv(a, p):  # Finds the inverse of a mod p, if it exists
    for i in range(1, p):
        if (i * a) % p == 1:
            return i
    raise ValueError(str(a) + " has no inverse mod " + str(p))
 
 
def minor(A, i, j):  # Return matrix A with the ith row and jth column deleted
    A = np.array(A)
    minor = np.zeros(shape=(len(A) - 1, len(A) - 1))
    p = 0
    for s in range(0, len(minor)):
        if p == i:
            p = p + 1
        q = 0
        for t in range(0, len(minor)):
            if q == j:
                q = q + 1
            minor[s][t] = A[p][q]
            q = q + 1
        p = p + 1
    return minor
 
 
# ################################################################
 
def encrypt_hill(_plaintext, _key):
    # generate key matrix to be used from the given string key
    key_matrix = generate_key_matrix(_key)
 
    # remove all unknown characters from the input string, also make it all uppercase, just for the simplicity
    clean_text = sanitize_input(_plaintext)
    # chop the text into blocks of the set length, pad the remaining space with letters from alphabet
    chopped_text = chop_string_into_blocks(clean_text)
    # convert the blocks of text into blocks of integers % n, where n is the length of the alphabet
    array_of_vectors = chopped_input_to_array_of_modulus_int_vectors(chopped_text)
 
    # multiply each vector by the key matrix in modulus n
    encrypted_vectors = multiply_array_of_vectors_by_matrix_in_modulus(array_of_vectors, key_matrix)
 
    # convert the array of int vectors back to a string
    return vectors_to_text(encrypted_vectors)
 
 
def decrypt_hill(_ciphertext, _key):
    key_matrix = generate_key_matrix(_key)
    # calculate the inverse of the key matrix in modulus n for decryption
    inverse_key_matrix = modMatInv(key_matrix, ALPHABET_LEN)
 
    # same steps as for the plaintext (except for the sanitization, since the encryption is done with my application)
    chopped_ciphertext = chop_string_into_blocks(_ciphertext)
    array_of_vectors = chopped_input_to_array_of_modulus_int_vectors(chopped_ciphertext)
 
    # same multiplication, but this time using the inverse key matrix
    plaintext_vectors = multiply_array_of_vectors_by_matrix_in_modulus(array_of_vectors, inverse_key_matrix)
 
    # conversion back to the plaintext
    return vectors_to_text(plaintext_vectors)
 
 
# key = 'GYBNQKURP'
key = 'reallybad'
plaintext = 'the spaces will be lost and all will be in upper case, without punctuation'
 
ciphertext = encrypt_hill(plaintext, key)
decrypted_ciphertext = decrypt_hill(ciphertext, key)
 
print('plaintext:', plaintext)
print('key:', key)
print('ciphertext:', ciphertext)
print('recovered plaintext:', decrypted_ciphertext)