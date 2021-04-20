# Project Package Root

### Instructions for generating documentation
- First install the updated python package using `pip install . ` @project root (this folder)
- `cd docs`
- Run `make clean`
- Run `sphinx-apidoc -f -o source/ ../src/loadPullDataAnalysis`
- Run `make html`
