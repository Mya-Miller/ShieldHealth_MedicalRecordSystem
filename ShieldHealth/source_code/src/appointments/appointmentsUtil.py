import string
import random
import csv
from ShieldHealth.source_code.src import util

KeyLength = 7
dbFields = ['ID', 'Name', 'Date', 'Time', 'Reason', 'Doctor', 'HealthIssue', 'Age', 'Allergies', 'Surgery',
            'SmokingStatus', 'AlcoholConsumption', 'Exercise', 'Sleep', 'Stress', 'FamilyHistory']


class Appointment:
    def __init__(self, appointmentID, patientID):
        self.patientID = patientID
        self.appointmentID = appointmentID

    @staticmethod
    def get_appointments_from_db():
        appointments = []
        with open(util.APPOINTMENTS_DB, mode='r') as csv_file:
            for row in csv.DictReader(csv_file):
                appointments = appointments + [row]
        return appointments

    @staticmethod
    def add_appointments_to_db(appointmentDict):
        appointmentsFormatForDB = {"ID":                ''.join(random.choices(string.ascii_uppercase + string.digits,
                                                                               k=KeyLength)),
                                   "Name":              appointmentDict["Name"],
                                   "Date":              appointmentDict["Date"],
                                   "Time":              appointmentDict["Time"],
                                   "Reason":            appointmentDict["Reason"],
                                   "Doctor":            appointmentDict["Doctor"],
                                   "HealthIssue":       appointmentDict["HealthIssue"],
                                   "Age":               appointmentDict["Age"],
                                   "Allergies":         appointmentDict["Allergies"],
                                   "Surgery":           appointmentDict["Surgery"],
                                   "SmokingStatus":     appointmentDict["SmokingStatus"],
                                   "AlcoholConsumption": appointmentDict["AlcoholConsumption"],
                                   "Exercise":          appointmentDict["Exercise"],
                                   "Sleep":             appointmentDict["Sleep"],
                                   "Stress":            appointmentDict["Stress"],
                                   "FamilyHistory":     appointmentDict["FamilyHistory"]}
        with open(util.APPOINTMENTS_DB, mode='a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=dbFields)
            csv_writer.writerow(appointmentsFormatForDB)

    @staticmethod
    def delete_appointment_from_db(deleteAppID):
        with open(util.APPOINTMENTS_DB, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = [row for row in csv_reader]

        modified_data = [row for row in data if row[0] != deleteAppID]

        with open(util.APPOINTMENTS_DB, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(modified_data)
