from flask import Flask, render_template, request
from cgi import escape #used to escape html special characters
import csv
import re

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
    dateStr = time.strftime("%d-%m-%y")
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

@app.route('/book')
def book():
    return render_template('Book.html',bookList=readFile('static/booking.csv'))

@app.route('/processBooking', methods=['post'])
def processBooking():#TODO perform regex checks on fields and set errorlist if any errors found
    errorList = [0]
    dateRegex = re.compile('^([0-2]?[0-9]|3[0-1])/(0?[0-9]|1[0-2])/([0-9]?[0-9]?[0-9]?[0-9]?)$')
    emailRegex = re.compile('\w+@\w+\.\w+')
    startDate = '/'.join([request.form[('startDateDay')], request.form[('startDateMonth')], request.form[('startDateYear')]])
    endDate = '/'.join([request.form[('startDateDay')], request.form[('startDateMonth')], request.form[('startDateYear')]])
    email = request.form[('email')]
    name = request.form[('name')]
    if not(dateRegex.match(startDate)):
        errorList[0] = 1
        errorList.append('startdateformatexception')
    if not(dateRegex.match(endDate)):
        errorList[0] = 1
        errorList.append('enddateformatexception')
    if not(emailRegex.match(email)):
        errorList[0] = 1
        errorList.append('emailformatexception')

    bookList = readFile('static/booking.csv')
    bookList.append([startDate, endDate, name, email, False])
    writeFile('static/booking.csv', bookList)
    return render_template('ProcessBooking.html', errorList=errorList)


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
