// Function to format date
function formatDate(date) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Function to add a new habit
async function addHabit(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    const response = await fetch('/addhabit', {
        method: 'POST',
        body: data,
    });

    const result = await response.json();
    if (result.success) {
        const habitsList = document.querySelector('.habit-list');
        const newHabitElement = document.createElement('div');
        newHabitElement.innerHTML = `<input type="hidden" name="habit_id" value="${result.habit_id}">
            <label class="habit-description" for="habit_${result.habit_id}">${data.get('habitdesc')}</label>
            <div class="checkbox-container">
                ${['Daily', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].map((label, i) => `
                    <input type="checkbox" id="habit_${result.habit_id}_checkbox_${i}" name="habit_${result.habit_id}_checkbox_${i}" class="day-checkbox" ${i === 0 ? `onclick="dailyCheckbox('${result.habit_id}')"` : ''}>
                    <label class="day" for="habit_${result.habit_id}_checkbox_${i}">${label}</label>
                `).join('')}
            </div>
            <button type="button" onclick="deleteHabit('${result.habit_id}', event)">Delete</button>
        `;
        habitsList.insertBefore(newHabitElement, form);
        form.reset();
    } else {
        alert(result.message);
    }
}

//function that allows a coach to add a habit to their client's habits
async function coachAddHabit(event) {
    event.preventDefault();

    // Retrieve user_id from hidden input
    const userId = document.getElementById('user_id').value;

    // Retrieve habit description from input field
    const habitDescription = document.getElementById('habitdesc').value;

    // Create data object including user_id and habit description
    const habitData = {
        user_id: userId,
        habitdesc: habitDescription
    };

    // Send POST request with JSON data
    const response = await fetch('/coachAddHabit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(habitData)
    });

    // Handle response
    const result = await response.json();
    if (result.success) {
        // Process successful response
        const habitsList = document.querySelector('.habit-list');
        const newHabitElement = document.createElement('div');
        newHabitElement.innerHTML = `<form id="habitForm_${result.habit_id}" onchange="checkBox(event, this)">
                                        <input type="hidden" name="habit_id" value="${result.habit_id}">
                                        <input type="checkbox" id="habit_${result.habit_id}" name="completed" value="True">
                                        <label class="habit-description" for="habit_${result.habit_id}">${habitData.habitdesc}</label>
                                        <button type="button" onclick="showEditPopup('${result.habit_id}', '${habitData.habitdesc}')">Edit</button>
                                        <button type="button" onclick="deleteHabit('${result.habit_id}', event)">Delete</button>
                                    </form>`;
        habitsList.appendChild(newHabitElement);
        // Reset input field
        document.getElementById('habitdesc').value = '';
    } else {
        // Handle unsuccessful response
        alert(result.message);
    }
}

