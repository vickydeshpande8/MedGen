__author__ = 'kai'

from flask import Flask, render_template, request
from xl2dict import XlToDict
from collections import defaultdict
import pandas
import xlrd
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/medDetails', methods=['POST'])
def medDetails():
	med = request.form['med']
	#return myDict.keys()
	inDict = myDict[med]
	category = inDict["Category"]
	mrp = inDict["New_MRP (Oct-15)"]
	units = inDict["Strip/Unit"]
	retStr = '''
			<table border=1 cellspacing=3 cellpadding=3 bordercolor=black>
			<tr>
			<td><b>Generic Name of the Medicine</b></td>
			<td>{0}</td>
			</tr>
			<tr>
			<td><b>Category</b></td>
			<td>{1}</td>
			</tr>
			<tr>
			<td><b>Strip/Unit</b></td>
			<td>{2}</td>
			</tr>
			<tr>
			<td><b>New MRP (Oct-15)</b></td>
			<td>{3}</td>
			</tr>
			</table>
			'''.format(med, category, units, mrp)
	return retStr

@app.route('/medSuggest', methods=['POST'])
def medSuggest():
	reqName = request.form['medName']
	regex = '[a-zA-Z]*'.join([i for i in reqName])
	#print(regex)
	r = re.compile(regex, re.IGNORECASE)
	matchMeds = list(filter(r.match, medNames))
	retStr = '''
			<h1>DID YOU MEAN ANY OF THE FOLLOWING : </h1><br>
			'''
	for i in matchMeds:
		retStr = retStr + '''
						<input type="radio" name="med" value="{0}">{0}<br>
						'''.format(i)
	return "<form action='/medDetails' method='post'>" + retStr + "<input type='submit' name='form1' value='submit'></form>"

if __name__ == '__main__':
	myxlobject= XlToDict()
	myData = myxlobject.convert_sheet_to_dict(file_path="static/meds.xlsx", sheet="Sheet1")
	myDict = defaultdict()
	for entry in myData:
		myDict[entry["Generic Name of the Medicines"]] = entry
	#df = pandas.read_excel('static/meds.xlsx')
	#medNames = df['Generic Name of the Medicines'].values
	medNames = myDict.keys()
	app.run()