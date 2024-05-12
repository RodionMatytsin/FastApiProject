const cartTable = document.getElementById('cart-table');

function fetchData(url) {
    return fetch(url).then(response => response.json());
}

function displayCartTable(data) {
    cartTable.innerHTML = '<tbody><tr><td>ID продукта</td><td>Название продукта</td><td>ID пользователя</td></tr></tbody>';
    if (data && Array.isArray(data.data)) {
        data.data.forEach(cart => {
            const row = cartTable.insertRow();
            row.insertCell(0).textContent = cart.product_id;
            row.insertCell(1).textContent = cart.name_product;
            row.insertCell(2).textContent = cart.user_id;
        });
    } else {
        cartTable.insertRow().insertCell(0).textContent = 'Корзина пользователя не найдена';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData('/api/cart', {
        method: 'GET',
        headers: {
            'Authorization': 'Basic ' + btoa('username:password')
        }
    }).then(displayCartTable).catch(error => console.error('Ошибка при получении данных:', error));

    document.getElementById('add-product-in-cart-form').addEventListener('submit', function (event){
        event.preventDefault();
        const product_id = this["product_id"].value;
        fetch('/api/cart/' + product_id, {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('username:password'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"product_id": product_id})
        }).then(response => response.json()).then(data => {
            if (data.result === true) {
                cartTable.innerHTML = '';
                fetchData('/api/cart').then(displayCartTable);
            }
        }).catch(error => console.error('Ошибка при добавление данных:', error));
    });

    document.getElementById('checkoutButton').addEventListener('click', function (event){
        event.preventDefault();
        fetch('/api/cart', {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('username:password')
            }
        }).then(response => response.json()).then(data => {
            if (data.result === true) {
                cartTable.innerHTML = '';
                fetchData('/api/cart').then(displayCartTable);
            }
       }).catch((error) => {console.error('Error:', error)});
    });
});