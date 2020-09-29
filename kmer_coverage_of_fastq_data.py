#!/usr/bin/env python

import matplotlib.pyplot as plt
import argparse
import math

def get_args():
    parser = argparse.ArgumentParser(description = "Takes Fastq file and returns kmer frequency and number of kmers in that category as well as distribution plotted for specified kmer length")
    parser.add_argument("-k", "--kmer_length", help = "How Long are your kmers?", type = int, default = 9)
    parser.add_argument("-f", "--file", help = "which file are you using?", required = True)
    parser.add_argument("-c", "--coverage", help="what was the coverage of this normalized file?", required = False, default = 0)
    return parser.parse_args()

args = get_args()
#global variables retrieved from argparse
kmer_size = args.kmer_length
file = args.file
coverage = args.coverage

#key of kmer_dict will be string (kmer)
#value of kmer_dict will be number of occurences of key  kmer
kmer_dict = {}
#keys are ints 1,2,3,...
#value of kmer_summary will be the number of kmers that occur their corresponding key occurences
kmer_summary = {}

#function calculates number of k-mers per record given kmer length and sequence length
def recordNumber(kmer_length, record_length):
    return record_length - kmer_length + 1

kmer_number = recordNumber(kmer_size, 101)

def createKmerDict():
    #opens fastq file and reads line by line
    with open(file, "r") as fh:
        lineCount = 0
        for line in fh:
            line.strip()
            lineCount+=1
            #every sequence line is taken and kmerized and added to dictionary
            if lineCount % 4 == 2:
                #i = 0
                for i in range(kmer_number):
                    kmer = line[i:i+kmer_size]
                    #print(kmer)
                    if kmer in kmer_dict:
                        kmer_dict[kmer] += 1
                    else:
                        kmer_dict[kmer] = 1
def createKmerSum():
    #fills second kmer dictionary (counts the number of kmers that occur once, twice, etc.)
    for item in kmer_dict:
        value = kmer_dict[item]
        #print(value)
        if value in kmer_summary:
            kmer_summary[value] += 1
        else:
            kmer_summary[value] = 1
    #print(len(kmer_summary))
    print("kmer frequency","number of kmers in this category", sep="\t")

def printDict():
    #prints dictionary, self explanatory
    for item in sorted(kmer_summary.keys()):
       print(item, kmer_summary[item], sep="\t")


def plot():
    #all below code is for plotting
    x = []
    y = []
    for item in kmer_summary:
        x.append(item)
        y.append(kmer_summary[item])
    #print(x)
    #print(y)
    plt.figure(figsize=(10, 8))
    plt.bar(x, y)
    plt.show()
    plt.yscale("log")
    plt.xlabel("K-mer Frequency")
    plt.ylabel("Number of K-mers in this Category")
    #print(int(coverage))
    if int(coverage) > 0:
        plt.xlim(right=3000, left = 0)
        plt.title("K-mer Spectrum for Length of {} with {}x Coverage".format(kmer_size, coverage))
        plt.savefig("{}mer at {}x coverage.jpg".format(kmer_size, coverage))
    else:
        plt.xlim(right=10000, left = 0)
        plt.title("K-mer Spectrum for Length of " + str(kmer_size))
        plt.savefig("{}mer with no Normalization.jpg".format(kmer_size))


#run code
createKmerDict()
createKmerSum()
printDict()
plot()