from mdfParser import *


def example_parse():
    # Input: Name of MDF in current dir
    filename = "../rawData/UTD_LP_File_1.mdf"
    #mdfName = filename + ".mdf"

    # Parse the MDF and read all relevant values
    df_parsed = parseMdf(filename)

    # Additional Calculations like Pin, Pout, Gain, Pdc1, Pdc2, Gamma
    df_prePrcoessed = calculateMetrics(df_parsed)

    # Convert columns to correct units
    df_prePrcoessed = unitConversions(df_prePrcoessed)

    saveName = "../generatedData/UTD_LP_File_1"
    # Export
    exportFiles(df_prePrcoessed, saveName)



# Execute Main
if __name__ == "__main__":
    example_parse()
