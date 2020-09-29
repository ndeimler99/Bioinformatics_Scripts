#!/usr/bin/env python

import argparse

def get_args():
    parser = argparse.ArgumentParser(description = "Normalization of Kmer Coverage")
    parser.add_argument("-c", "--coverage", help = "What is your coverage limit", type = int, default = 10)
    parser.add_argument("-f", "--file", help = "which file are you using?")
    parser.add_argument("-o", "--output", help="what file do you want to output to")
    parser.add_argument("-k", "--kmer_length", help = "what do you want your kmer length to be", default = 15)
    return parser.parse_args()

args = get_args()
#assigns inputted file name and coverage to global variables
kmer_coverage_limit = args.coverage
kmer_length = int(args.kmer_length)
f = args.file
output_file = args.output

#the keys in below dict will be kmers themselves
#the values will be the number of times each kmer occurs
kmer_dict = {}

def kmerization():
    with open(f, "r") as fh:
        with open (output_file, "w") as out:
            #record is a temporary variable that stores the current record being analyzed
            record = ["","","",""]
            lineCount = 0
            for line in fh:
                line = line.strip()
                #if the line is not the quality score add to record
                if lineCount % 4 != 3:
                    record[lineCount % 4] = line
                #if line is quality score, record is complete and then gets analyzed.
                else:
                    record[lineCount % 4] = line
                    #print(record)
                    #kmerize sequence line and adds to dictionary
                    sequence = record[1]
                    for i in range(len(sequence) - int(kmer_length) + 1):
                        kmer = sequence[i:i +kmer_length]
                        if kmer in kmer_dict:
                            kmer_dict[kmer] += 1
                        else:
                            kmer_dict[kmer] = 1
                       # print(kmer)
                    #rekmerizes again and retrieves each value from dictionary and creates list of values per kmer
                    values = []
                    for i in range(len(sequence) - kmer_length + 1):
                        kmer = sequence[i:i+kmer_length]
                        values.append(kmer_dict[kmer])
                        #print(values)
                        #print (kmer)
                    #sorts list then finds median of list
                    values.sort()
                    temp_length = len(values)
                    #print(temp_length)
                    if temp_length % 2 == 0:
                        median1 = values[temp_length//2]
                        median2 = values[temp_length//2 - 1]
                        median = (median1 + median2)/2
                    else:
                        median = values[temp_length//2]

                    #determines if record should be kept or discarded
                    if median <= kmer_coverage_limit:
                        #keep record
                        for item in record:
                            out.write(str(item) + "\n")
                    #else do nothing

                lineCount += 1

kmerization()

