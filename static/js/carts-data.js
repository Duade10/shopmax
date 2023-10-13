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
        var cartItemVariation = cart_items[i].cart_item_variations
        var currentItem = formatRightSideBarCartProduct(cartProduct, cartItemVariation)
        formattedSideBarCartProduct += currentItem
        cartList.innerHTML = formattedSideBarCartProduct
    }
}

function handleRightSideBarCart(data) {
    const context_data = data.context_data;
    const cart_items = data.cart_items;
    handleRightSideBarCartItemContent(cart_items);
    var totalProductCountMainHTML = document.getElementById("total-product-count-main-container");
    var totalProductCountMinHTML = document.getElementById("total-product-count-min-container");
    var subTotalContainer = document.getElementById("summary-table-sub_total");
    var taxContainer = document.getElementById("summary-table-tax");
    var grandTotalContainer = document.getElementById("summary-table-total");
    totalProductCountMainHTML.innerText = context_data.total_quantity;
    totalProductCountMinHTML.innerText = context_data.total_quantity;
    subTotalContainer.innerText = `# ${context_data.sub_total}`;
    taxContainer.innerText = `# ${context_data.tax}`;
    grandTotalContainer.innerText = `# ${context_data.grand_total}`;
}


// // Example usage:
// const cartResponse = /* your cart response data */;
// handleCartPageData(cartResponse);


function getContextData() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/carts/context-data/");
    xhr.responseType = "json"
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const response = xhr.response
                handleRightSideBarCart(response)
            }
        }
    }
    xhr.send()
}

getContextData();

