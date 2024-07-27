/*
Edited by Sangmork Park, July-2024 
-------------------------------------------------------------------
# This 'C' code converts one byte hexa digits into int value.

@input: one byte hexa digits (00 ~ FF)
@output: integer value
-------------------------------------------------------------------
*/

#include <stdio.h>
#include <stdlib.h>

// convert two hexa digits into integer value on bit operation
int hex2int(char a, char b)
{
    a = (a <= '9') ? a - '0' : (a & 0x7) + 9;
    b = (b <= '9') ? b - '0' : (b & 0x7) + 9;

    return (a << 4) + b;
}

int main()
{
    char *data = "FFFE125588A1BF3A";
    int i_data[8];
    int i_count = 0;
    char hexa_digit1, hexa_digit2;
    for (int i = 0; i < 16; i++)
    {
        if (i % 2 != 0)
        {
            hexa_digit1 = data[i - 1];
            hexa_digit2 = data[i];
            i_data[i_count] = hex2int(hexa_digit1, hexa_digit2);
            printf("%d\n", i_data[i_count]);
            i_count++;
        }
    }
}