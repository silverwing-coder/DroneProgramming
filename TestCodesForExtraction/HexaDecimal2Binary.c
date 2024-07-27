
/*
Edited by Sangmork Park, July-2024 
---------------------------------------------------------------------
# This 'C' code converts one hexa digit into four bits binary string.

@input: one hexa digit (0 ~ F)
@output: 4 bits binary string
---------------------------------------------------------------------
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// convert one hexa digit into binary string and return the string
char *hex2binary(char a)
{
    char *binary_string = malloc(5 * sizeof(char));
    char tmp_char = (a <= '9') ? a - '0' : (a & 0x7) + 9;

    for (int i = 3; i >= 0; i--)
    {
        // tmp_char = a << i;
        binary_string[3 - i] = (tmp_char >> i) % 2 + '0';
        printf("%c\n", binary_string[3 - i]);
        // printf("%d\n", (tmp_char >> i) % 2);
    }
    binary_string[4] = '\0';
    // printf("%s\n", bin_string);

    return bin_string;
}

int main()
{
    char a = 'f';
    char *rst = hex2binary(a);

    printf("%s\n", rst);
}