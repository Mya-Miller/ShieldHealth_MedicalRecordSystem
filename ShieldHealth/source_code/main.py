import logging
import os

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session, current_app

from ShieldHealth.source_code.src.patients import patientsUtil
from ShieldHealth.source_code.src.register import registerUtil
from ShieldHealth.source_code.src.login import loginUtil
from ShieldHealth.source_code.src.appointments import appointmentsUtil

from ShieldHealth.source_code.src.medication.medicationUtils import *
from ShieldHealth.source_code.src.medication.medicationUtils import add_medication, update_medication, remove_medication
from ShieldHealth.source_code.src.util import MEDICATION_DB, APPOINTMENTS_DB

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()


@app.route('/')
def default():
    return render_template('index.html')


@app.route('/index')
def index():
    access = session.get('access')
    return render_template('index.html', access=access)


@app.route('/login', methods=["GET", "POST"])
def login():
    access = session.get('access')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        credentials = loginUtil.Login.get_credentials()
        if username in credentials and credentials[username] == registerUtil.Register.hash_password(password):
            session['access'] = str(loginUtil.Login.get_access(username))
            session['username'] = str(username)
            return redirect(url_for('index'))
        else:
            message = "Invalid username or password. Please try again."
            return redirect(url_for('login', invalid_message=message))
    return render_template('login/login.html', access=access)


@app.route('/register', methods=["GET", "POST"])
def register():
    access = session.get('access')

    if request.method == 'POST':
        credentials = loginUtil.Login.get_credentials()
        if request.form['username'] in credentials:
            message = "This username is taken. Please try again."
            return redirect(url_for('register', invalid_message=message))

        password = request.form['password']
        creditialsDic = {
            'username': request.form['username'],
            'account_type': request.form['account_type'],
            'password': registerUtil.Register.hash_password(password),
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
        }
        registerUtil.Register.add_user_to_db(creditialsDic)
        message = "Registration successful! You can now login."
        return redirect(url_for('login', success_message=message))
    return render_template('register/register.html', access=access)


