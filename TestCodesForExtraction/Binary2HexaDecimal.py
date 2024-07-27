'''
Edited by Sangmork Park, July-2024 
-------------------------------------------------------------------
# This Python code converts binary string into hexa-decimal format.

@input: binary string
@output: value in hexa-decimal format
-------------------------------------------------------------------
'''

def binary2hex(bin_num):
   
    # convert binary to int
    int_num = int(bin_num, 2)
     
    # convert int to hexa-decimal
    hex_num = hex(int_num)

    return hex_num
 
if __name__ == '__main__':
    # binary_num = '11111110111111101111111011111110'
    # binary_num = '11111111111111111111111011111110'
    binary_num = '00010001000100010001000100010001'
    
    for i in range(4):
        print(binary2hex(binary_num[i*8:i*8+8]))