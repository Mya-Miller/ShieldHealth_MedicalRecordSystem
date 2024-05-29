import os
import csv
from flask import jsonify

from ShieldHealth.source_code.src.util import MEDICATION_DB

# CRUD functions that link to the Flask endpoints in main.py

# Read medication helps the other function access the csv
def read_medications(filepath=MEDICATION_DB):
    try:
        with open(filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print("Medication database file not found.")
        return []  # return empty if not found
    except Exception as e:
        print(f"Error reading medications: {e}")
        return []

def get_medications():
    medications = read_medications()
    if medications:
        return jsonify(medications)
    else:
        return jsonify({'message': 'No medications found'}), 404


def add_medication(medication_data, filepath=MEDICATION_DB):
    try:
        # Read CSV
        medications = read_medications(filepath)
        if not medications:
            new_id = "M1"
        else:
            highest_id = max(int(med['MedicationID'][1:]) for med in medications)
            new_id = f"M{highest_id + 1}" 

        # Insert new ID
        medication_data['MedicationID'] = new_id

        # defines the order of the fields of the csv
        required_fields = [ 'MedicationID', 'MedicationName', 'MedicationRecipient', 'MedicationRefills', 'MedicationLastPassed',
                            'MedicationParameters', 'MedicationPharmacologicalClass', 'MedicationPrescribedBy',
                            'MedicationDose', 'MedicationFrequency']    

        sorted_med_data = {field: medication_data.get(field, '') for field in required_fields}
            
        print("Writing data:", medication_data)
        # Append the new medication entry
        with open(filepath, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=required_fields)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(sorted_med_data)
        
        return True
    except Exception as e:
        print(f"Error adding medication: {e}")
        return False


def update_medication(update_medication_name, update_data, filepath=MEDICATION_DB):
    try:
        # Read existing entries
        medications = read_medications(filepath)
        updated = False
        temp_filepath = filepath + '.tmp'

        # Define the order of fields to ensure consistency
        required_fields = ['MedicationID', 'MedicationName', 'MedicationRecipient', 'MedicationRefills', 
                           'MedicationLastPassed', 'MedicationParameters', 'MedicationPharmacologicalClass', 
                           'MedicationPrescribedBy', 'MedicationDose', 'MedicationFrequency']

        with open(temp_filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=required_fields)
            writer.writeheader()

            for med in medications:
                # Check if the current record is the one to update
                if med['MedicationName'].lower() == update_medication_name.lower():
                    # Update only the fields that are provided in update_data
                    for key, value in update_data.items():
                        if key in med:
                            med[key] = value
                    updated = True
                # Ensure all fields are included when rewriting
                sorted_med_data = {field: med.get(field, '') for field in required_fields}
                writer.writerow(sorted_med_data)

        # Replace the original file with the updated temporary file
        if updated:
            os.replace(temp_filepath, filepath)
        else:
            os.remove(temp_filepath)

        return updated
    except Exception as e:
        print(f"Error updating medication: {e}")
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        return False



def remove_medication(remove_medication_name, filepath=MEDICATION_DB):
    try:
        # Read existing entries
        medications = read_medications(filepath)
        updated = False
        temp_filepath = f"{filepath}.temp"

        # Check if there are medications to process
        if not medications:
            print("No medications to remove.")
            return False

        # Open temporary file for writing
        with open(temp_filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=medications[0].keys())
            writer.writeheader()

            # Write only those medications that do not match the provided name
            for med in medications:
                if med['MedicationName'].lower() != remove_medication_name.lower():
                    writer.writerow(med)
                else:
                    updated = True

        # Replace the original file with the temp file if updates were made
        if updated:
            os.replace(temp_filepath, filepath)
        else:
            os.remove(temp_filepath)

        return updated
    except Exception as e:
        print(f"Error removing medication: {e}")
        # Ensure the temp file is removed if it exists using os.path
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        return False
