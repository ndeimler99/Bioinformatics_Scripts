#!/usr/bin/env python

import argparse

def get_args():
    parser = argparse.ArgumentParser(description = "Goes through Sam file and counts number of mapped and unmapped reads")
    parser.add_argument("-f", "--file", help = "what is your sam input file?", required = True)
    return parser.parse_args()

args = get_args()
input_file = args.file

#line.split by tab
#first index will be bit flag
#convert bit flag to binary
#check to see if 4 - yes add to mapped += 1 else unmapped +=1 
#print mapped and unmapped counts

def countMapped():
    with open(input_file, "r") as fh:
        lineCount = 0
        query_dict = {}
        mapped = 0
        unmapped = 0
        secondary = 0
        for line in fh:
            #print(lineCount)
            #check if header line
            if line.startswith("@"):
                lineCount += 1
            else:
                line = line.split("\t")
                if ((int(line[1]) & 4) != 4):
                    #if mapped

                    if ((int(line[1]) & 256) != 256 ):
                        #if primary
                        mapped += 1
                    else:
                        #secondary
                        secondary += 1
                else:
                    #not mapped
                    #check for secondary alignment
                    '''
                    string = bin(int(line[1]))
                    if len(string) > 9:
                        string = string[-9]
                        if string == 1:
                            print(SECONDARY)
                    '''
                    if ((int(line[1]) & 256) != 256 ):
                        #if primary
                        unmapped += 1
                    else:
                        secondary += 1
                

                lineCount += 1
    print("Number of Primary Mapped Reads: " + str(mapped))
    print("Number of Secondary Mapped Reads: " + str(secondary))
    print("Number of Unmapped Reads: " + str(unmapped))
                
                
countMapped()
            