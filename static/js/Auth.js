function handleLoginSubmit(event) {
    event.preventDefault();
    const formLoginData = new FormData(event.target);
    const loginUsername = formLoginData.get('username');
    const loginPassword = formLoginData.get('password');

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"username": loginUsername, "password": loginPassword})
    }).then(response => response.json()).then(data => {
        console.log('Success:', data);
        alert(data.message);
        document.cookie = `user_token=${data.data.access_token}; HttpOnly`;
    }).catch((error) => {
        console.error('Error:', error);
    });
}

function handleSigUpSubmit(event) {
    event.preventDefault();
    const formSigUpData = new FormData(event.target);
    const regisUsername = formSigUpData.get('username');
    const regisPassword = formSigUpData.get('password');
    const regisEmail = formSigUpData.get('email');

    fetch('/api/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"username": regisUsername, "password": regisPassword, "email": regisEmail})
    }).then(response => response.json()).then(data => {
        console.log('Success:', data);
        alert(data.message);
    }).catch((error) => {
        console.error('Error:', error);
    });
}

function handleLogoutClick() {
    fetch('/api/logout', {
        method: 'GET',
        credentials: 'include'
    }).then(response => response.json()).then(data => {
        console.log('Success:', data);
        alert(data.message);
        document.cookie = 'user_token=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }).catch((error) => {
        console.error('Error:', error);
    });
}

function handleHomeClick() {
    fetch('/api/home', {
        method: 'GET',
        credentials: 'include'
    }).then(response => response.json()).then(data => {
        console.log('Success:', data);
        alert(data.message);
    }).catch((error) => {
        console.error('Error:', error);
    });
}

document.getElementById('loginForm').addEventListener('submit', handleLoginSubmit);
document.getElementById('regisForm').addEventListener('submit', handleSigUpSubmit);
document.getElementById('logoutButton').addEventListener('click', handleLogoutClick);
document.getElementById('homeButton').addEventListener('click', handleHomeClick);