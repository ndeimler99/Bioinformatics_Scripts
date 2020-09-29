#!/usr/bin/env python

import re

fh = "PE_RNAseq_R1.fastq"

countA = 0
countT = 0
countG = 0
countC = 0
lineCount = 0

with open(fh,"r") as fh1:
  print("opened")
  for line in fh1:
    line=line.strip()
    lineCount += 1
    if lineCount % 4 == 2:
      if re.search("A{15}", line):
        countA +=1
      if re.search("T{15}", line):
        countT += 1
      if re.search("C{15}", line):
        countC += 1
      if re.search("G{15}", line):
        countG += 1
    if lineCount % 100000 == 0:
      print(lineCount)
      
print("Poly A sequences: " + str(countA) + "\nPoly T Sequences: " + str(countT) + "\nPoly C Sequences: " + str(countC) + "\n Poly G Sequences: " + str(countG))

