function fetchData(url) {
    return fetch(url).then(response => response.json());
}

function displayProductsTable(data) {
    const table = document.getElementById('products-table');
    table.innerHTML = '<tbody><tr><td>ID продукта</td><td>Название продукта</td></tr></tbody>';
    if (data && data.data) {
        data.data.forEach(product => {
            const row = table.insertRow();
            row.insertCell(0).textContent = product.product_id;
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
});
