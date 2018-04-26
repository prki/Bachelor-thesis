"""
@author: Marek Pikna
Evaluates partial guessing entropy from a pge.txt files generated by
AES_CPA.py.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

"""
Returns a zero-value matrix with T (amount of traces used) rows and 16
(subkeys) columns. Size is obtained from the first PGE file.
@param filePath - File is only used to determine the size of the PGE
table.
"""
def initPGETable(filePath):
    fileIn = open(filePath, "r")
    linesNum = 0

    for line in fileIn:
        linesNum = linesNum + 1

    fileIn.close()

    pgetable = [[0 for x in range(16)] for x in range(linesNum)]

    return pgetable


"""
@param fileIn - file with PGE input
@param PGETable_acc - accumulated values in PGE table, has to be averaged later!
"""
def readPGETable(fileIn, PGETable_acc):
    i = 0
    j = 0
    for line in fileIn:
        j = 0
        for word in line.split():
            PGETable_acc[i][j] = float(PGETable_acc[i][j] + int(word))
            j = j + 1 
        i = i + 1 


"""
Averages each element of the table with accumulated PGE values according
to the number of experiments done.
"""
def avgPGEAcc(PGETable_acc, numOfExperiments):
    PGETable = np.array(PGETable_acc)
    PGETable = np.divide(PGETable, numOfExperiments)

    return PGETable


"""
Plots partial guessing entropy of a subkey into a graph.
@param plotAll - if plotAll is false, only the @param subkey gets plotted.
"""
def plotPGE(subkey, PGETable, plotAll = False):
    PGETableTr = np.transpose(PGETable)
    xRange = np.arange(15, len(PGETable)+15, 1)
    plt.axis([15, len(PGETable) + 15, 0, 255])
    if plotAll == False:
        plt.plot(xRange, PGETableTr[subkey])
        plt.title("Partial guessing entropy of the first subkey, Gaussian noise in traces")
    else:
        plt.title("Partial guessing entropy of all subkeys, only MSB used.")
        for i in range(0, 16):
            plt.plot(xRange, PGETableTr[i])

    plt.xlabel("Number of traces used")
    plt.ylabel("Partial guessing entropy")
    plt.savefig("pge-msb.pdf")


def main():
    if len(sys.argv) == 1:
        print("Usage: PGE_eval.py [pgefile1 [pgefile2[...]]]")
        return 1
   
    PGETable_acc = initPGETable(sys.argv[1]) #sys.argv[1] - first filename
    numOfExperiments = 0
 
    for i in range(1, len(sys.argv)):
        try:
            fileIn = open(sys.argv[i], "r")
        except IOError:
            print("Could not open PGE file.")
            return 1
        readPGETable(fileIn, PGETable_acc)
        fileIn.close()
        numOfExperiments = numOfExperiments + 1

    PGETable = avgPGEAcc(PGETable_acc, numOfExperiments)

    plotPGE(11, PGETable, True)
    
    return 0


if __name__ == "__main__":
    main()