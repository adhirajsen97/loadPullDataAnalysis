from loadPullDataAnalysis.dataXformation import *
import matplotlib.pyplot as plt


# Retrieve the data frame stored as a pickle file
parsedDf = dfFromPkl('../../generatedData/UTD_LP_File_1.pkl')

# filter data frame to include rows with harmonic values equal to 1 only
parsedDf = filterColVal(parsedDf, 'harmonic', 1, 'eq')

# Reduce the number of columns only to have the relevant ones
parsedDf = dfWithCols(parsedDf, ['gammaTuple', 'power', 'harmonic', 'Pin', 'Pout', 'Gain', 'PAE', 'drainEff',
        'r', 'jx'])

# split the gamma tuple into gamma1 through gammaN where N is the number of gamma sweeps
parsedDf = splitGammaTuple(parsedDf)

# create a list of data frames, where each data frame has the n power indices for
# each unique gamma tuple value
listGamDf = splitOnUniqueGammaTuples(parsedDf)

# calculate the gComp values for each row in each DF.

#print(listGamDf[0])

for i in range(len(listGamDf)):
    df = listGamDf[i]
    listGamDf[i] = calcGComp(df)
    variance = listGamDf[i]['gComp'].var()
    #listGamDf[i], x, f = filterOnCompressionThreshold(listGamDf[i], 3)
    listGamDf[i] = filterOnCompressionThreshold(listGamDf[i], 3)
    if variance <= 10:
        pass
        #plt.plot(x, f, '-')

#plt.show()


#print(listGamDf[0])

# select a variable to slice on
sliceVarName = input('What variable is the slice going to be on? ')

print(pickVariable(sliceVarName, parsedDf))

sliceVarVal = float(input('What value should ' + sliceVarName + ' be sliced at? '))

colList, slicedDf = interpolatedSlice(listGamDf, sliceVarName, sliceVarVal)

print(slicedDf.describe())

print(colList)
