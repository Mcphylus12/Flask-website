from flask import Flask, render_template, request
from cgi import escape #used to escape html special characters
import time
import csv

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/attractions')
def attractions():
    return render_template('Attractions.html')

@app.route('/comments')
def comments():
    comList = readFile("static/comments.csv")
    return render_template('Comments.html', comList=comList, err=False)

@app.route('/addComment', methods=['post'])
def addComment():
    uName = escape(request.form[('uName')]).replace('\n', ' ').replace('\r', ' ')
    uComment = (request.form[('uComment')]).replace('\n', ' ').replace('\r', ' ')
    dateStr = time.strftime("%d-%m-%y %H:%M")
    if uName == '':
        uName = 'Anonymous'
    comList = readFile("static/comments.csv")
    if uComment == '':
        err = True
    else:
        err = False
        comList.append([uName, uComment, dateStr])
        writeFile("static/comments.csv", comList)
    return render_template('Comments.html', comList=comList, err=err)

@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/gallery')
def gallery():
    return render_template('Gallery.html')


def readFile(File):
	with open(File, 'r', newline='') as inFile:
		reader = csv.reader(inFile)
		comList = [row for row in reader]
	return comList


def writeFile(File, appendedList):
	with open(File, 'w', newline='') as outFile:
		writer = csv.writer(outFile)
		writer.writerows(appendedList)


if __name__ == '__main__':
    app.run(debug=True)
