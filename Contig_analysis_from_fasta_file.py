#!/usr/bin/env python

#import argparse, regex, matplotlib
import argparse
import re
import matplotlib.pyplot as plt

#allow user input for input and output files
def get_args():
    parser = argparse.ArgumentParser(description = "PS6 - Prints and plots the distribution of contig lengths")
    parser.add_argument("-f", "--file", help = "what is your input file?", required = True)
    parser.add_argument("-o", "--output", help = "what is the name you wish to appear in results?", default = "output.txt")
    parser.add_argument("-k", "--kmer_length", help = "what is your kmer length? default is 49", default = 49)
    return parser.parse_args()

args = get_args()

#assign inputted values to global variables
fh = args.file
out = args.output
kmer_length = args.kmer_length

def get_ID(myFile):
    #creates a list of all header lines in the FASTA file
    id_list = []
    with open(myFile, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                id_list.append(line.strip())
    #print(id_list)
    #print(len(id_list))
    return id_list

def extract_length_coverage(id_list):
    #creates two lists of length of sequence and kmer coverage
    length = []
    coverage = []
    pattern = '[0-9]+\.\d+|\d+'
    for item in id_list:
        match = re.findall(pattern, item)
        #print(match)
        #it is match1 and match 2 because match 0 = node.
        #length give in header is number of kmers (kcount) must be adjusted to get strlength
        length.append(int(match[1]) + int(kmer_length) - 1)
        coverage.append(match[2])
   # for i in range(len(length)):
    #    print(length[i], coverage[i], sep = "\t")
    return length, coverage

def calculate_N50(length, genome_length):
    length.sort(reverse=True)
    sum = 0
    for item in length:
        sum += item
        if sum > genome_length/2:
            return item


def calculations(length, coverage):
    #calculates the number of contigs, maximum contig length, mean contig length, and total length of assembly
    #calculates mean depth of coverage for contigs
    number_of_contigs = len(length)
    sum_length = 0
    sum_coverage = 0
    max_contig_length = 0

    #below loop finds length of assembly and sum of all coverages to use to determine mean coverage length
    #also finds max contig length
    for i in range(len(length)):
        sum_length += length[i]
        if length[i] > max_contig_length:
            max_contig_length = length[i]

    #calculate mean contig length
    mean_contig_length = sum_length / number_of_contigs

    cov = 0
    #calculate mean depth of coverage
    for i in range(len(coverage)):
        #Ck = C * (mean_lengh - k + 1)/ Lm
        coverage[i] = (coverage[i] * mean_contig_length) / (mean_contig_length - int(kmer_length) + 1)
        cov += length[i] * coverage[i]
    
    mean_coverage = cov / sum_length

    N50 = calculate_N50(length, sum_length)

    with open("master.txt", "a") as wo:
        wo.write(out + "\t" + str(N50) + "\t" + str(number_of_contigs) + "\t" + str(max_contig_length) + "\t" + str(mean_contig_length) + "\t" + str(sum_length) + "\t" + str(mean_coverage) + "\n")
    
    #return N50, number_of_contigs, max_contig_length, mean_contig_length, sum_length, mean_coverage

length, coverage = extract_length_coverage(get_ID(fh))
calculations(length, coverage)
#print(N50, number_of_contigs, max_contig_length, mean_contig_length, genome_length, mean_coverage)

def distribution_dict(length):
    #bins reads into dictionary based on length for plotting
    distribution_dict = {}
    for item in length:
        key = (int(item/100))*100
        if key in distribution_dict:
            distribution_dict[key] += 1
        else:
            distribution_dict[key] = 1
    return distribution_dict

def print_plot(binned_lengths):
    #prints and plots binned lengths as desired
    #print("# Contig Length", "Number of contigs in this category", sep ="\t")
    output = "{}_Distribution_Results.txt".format(out)
    ymax = 0
    with open(output, "w") as w:
        w.write("# of Contig Length" + "\t" + "Number of Contigs in this Category\n")
        for item in sorted(binned_lengths.keys()):
            w.write(str(item) + "\t" + str(binned_lengths[item]) + "\n")
            if binned_lengths[item] > ymax:
                ymax = binned_lengths[item]
    
            #print(item, binned_lengths[item], sep="\t")
    #all below code is for plotting
    x = []
    y = []
    for item in binned_lengths:
        x.append(item)
        y.append(binned_lengths[item])
    #print(x)
    #print(y)
    plt.figure(figsize=(10, 8))
    plt.bar(x, y, width = 100)
    plt.ylim(0, ymax + 50)
    plt.xlim(0, 10000)
    plt.show()
    plt.xlabel("Contig Length")
    plt.ylabel("Number of Contigs")
    plt.title("Distribution of Contig Lengths from {}".format(out))
    plt.savefig("{}_Contig_Distribution.png".format(out))
        
binned_lengths = distribution_dict(length)
print_plot(binned_lengths)