@app.route('/patients', methods=["GET", "POST"])
def patients():
    access = session.get('access')
    username = session.get('username')
    patientsList = patientsUtil.Patient.get_patients_from_db()
    medicationsList = patientsUtil.Patient.get_medications_from_db()
    medRecordsList = patientsUtil.Patient.get_med_records_from_db()
    if request.method == "POST":
        if request.form.get('addPatient') == 'add':
            # Fields - PatientID,Name,DrugAllergies,DNRStatus,Age,Height,Weight,Gender,EmergencyContact,Phone,Address
            patientDict = {'patientFirstName': request.form.get('inputFirstNameAdd'),
                           'patientLastName': request.form.get('inputLastNameAdd'),
                           'patientDrugAllergies': request.form.get('inputDrugAllergiesAdd'),
                           'patientDNRStatus': request.form.get('inputDNRStatusAdd'),
                           'patientAge': request.form.get('inputAgeAdd'),
                           'patientHeight': request.form.get('inputHeightAdd'),
                           'patientWeight': request.form.get('inputWeightAdd'),
                           'patientGender': request.form.get('inputGenderAdd'),
                           'patientEmergencyContact': request.form.get('inputEmergencyContactAdd'),
                           'patientPhone': request.form.get('inputPhoneAdd'),
                           'patientAddress': '{0} {1}'.format(', '.join([request.form.get('inputAddressAdd'),
                                                                         request.form.get('inputCityAdd'),
                                                                         request.form.get('inputStateAdd')]),
                                                              str(request.form.get('inputZipAdd')))}
            patientsUtil.Patient.add_patient_to_db(patientDict)
            patientsList = patientsUtil.Patient.get_patients_from_db()
        elif request.form.get('updatePatient') == 'update':
            # Fields - PatientID,Name,DrugAllergies,DNRStatus,Age,Height,Weight,Gender,EmergencyContact,Phone,Address
            editPatientDict = {'patientID': request.form.get('editPatientID'),
                               'patientName': request.form.get('inputNameEdit'),
                               'patientDrugAllergies': request.form.get('inputDrugAllergiesEdit'),
                               'patientDNRStatus': request.form.get('inputDNRStatusEdit'),
                               'patientAge': request.form.get('inputAgeEdit'),
                               'patientHeight': request.form.get('inputHeightEdit'),
                               'patientWeight': request.form.get('inputWeightEdit'),
                               'patientGender': request.form.get('inputGenderEdit'),
                               'patientEmergencyContact': request.form.get('inputEmergencyContactEdit'),
                               'patientPhone': request.form.get('inputPhoneEdit'),
                               'patientAddress': request.form.get('inputAddressEdit')}
            patientsUtil.Patient.edit_patient_in_db(editPatientDict)
            patientsList = patientsUtil.Patient.get_patients_from_db()
        elif request.form.get('deletePatient') == 'delete':
            patientsUtil.Patient.delete_patient_from_db(request.form.get('deletePatientID'))
            patientsList = patientsUtil.Patient.get_patients_from_db()
        elif request.form.get('searchPatientBtn') == 'search':
            patientsList = patientsUtil.Patient.search_patients_from_db(request.form.get('searchPatientInput'))
        elif request.form.get('addMedicalRecord') == 'add':
            # Fields - MedRecId,PatientID,DocUserName,MedicationID,MedicationName,MedicationParameters,MedicationDose,
            # MedicationFrequency,MedicationLastPassed
            recordDict = {'patientID': request.form.get('editPatientIDAMR'),
                          'docUserName': request.form.get('editPatientDocUserName'),
                          'medicationID': request.form.get('editPatientMedicationID'),
                          'medicationName': request.form.get('medicationNameAdd'),
                          'medicationParameters': request.form.get('medicationParamAdd'),
                          'medicationDose': request.form.get('medicationDoseAdd'),
                          'medicationFrequency': request.form.get('medicationFrequencyAdd'),
                          'medicationLastPassed': request.form.get('medicationLastPassedAdd')}
            patientsUtil.Patient.add_medRecord_to_db(recordDict)
            medRecordsList = patientsUtil.Patient.get_med_records_from_db()
        elif request.form.get('updateMedicalRecord') == 'update':
            # Fields - MedRecId,PatientID,DocUserName,MedicationID,MedicationName,MedicationParameters,MedicationDose,
            # MedicationFrequency,MedicationLastPassed
            recordDict = {'medRecId': request.form.get('editPatientIDMRID'),
                          'patientID': request.form.get('editPatientIDUMR'),
                          'medicationName': request.form.get('medicationNameEdit'),
                          'medicationParameters': request.form.get('medicationParamEdit'),
                          'medicationDose': request.form.get('medicationDoseEdit'),
                          'medicationFrequency': request.form.get('medicationFrequencyEdit'),
                          'medicationLastPassed': request.form.get('medicationLastPassedEdit')}
            patientsUtil.Patient.edit_medRecord_in_db(recordDict)
            medRecordsList = patientsUtil.Patient.get_med_records_from_db()
        elif request.form.get('deleteMedicalRecord') == 'delete':
            patientsUtil.Patient.delete_medRecord_from_db(request.form.get('deletePatientIDMRID'))
            medRecordsList = patientsUtil.Patient.get_med_records_from_db()
    return render_template('patients/patients.html', access=access, username=username,
                           patientsList=patientsList, medicationsList=medicationsList, medRecordsList=medRecordsList)


# medication page endpoint
@app.route('/medication', methods=["GET", "POST"])
def medication():
    access = session.get('access')
    patientsList = patientsUtil.Patient.get_patients_from_db()
    medicationsList = patientsUtil.Patient.get_medications_from_db()
    if request.method == "POST":
        if request.form.get('searchPatientName') == 'search':
            patientsList = patientsUtil.Patient.search_patients_from_db(request.form.get('searchPatientNameInp'))

    return render_template('medication/medication.html', patientsList=patientsList, access=access,
                           medicationsList=medicationsList)


