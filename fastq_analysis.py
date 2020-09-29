#!/usr/bin/env python

import numpy as np
import argparse
from matplotlib import pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description = "PS9")
    parser.add_argument("-f", "--file", help = "What is your input file?", required = True)
    parser.add_argument("-c", "--lineCount", help = "how many lines are in the file", required = True)
    parser.add_argument("-o", "--output", help = "what is the output file name, will overwrite if already existing", default = "output")
    return parser.parse_args()

args = get_args()

records = int(args.lineCount) / 4
infile = args.file
out_file_name = args.output

def fill_array():
    #fills created numpy array then returns 2d array
    lineCount = 1
    recordNumber = 0
    with open(infile, "r") as fh:
        for line in fh:
            line = line.strip()
            if lineCount == 4:
                #index number, record number
                all_qscores = np.zeros((len(line), int(records)),dtype=int)
                #print(len(all_qscores))
                #print(len(all_qscores[0]))
            if lineCount % 4 == 0:
                #takes quality scores and adds to array
                for i in range(len(line)):
                    all_qscores[i][recordNumber] = ord(line[i]) - 33
                recordNumber += 1
            lineCount += 1
    return all_qscores

def create_stat_arrays():
    #runs the statistics and plots quality score distribution at index 6 and 95
    
    mean = np.mean(all_qscores, axis = 1)
    print("mean ran")
    stdev = np.std(all_qscores, axis = 1)
    print("stdev ran")
    var = np.var(all_qscores, axis = 1)
    print("var ran")
    median = np.median(all_qscores, axis = 1)
    print("median ran")

    with open("{}_output.txt".format(out_file_name), "w") as out:
        out.write("# Base Pair\tMean Quality Score\tVariance\tStandard Deviation\tMedian\n")
        for i in range(len(all_qscores)):
            out.write(str(i) + "\t" + str(mean[i]) + "\t" + str(var[i]) + "\t" + str(stdev[i]) + "\t" + str(median[i]) + "\n")

    x = [x for x in range(101)]

    plt.subplots(nrows = 2, ncols = 1)
    plt[0][0].plot(x, mean, label = "Mean")
    plt[0][0].plot(x, median, label = "Median")
    plt[0][0].xlabel("Index")
    plt[0][0].ylabel("Mean / Median Score")
    plt[0][0].title("Mean and Median Across all Indices")
    plt[0][0].legend()

    
    plt[0][1].plot(x, stdev, label = "Standard Deviation")
    plt[0][1].plot(x, var, label = "Variance")
    plt[0][1].xlabel("Index")
    plt[0][1].ylabel("Standard Deviation / Variance")
    plt[0][1].title("Standard Deviation and Variance Across all Indices")
    plt[0][1].legend()
    plt.show()
    plt.savefig("Mean_median_stdev_var.png")





def make_plots():
    with open("p6.tsv", "w+") as p6, open("p95.tsv", "w+") as p95:
        #create and add to dictionaries
        p6dict = {}
        p95dict={}
        for item in all_qscores[6]:
            if item in p6dict:
                p6dict[item] += 1
            else:
                p6dict[item] = 1
        for item in all_qscores[95]:
            if item in p95dict:
                p95dict[item] +=1
            else:
                p95dict[item] = 1
        #create distribution files
        p6.write("Quality Score\tNumber of Appearances\n")
        for item in sorted(p6dict):
            p6.write(str(item) + "\t" + str(p6dict[item]) + "\n")
        
        p95.write("Quality Score\tNumber of Appearances\n")
        for item in sorted(p95dict):
            p95.write(str(item) + "\t" + str(p95dict[item]) + "\n")
    
    with open("p6.tsv", "r") as p6, open("p95.tsv", "r") as p95:
        #create plots
        p6Count = 0
        p6x = []
        p6y = []

        for line in p6:
            if p6Count == 0:
                pass
            else: 
                line = line.strip().split()
                p6x.append(int(line[0]))
                p6y.append(int(line[1]))
            p6Count += 1
        
        plt.plot(p6x, p6y, label = "Index 6")
        plt.xlabel("Quality Score")
        plt.ylabel("Number of Occurences")
        plt.title("Distribution of Quality Scores at Position 6")
        plt.show()
        plt.savefig("p6_distribution.png")

        p95Count = 0
        p95x = []
        p95y = []

        for line in p95:
            if p95Count == 0:
                pass
            else: 
                line = line.strip().split()
                p95x.append(int(line[0]))
                p95y.append(int(line[1]))
            p95Count += 1
        
        plt.plot(p95x, p95y, label = "Index 95")
        plt.xlabel("Quality Score")
        plt.ylabel("Number of Occurences")
        plt.title("Distribution of Quality Scores at Position 6 and 95")
        plt.legend()
        plt.show()
        plt.savefig("p95_distribution.png")

            
all_qscores = fill_array()
create_stat_arrays()
make_plots()
#print(all_scores) 