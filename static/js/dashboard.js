//function to add a habit and reflect in frontend
function addHabit(event){
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    fetch('/addhabit', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                const habitsList = document.getElementById('habit-list');
                const newHabit = `
                <form id="habitForm_${data.habit_id}">
                    <input type="hidden" name="habit_id" value="${data.habit_id}">
                    <label class="habit-description" for="habit_${data.habit_id}" onclick="makeEditable(this)">${data.desc}</label>
                    <input type="text" class="habit-input" style="display: none;" onblur="saveText(this)" onkeydown="handleKeyPress(event, this)">
                    <div class="checkbox-container">
                        ${['Daily', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].map((label, i) => `
                            <input type="checkbox" id="habit_${data.habit_id}_checkbox_${i}" name="habit_${data.habit_id}_checkbox_${i}" class="day-checkbox"
                            ${i === 0 ? `onclick="toggleCheckboxes('${data.habit_id}')"` : `onchange="updateDailyCheckbox('${data.habit_id}')"`} checked>
                            <label class="day" for="habit_${data.habit_id}_checkbox_${i}">${label}</label>
                            `).join('')}
                    </div>
                    <button type="button" onclick="deleteHabit('${data.habit_id}', event)">Delete</button>
                </form>
                `;
                //habitsList.insertAdjacentHTML('beforeend', newHabit);
                habitsList.innerHTML += newHabit;
                form.reset();
            }
            else{
                alert('Failed to add habit');
            }
        })
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
    const forms = document.querySelectorAll('#habit-list form[id^="habitForm_"]'); //gets each individual habit form, use # to get by id
    const changes = [];
    const userId = document.getElementById('user_id').value;

    forms.forEach(form => {
        const habitId = form.querySelector('input[name="habit_id"]').value;
        const habitDescription = form.querySelector('.habit-description').textContent;
        
        const checkboxes = form.querySelectorAll('.day-checkbox');
        const days = ['sun', 'mon', 'tues', 'wed', 'thurs', 'fri', 'sat'];
        const habitData = { habit_id: habitId, habit_description: habitDescription};

        checkboxes.forEach((checkbox, index) => {
            if (index > 0) { //skip 'daily' checkbox
                habitData[days[index - 1]] = checkbox.checked; //store whether or not each checkbox is checked
            }
        });

        changes.push(habitData);
    });

    //restructuring data to include userId
    const payload = {
        user_id: userId,
        habits: changes
    };

    //organize data into JSON array and send to /updatehabits
    const response = await fetch('/updatehabits', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    
    const result = await response.json();
    
    if (result.success) {
        alert('Changes applied successfully!');
    } else {
        alert('Failed to apply changes: ' + result.message);
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
            if (!data.success) {
                alert('Failed to log habit completion')
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

//function to delete a coach-client relationship and reflect that in the html
function removeCoach(user_id, event){
    event.preventDefault();
    const formData = new FormData();
    formData.append('user_id', user_id);
    fetch('/deletecoachinggroup', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                //get the content of coach containers
                const connectedCoach = document.getElementById('connected-coach');
                const coachContainer = document.getElementById('coach-container');
                //remove current content
                connectedCoach.innerHTML = '';
                coachContainer.innerHTML = '';
                //replace with message
                const connCoach = `<p style="color: black;">You have no coach</p>`;
                connectedCoach.innerHTML = connCoach;
                //replace with search form
                const searchFormHtml = `
                    <form id="search-coach-form" method="POST" onsubmit="searchCoach(event)">
                        <input type="text" id="coach_name" name="coach_name" required>
                        <button type="submit" class="btn btn-primary">Search</button>
                    </form>
                `;
                coachContainer.innerHTML = searchFormHtml;
            } else {
                alert('Failed to delete coaching group');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

//function to search for a coach and display a response
function searchCoach(event){
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    fetch('/searchcoach', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                const coach = data.coach_data;
                const coachContainer = document.getElementById('coach-container');
                coachContainer.innerHTML = '';
                const coachInfo = `<form id="search-coach-form" method="POST" onsubmit="searchCoach(event)">
                                        <input type="text" id="coach_name" name="coach_name" required>
                                        <button type="submit" class="btn btn-primary">Search</button>
                                    </form>
                                    <label style="color: black;">${coach.username}</label>
                                    <button type="button" onclick="sendRequest('${ coach.id }', event)">Request</button>`;
                coachContainer.innerHTML = coachInfo
            }
            else{
                const coachContainer = document.getElementById('coach-container');
                coachContainer.innerHTML = '';
                const message = `<form id="search-coach-form" method="POST" onsubmit="searchCoach(event)">
                                    <input type="text" id="coach_name" name="coach_name" required>
                                    <button type="submit" class="btn btn-primary">Search</button>
                                </form>
                                <p style="color: black;">No coaches found</p>`
                                ;
                coachContainer.innerHTML = message;
            }
        })
}

//function to send a 'friend' request from user to a lifecoach
function sendRequest(coach_id, event){
    event.preventDefault();
    const formData = new FormData();
    formData.append('coach_id', coach_id);
    fetch('/sendrequest', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const coach = data.coach_data;
                //get the content of coach containers
                const coachContainer = document.getElementById('coach-container');
                //remove current content
                coachContainer.innerHTML = '';
                //replace with request
                const requestFormHtml = `
                    <label style="color: black;">${coach.username}</label>
                    <button type="button" onclick="removeCoach('${ coach.id }', event)">Cancel Request</button>
                `;
                coachContainer.innerHTML = requestFormHtml;
            } else {
                alert('Failed to send request');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function acceptRequest(user_id, event){
    event.preventDefault();
    const formData = new FormData();
    formData.append('user_id', user_id);
    fetch('/setcoachinggroup', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                //get the content of request container, the div for the user clicked, and the users displayed
                const requestsContainer = document.getElementById('requests-container');
                const userDiv = document.getElementById(`user-${user_id}`);
                const userLabels = requestsContainer.getElementsByTagName('label');
                //remove the user
                userDiv.remove();
                //if there are no users to display, replace with the message
                if (userLabels.length == 0){
                    const noRequests = `<p style="color: black;">You have no incoming requests</p>`;
                    requestsContainer.innerHTML = noRequests;
                }
                 //get the clients container
                const clientsContainer = document.getElementById('clients-container');
                //if the message 'you have no clients' is there, get rid of it
                if (clientsContainer.textContent.includes('You have no clients')) {
                    clientsContainer.innerHTML = '';
                }
                //add the new client to the container
                const newClient = `
                        <form action="/viewuser/${user_id}" method="GET">
                            <label style="color: black;">${data.username}</label>
                            <button type="submit" class="btn btn-primary">View User</button>
                            <button type="button" onclick="deleteClient('${ user_id }', event)">Delete</button>
                        </form>
                    `;
                clientsContainer.innerHTML += newClient;
            } else {
                alert('Failed to accept request');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

function denyRequest(user_id, event){
    event.preventDefault();
    const formData = new FormData();
    formData.append('user_id', user_id);
    fetch('/deletecoachinggroup', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                const requestsContainer = document.getElementById('requests-container');
                const userDiv = document.getElementById(`user-${user_id}`);
                const userLabels = requestsContainer.getElementsByTagName('label');
                userDiv.remove();
                if (userLabels.length == 0){
                    const noRequests = `<p style="color: black;">You have no incoming requests</p>`;
                    requestsContainer.innerHTML = noRequests;
                }
            }
        })
}

function deleteClient(user_id, event){
    event.preventDefault();
    const formData = new FormData();
    formData.append('user_id', user_id);
    fetch('/deletecoachinggroup', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                const clientsContainer = document.getElementById('clients-container');
                const clientLabels = clientsContainer.getElementsByTagName('label');
                const clientDiv = document.getElementById(`client-${user_id}`);
                clientDiv.remove();
                if (clientLabels.length == 0){
                    const noClients = `<p style="color: black;">You have no clients</p>`;
                    clientsContainer.innerHTML = noClients;
                }
            }
        })
}

// Function to format date
function formatDate(date) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
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
    const carbs = document.getElementById('carbsInput').value;
    const fats = document.getElementById('fatsInput').value;
    const calories = document.getElementById('caloriesInput').value;
    const weightlbs = document.getElementById('weightInput').value;
    const user_id = document.getElementById('user_id').value

    const data = {
        user_id: user_id,
        protein: protein,
        calories: calories,
        weightlbs: weightlbs,
        carbs: carbs,
        fats: fats,
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

function getCurrentDateString() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const day = currentDate.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}

//function used to open and close the sliding menu
function toggleMenu() {
    var menu = document.getElementById("myMenu");
    var mainContent = document.getElementById("home");
    if (menu.style.width === "0px" || menu.style.width === "") {
        menu.style.width = "250px";
        mainContent.style.marginLeft = "250px";
    } else {
        menu.style.width = "0";
        mainContent.style.marginLeft = "0";
    }
}