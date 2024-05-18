function fetchData(url) {
    return fetch(url).then(response => response.json());
}

function displayCartTable(data) {
    const table = document.getElementById('cart-table');
    table.innerHTML = '<tbody><tr><td>ID корзины</td><td>ID продукта</td><td>ID пользователя</td></tr></tbody>';
    if (data && Array.isArray(data.data)) {
        data.data.forEach(cart => {
            const row = table.insertRow();
            row.insertCell(0).textContent = cart.id;
            row.insertCell(1).textContent = cart.product_id;
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

    document.getElementById('add-product-in-cart-form').addEventListener('submit', function (event){
        event.preventDefault();
        const productId = document.getElementById('product-id').value;
        fetch('/api/cart/' + productId, {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('username:password'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"product_id": productId})
        }).then(response => response.json()).then(data => {
            if (data.result === true) {
                const table = document.getElementById('cart-table');
                table.innerHTML = '';
                fetchData('/api/cart').then(displayCartTable);
            } else {
                const table = document.getElementById('cart-table');
                table.innerHTML = '';
                fetchData('/api/cart').then(displayCartTable);
            }
        }).catch(error => {
            console.error('Ошибка при добавление данных:', error);
            alert("Произошла ошибка при добавлении продукта в корзину.");
        });
    });

    document.getElementById('checkoutForm').addEventListener('submit', function (event){
        event.preventDefault();
        fetch('/api/cart', {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('username:password')
            }
        }).then(response => response.json()).then(data => {
            if (data.result === true) {
                alert(data.message);
                const table = document.getElementById('cart-table');
                table.innerHTML = '';
                fetchData('/api/cart').then(displayCartTable);
            } else {
                alert("Ошибка при оформлении заказа: " + data.message);
            }
       }).catch((error) => {
           console.error('Error:', error);
           alert("Произошла ошибка при оформлении заказа. Пожалуйста, попробуйте позже.");
       });
    });
});