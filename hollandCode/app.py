from flask import Flask, render_template, request, redirect,url_for
from email.mime.text import MIMEText
import json, ast
import smtplib

app=Flask(__name__)


def extractKey(sortDict):
    sortDict = sorted(sortDict, key=sortDict.get)
    return sortDict

def extractValue(sortDict):
    sortDict = sorted(sortDict.values())
    return sortDict

def send_to_mail(dataDict,getKey):
    first_name = dataDict['first_name']
    last_name = dataDict['last_name']
    age = dataDict['age']
    gender = dataDict['gender']
    ps = dataDict['ps']
    email = dataDict['email']

    # DONT FORGET TO AUTHENTICATE SMTP LIBRARY FOR YOUR GMAIL ACC
    from_email="yourEmailHere"
    from_password="yourPasswordHere"
    to_email=email

    threeCodes = getKey[5]+getKey[4]+getKey[3]
    fourCodes = getKey[5]+getKey[4]+getKey[3]+getKey[2]
    fullname = first_name+" "+last_name
    details = "<br> <strong>Details</strong> <br> First name : %s ,<br> Last name : %s ,<br> Age : %s ,<br> Gender : %s ,<br> Profession/Studies : %s , <br>" \
    % (first_name,last_name,age,gender,ps)
    subject="Holland Code Personality Test"
    message="Hey %s,<br> Your 3-letters code is <strong>%s</strong>.<br> Your 4-letters code is <strong>%s</strong>. %s Thanks for using the site!" \
    % (fullname,threeCodes,fourCodes,details)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['from']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def validateCode():
    getCode = request.form['inputCode']
    if getCode == "hoNyanCode2018":
        return render_template("hollandCode.html")
    else:
        return render_template("hahaha.html")

@app.route('/success/<response_data>')
def success(response_data):
    raw_data = response_data
    list_data = raw_data.split(",")
    list_holland = list_data[0:12]
    list_userData = list_data[12:]
    dict_holland = dict(zip(list_holland[::2], list_holland[1::2]))
    dict_userData = dict(zip(list_userData[::2], list_userData[1::2]))
    getOrderedKey = extractKey(dict_holland)
    getOrderedValue = extractValue(dict_holland)
    send_to_mail(dict_userData,getOrderedKey)
    return render_template("success.html",codeOrdered=getOrderedKey,valueOrdered=getOrderedValue)

@app.route('/twitter')
def twitter():
    twitter_acc = "http://www.twitter.com/yunara_zulfiqar"
    return redirect(twitter_acc)

@app.route('/github')
def github():
    github_acc = "http://www.github.com/yunaranyancat"
    return redirect(github_acc)

@app.errorhandler(405)
def page_not_found(e):
    return render_template('405.html'), 405

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.debug = False
    app.run()
