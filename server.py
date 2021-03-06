from flask import Flask, render_template, request, redirect, send_from_directory
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import sys
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/recording")
def make():
    return render_template('recording.html')

@app.route("/send", methods=['POST'])
def send():
    us = "appreciation10x@gmail.com"
    sender = request.form['sender']
    mom = request.form['mom']
    body = request.form['body']
    subject = "Fijne moederdag, mama"

    message = MIMEMultipart()
    message['From'] = sender
    message['Reply-To'] = sender
    message['To'] = mom
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = subject
    
    log_message = "{} sent a message for {}".format(sender, mom)

    video_name = "message.mp4"
    video_data = request.files['video'].read()
    video = MIMEApplication(video_data, Name=video_name)
    video['Content-Disposition'] = 'attachement; filename="{}"'.format(video_name)
    message.attach(video)
    message.attach(MIMEText(body))

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(us, os.environ.get('PASSWORD', ""))
    server.sendmail(sender, mom, message.as_string())
    server.sendmail(us, sender, message.as_string())
    server.sendmail(us, us, log_message)
    server.close()

    return redirect("share")

@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('static', path)

@app.route("/share")
def share():
    return render_template('share.html')

if __name__ == '__main__':
     app.run(debug=True, host="0.0.0.0", port=int(sys.argv[1]))
