import hashlib
import csv
import random
import smtplib
from ShieldHealth.source_code.src import util
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# This page is for interacting with your csv or DB no need for a class
class Login:
    @staticmethod
    def get_credentials():
        credentials = {}
        with open(util.LOGIN_DB, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                credentials[row['Username']] = row['Password']
        return credentials

    @staticmethod
    def get_access(username):
        with open(util.LOGIN_DB, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    return row['Access']
        return None  # Return None if username not found