// Page interactions section
document.addEventListener('DOMContentLoaded', function() {
    // Initialize interactive dropdowns
    InteractiveDropdown('medication-actions-btn', 'dropdown-content-medication');
    InteractiveDropdown('browse-patients', 'patient-dropdown-medication');
    InteractiveDropdown('search-patients-btn-medication', 'patient-dropdown-medication');
    InteractiveDropdown('add-medication', 'add-medication-form');
    InteractiveDropdown('edit-medication', 'edit-medication-form');
    InteractiveDropdown('remove-medication', 'remove-medication-form');

    setupAjaxFormSubmission();

});

function InteractiveDropdown(toggleButtonId, dropdownId) {
    const toggleButton = document.getElementById(toggleButtonId);
    const dropdown = document.getElementById(dropdownId);

    if (!toggleButton || !dropdown) {
        console.error("Dropdown or Button not found:", toggleButtonId, dropdownId);
        return; // Exit if elements are not found
    }

    toggleButton.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent event from propagating to the document
        // Toggle visibility with a check to ensure it doesn't close if already open due to another interaction
        dropdown.style.display = (dropdown.style.display === 'none' || dropdown.style.display === '') ? 'block' : 'none';
    });

    // Adding event listener to handle clicks outside the dropdown to hide it
    document.addEventListener('click', function(event) {
        if (!dropdown.contains(event.target) && event.target !== toggleButton) {
            dropdown.style.display = 'none';
        }
    });

    // Optional: Adjust hover handling if required
    let isHovering = false;
    dropdown.addEventListener('mouseenter', function() {
        isHovering = true;
    });
    dropdown.addEventListener('mouseleave', function() {
        isHovering = false;
        setTimeout(function() {
            if (!isHovering && dropdown.style.display !== 'none') {
                dropdown.style.display = 'none';
            }
        }, 300); // Allow for slight delay before closing on mouse leave
    });
}

function manageForms(currentFormId) {
    const forms = ['add-medication-form', 'edit-medication-form', 'remove-medication-form', 'patient-dropdown-medication'];
    forms.forEach(formId => {
        const form = document.getElementById(formId);
        form.style.display = formId === currentFormId && form.style.display !== 'block' ? 'block' : 'none';
    });
}

function setupAjaxFormSubmission() {
    const searchForm = document.getElementById('search-form'); // Ensure this ID matches your form's ID

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const searchTerm = document.getElementById('patient-name').value;
        fetch('/medication_search_patients', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ searchPatientName: searchTerm })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with non-OK status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                updatePatientDropdown(data.patients);
            }
        })
        .catch(error => console.error('Error:', error));
    });
}


function updatePatientDropdown(patients) {
    const dropdown = document.getElementById('patient-dropdown-medication');
    const tbody = dropdown.querySelector('table tbody');
    tbody.innerHTML = ''; // Clear previous entries

    if (patients.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">No patients found.</td></tr>';
    } else {
        patients.forEach(patient => {
            const row = tbody.insertRow();
            row.innerHTML = `<td>${patient.Name}</td>
                             <td>${patient.Age}</td>
                             <td>${patient.Address}</td>
                             <td>${patient.Phone}</td>
                             <td><!-- Additional Data Here --></td>`;
        });
    }
}

function toggleDropdownVisibility(dropdownId) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.style.display = (dropdown.style.display === 'none' || dropdown.style.display === '') ? 'block' : 'none';
}


// submit buttons

function submitNewMedication() {
    const MedicationName = document.getElementById("MedicationName").value;
    const MedicationRecipient = document.getElementById("MedicationRecipient").value;
    const MedicationRefills = document.getElementById("MedicationRefills").value;
    const MedicationLastPassed = document.getElementById("MedicationLastPassed").value;
    const MedicationParameters = document.getElementById("MedicationParameters").value;
    const MedicationPharmacologicalClass = document.getElementById("MedicationPharmacologicalClass").value;
    const MedicationPrescribedBy = document.getElementById("MedicationPrescribedBy").value;
    const MedicationDose = document.getElementById("MedicationDose").value;
    const MedicationFrequency = document.getElementById("MedicationFrequency").value;

    const newMedication = new Medication(
        MedicationName,
        MedicationRecipient,
        MedicationRefills,
        MedicationLastPassed,
        MedicationParameters,
        MedicationPharmacologicalClass,
        MedicationPrescribedBy,
        MedicationDose,
        MedicationFrequency,
    );

    console.log("Submit new medication is fine before fetching")
    
    // Routing add medication to flask endpoint
    fetch('/add_medication', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        
        body: JSON.stringify(newMedication),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    console.log(newMedication);
    document.getElementById("add-medication-form"); // Resets the form after submission
    location.reload();
};


function submitEditMedication() {
    const MedicationName = document.getElementById("edit-MedicationName").value;
    const MedicationRecipient = document.getElementById("edit-MedicationRecipient").value;
    const MedicationRefills = document.getElementById("edit-MedicationRefills").value;
    const MedicationParameters = document.getElementById("edit-MedicationParameters").value;
    const MedicationPharmacologicalClass = document.getElementById("edit-MedicationPharmacologicalClass").value;
    const MedicationPrescribedBy = document.getElementById("edit-MedicationPrescribedBy").value;
    const MedicationDose = document.getElementById("edit-MedicationDose").value;
    const MedicationFrequency = document.getElementById("edit-MedicationFrequency").value;

    const updateMedication = {
        updateMedicationName: MedicationName,
        updateMedication: {
            MedicationRecipient,
            MedicationRefills,
            MedicationParameters,
            MedicationPharmacologicalClass,
            MedicationPrescribedBy,
            MedicationDose,
            MedicationFrequency
        }
    };

    fetch('/edit_medication', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateMedication)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data);
        if(data.success) {
            location.reload();
            alert("medication updated successfully");
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error updating medication:', error);
        alert('Error updating medication: ' + error);
    });
    console.log("Medication update:", MedicationName);
};

function submitRemoveMedication() {
    const medicationName = document.getElementById("remove-MedicationName").value;
    
    // Check if the name is entered in the field
    if (!medicationName) {
        alert("Please enter the name of the medication to remove.");
        return;
    }

    // Confirmation dialog
    if (confirm("Are you sure you want to remove " + medicationName + "?")) {
        fetch('/delete_medication', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                removeMedicationName: medicationName  // Ensure this matches exactly with your server expectations
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Response from server:", data);
            location.reload();
            alert("Medication removed successfully.");
        })
        .catch(error => {
            console.error('Error removing medication:', error);
            alert("Error removing medication: " + error.message);
        });
        console.log("Medication Removed: ", medicationName);
    } else {
        console.log("Removal cancelled.");
    }
}

// Medication class
class Medication {
    constructor( MedicationName, MedicationRecipient, MedicationRefills, MedicationLastPassed,
        MedicationParameters, MedicationPharmacologicalClass, MedicationPrescribedBy,
         MedicationDose, MedicationFrequency) {
    this.MedicationName = MedicationName;
    this.MedicationRecipient = MedicationRecipient;
    this.MedicationRefills = MedicationRefills;
    this.MedicationLastPassed = MedicationLastPassed;
    this.MedicationParameters = MedicationParameters;
    this.MedicationPharmacologicalClass = MedicationPharmacologicalClass;
    this.MedicationPrescribedBy = MedicationPrescribedBy;
    this.MedicationDose = MedicationDose;
    this.MedicationFrequency = MedicationFrequency;
    };
};

function selectPatient(patientName) {
    console.log('selected patient Name', patientName);
};
