from loadPullDataAnalysis.mdfParser import *


def example_parse():
    # Input: Name of MDF in current dir
    filename = "../../rawData/UTD_LP_File_1.mdf"
    #mdfName = filename + ".mdf"

    # Parse the MDF and read all relevant values
    df_parsed = parseMdf(filename)

    # Additional Calculations like Pin, Pout, Gain, Pdc1, Pdc2, Gamma
    df_preProcessed = calculateMetrics(df_parsed)

    # Convert columns to correct units
    df_preProcessed = unitConversions(df_preProcessed)

    saveName = "../../generatedData/UTD_LP_File_1"
    # Export
    exportFiles(df_preProcessed, saveName)



# Execute Main
if __name__ == "__main__":
    example_parse()
