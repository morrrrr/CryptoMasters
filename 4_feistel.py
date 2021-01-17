# Utilities
def string_to_int_blocks(_text):
    int_blocks = []
    for i in range(0, len(_text), 2):
        block = [ord(_text[i])]
        if i + 1 < len(_text):
            block.append(ord(_text[i + 1]))
        else:
            # append letter A to pad the last block if needed
            block.append(ord('A'))
        int_blocks.append(block)
    return int_blocks
 
 
def int_blocks_to_string(_blocks):
    plaintext = ''
    for _block in _blocks:
        for _number in _block:
            plaintext += chr(_number)
    return plaintext
 
 
# Feistel
def single_feistel_iteration(_block, _key, _function, is_last_iteration):
    _right = _block[1]
    _left = _block[0] ^ eval(_function)
    # not switching left with right in the last iteration
    return [_left, _right] if is_last_iteration else [_right, _left]
 
 
# The procedure for encryption and decryption is identical, only inverting keys order for decryption
def single_feistel_block(keys_iterator, keys_count, block, function):
    for idx, key in keys_iterator:
        block = single_feistel_iteration(block, key, function, idx + 1 == keys_count)
    return block
 
 
def decrypt_encrypt_feistel_blocks(_int_blocks, keys_int, function, encrypt=True):
    plaintext_int_blocks = []
    # The only difference between encryption and decryption is the inversion of keys order
    keys_iterator = enumerate(keys_int) if encrypt else enumerate(reversed(keys_int))
    for block in _int_blocks:
        plaintext_int_blocks.append(single_feistel_block(keys_iterator, len(keys_int), block, function))
    return plaintext_int_blocks
 
 
def encrypt_decrypt_feistel(_text, keys_int, _function, encrypt=True):
    # transforming string into integer blocks of two numbers: AAAA -> [[65, 65], [65, 65]]
    int_blocks = string_to_int_blocks(_text)
    # applying Feistel encryption / decryption on a single block
    output_blocks = decrypt_encrypt_feistel_blocks(int_blocks, keys_int, _function, encrypt)
    # transforming the integer blocks back to a string
    output_string = int_blocks_to_string(output_blocks)
 
    return output_string
 
 
# a function to be applied in each block iteration
f = '(_right|_key)^((_key//16)&_right)'
 
# given in practice exercise
keys = [212, 7, 75]
cipher = [[89, 194], [79, 200], [77, 200], [86, 204], [77, 214], [84, 204], [88, 212], [85, 214], [81, 198], [90, 209], [66, 218], [65, 222], [76, 206], [92, 215], [68, 212], [76, 222], [90, 194], [76, 206], [94, 211], [68, 212], [77, 198], [78, 204], [86, 207], [76, 198], [90, 209], [66, 218], [65, 222], [68, 222], [89, 211], [76, 221], [84, 204], [67, 222], [77, 214], [70, 214], [76, 206], [72, 202], [72, 208], [64, 209], [64, 214], [93, 215], [74, 211], [84, 205], [75, 216], [77, 200], [68, 214], [77, 194], [66, 219], [75, 200], [75, 222], [80, 202], [79, 204], [66, 218], [82, 201], [66, 218], [65, 222], [74, 192], [88, 197], [92, 196], [84, 205], [90, 197], [92, 205], [88, 212], [75, 214], [68, 212], [75, 198], [76, 198], [89, 212], [66, 210], [88, 212], [88, 196], [69, 222], [70, 218], [75, 222], [71, 216], [75, 214], [79, 200], [80, 207], [68, 212], [75, 198], [76, 206], [79, 197], [69, 222], [88, 213], [88, 212], [89, 194], [79, 200], [66, 222], [77, 200], [66, 222], [76, 198], [84, 204], [68, 214], [78, 222], [84, 205], [75, 200], [79, 210], [76, 206], [75, 214], [79, 197], [69, 222], [88, 213], [88, 196], [65, 214], [108, 135]]
 
# A nice test for exam
test_plaintext = 'This time I support spaces, uppercase and lowercase. Only punctuation will be lost.'
test_ciphertext = encrypt_decrypt_feistel(test_plaintext, keys, f)
test_decrypted_ciphertext = encrypt_decrypt_feistel(test_ciphertext, keys, f, False)
 
print('plaintext:', test_plaintext)
print('key:', keys)
print('ciphertext:', test_ciphertext)
print('recovered plaintext:', test_decrypted_ciphertext)