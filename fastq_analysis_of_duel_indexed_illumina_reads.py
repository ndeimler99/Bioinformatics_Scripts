#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import gzip

def get_args():
    #argparse function takes user input 
    parser = argparse.ArgumentParser(description = "analyzes quality scores of all four files and outputs results to graph")
    parser.add_argument("-f1", "--fileOne", help="What is your Read 1 file name?", required = True)
    parser.add_argument("-f2", "--fileTwo", help="What is your Read 2 file name? (Index One)", required = True)
    parser.add_argument("-f3", "--fileThree", help="What is your Read 3 file name? (Index Two)", required = True)
    parser.add_argument("-f4", "--fileFour", help="What is your Read 4 file name? (Read Two)", required = True)
    return parser.parse_args()

#assign user input to global variables
args = get_args()
f1 = args.fileOne
f2 = args.fileTwo
f3 = args.fileThree
f4 = args.fileFour



def fill_arrays():
    ''' Fills each files lists'''
    lineCount = 0
    recordNumber = 0
    print("in method")

    with gzip.open(f1, "rt") as readOneFile, gzip.open(f2, "rt") as indexOneFile, gzip.open(f3, "rt") as indexTwoFile, gzip.open(f4, "rt") as readTwoFile:
        
        print("files open")

        for readOne, indexOne, indexTwo, readTwo in zip(readOneFile, indexOneFile, indexTwoFile, readTwoFile):
            #opened all four input files and reading through all four files simultaneously
            lineCount += 1
            #print(lineCount)
            #strip newline character from end of each line (otherwise lengths will be messed up)
            readOne = readOne.strip()
            readTwo = readTwo.strip()
            indexOne = indexOne.strip()
            indexTwo = indexTwo.strip()
            
            if lineCount == 4:
                print(readOne)
                print(indexOne)
                print("4")
                #the first time lineCount % 4 == 0 create numpy lists
                #lists were experimentally determined to be faster
                #print(readOne, indexOne, indexTwo, readTwo)
                readOneList = [0 for x in range(len(readOne))]
                print("one created")
                readTwoList = [0 for x in range(len(readTwo))]
                indexOneList = [0 for x in range(len(indexOne))]
                print("index created")
                indexTwoList = [0 for x in range(len(indexTwo))]
                print("arrays created")
                print(len(readOneList))
                #print(len(readOneNP), readTwoNP, len(indexOneNP), indexTwoNP)

            if lineCount % 4 == 0:
                #print("in for")
                #print("Record")
                #fill numpy arrays
                for i in range(len(readOne)):
                    readOneList[i] += ord(readOne[i]) - 33
                    readTwoList[i] += ord(readTwo[i]) - 33
                for i in range(len(indexOne)):
                    indexOneList[i] += ord(indexOne[i]) - 33
                    indexTwoList[i] += ord(indexTwo[i]) - 33
                recordNumber += 1
                #print(recordNumber)

            if lineCount % 10000000 == 0:
                print(lineCount)
    print("Method Done")
    #print(readOneNP, readTwoNP, indexOneNP, indexTwoNP)
    return readOneList, readTwoList, indexOneList, indexTwoList, recordNumber

def mean_and_plot():
    ''' takes np arrays and calculates mean/and plots mean '''
    #readOneMean = np.divide(readOne, recordNumber)
    for i in range(len(readOne)):
        readOne[i] = readOne[i] / recordNumber
        readTwo[i] = readTwo[i] / recordNumber
    for i in range(len(indexOne)):
        indexOne[i] = indexOne[i] / recordNumber
        indexTwo[i] = indexTwo[i] / recordNumber

    #print("readOne")
    #readTwoMean = np.divide(readTwo, recordNumber)
    #print("readTwo") 
    #indexOneMean = np.divide(indexOne, recordNumber)
    #print("indexOne")
    #indexTwoMean = np.divide(indexTwo, recordNumber)
    #print("indexTwo")
    #print(readOneMean, readTwoMean, indexOneMean, indexTwoMean)

    x = [x for x in range(len(readOne))]
    y = [y for y in range(len(indexOne))]

    fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize=(12,12))
    
    axs[0, 0].plot(x, readOne)
    axs[0][0].set(xlabel = "Index", ylabel ="Mean Quality Score")
    axs[0][0].set_title("Mean Quality Score for Read One")
    axs[0][1].plot(x, readTwo)
    axs[0][1].set(xlabel = "Index", ylabel = "Mean Quality Score")
    axs[0][1].set_title("Mean Quality Score for Read Two")
    axs[1][0].plot(y, indexOne)
    axs[1][0].set(xlabel = "Index", ylabel = "Mean Quality Score")
    axs[1][0].set_title("Mean Quality Score for Index One")
    axs[1][1].plot(y, indexTwo)
    axs[1][1].set(xlabel = "Index", ylabel = "Mean Quality Score")
    axs[1][1].set_title("Mean Quality Score for Index Two")
    plt.show()
    plt.savefig("mean_quality_scores_for_all_files.png")



readOne, readTwo, indexOne, indexTwo, recordNumber = fill_arrays()
mean_and_plot()
