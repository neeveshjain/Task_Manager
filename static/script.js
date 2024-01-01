
const API_BASE_URL = '/api/tasks';

async function fetchTasks() {
    const response = await fetch(API_BASE_URL);
    const tasks = await response.json();

    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '<h2>List of Tasks</h2>';

    tasks.forEach(task => {
        const taskItem = document.createElement('div');
        taskItem.classList.add('task');
        taskItem.innerHTML = `
            <input type="checkbox" ${task.completed ? 'checked' : ''} onchange="updateTask(${task.id},event)">
            <span>${task.name}</span>
            <button onclick="deleteTask(${task.id})">Delete</button>
            <button onclick="editTask(${task.id})">Edit</button>
        `;
        taskList.appendChild(taskItem);
    });
}

async function addTask() {
    const taskName = document.getElementById('taskName').value;

    if (taskName.trim() !== '') {
        await fetch(API_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: taskName }),
        });

        document.getElementById('taskName').value = '';
        fetchTasks();
        alert('Task added successfully!');
    }
}


async function updateTask(taskId, event) {
    console.log(event.target.checked); // Log the checkbox state
    await fetch(`${API_BASE_URL}/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: event.target.checked }),
    });

    fetchTasks();
}

async function deleteTask(taskId) {
    await fetch(`${API_BASE_URL}/${taskId}`, {
        method: 'DELETE',
    });

    fetchTasks();
}

async function displayTasks() {
    await fetchTasks();
}

async function editTask(taskId) {
    const newTaskName = prompt('Enter the new task name:');

    if (newTaskName !== null) {
        await fetch(`${API_BASE_URL}/${taskId}/edit`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: newTaskName }),
        });

        fetchTasks();
    }
}

