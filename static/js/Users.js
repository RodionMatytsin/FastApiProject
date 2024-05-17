function fetchData(url) {
    return fetch(url).then(response => response.json());
}

function displayUsersTable(data) {
    const table = document.getElementById('users-table');
    table.innerHTML = '<tbody><tr><td>ID пользователя</td><td>Имя пользователя</td><td>Пароль</td><td>Электронная почта</td></tr></tbody>';
    if (data && Array.isArray(data.data)) {
        data.data.forEach(user => {
            const row = table.insertRow();
            row.insertCell(0).textContent = user.id;
            row.insertCell(1).textContent = user.username;
            row.insertCell(2).textContent = user.password;
            row.insertCell(3).textContent = user.email;
        });
    } else {
        table.insertRow().insertCell(0).textContent = 'Пользователи не найдены';
    }
}

function displayTokensTable(data) {
    const table = document.getElementById('tokens-table');
    table.innerHTML = '<tbody><tr><td>ID токена</td><td>Токен доступа</td><td>Дата и время создания</td><td>Время истечения</td><td>ID user</td></tr></tbody>';
    if (data && Array.isArray(data.data)) {
        data.data.forEach(token => {
            const row = table.insertRow();
            row.insertCell(0).textContent = token.id;
            row.insertCell(1).textContent = token.access_token;
            row.insertCell(2).textContent = token.datetime_create;
            row.insertCell(3).textContent = token.expires;
            row.insertCell(4).textContent = token.user_id;
        });
    } else {
        table.insertRow().insertCell(0).textContent = 'Токены не найдены';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData('/api/users', {method: 'GET'}).then(displayUsersTable);
    fetchData('/api/users_token', {method: 'GET'}).then(displayTokensTable);
});