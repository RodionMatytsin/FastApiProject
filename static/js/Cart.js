function fetchData(url) {
    return fetch(url).then(response => response.json());
}

function displayCartTable(data) {
    const table = document.getElementById('cart-table');
    table.innerHTML = '<tbody><tr><td>ID продукта</td><td>Название продукта</td><td>ID пользователя</td></tr></tbody>';
    if (data && data.data) {
        data.data.forEach(cart => {
            const row = table.insertRow();
            row.insertCell(0).textContent = cart.product_id;
            row.insertCell(1).textContent = cart.name_product;
            row.insertCell(2).textContent = cart.user_id;
        });
    } else {
        table.insertRow().insertCell(0).textContent = 'Корзина пользователя не найдена';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData('/api/cart', {
        method: 'GET',
        headers: {
            'Authorization': 'Basic ' + btoa('username:password')
        }
    }).then(displayCartTable).catch(error => console.error('Ошибка при получении данных:', error));
});