// Function to handle habit checkbox
function checkBox(event, form) {
    event.preventDefault();
    const checkbox = form.querySelector('[name="completed"]');
    const formData = new FormData(form);
    formData.append('completed', checkbox.checked ? 'True' : 'False');

    fetch('/checkbox', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Habit completion logged');
                location.reload()
            } else {
                alert('Failed to log habit completion');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

//functionality: when the daily checkbox is clicked in ManageHabits.html, the rest get checked
function toggleCheckboxes(habitId) {
    var checkboxes = document.querySelectorAll('#habitForm_' + habitId + ' .day-checkbox'); //all day checkboxes
    var dailyCheckbox = checkboxes[0];

    checkboxes.forEach(function(checkbox) {
        checkbox.checked = dailyCheckbox.checked;
    });
}

//functionality: when all checkboxes are clicked, the daily checkbox gets checked
function updateDailyCheckbox(habitId) {
    var checkboxes = document.querySelectorAll('#habitForm_' + habitId + ' .day-checkbox');
    var dailyCheckbox = checkboxes[0];
    let allChecked = true;

    //skip the first checkbox (dailyCheckbox) and check the others
    for (let i = 1; i < checkboxes.length; i++) {
        if (!checkboxes[i].checked) {
            allChecked = false;
            break;
        }
    }

    dailyCheckbox.checked = allChecked;
}

//function to make a label editable, used for the habits in ManageHabits.html
function makeEditable(label) {
    const input = label.nextElementSibling; //gets the input field
    input.value = label.textContent; //puts the text of the label into the input
    label.style.display = 'none'; //hides label
    input.style.display = 'inline-block'; //makes the input field visible
    input.focus(); //puts user's cursor in the input field
}

//function to save the text a user has entered when they click outside of the input field
function saveText(input) {
    const label = input.previousElementSibling;
    label.textContent = input.value;
    input.style.display = 'none';
    label.style.display = 'inline-block';
}

//when enter is clicked after editing a habit description, switches back to the label
function handleKeyPress(event, input) {
    if (event.key === 'Enter') {
        input.blur();
    }
}

// Function to delete a habit
function deleteHabit(habitId, event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('habit_id', habitId);
    formData.append('date', getCurrentDateString()); // Append the date to the form data

    fetch('/deletehabit', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Habit deleted');
                const habitElement = document.getElementById(`habitForm_${habitId}`);
                habitElement.parentNode.removeChild(habitElement);
                closeEditPopup();
            } else {
                alert('Failed to delete habit');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

//function to apply the changes a user has made to habits
async function applyChanges() {
    const forms = document.querySelectorAll('.habit-list form[id^="habitForm_"]'); //gets each individual habit form
    const changes = [];

    forms.forEach(form => {
        const habitId = form.querySelector('input[name="habit_id"]').value;
        const habitDescription = form.querySelector('.habit-description').textContent;
        const checkboxes = form.querySelectorAll('.day-checkbox');
        const days = ['sun', 'mon', 'tues', 'wed', 'thurs', 'fri', 'sat'];
        const habitData = { habit_id: habitId, habit_description: habitDescription };

        checkboxes.forEach((checkbox, index) => {
            if (index > 0) { //skip 'daily' checkbox
                habitData[days[index - 1]] = checkbox.checked; //store whether or not each checkbox is checked
            }
        });

        changes.push(habitData);
    });

    //organize data into JSON array and send to /updatehabits
    const response = await fetch('/updatehabits', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ habits: changes })
    });

    const result = await response.json();
    if (result.success) {
        alert('Changes applied successfully!');
    } else {
        alert('Failed to apply changes.');
    }
}

function previousDate() {
    // Send POST request to /prevday endpoint
    fetch('/prevday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => {
        if (response.ok) {
            // Reload the page or update the content as needed
            location.reload(); // Reload the page to reflect the updated date
        } else {
            console.error('Failed to set previous day');
        }
    }).catch(error => {
        console.error('Error:', error);
    });

}

function nextDate() {
    // Send POST request to /nextday endpoint

    fetch('/nextday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => {
        if (response.ok) {
            // Reload the page or update the content as needed
            location.reload(); // Reload the page to reflect the updated date
        } else {
            console.error('Failed to set next day');
        }
    }).catch(error => {
        console.error('Error:', error);
    });

}

// Function to log macros
async function logMacros(event) {
    event.preventDefault();

    const protein = document.getElementById('proteinInput').value;
    const calories = document.getElementById('caloriesInput').value;
    const weightlbs = document.getElementById('weightInput').value;

    const data = {
        protein: protein,
        calories: calories,
        weightlbs: weightlbs,
        date: getCurrentDateString()
    };

    const response = await fetch('/addmacros', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.success) {
        console.log('Macros logged');
        location.reload()
    } else {
        alert('Failed to log macros');
    }

    updateDate();
}

// Function to log macros
async function lifecoachLogMacros(event) {
    event.preventDefault();

    const protein = document.getElementById('proteinInput').value;
    const calories = document.getElementById('caloriesInput').value;
    const weightlbs = document.getElementById('weightInput').value;

    const user_id = document.getElementById('user_id').value; // Get user_id from hidden input

    const data = {
        user_id: user_id, // Include user_id in the data
        protein: protein,
        calories: calories,
        weightlbs: weightlbs,
        date: getCurrentDateString()
    };

    const response = await fetch('/coach/logmacros', { // Use the new endpoint for coaches
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.success) {
        console.log('Macros logged');
        location.reload()
    } else {
        alert('Failed to log macros');
    }

    updateDate();
}

function getCurrentDateString() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const day = currentDate.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}