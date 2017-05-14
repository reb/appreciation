from flask import Flask, render_template, request, redirect
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/send", methods=['POST'])
def send():
    sender = "appreciation10x@gmail.com"
    receiver = "appreciation10x@gmail.com"
    subject = "Yo mom! Check this out"

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = subject
    
    video_name = "message.mp4"
    video_data = request.files['video'].read()
    video = MIMEApplication(video_data, Name=video_name)
    video['Content-Disposition'] = 'attachement; filename="{}"'.format(video_name)
    message.attach(video)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login("appreciation10x@gmail.com", "secret")
    server.sendmail(sender, receiver, message.as_string())
    server.close()

    return redirect("success")


@app.route("/success")
def success():
    return render_template('success.html')

if __name__ == '__main__':
     app.run(debug=True, host="0.0.0.0", port=int(sys.argv[1]))
