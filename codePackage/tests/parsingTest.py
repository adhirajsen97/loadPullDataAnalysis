from loadPullDataAnalysis.mdfParser import *


def example_parse(file, save):
    # Input: Name of MDF in current dir
    filename = file
    #mdfName = filename + ".mdf"

    # Parse the MDF and read all relevant values
    df_parsed = parseMdf(filename)

    # Additional Calculations like Pin, Pout, Gain, Pdc1, Pdc2, Gamma
    df_preProcessed = calculateMetrics(df_parsed)

    # Convert columns to correct units
    df_preProcessed = unitConversions(df_preProcessed)

    saveName = save
    # Export
    exportFiles(df_preProcessed, saveName)



# Execute Main
if __name__ == "__main__":
    files = ["../../rawData/UTD_LP_File_1.mdf", "../../rawData/test.mdf"]
    saves = ["../../generatedData/UTD_LP_File_1", "../../generatedData/test"]

    for f, s in zip(files, saves):
        example_parse(f,s)
