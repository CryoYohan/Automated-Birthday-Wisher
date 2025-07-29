import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import datetime as dt
from random import choice

load_dotenv()

sender_email = os.getenv("sender_email")
receiver_email = os.getenv("receiver_email")
app_password = os.getenv("PASSWORD")

# msg = MIMEText("HAPPY BIRTHDAY KNEE GEAR!")
# msg["Subject"] = "Happy Birthday Wish"
# msg["From"] = sender_email
# msg["To"] = receiver_email

def send_email(message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully.")
    except Exception as e:
        print("Error:", e)

def motivational_quote():
    try:
        with open("quotes.txt", "r") as file:
            quotes = file.read()
            quotes = quotes.split("\n")
            message = choice(quotes)
    except FileNotFoundError:
        print("File does not exist!")
    else:
        return message


now = dt.datetime.now()
day_today = now.weekday()
if day_today == 2:
     quote = motivational_quote()
     print(quote)
     send_email(f"Subject: Tuesday Motivational Quotes\n\n{quote}")
