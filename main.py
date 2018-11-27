from flask import Flask, render_template, make_response, request, redirect
import mysql.connector
import lxml.etree as ET
from db_credentials import credentials as cred

app = Flask(__name__)

db = mysql.connector.connect(host=cred["host"],
	user=cred["username"],
	passwd=cred["password"],
	db=cred["db"])

cursor = db.cursor()


@app.route("/upload_form")
def upload_form():
	return render_template("form.html")


@app.route("/update", methods=['GET', 'POST'])
def update():
	if request.method == 'GET': # the iframe will open up with GET.
		return "GET request"

	p_id = request.form['id']
	name = request.form['name']
	content = request.form['content']

	query = "UPDATE pastes SET paste_name = %s, paste_content = %s WHERE paste_id = %s"
	cursor.execute(query, (name, content, p_id))
	db.commit()

	return "submitted!"


@app.route("/upload", methods=['POST'])
def upload():
	name = request.form['name']
	content = request.form['content']
	tpe = request.form['type']

	query = "INSERT INTO pastes (paste_name, paste_content, paste_type) VALUES(%s, %s, %s)"
	cursor.execute(query, (name, content, tpe))
	db.commit()

	return redirect("/", code=302)

def xslt(xml, xsl_path):
	xsl = ET.parse(xsl_path)
	transform = ET.XSLT(xsl)
	return transform(xml)

@app.route("/")
def list():
	cursor.execute("SELECT * FROM pastes")
	
	parser = ET.XMLParser(dtd_validation=True)
	dom = ET.fromstring(render_template('list.xml', pastes=[e for e in cursor]), parser)
	
	newdom = xslt(dom, "xsl/list.xsl")

	data = ET.tostring(newdom, pretty_print=True)

	response = make_response(data)
	response.headers['Content-type'] = 'text/html; charset=utf-8'
	
	return response


@app.route("/css/<file>")
def css(file):
	with open("css/"+file) as f:
		return f.read()


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug = True)
