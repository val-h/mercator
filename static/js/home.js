document.addEventListener('DOMContentLoaded', () => {
    getAllProducts();
});

// Just a sample for now, probably could use pagination and filters
function getAllProducts() {
    fetch('api/products')
    .then(res => res.json())
    .then(data => {
        data.products.forEach(prod => addProduct(contents = prod));
    });
}

function addProduct(contents) {
    product = createProductElement(contents);
    console.log(product);
    document.querySelector('#trending-container').append(product);
}

function createProductElement(product) {
    console.log(product)
    let productElement = document.createElement('div');
    productElement.className = 'trending-product';
    productElement.innerHTML = `
        <img src="${product.images[0].url}" alt='${product['title']}_cover'>
        <div class="title">${product['title']}</div>
        <div class="description">${product['description']}</div>
        <strong><div class="price">${product['price']}</div></strong>
    `;
    return productElement;
}
