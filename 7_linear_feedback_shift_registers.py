def gen_next_key_by_coefs(_current_key, coefs):
    sum_current_state_registers_by_coefficients = 0
    # calculate the sum of registers using the coefficients
    for idx, coeff in enumerate(coefs):
        if coeff == 1:
            sum_current_state_registers_by_coefficients += _current_key[idx]
 
    # the new register value is equal to the sum % 2
    new_value = sum_current_state_registers_by_coefficients % 2
    # shift the existing state and include the newly calculated bit
    return [_current_key[1], _current_key[2], _current_key[3], _current_key[4], _current_key[5], _current_key[6],
            _current_key[7], new_value]
 
 
# Used to shift the bits in the key by n positions -> to generate a completely new 8 bit number you shift by 8
def shift_n_keys(current_key, polynomial, n):
    tmp_key = current_key
    for i in range(n):
        tmp_key = gen_next_key_by_coefs(tmp_key, polynomial)
    return tmp_key
 
 
def binary_array_to_integer(bin_array):
    result = 0
    for idx, num in enumerate(reversed(bin_array)):
        result += num * (2 ** idx)
    return result
 
 
# Given in the practice task
cipherText = [9, 109, 181, 206, 184, 82, 223, 24, 198, 51, 40, 142, 7, 238, 195, 135, 183, 116, 63, 187, 231, 70, 246,
              233, 99, 15, 82, 78, 119, 144, 62, 9, 123, 172, 220, 191, 90, 211, 31, 217, 36, 52, 143, 31, 244, 221,
              148, 191, 125, 57, 176, 229, 78, 229, 228, 97, 19, 79, 80, 104, 156, 32, 22, 99, 178, 217, 162, 67, 207,
              25, 200, 53, 40, 144, 9, 232, 192, 156, 161, 100, 44, 183, 255, 66, 232, 233, 98, 28, 79, 76, 109, 156,
              63, 28, 107, 166, 218, 170, 94, 206, 26, 198, 55, 40, 149, 26, 239, 221, 156, 190, 125, 44, 174, 240, 66,
              237, 228, 100, 18, 79, 81, 105, 128, 38, 11, 114, 166, 220, 191, 66, 195, 1, 215, 32, 46, 140, 26, 252,
              195]
 
 
# validation of results
def encrypt_decrypt_using_lfsr():
    # setting the initial state of the registers
    seed_key = [0, 1, 0, 1, 1, 1, 1, 1]
    # the coefficients of the registers, could be expressed as a polynomial y = x1 + x2 + x4 + x5 + x7
    poly = [1, 1, 0, 1, 1, 0, 1, 0]
    prev_key = seed_key
    resulting_text = ''
 
    # The usage of LFSR generated keystream for encryption/decryption is a simple XOR operation for each of the
    # symbols of the text
 
    # For each symbol in the text, that is represented as an array of integers instead of chars
    for c in cipherText:
        # calculate an integer key value from the 8bit binary array
        key_to_use = binary_array_to_integer(prev_key)
        # xor the single character integer with the key
        xored_number = c ^ key_to_use
        # store the ASCII character of the calculated position as a result
        resulting_text += chr(xored_number)
        # generate the key for the next symbol by shifting the used key by 8 positions
        prev_key = shift_n_keys(prev_key, poly, 8)
    print(resulting_text)
 
encrypt_decrypt_using_lfsr()