@app.route('/medication_search_patients', methods=["POST"])
def medication_search_patients():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            searchPatientName = data.get('searchPatientName', '')
            # Call the static method to search patients
            patients = patientsUtil.Patient.search_patients_from_db(searchPatientName)
            return jsonify({'patients': patients})
        except Exception as e:
            logging.error(f"Error processing the search request: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    else:
        return jsonify({'error': 'Request must be JSON'}), 400


# medicationUtil endpoints
@app.route('/all_medication', methods=['GET'])
def get_medications_endpoint():
    try:
        medications = get_medications()
        return jsonify([medication.to_dict() for medication in medications])
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/add_medication', methods=['POST'])
def add_medication_endpoint():
    try:
        medication_data = request.get_json()
        if not medication_data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        if add_medication(medication_data, MEDICATION_DB):
            return jsonify({"success": True, "message": "Medication added successfully"}), 201
        else:
            return jsonify({"success": False, "message": "Failed to add medication"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/edit_medication', methods=['PUT'])
def edit_medication_endpoint():
    try:
        json_data = request.get_json()
        update_medication_name = json_data.get('updateMedicationName')
        update_medication_data = json_data.get('updateMedication')

        #  check for errors first
        if not update_medication_data:
            return jsonify({"success": False, "message": "No medication name provided"}), 400
        if not update_medication_name:
            return jsonify({"success": False, "message": "No medication data provided"}), 400
        if update_medication(update_medication_name, update_medication_data, filepath=MEDICATION_DB):
            return jsonify({"success": True, "message": "Medication updated successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to update medication"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/delete_medication', methods=['DELETE'])
def delete_medication_endpoint():
    try:
        remove_medication_name = request.get_json().get('removeMedicationName')
        if not remove_medication_name:
            return jsonify({"success": False, "message": "No medication name provided"}), 400

        # Assuming remove_medication is a function that returns True if successful
        if remove_medication(remove_medication_name):
            return jsonify({"success": True, "message": "Medication deleted successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Medication not found or failed to delete"}), 404
    except Exception as e:
        # Log exception to be able to troubleshoot
        app.logger.error('Failed to delete medication: %s', str(e))
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/appointments', methods=["GET", "POST"])
def appointments():
    access = session.get('access')
    appointmentsList = appointmentsUtil.Appointment.get_appointments_from_db()
    if request.method == "POST":
        if request.form.get('addBookAppointment') == 'add':
            appointmentDict = {"Name":              request.form.get('name'),
                               "Date":              request.form.get('date'),
                               "Time":              request.form.get('time'),
                               "Reason":            request.form.get('reason'),
                               "Doctor":            request.form.get('doctor'),
                               "HealthIssue":       request.form.get('healthIssue'),
                               "Age":               request.form.get('age'),
                               "Allergies":         request.form.get('allergies'),
                               "Surgery":           request.form.get('surgery'),
                               "SmokingStatus":     request.form.get('smokingStatus'),
                               "AlcoholConsumption": request.form.get('alcoholConsumption'),
                               "Exercise":          request.form.get('exercise'),
                               "Sleep":             request.form.get('sleep'),
                               "Stress":            request.form.get('stress'),
                               "FamilyHistory":     request.form.get('familyHistory')}
            appointmentsUtil.Appointment.add_appointments_to_db(appointmentDict)
            appointmentsList = appointmentsUtil.Appointment.get_appointments_from_db()
        elif request.form.get('deleteAppointment') == 'delete':
            appointmentsUtil.Appointment.delete_appointment_from_db(request.form.get('deleteAppID'))
            appointmentsList = appointmentsUtil.Appointment.get_appointments_from_db()
    return render_template('appointments/appointments.html',
                           access=access, appointmentsList=appointmentsList)


@app.route('/changePassword', methods=["GET", "POST"])
def changePassword():
    access = session.get('access')
    if request.method == 'POST':
        username = request.form['username']
        current_password = registerUtil.Register.hash_password(request.form['current_password'])
        new_password = registerUtil.Register.hash_password(request.form['new_password'])
        credentials = loginUtil.Login.get_credentials()

        if username in credentials and credentials[username] == current_password:
            registerUtil.Register.update_password(username, new_password)
            message = "Your password was successfully updated! You can now login."
            return redirect(url_for('login', success_message=message))
        elif username not in credentials or credentials[username] != current_password:
            message = "Invalid username or password. Please try again."
            return redirect(url_for('changePassword', invalid_message=message))

    return render_template('changePassword/changePassword.html', access=access)


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page or any other desired page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
