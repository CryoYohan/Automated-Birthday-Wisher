import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import datetime as dt
from random import choice, randint
import pandas as pd

load_dotenv()

now = dt.datetime.now()
day_today = now.weekday()

sender_email = os.getenv("sender_email")
#receiver_email = os.getenv("receiver_email")
app_password = os.getenv("PASSWORD")

def send_email(message, receiver_email, subject):
    """
        Send email to recipients
    """
    msg = MIMEText(f"{message}")
    msg["Subject"] = subject
    msg["From"] = "Cyril John Ypil"
    msg["To"] = receiver_email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print("Error:", e)

def get_motivational_quote():
    """
        Pick random motivational quote
    """
    try:
        with open("quotes.txt", "r") as file:
            quotes = file.read()
            quotes = quotes.split("\n")
            message = choice(quotes)
    except FileNotFoundError:
        print("File does not exist!")
    else:
        return message

def get_birthdays():
    """
        Get close friends birthday data
    """
    try:
        df = pd.read_csv("birthdays.csv")
    except FileNotFoundError:
        print("The 'birthdays.csv' file is missing!")
    else:
        birthdays_data = df.to_dict(orient="records")
        return birthdays_data

def letter_template():
    """
        Pick random letter template
    """
    random_template = f"letter_{randint(1,7)}.txt"
    return random_template

def wish_happy_birthday():
    """
        Greet close friends and love ones HAPPY BIRTHDAY
    """
    birthdays = get_birthdays()
    count = 0
    for birthday in birthdays:
        birthdate = datetime(year=birthday["year"], month=birthday["month"], day=birthday["day"])
        if birthdate.month == now.month and birthdate.day == now.day:
            try:
                with open(f"letter_templates/{letter_template()}", "r") as letter:
                    message = letter.read()
                    message = message.replace("[NAME]", f"{birthday["name"]}")
                    print(f"Birthday Message:\nTo: {birthday["email"]}\n{message}")
                    send_email(message=message, receiver_email=birthday["email"], subject="Happy Birthday Wish")
                    count += 1
            except FileNotFoundError:
                print(f"File '{letter_template()}' does not exist!")
    print(f"There are {count} birthday(s) for this day: {now.date()}")

def share_motivational_quote():
    """
        Send motivational quotes on Mondays
    """
    day_of_week = now.weekday()
    monday = 2
    if day_of_week == monday:
        data = pd.read_csv("birthdays.csv")
        friends = data.to_dict(orient="records")

        for friend in friends:
            message = get_motivational_quote()
            subject = "Monday Motivational Quote"
            email = friend["email"]
            send_email(message=message, receiver_email=email, subject=subject)

if __name__ == "__main__":
    share_motivational_quote()
    wish_happy_birthday()