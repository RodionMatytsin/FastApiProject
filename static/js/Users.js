function fetchData(url) {
    return fetch(url).then(response => response.json());
}

function displayUsersTable(data) {
    const table = document.getElementById('users-table');
    table.innerHTML = '<tbody><tr><td>ID пользователя</td><td>Имя пользователя</td><td>Электронная почта</td><td>Пароль</td></tr></tbody>';
    if (data && Array.isArray(data.data)) {
        data.data.forEach(user => {
            const row = table.insertRow();
            row.insertCell(0).textContent = user.user_id;
            row.insertCell(1).textContent = user.username;
            row.insertCell(2).textContent = user.email;
            row.insertCell(3).textContent = user.password;
        });
    } else {
        table.insertRow().insertCell(0).textContent = 'Пользователи не найдены';
    }
}

function displayTokensTable(data) {
    const table = document.getElementById('tokens-table');
    table.innerHTML = '<tbody><tr><td>ID пользователя</td><td>Токен доступа</td><td>Время истечения</td><td>Дата и время создания</td></tr></tbody>';
    if (data && Array.isArray(data.data)) {
        data.data.forEach(token => {
            const row = table.insertRow();
            row.insertCell(0).textContent = token.user_id;
            row.insertCell(1).textContent = token.access_token;
            row.insertCell(2).textContent = token.expire;
            row.insertCell(3).textContent = token.datetime_create;
        });
    } else {
        table.insertRow().insertCell(0).textContent = 'Токены не найдены';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData('/api/users', {method: 'GET'}).then(displayUsersTable);
    fetchData('/api/users_token', {method: 'GET'}).then(displayTokensTable);
});