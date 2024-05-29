import string
import random
import csv
from ShieldHealth.source_code.src import util

patientKeyLength = 7

dbFields = ["PatientID", "Name", "DrugAllergies", "DNRStatus", "Age", "Height",
            "Weight", "Gender", "EmergencyContact", "Phone", "Address"]
dbFieldsMedRec = ["MedRecId", "PatientID", "DocUserName", "MedicationID", "MedicationName", "MedicationParameters",
                  "MedicationDose", "MedicationFrequency", "MedicationLastPassed"]


class Patient:
    def __init__(self, patientID, medicalRecords):
        self.patientID = patientID
        self.medicalRecords = medicalRecords

    @staticmethod
    def search_patients_from_db(searchPatientName):
        patients = []
        with open(util.PATIENTS_DB, mode='r') as csv_file:
            for row in csv.DictReader(csv_file):
                if searchPatientName.lower() in row["Name"].lower():
                    patients = patients + [row]
        return patients

    def set_patient_profile(self, patient_id, csv_file_path):
        pass

    @staticmethod
    def get_patients_from_db():
        patients = []
        with open(util.PATIENTS_DB, mode='r') as csv_file:
            for row in csv.DictReader(csv_file):
                patients = patients + [row]
        return patients

    @staticmethod
    def get_medications_from_db():
        medications = []
        with open(util.MEDICATION_DB, mode='r') as csv_file:
            for row in csv.DictReader(csv_file):
                medications = medications + [row]
        return medications

    @staticmethod
    def get_med_records_from_db():
        records = []
        with open(util.MEDICAL_RECORD_DB, mode='r') as csv_file:
            for row in csv.DictReader(csv_file):
                records = records + [row]
        return records

    @staticmethod
    def get_patient_from_db(patient_id):
        with open(util.PATIENTS_DB, mode='r') as csv_file:
            for row in csv.DictReader(csv_file):
                if row["PatientID"] == patient_id:
                    return row

    @staticmethod
    def add_patient_to_db(patientDict):
        patientsFormatForDB = {"PatientID": ''.join(random.choices(string.ascii_uppercase
                                                                   + string.digits, k=patientKeyLength)),
                               "Name": patientDict["patientFirstName"] + " " + patientDict["patientLastName"],
                               "DrugAllergies": patientDict["patientDrugAllergies"],
                               "DNRStatus": patientDict["patientDNRStatus"], "Age": patientDict["patientAge"],
                               "Height": patientDict["patientHeight"], "Weight": patientDict["patientWeight"],
                               "Gender": patientDict["patientGender"],
                               "EmergencyContact": patientDict["patientEmergencyContact"],
                               "Phone": patientDict["patientPhone"], "Address": patientDict["patientAddress"]}
        with open(util.PATIENTS_DB, mode='a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=dbFields)
            csv_writer.writerow(patientsFormatForDB)

    @staticmethod
    def add_medRecord_to_db(recordDict):
        recordsFormatForDB = {"MedRecId": ''.join(random.choices(string.ascii_uppercase
                                                                 + string.digits, k=patientKeyLength)),
                              "PatientID": recordDict["patientID"],
                              "DocUserName": recordDict["docUserName"],
                              "MedicationID": recordDict["medicationID"],
                              "MedicationName": recordDict["medicationName"],
                              "MedicationParameters": recordDict["medicationParameters"],
                              "MedicationDose": recordDict["medicationDose"],
                              "MedicationFrequency": recordDict["medicationFrequency"],
                              "MedicationLastPassed": recordDict["medicationLastPassed"]}
        with open(util.MEDICAL_RECORD_DB, mode='a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=dbFieldsMedRec)
            csv_writer.writerow(recordsFormatForDB)

    @staticmethod
    def edit_patient_in_db(editPatientDict):
        data = []
        with (open(util.PATIENTS_DB, mode='r') as csv_file):
            for row in csv.DictReader(csv_file):
                if row["PatientID"] == editPatientDict["patientID"]:
                    row["Name"] = editPatientDict["patientName"]
                    row["DrugAllergies"] = editPatientDict["patientDrugAllergies"]
                    row["DNRStatus"] = editPatientDict["patientDNRStatus"]
                    row["Age"] = editPatientDict["patientAge"]
                    row["Height"] = editPatientDict["patientHeight"]
                    row["Weight"] = editPatientDict["patientWeight"]
                    row["Gender"] = editPatientDict["patientGender"]
                    row["EmergencyContact"] = editPatientDict["patientEmergencyContact"]
                    row["Phone"] = editPatientDict["patientPhone"]
                    row["Address"] = editPatientDict["patientAddress"]
                data.append(row)
        keys = data[0].keys()
        with open(util.PATIENTS_DB, 'w', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    @staticmethod
    def edit_medRecord_in_db(recordEditDict):
        data = []
        print(recordEditDict)
        with (open(util.MEDICAL_RECORD_DB, mode='r') as csv_file):
            for row in csv.DictReader(csv_file):
                if row["MedRecId"] == recordEditDict["medRecId"]:
                    row["PatientID"] = recordEditDict["patientID"]
                    row["MedicationName"] = recordEditDict["medicationName"]
                    row["MedicationParameters"] = recordEditDict["medicationParameters"]
                    row["MedicationDose"] = recordEditDict["medicationDose"]
                    row["MedicationFrequency"] = recordEditDict["medicationFrequency"]
                    row["MedicationLastPassed"] = recordEditDict["medicationLastPassed"]
                data.append(row)
        keys = data[0].keys()
        with open(util.MEDICAL_RECORD_DB, 'w', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    @staticmethod
    def delete_patient_from_db(deletePatientID):
        with open(util.PATIENTS_DB, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = [row for row in csv_reader]

        modified_data = [row for row in data if row[0] != deletePatientID]

        with open(util.PATIENTS_DB, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(modified_data)

    @staticmethod
    def delete_medRecord_from_db(deleteMedRecID):
        with open(util.MEDICAL_RECORD_DB, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = [row for row in csv_reader]

        modified_data = [row for row in data if row[0] != deleteMedRecID]

        with open(util.MEDICAL_RECORD_DB, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(modified_data)


class PatientInfo:
    def __init__(self, name, drugAllergies, DNRStatus, age, height, weight, gender, emergencyContact, phone, address):
        self.Name = name
        self.DrugAllergies = drugAllergies
        self.DNRStatus = DNRStatus
        self.Age = age
        self.Height = height
        self.Weight = weight
        self.Gender = gender
        self.EmergencyContact = emergencyContact
        self.Phone = phone
        self.Address = address


class PatientSearchParse:
    def __init__(self, patientIDs):
        # Assume 'patientIDs' is a list of PatientIDs
        self.patientIDs = patientIDs

    def retrieve_patient_info(self, id):
        # based on returned patientID retrieve patient info from the database
        pass
