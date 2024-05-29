import hashlib
import csv
from ShieldHealth.source_code.src import util

dbFields = ["Username","Password","Access","FirstName","LastName"]
class Register:
    # Function to hash passwords
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def add_user_to_db(userDic):
        userFormatForDB = {
            "Username": userDic["username"],
            "Password": userDic["password"],
            "Access": userDic["account_type"],
            "FirstName": userDic["first_name"],
            "LastName": userDic["last_name"]
        }
        with open(util.LOGIN_DB, mode='a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=dbFields)
            csv_writer.writerow(userFormatForDB)

    @staticmethod
    def update_password(username, password):
        rows = []

        # Read the CSV file and update the password
        with open(util.LOGIN_DB, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    row['Password'] = password
                    updated = True
                rows.append(row)

        # Write the updated data back to the CSV file
        with open(util.LOGIN_DB, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)