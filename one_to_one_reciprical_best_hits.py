#!/usr/bin/env python

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Returns tsv file with reciprocal 1 to 1 best hits")
    parser.add_argument("-f1", "--file1", help="What is the first blastp file input?")
    parser.add_argument("-f2", "--file2", help="What is the second blastp file input?")
    parser.add_argument("-t1", "--table_1", help = "What is the first blastp species biosmart table")
    parser.add_argument("-t2", "--table_2", help = "What is the second blastp species biosmart table")
    parser.add_argument("-o", "--output", help="What two species are you comparing?")
    return parser.parse_args()

args = get_args()

fh1 = args.file1
fh2 = args.file2
out = args.output
table_1 = args.table_1
table_2 = args.table_2

#filter through file and retain best evalue per protein, may be numerous
#create a dictionary -key protein id, -value list of tuples with information from input file
#go through file line by line checking evalues
#if evalue is less than switch with one in dictionary, else add another tuple to end of list

def create_dict(outputs):
    #going through input file line by line
    query_dict = {}
    with open(outputs, "r") as fh:
        for line in fh:
            line = line.strip()
            #split lines into tuple so they entries are immutable (works)
            line = line.split("\t")
            ID = line[0].split(".")
            line[0] = ID[0]
            prot_ID = line[1].split(".")
            line[1] = prot_ID[0]
            line = tuple(line)
            #print(line)
            #print(len(line))
            #check to see if in dictionary
            if line[0] in query_dict:
                #if it is check and compare evalues
                if line[10] < query_dict[line[0]][0][10]:
                    #if it is less it will be less than every tuple in list so replace
                    query_dict[line[0]] = [line]
                elif line[10] == query_dict[line[0]][0][10]:
                    #if evalue is equal save it by appending
                    query_dict[line[0]].append(line)
                else:
                    #means evalue is greater so do nothing
                    pass
            else:
                #if it is not in dict add it to the dictionary in a list that way numerous entries with
                #the same evalue can be appended to list
                query_dict[line[0]] = [line]
    #check to see if function is working properly (appears to be working)
    '''i = 0
    for item in query_dict:
        print(query_dict[item])
        i+=1
    print(i)'''
    
    return query_dict

def retain_one_to_one(protein_dict):
    #removes 
    for item in list(protein_dict.keys()):
        #item is a list of tuples
        x = len(protein_dict[item])
        if x > 1:
            #if I have more than one tuple
            count = 0
            for y in range(x-1):
                #if the db protein are the same across tuples add to count
                if protein_dict[item][y][1] == protein_dict[item][y+1][1]:
                    count += 1
                
            if count == x - 1:
                #this means that all database proteins are the same
                #keep entry
                pass
            else:
                protein_dict.pop(item)

    '''i=0
    for item in protein_dict:
        print(protein_dict[item])
        i+=1
    print(i)'''

    return protein_dict

def compare_dicts(dict_1, dict_2):
    #iterate through one dictionary checking proteins in other dictionary
    for item in list(dict_1.keys()):
        #item is query protein
        if dict_1[item][0][1] in dict_2:
            #if reference protein of query protein is in dict 2
            dict_2_key = dict_1[item][0][1]
            dict_2_ref = dict_2[dict_2_key][0][0]
            if dict_1[item][0][1] == dict_2_ref:
                #check to see if they match with eachother
                #if they match do nothing
                pass
            else:
                #if they do not match pop
                dict_2.pop(dict_1[item][0][1])
                dict_1.pop(item)
        else:
            #if they are not related remove as well
            dict_1.pop(item)

    for item in list(dict_2.keys()):
        #we already checked matching sequences
        #so if its not in dict_1 remove it
        if dict_2[item][0][1] in dict_1:
            pass
        else:
            dict_2.pop(item)
    return dict_1, dict_2

def get_gene_names(table):
    #create dictionary from biosmart table
    #key wil be protein value will be gene ID and gene name
    gene_dict = {}
    with open(table, "r") as t:
        LN = 0
        gene_ID_column = 0
        protein_ID_column = 0
        gene_name_column = 0
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
                    elif item == "Gene name":
                        gene_name_column = count
                    count+=1

            if line_list[protein_ID_column].startswith("ENS"):
                gene_dict[line_list[protein_ID_column]] = [line_list[gene_ID_column], line_list[gene_name_column]]
            
            #print(line_list[gene_ID_column])
            LN += 1
        #print(len(gene_dict))
    return gene_dict


def file_write(dict_1, table1, dict_2, table2):
    #dict_1 correspondes to file 1
    #dict_2 to file 2
    with open("{}_one_to_one.tsv".format(out), "w") as output:
        for item in dict_1:
            dict_2_key = dict_1[item][0][1]
            output.write(table1[item][0] + "\t" + item + "\t" +  table1[item][1] + "\t" +  table2[dict_2_key][0] + "\t" +  dict_2_key + "\t" +  table2[dict_2_key][1] + "\n")




f1_dict = create_dict(fh1)
f2_dict = create_dict(fh2)
f1_1_to_1 = retain_one_to_one(f1_dict)
f2_1_to_1 = retain_one_to_one(f2_dict)
compared_dict_1, compared_dict_2 = compare_dicts(f1_1_to_1, f2_1_to_1)
f1_gene_IDs = get_gene_names(table_1)
f2_gene_IDs = get_gene_names(table_2)
file_write(compared_dict_1, f1_gene_IDs, compared_dict_2, f2_gene_IDs)



