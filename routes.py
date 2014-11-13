from flask import Flask, render_template, request
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
    return render_template('Comments.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/gallery')
def gallery():
    return render_template('Gallery.html')


if __name__ == '__main__':
    app.run(debug=True)
