#!/usr/bin/env python

import argparse
#allow user input of fasta file and comparable biomart table
def get_args():
    parser = argparse.ArgumentParser(description = "PS7 part 1 - Parases through fasta file and keeps longest protein record per gene")
    parser.add_argument("-f", "--file", help = "What is your input fasta file?", required = True)
    parser.add_argument("-t", "--table", help = "what is your gene table file?", required = True)
    return parser.parse_args()

args = get_args()

#assign user inputs to global variables
fh = args.file
table = args.table
output1 = fh + "_condensed"
output2 = fh + "_longest_reads"

#create dictionary from biosmart table
def create_dict():
    gene_dict = {}
    with open(table, "r") as t:
        LN = 0
        gene_ID_column = 0
        protein_ID_column = 0
        for line in t:  
            line = line.strip("\n")
            line_list = line.split("\t")
            #print(len(line_list[0]))

            #determines which columns are which
            if LN == 0:
                count = 0
                for item in line_list:
                    if item == "Gene stable ID":
                        gene_ID_column = count
                    elif item == "Protein stable ID":
                        protein_ID_column = count
                    count+=1

            if line_list[protein_ID_column].startswith("ENS"):
                gene_dict[line_list[gene_ID_column]] = ["",""]
                #print(line_list[gene_ID_column])
            LN += 1
        #print(len(gene_dict))
    return gene_dict

#go through records in fasta file line by line and condenses into two lines (header and sequence)
def condense_file():
    with open(fh, "r") as fasta, open(output1, "w") as condensed:
        seq = ""
        for line in fasta:
            if line.startswith(">"):
                if seq != "":
                    condensed.write(seq + "\n")
                    seq = ""
                seq += line
            else:
                seq += line.strip().replace('\n',"")
        else:
           #last sequence after last line
           if seq != "":
               condensed.write(seq)
               seq = ""

def find_longest():
    #this function will find the longest record and add record to dictionary
    gene_dict = create_dict()
    #print(len(gene_dict))
    with open(output1, "r") as condensed, open(output2, "w") as out:
        LN=0
        temp_record = ["",""]
        for line in condensed:
            LN+=1
            line = line.strip()
            #print(LN)
            if LN % 2 == 1:
                
                #print(line)
                temp_record[0] = line
            else:
                #isolate key used in dictionary (Gene ID)
                temp_record[1] = line
                #print (temp_record)
                temp_key = temp_record[0].split(" ")
                temp_key = temp_key[3].split(".")
                temp_key = temp_key[0][5:]

                if temp_key in gene_dict:
                    #if length temp_record[1] > then that in dictionary. replace
                    if len(temp_record[1]) > len(gene_dict[temp_key][1]):
                        gene_dict[temp_key] = temp_record
                temp_record = ["",""]
            
        #write dictionary of longest protein sequences to file     
        for item in gene_dict:
            out.write(gene_dict[item][0] + "\n" + gene_dict[item][1] + "\n")
        #print(len(gene_dict))

condense_file()
find_longest()


