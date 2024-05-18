function fetchData(url) {
    return fetch(url).then(response => response.json());
}

function displayProductsTable(data) {
    const table = document.getElementById('products-table');
    table.innerHTML = '<tbody><tr><td>ID продукта</td><td>Название продукта</td></tr></tbody>';
    if (data && Array.isArray(data.data)) {
        data.data.forEach(product => {
            const row = table.insertRow();
            row.insertCell(0).textContent = product.id;
            row.insertCell(1).textContent = product.name_product;
        });
    } else {
        table.insertRow().insertCell(0).textContent = 'Продукты не найдены';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData('/api/products', {
        method: 'GET',
        headers: {
            'Authorization': 'Basic ' + btoa('username:password')
        }
    }).then(displayProductsTable).catch(error => console.error('Ошибка при получении данных:', error));

    document.getElementById('add-product-form').addEventListener('submit', function (event){
        event.preventDefault();
        const formCreateProductData = new FormData(this);
        const name_product = formCreateProductData.get("name_product");
        fetch('/api/products', {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('username:password'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"name_product": name_product})
        }).then(response => response.json()).then(data => {
            if (data.result === true) {
                const table = document.getElementById('products-table');
                table.innerHTML = '';
                fetchData('/api/products').then(displayProductsTable);
            }
        }).catch(error => console.error('Ошибка при добавление данных:', error));
    });

    document.getElementById('clearButton').addEventListener('click', function () {
        const inputField = document.querySelector('input[name="name_product"]');
        inputField.value = '';
    });
});