# loadPullDataAnalysis

Follow the link for [API-Documentation](https://github.com/0xrutvij/loadPullDataAnalysis/blob/main/loadpulldataanalysis.pdf)

To install the API module as a local python pacakge, run `pip3 install .`

Install requirements.txt:
  `cd <Path to repository>/GUI_Dash/ && pip3 install -r requirements.txt`

Create Unix Executable:

        cd <Path to repository>/GUI_Dash/
        cp app.py ./app
        chmod 755 app
        
Launch App on Unix Machines:

       
        cd <Path to repository>/GUI_Dash/
        python3 app.py
        
OR Double click on 'app' created in the earlier step.

Launch App on Windows Machines:
- Ensure Python3 is installed and Python and pip are up to date
- Follow steps to install requirements.txt
- Launch the app by running
        
        cd <Path to repository>\GUI_Dash\ 
        .\app.py 
        
OR executing app.py with python `python .\app.py`

### Reposito-ree
```
.
├── GUI_Dash
│   ├── DataFiles
│   │   ├── Requirements.txt
│   │   ├── UTD_LP_File_1.csv
│   │   ├── UTD_LP_File_1.mdf
│   │   ├── UTD_LP_File_1.pkl
│   │   └── test.mdf
│   ├── Readme.md
│   ├── app.py
│   ├── app_uploaded_files
│   │   ├── UTD_LP_File_1.csv
│   │   ├── UTD_LP_File_1.mdf
│   │   └── UTD_LP_File_1.pkl
│   ├── assets
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   └── undraw_data_processing_yrrv.png
│   └── requirements.txt
├── README.md
├── codePackage
│   ├── README.md
│   ├── build
│   │   └── lib
│   │       └── loadPullDataAnalysis
│   │           ├── __init__.py
│   │           ├── dataXformation.py
│   │           └── mdfParser.py
│   ├── docs
│   ├── requirements.txt
│   ├── setup.py
│   ├── src
│   │   ├── loadPullDataAnalysis
│   │   │   ├── __init__.py
│   │   │   ├── dataXformation.py
│   │   │   └── mdfParser.py
│   └── tests
│       ├── dataXformationTest.py
│       └── parsingTest.py
├── dataXformationNBs
│   ├── 2021-04-15-143121.ipynb
│   ├── df_processing.ipynb
│   └── interpolatedSlicing.ipynb
├── generatedData
│   ├── UTD_LP_File_1.csv
│   ├── UTD_LP_File_1.pkl
│   ├── test.csv
│   └── test.pkl
├── loadpulldataanalysis.pdf
└── rawData
    ├── UTD_LP_File_1.mdf
    └── test.mdf
```
19 directories, 55 files
