function formatRightSideBarCartProduct(item, cart_item_variation) {
    var sizeHTML = cart_item_variation.map(crt => ` ${crt.variation.size}`).join(',')
    return `<div class="single-cart-item">
                <a href="/product/${item.slug}/" class="product-image">
                    <img src="${item.image}" class="cart-thumb" alt="">
                    <!-- Cart Item Desc -->
                    <div class="cart-item-desc">
                        <span class="product-remove"><i class="fa fa-close" aria-hidden="true"></i></span>
                        <span class="badge">${item.brand}</span>
                        <h6>${item.name}</h6>
                        <p class="size"><span>Size: </span>${sizeHTML}</p>
                        <p class="price">#${item.price}</p>
                    </div>
                </a>
            </div>`
}

function handleRightSideBarCartItemContent(cart_items) {
    var cartList = document.getElementById("cart-list-container")
    var formattedSideBarCartProduct = ""
    for (i = 0; i < cart_items.length; i++) {
        var cartProduct = cart_items[i].product
        var cartItemVariation = cart_items[i].cart_item_variation
        var currentItem = formatRightSideBarCartProduct(cartProduct, cartItemVariation)
        formattedSideBarCartProduct += currentItem
        cartList.innerHTML = formattedSideBarCartProduct
    }
}

function handleRightSideBarCart(cart_response) {
    const cart_data = cart_response.cart_data;
    const cart_items = cart_response.cart_items;
    handleRightSideBarCartItemContent(cart_items);
    var totalProductCountMainHTML = document.getElementById("total-product-count-main-container");
    var totalProductCountMinHTML = document.getElementById("total-product-count-min-container");
    var subTotalContainer = document.getElementById("summary-table-sub_total");
    var taxContainer = document.getElementById("summary-table-tax");
    var grandTotalContainer = document.getElementById("summary-table-total");
    totalProductCountMainHTML.innerText = cart_data.total_product_quantity;
    totalProductCountMinHTML.innerText = cart_data.total_product_quantity;
    subTotalContainer.innerText = `# ${cart_data.sub_total_price}`;
    taxContainer.innerText = `# ${cart_data.tax}`;
    grandTotalContainer.innerText = `# ${cart_data.total_price}`;
}


function formatCartProductVariation(variation) {
    return `
    <tr class="Variation-table-row">
    <td>${variation.variation.size}</td>
    <td>
        <div class="input-group">
            <button class="btn btn-outline-primary js-btn-minus"
                type="button">
                &minus;
            </button>
            <input type="text" class="form-control text-center" value="${variation.quantity}"
                placeholder="" aria-label="Example text with button addon"
                aria-describedby="button-addon1">
            <button class="btn btn-outline-primary js-btn-plus"
                type="button">
                &plus;
            </button>
        </div>
    </td>
</tr>`;
}

function loopAndReturnVariation(variations) {
    const formattedVariations = variations.map(variation => formatCartProductVariation(variation));
    return formattedVariations.join('');

}

function formatCartTableRow(item) {
    console.log(item)
    let product = item.product;
    return `
    <tr>
    <th class="cart-product-thumbnail"><img style="width:80px;" src="${product.image}" class="img-fluid" alt=""></th>
    <th class="cart-product-name">
        <h2 class="h6 text-black">${product.name}</h2>
    </th>
    <td class="cart-product-total">$49.00</td>
    <td class="cart-product-total">$49.00</td>
    <td class="cart-product-total">$490000.00</td>
    <td class="cart-product-variation text-center">
        <table class="table Variation-table">
            <thead>
                <tr>
                    <th>Size</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            ${loopAndReturnVariation(item.cart_item_variation)}
            </tbody>
        </table>
    </td>
</tr>
    `;
}

function handleCartTableData(cartItems) {
    const cartTableBody = document.getElementById("cart-product-table-body");
    const formattedCartTableProducts = cartItems.map(item => formatCartTableRow(item));
    const formattedCartTable = formattedCartTableProducts.join('');
    cartTableBody.innerHTML = formattedCartTable; // Set innerHTML once after generating all rows
}

function handleCartPageData(cart_response) {
    handleCartTableData(cart_response.cart_items);
}

// // Example usage:
// const cartResponse = /* your cart response data */;
// handleCartPageData(cartResponse);


function getCartData() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/carts/get-data/true/");
    xhr.responseType = "json"
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const response = xhr.response
                handleRightSideBarCart(response)
                if (location.pathname === '/carts/') {
                    handleCartPageData(response)
                }
            }
        }
    }
    xhr.send()
}

getCartData();