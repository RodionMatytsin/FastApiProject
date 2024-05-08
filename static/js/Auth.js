function handleLoginSubmit(event) {
    event.preventDefault();
    const formdata = new FormData(event.target);
    const username = formdata.get('username');
    const password = formdata.get('password');

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"username": username, "password": password})
    }).then(response => response.json()).then(data => {
        console.log('Success:', data);
        alert(data.message);
        document.cookie = `user_token=${data.data.access_token}; HttpOnly`;
    }).catch((error) => {
        console.error('Error:', error);
    });
}

document.getElementById('loginForm').addEventListener('submit', handleLoginSubmit)
