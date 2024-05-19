function fetchData(url) {
    return fetch(url).then(response => response.json());
}

function displayCartTable(data) {
    const ordersTable = document.getElementById('orders-table');
    ordersTable.innerHTML = '<tbody><tr><td>Название продукта</td><td>ID пользователя</td></tr></tbody>';
    if (data && Array.isArray(data.data)) {
        data.data.forEach(order => {
            const row = ordersTable.insertRow();
            row.insertCell(0).textContent = order.name_product;
            row.insertCell(1).textContent = order.user_id;
        });
    } else {
        ordersTable.insertRow().insertCell(0).textContent = 'Заказ пользователя не найден';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData('/api/order', {
        method: 'GET',
        headers: {
            'Authorization': 'Basic ' + btoa('username:password')
        }
    }).then(displayCartTable).catch(error => console.error('Ошибка при получении данных:', error));
});