from random import randint
# https://www.highgo.ca/2019/08/08/the-difference-in-five-modes-in-the-aes-encryption-algorithm/
 
BLOCK_SIZE = 4
 
 
# Trivial encryption and decryption functions, because the focus here is on the different modes
def encrypt_single_block(a, _key):
    return [(a[i] ^ _key[i]) * 3 for i in range(len(a))]
 
 
def decrypt_single_block(a, _key):
    return [(a[i] // 3) ^ _key[i] for i in range(len(a))]
 
 
def string_to_int_blocks(_text, _block_size=BLOCK_SIZE):
    int_blocks = []
    for i in range(0, len(_text), _block_size):
        block = []
        for j in range(_block_size):
            if i + j < len(_text):
                block.append(ord(_text[i + j]))
            else:
                block.append(ord('_'))
        int_blocks.append(block)
    return int_blocks
 
 
def int_blocks_to_string(_blocks):
    plaintext = ''
    for _block in _blocks:
        for _number in _block:
            plaintext += chr(_number)
    return plaintext
 
 
def ecb_mode(input_blocks, key, encrypt=True):
    # In ECB mode encryption and decryption is done in the same way,
    # blocks are not related one to each other in any way
    fn_to_use = encrypt_single_block if encrypt else decrypt_single_block
 
    return [fn_to_use(block, key) for block in input_blocks]
 
 
def ecb_demo(text_int_blocks, key):
    encrypted_blocks = ecb_mode(text_int_blocks, key)
    recovered_blocks = ecb_mode(encrypted_blocks, key, False)
    recovered_plaintext = int_blocks_to_string(recovered_blocks)
 
    print('-------------------------')
    print('ECB encrypted blocks:', encrypted_blocks)
    print('ECB recovered:', recovered_plaintext)
    print('-------------------------')
 
 
def xor_two_arrays(a, b):
    return [a[i] ^ b[i] for i in range(len(a))]
 
 
def cbc_mode(input_blocks, key, initialization_vector, encrypt=True):
    xor_param = initialization_vector
    result = []
 
    for block in input_blocks:
        if encrypt:
            # In CBC mode first plaintext block is XORed with the initialization vector IV, then the result is
            # encrypted. Every next block plaintext is XORed with the encrypted output of the previous block instead
            # of the IV.
            xored = xor_two_arrays(block, xor_param)
            encrypted = encrypt_single_block(xored, key)
            result.append(encrypted)
            xor_param = encrypted
        else:
            # As for decryption, the ciphertext block is firstly run through decryption fn, then XORed - first block is
            # XORed with the same IV, the next ones are XORed with the ciphertext (before their decryption) of the
            # previous block
            decrypted = decrypt_single_block(block, key)
            xored = xor_two_arrays(decrypted, xor_param)
            result.append(xored)
            xor_param = block
    return result
 
 
def cbc_demo(text_int_blocks, key):
    iv = string_to_int_blocks('4 symbols will be used')[0]
 
    encrypted_blocks = cbc_mode(text_int_blocks, key, iv)
    recovered_blocks = cbc_mode(encrypted_blocks, key, iv, False)
    recovered_plaintext = int_blocks_to_string(recovered_blocks)
 
    print('-------------------------')
    print('CBC encrypted blocks:', encrypted_blocks)
    print('CBC recovered:', recovered_plaintext)
    print('-------------------------')
 
 
def cfb_mode(input_blocks, key, initialization_vector, encrypt=True):
    encryption_param = initialization_vector
    result = []
 
    for block in input_blocks:
        if encrypt:
            # In CFB mode the initialization vector IV is encrypted with the key, not the plaintext. Then this result
            # is XORed with a block of plaintext, which is the result of single block encryption. For further blocks
            # encryption the result of the previous block encryption is used instead of the IV.
            encrypted = encrypt_single_block(key, encryption_param)
            xored = xor_two_arrays(encrypted, block)
            result.append(xored)
            encryption_param = xored
        else:
            # In CFB mode decryption one important aspect - the same encryption function is used to encrypt and
            # decrypt. IV is encrypted with the key (same as in encryption first step), then this result is XORed with
            # the first block of ciphertext and it results in a block of plaintext. When decrypting the next block,
            # ciphertext of the previous block is used instead of IV.
            encrypted = encrypt_single_block(key, encryption_param)
            xored = xor_two_arrays(encrypted, block)
            result.append(xored)
            encryption_param = block
    return result
 
 
def cfb_demo(text_int_blocks, key):
    iv = string_to_int_blocks('4 symbols will be used')[0]
 
    encrypted_blocks = cfb_mode(text_int_blocks, key, iv)
    recovered_blocks = cfb_mode(encrypted_blocks, key, iv, False)
    recovered_plaintext = int_blocks_to_string(recovered_blocks)
 
    print('-------------------------')
    print('CFB encrypted blocks:', encrypted_blocks)
    print('CFB recovered:', recovered_plaintext)
    print('-------------------------')
 
 
def ofb_mode(input_blocks, key, initialization_vector):
    encryption_param = initialization_vector
    result = []
    # In OFB mode encryption and decryption algorithms are absolutely identical, the only difference is either
    # plaintext block or ciphertext block is used. It's very similar to CFB, but in this case for the next block
    # encryption the result of previous block encryption is used. So step by step:
    # Encrypt IV with key, XOR the result of encryption with the plaintext/ciphertext block. For every next block use
    # the result of 'encrypt IV with key' operation instead of the IV.
 
    for block in input_blocks:
        encrypted = encrypt_single_block(key, encryption_param)
        xored = xor_two_arrays(encrypted, block)
        result.append(xored)
        encryption_param = encrypted
 
    return result
 
 
def ofb_demo(text_int_blocks, key):
    iv = string_to_int_blocks('4 symbols will be used')[0]
 
    encrypted_blocks = ofb_mode(text_int_blocks, key, iv)
    recovered_blocks = ofb_mode(encrypted_blocks, key, iv)
    recovered_plaintext = int_blocks_to_string(recovered_blocks)
 
    print('-------------------------')
    print('OFB encrypted blocks:', encrypted_blocks)
    print('OFB recovered:', recovered_plaintext)
    print('-------------------------')
 
 
def ctr_mode(input_blocks, key, counter):
    encryption_param_counter = counter
    result = []
    # In CTR mode encryption and decryption algorithms are absolutely identical, the only difference is either
    # plaintext block or ciphertext block is used. It's very similar to OFB, but in this case for the next block
    # encryption an incremented counter is used. So step by step:
    # 1. Create a counter of the same length as the key
    # 2. Encrypt counter with the key, XOR the result of the encryption with a plaintext/ciphertext block.
    # 3. Increment the counter
 
    for block in input_blocks:
        encrypted = encrypt_single_block(key, encryption_param_counter)
        xored = xor_two_arrays(encrypted, block)
        result.append(xored)
        encryption_param_counter = [x + 1 for x in encryption_param_counter]
    return result
 
 
def ctr_demo(text_int_blocks, key):
    counter = [randint(1, 3000) for _ in range(BLOCK_SIZE)]
 
    encrypted_blocks = ctr_mode(text_int_blocks, key, counter)
    recovered_blocks = ctr_mode(encrypted_blocks, key, counter)
    recovered_plaintext = int_blocks_to_string(recovered_blocks)
 
    print('-------------------------')
    print('CTR encrypted blocks:', encrypted_blocks)
    print('CTR recovered:', recovered_plaintext)
    print('-------------------------')
 
 
def blocks_demo():
    text = 'This time I am not tied to any alphabet, any symbol goes.'
    text_int_blocks = string_to_int_blocks(text)
    key = string_to_int_blocks('anything, first 4 symbols will be used')[0]
    print('Plaintext:', text)
    print('Key:', key)
 
    ecb_demo(text_int_blocks, key)
    cbc_demo(text_int_blocks, key)
    cfb_demo(text_int_blocks, key)
    ofb_demo(text_int_blocks, key)
    ctr_demo(text_int_blocks, key)
 
 
blocks_demo()