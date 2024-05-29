import os

# gets absolute path of current dir
base_dir = os.path.abspath(os.path.dirname(__file__))

# moves up one directory up to sourceCode
source_code_dir = os.path.dirname(base_dir)

# Using os.path.join for cross-platform compatibility

PATIENTS_DB = os.path.join(source_code_dir, "database", "patients.csv")
MEDICATION_DB = os.path.join(source_code_dir, "database", "medication.csv")
LOGIN_DB = os.path.join(source_code_dir, "database", "login.csv")
MEDICAL_RECORD_DB = os.path.join(source_code_dir, "database", "medicalRecord.csv")
APPOINTMENTS_DB = os.path.join(source_code_dir, "database", "appointments.csv")
