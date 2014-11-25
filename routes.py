from flask import Flask, render_template, request
from datetime import datetime, timedelta
from cgi import escape #used to escape html special characters
import csv
import re
import time

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/attractions')
def attractions():
    return render_template('Attractions.html')

@app.route('/comments')
def comments():#
    comList = readFile("static/comments.csv")
    return render_template('Comments.html', comList=comList, err=False)#errors can only occur when the page is rendered through addComment

@app.route('/addComment', methods=['post'])
def addComment():
    uName = escape(request.form[('uName')]).replace('\n', ' ').replace('\r', ' ')
    uComment = (request.form[('uComment')]).replace('\n', ' ').replace('\r', ' ')#remove new lines for csv storage
    dateStr = time.strftime("%d-%m-%Y")#get current date as string
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
    bookList=readFile('static/booking.csv')
    dateBook = []
    for booking in bookList:
        startDateTime = datetime.strptime(booking[0], '%d/%m/%Y')
        endDateTime = datetime.strptime(booking[1], '%d/%m/%Y')
        dateBook.append([booking[0], (endDateTime - startDateTime).days])#create a 2D list containing the start date and duration of each booking
    return render_template('Book.html', dateBook=dateBook)


@app.route('/processBooking', methods=['post'])
def processBooking():
    errorList = [0]#flag to check for see if any errors have occured, each subsequent element could contain a string identifying the error
    dateRegex = re.compile('^([0-2]?[0-9]|3[0-1])/(0?[0-9]|1[0-2])/([0-9]?[0-9]?[0-9]?[0-9]?)$')#Check for valid date format
    emailRegex = re.compile('\w+@\w+\.\w+')#check for valid email adress
    startDate = '/'.join([request.form[('startDateDay')], request.form[('startDateMonth')], request.form[('startDateYear')]])
    endDate = '/'.join([request.form[('endDateDay')], request.form[('endDateMonth')], request.form[('endDateYear')]])#compile date string from input fields
    email = request.form[('email')]
    name = request.form[('name')]
    bookList = readFile('static/booking.csv')

    #try to create a date from the string. This will throw an error if the date is a bad format or an invlid date(e.g. 32/11/2014)
    try:
        startDateTime = datetime.strptime(startDate, '%d/%m/%Y')
        endDateTime = datetime.strptime(endDate, '%d/%m/%Y')
    except ValueError:
        errorList[0] = 1
        errorList.append('invaliddateexception')
    else:
        print(startDateTime, ' ', endDateTime)
        print((startDateTime - endDateTime).days)
        if (startDateTime - endDateTime) > timedelta(0):
            errorList[0] = 1
            errorList.append('leavebeforearriveexception')
        if (startDateTime - datetime.now()) < timedelta(0) or (endDateTime - datetime.now()) < timedelta(0):
            errorList[0] = 1
            errorList.append('bookinpastexception')
    #if statements to check for each possible error
    if not(dateRegex.match(startDate)):
        errorList[0] = 1
        errorList.append('startdateformatexception')
    if not(dateRegex.match(endDate)):
        errorList[0] = 1
        errorList.append('enddateformatexception')
    if not(emailRegex.match(email)):
        errorList[0] = 1
        errorList.append('emailformatexception')
    for booking in bookList:
        prevStartDateTime = datetime.strptime(booking[0], '%d/%m/%Y')
        prevEndDateTime = datetime.strptime(booking[1], '%d/%m/%Y')
        if not (prevStartDateTime > endDateTime or prevEndDateTime < startDateTime):
            errorList[0] = 1
            errorList.append('alreadybookedexception')

    if errorList[0] == 0:
        bookList.append([startDate, endDate, name, email, False])
        writeFile('static/booking.csv', bookList)
    return render_template('ProcessBooking.html', errorList=errorList)

@app.errorhandler(404)#404 page
def notFound(e):
    return render_template('404.html'), 404

#read and wite between files and lists
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
