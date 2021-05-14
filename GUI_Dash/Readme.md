README.MD

Generate requirements.txt: 
  $ pip3 install pipreqs
  $ pipreqs .

Install requirements.txt:
  $ pip3 install -r requirements.txt

Create Unix Executable:

	#! /bin/bash
	cd /Users/adhirajsen/Desktop/Qorvo/Github_Final/LP_S21_AAHRS/GUI_Dash/
	cp app.py ./app
	chmod 755 app