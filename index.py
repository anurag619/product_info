from flask import Flask, jsonify, request, render_template, json
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static', template_folder= 'templates')
app.secret_key= '\xbf\xb50\x94au\x8f\xf9\se2\x1f\x93\x06(\xdf\xe4\xaf\x1f\x86k\xb3\x2fQ%1'



@app.route('/' )
def index():
	
	return render_template('index.html')


@app.route('/found', methods=('GET','POST') )
def found():
	if request.method=='POST':
		
		value= request.form['url']
		name = value.encode('utf-8')
		name1 = name.split('/')
		for i in name1:
			if i=='www.flipkart.com':
				details = flipkart(name)
				return render_template('found.html', url = name ,name=details[0], price=details[1], img=details[2])

			elif i=='www.amazon.com':
				detail = amazon(name)
				return render_template('found.html', url=name, name=detail[0], price=detail[1], img=detail[2])



def amazon(url):
	package = []
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	for i in soup.find_all('span', {"id":'productTitle'}):
		model_name = re.sub(' ', '', i.string)
		package.append(model_name)

	for j in soup.find_all('span', {"id":'priceblock_ourprice'}):
		price = re.sub(' ', '', j.string)
		package.append(price)
	for x in soup.find_all('img', {"id":'landingImage'}):
		img = x['src']
		package.append(img)



	return package


def flipkart(url):
	package = []
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	name1 = re.search(r'<h1\sitemprop="name">([\d\w\s]*)</h1>', data, re.IGNORECASE)
	name2 = re.search(r'<div class="line extra_text bmargin10">([()\w\s\d,]*)</div>', data, re.IGNORECASE)
	name = name1.group(1) + name2.group(1)
	model_name = re.sub(' ', '', name)
	package.append(model_name)
	price = re.search(r'<span class="fk-font-verybig pprice fk-bold">([\w\s\d.]*)</span>', data, re.IGNORECASE)
	package.append(price.group(1))
	for x in soup.find_all('img', {"id":'visible-image-small'}):
		image = x['src']
		package.append(image)

	
	return package



	

if __name__ == '__main__':
	app.run(debug=True)

	

