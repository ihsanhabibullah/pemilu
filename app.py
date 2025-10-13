from flask import Flask, render_template, request , redirect, url_for,session
from flask_mysqldb import MySQL , MySQLdb

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)


