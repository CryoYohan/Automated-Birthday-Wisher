import smtplib
from datetime import datetime
from email.mime.text import MIMEText
import datetime as dt
from datetime import timezone, timedelta
from random import choice, randint
import pandas as pd
import os

# Get the base directory where the script is located
BASE_DIR = os.path.dirname(__file__)
now = dt.datetime.now(timezone(timedelta(hours=8)))
day_today = now.weekday()

sender_email = os.environ.get("GMAIL_USER")
app_password = os.environ.get("GMAIL_APP_PASSWORD")

def send_email(message, receiver_email, subject):
    """
        Send email to recipients
    """
    msg = MIMEText(f"{message}")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print("Error:", e)

def get_motivational_quote():
    """
        Pick random motivational quote
    """
    quotes_path = os.path.join(BASE_DIR, "quotes.txt")
    try:
        with open(quotes_path, "r") as file:
            quotes = file.read().splitlines()
            message = choice(quotes)
    except FileNotFoundError:
        print("File does not exist!")
        message = "Stay motivated!"
    return message

def get_birthdays():
    """
        Get close friends birthday data
    """
    birthdays_path = os.path.join(BASE_DIR, "birthdays.csv")
    try:
        df = pd.read_csv(birthdays_path)
    except FileNotFoundError:
        print("The 'birthdays.csv' file is missing!")
        return []
    return df.to_dict(orient="records")

def wish_happy_birthday():
    """
        Greet close friends and loved ones HAPPY BIRTHDAY
    """
    birthdays = get_birthdays()
    count = 0
    for birthday in birthdays:
        if birthday["month"] == now.month and birthday["day"] == now.day:
            letter_template_path = os.path.join(BASE_DIR, "letter_templates", f"letter_{randint(1, 7)}.txt")
            try:
                with open(letter_template_path, "r") as letter:
                    message = letter.read().replace("[NAME]", birthday["name"])
                    print(f"Sending Birthday Message to: {birthday['email']}\n{message}")
                    send_email(message=message, receiver_email=birthday["email"], subject="Happy Birthday Wish")
                    count += 1
            except FileNotFoundError:
                print(f"File '{letter_template_path}' does not exist!")
    print(f"There are {count} birthday(s) for today: {now.date()}")

def share_motivational_quote():
    """
        Send motivational quotes on Mondays
    """
    monday = 0  # Monday is 0 in Python datetime
    if day_today == monday:
        print("Today is Monday!")
        friends = get_birthdays()
        for friend in friends:
            message = get_motivational_quote()
            subject = "Monday Motivational Quote"
            email = friend["email"]
            send_email(message=message, receiver_email=email, subject=subject)
    else:
        print("It's not Monday.")

if __name__ == "__main__":
    share_motivational_quote()
    wish_happy_birthday()
