#!/usr/bin/env python

#Same files must first be condensed in bash to only contain the bit score (all other information is not required to determine solely if the prep was stranded or not)
#this can be done using the following command
#grep -v "^@" <samfilename> | cut -f 2 > <desiredoutputfilename>
def bit_calc(bits):

        read_one_reverse = 0
        read_one_not_reverse = 0
        read_two_reverse = 0
        read_two_not_reverse = 0
        
        print("Results for ", bits)
        with open(bits, "r") as fh:
                for line in fh:
                        line = line.strip()
                        if(int(line) & 64 == 64):
                        #if its the first read
                                if(int(line) & 16 == 16):
                                #if read is reverse
                                        read_one_reverse += 1
                                else:
                                        read_one_not_reverse += 1
                        else:
                        #its the second read
                                if(int(line) & 16 == 16):
                                        read_two_reverse += 1
                                else:
                                        read_two_not_reverse += 1
                                        
        print("Read One and Reverse Strand: ", str(read_one_reverse), "\nRead One and Not Reversed: ", str(read_one_not_reverse), "\nRead Two and Reverse Strand: ", str(read_two_reverse), "\nRead Two and Not Reversed: ", str(read_two_not_reverse))
d

bit_calc("27_4C_bit.txt")
bit_calc("32_4G_bit.txt")

#if the data is strand specific you would expect only one of bit 16 or 32 to be activated almost the entire time in read one and the other bit in read 2.  
