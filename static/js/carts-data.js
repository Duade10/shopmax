function variationSizeList(variations) {
    var variation_list = []
    for (i = 0; i < variations.length; i++) {
        variation_list.push(variations[i].size)
    };
    return variation_list
}


function formatRightSideBarCartProduct(item, variations) {
    return `<div class="single-cart-item">
                <a href="/product/${item.slug}/" class="product-image">
                    <img src="${item.image}" class="cart-thumb" alt="">
                    <!-- Cart Item Desc -->
                    <div class="cart-item-desc">
                        <span class="product-remove"><i class="fa fa-close" aria-hidden="true"></i></span>
                        <span class="badge">${item.brand}</span>
                        <h6>${item.name}</h6>
                        <p class="size">Size: ${variationSizeList(variations)}</p>
                        <p class="price">#${item.price}</p>
                    </div>
                </a>
            </div>`
}

function handleRightSideBarCartItemContent(cart_items) {
    var cartList = document.getElementById("cart-list-container")
    var formattedSideBarCartProduct = ""
    console.log(cart_items.length)
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
                console.log(response)
                handleRightSideBarCart(response)
            }
        }
    }
    xhr.send()
}

getCartData();