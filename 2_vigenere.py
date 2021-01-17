ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz'
 
 
def left_rotate(s, d):
    tmp = s[d : ] + s[0 : d]
    return tmp
 
 
def generate_encryption_table(abc = ALPHABET):
    res = []
    for i in range(len(abc)):
        res.append(left_rotate(abc, i))
    return res
 
 
def sanitize_input(str_input):
    clean_input = ''
    for letter in str_input:
        if letter in ALPHABET:
            clean_input += letter
    return clean_input
 
 
def encrypt_vigenere(_plaintext, _key, abc = ALPHABET):
    # Generate the shifted alphabet table with n x n dimensions, where n is the length of the alphabet
    encryption_table = generate_encryption_table(abc)
    # sanitize input and key to get rid of all the unknown characters
    clean_input = sanitize_input(_plaintext)
    clean_key = sanitize_input(_key)
    _ciphertext = ''
 
    for idx, l in enumerate(clean_input):
        # since the key is possible shorter than the plaintext, simulate a circular array
        key_letter = clean_key[idx % len(clean_key)]
 
        # find the row index by the letter of plaintext
        row_index = abc.find(l)
        # find the column index by the letter of key
        column_index = abc.find(key_letter)
 
        _ciphertext += encryption_table[row_index][column_index]
    return _ciphertext
 
 
def decrypt_vigenere(_ciphertext, _key, abc = ALPHABET):
    encryption_table = generate_encryption_table(abc)
    clean_key = sanitize_input(_key)
    _plaintext = ''
 
    for idx, l in enumerate(_ciphertext):
        key_letter = clean_key[idx % len(clean_key)]
 
        # this time select the row by the key letter
        row_index = abc.find(key_letter)
        # the plaintext letter will be the header label of the column,
        # that matches the ciphertext letter in the selected row
        plaintext_letter_index = encryption_table[row_index].find(l)
 
        _plaintext += abc[plaintext_letter_index]
    return _plaintext
 
 
key = 'absolutely any key'
plaintext = 'This time I support spaces, uppercase and lowercase. Only punctuation will be lost.'
 
ciphertext = encrypt_vigenere(plaintext, key)
decrypted_ciphertext = decrypt_vigenere(ciphertext, key)
 
print('plaintext:', plaintext)
print('key:', key)
print('ciphertext:', ciphertext)
print('recovered plaintext:', decrypted_ciphertext)