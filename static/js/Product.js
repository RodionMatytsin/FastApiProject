document.addEventListener('DOMContentLoaded', function () {
   function readProducts() {
        fetch('/api/products', {
            headers: {
                'Authorization': 'Basic ' + btoa('username:password')
            }
        })
            .then(response => response.json())
            .then(data => {
                const productsTable = document.getElementById('products-table');
                productsTable.innerHTML = '';
                if (data && Array.isArray(data.data)) {
                    data.data.forEach(product => {
                        const row = productsTable.insertRow();
                        row.insertCell(0).textContent = product['product_id'];
                        row.insertCell(1).textContent = product['name_product'];
                    });
                } else {
                    console.error('Ошибка: данные не являются массивом');
                }
            })
            .catch(error => console.error('Ошибка при чтении продуктов:', error));
   }

   function createProduct() {
       const form = document.getElementById('create-product-form');
       form.addEventListener('submit', function(event) {
           event.preventDefault();
           const name_product = form.name_product.value;
           fetch('/api/products', {
               method: 'POST',
               headers: {
                   'Authorization': 'Basic ' + btoa('username:password'),
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify({ "name_product": name_product })
           }).then(response => response.json()).then(data => {
               alert(data.message);
               readProducts();
           }).catch(error => console.error('Ошибка при создании продукта:', error));
       });
   }

   readProducts();
   createProduct();
});