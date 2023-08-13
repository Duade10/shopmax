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
    <tr>
        <td class="cart-product-thumbnail"></td>
        <td class="cart-product-name"></td>
        <td class="cart-product-variation">
            ${variation.variation.size}
        </td>
        <td class="cart-product-quantity">
            <input type="number" class="form-control" value="1">
        </td>
        <td class="cart-product-total">$49.00</td>
        <td class="cart-product-action">
            <button class="btn btn-danger btn-sm">Remove</button>
        </td>
    </tr>`;
}

function loopAndReturnVariation(variations) {
    if (variations.length > 1) {
        const formattedVariations = variations.map(variation => formatCartProductVariation(variation));
        return formattedVariations.join('');
    } else {
        return ""
    }
}

function formatCartTableRow(item) {
    let product = item.product;
    let firstVariation = item.cart_item_variation[0]
    return `
    <tr>
    <td class="cart-product-thumbnail">
        <img src="${product.image}" alt="Image" class="img-fluid">
    </td>
    <td class="cart-product-name">
        <h2 class="h6 text-black">${product.name}</h2>
    </td>
    <td class="cart-product-variation">
        ${firstVariation.variation.size}
    </td>
    <td class="cart-product-quantity">
        <input type="number" class="form-control" value="1">
    </td>
    <td class="cart-product-total">$49.00</td>
    <td class="cart-product-action">
        <button class="btn btn-danger btn-sm">Remove</button>
    </td>
</tr>
        ${loopAndReturnVariation(item.cart_item_variation)}
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