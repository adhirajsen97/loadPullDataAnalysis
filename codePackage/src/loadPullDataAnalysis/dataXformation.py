import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def dfFromPkl(filename: str) -> pd.DataFrame:
    '''

    '''
    df = pd.read_pickle(filename)
    df.set_index(keys=['gammaTuple'], drop=False,inplace=True)
    return df

def filterColVal(
    df: pd.DataFrame,
    colName: str,
    value: float,
    filType: str = None
) -> pd.DataFrame:
    '''

    '''
    if filType == 'geq':
        return df[df[colName] >= value]
    elif filType == 'gt':
        return df[df[colName] > value]
    elif filType == 'lt':
        return df[df[colName] < value]
    elif filType == 'leq':
        return df[df[colName] <= value]
    else:
        return df[df[colName] == value]

def dfWithCols(df: pd.DataFrame, ls: list[str]) -> pd.DataFrame:
    '''
    '''
    return df[ls].copy()


def calcGComp(df: pd.DataFrame) -> pd.DataFrame:
    '''
    '''
    maxGain = df['Gain'].max()
    df['gComp'] = df['Gain'] - maxGain
    return df

def splitGammaTuple(df: pd.DataFrame) -> pd.DataFrame:
    '''
    '''
    numGammas = len(df['gammaTuple'][0])
    splitGammasList = []

    for i in range(numGammas):
        splitGammasList.append([])

    for i, row in df.iterrows():
        gT = row['gammaTuple']
        for j in range(numGammas):
            splitGammasList[j].append(gT[j])

    name = 'gamma'
    for i in range(numGammas):
        colName = name + str(i+1)
        df[colName] = splitGammasList[i]

    return df

def splitOnUniqueGammaTuples(df: pd.DataFrame) -> list[pd.DataFrame]:
    '''
    '''
    uniqGammas=df['gammaTuple'].unique().tolist()

    listGamDf = []

    for gam in uniqGammas:
        gamDf = df.loc[df.gammaTuple==gam]
        gamDf.index = range(len(gamDf))
        listGamDf.append(gamDf)

    return listGamDf

def pickVariable(sliceVar: str, df: pd.DataFrame) -> dict[str, float]:
    '''
    '''
    varInfoDict = {}
    varInfoDict['maxVal'] = df[sliceVar].max()
    varInfoDict['minVal'] = df[sliceVar].min()
    varInfoDict['stepSize'] = max((varInfoDict['maxVal']-varInfoDict['minVal'])/100, 0.1)
    varInfoDict['defaultVal'] = df[sliceVar].median()

    return varInfoDict


def interpolatedSlice(
    dfList: list[pd.DataFrame],
    sliceVar: str,
    sliceVal: float
) -> tuple[list[str], pd.DataFrame]:
    '''
    '''

    listGamDfC = dfList.copy()
    CONST_VAL = sliceVal
    selectedVariable = sliceVar
    dfOfLoadsAtVarX = pd.DataFrame()

    cols = listGamDfC[-1].columns.to_list()
    cols.remove(selectedVariable)
    cols.remove('gammaTuple')

    for i,gamDf in enumerate(listGamDfC):
        calcDict = {}
        selVarList = gamDf[[selectedVariable]].to_numpy().transpose().tolist()[0]
        for col in cols:
            colVals = gamDf[[col]].to_numpy().transpose().tolist()[0]
            calcVal = np.interp(CONST_VAL, selVarList, colVals)
            #calcVal = barycentric_interpolate(selVarList, colVals, FIXED_POUT)
            calcDict[col] = round(float(calcVal),6)
        calcDict[selectedVariable] = CONST_VAL
        calcDict['gammaTuple'] = gamDf['gammaTuple'][0]
        dfOfLoadsAtVarX = dfOfLoadsAtVarX.append(calcDict, ignore_index=True)
        listGamDfC[i] = gamDf.append(calcDict, ignore_index=True).sort_values(by=['power'],ignore_index=True)

    dfOfLoadsAtVarX = dfOfLoadsAtVarX.sort_values(by=['gammaTuple'],ignore_index=True)
    colList = dfList[0].columns
    selList = list(set(colList) - {sliceVar, 'r', 'jx'})

    return selList, dfOfLoadsAtVarX
