function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function formatRightSideBarCartProduct(item, cart_item_variation, cartItemId) {
    var sizeHTML = cart_item_variation.map(crt => ` ${crt.variation.size}`).join(',');

    return `
        <div class="single-cart-item">
            <a class="product-image">
                <img src="${item.image}" class="cart-thumb" alt="">
                <!-- Cart Item Desc -->
                <div class="cart-item-desc">
                    <span style="cursor:pointer;" class="product-remove">
                        <i data-product-id="${cartItemId}" class="fa fa-close product-remove" aria-hidden="true"></i>
                    </span>
                    <span class="badge">${item.brand}</span>
                    <h6 style="cursor:pointer;" class="product-name" data-product-slug="${item.slug}">${item.name}</h6>
                    <p class="size"><span>Size: </span>${sizeHTML}</p>
                    <p class="price">#${item.price}</p>
                </div>
            </a>
        </div>
    `;
}


function handleRightSideBarCartItemContent(cart_items) {
    var cartList = document.getElementById("cart-list-container");
    var formattedSideBarCartProduct = "";

    for (i = 0; i < cart_items.length; i++) {
        var cartItemId = cart_items[i].id;
        var cartProduct = cart_items[i].product;
        var cartItemVariation = cart_items[i].cart_item_variations;
        var currentItem = formatRightSideBarCartProduct(cartProduct, cartItemVariation, cartItemId);
        formattedSideBarCartProduct += currentItem;
    }

    cartList.innerHTML = formattedSideBarCartProduct;
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

const cartListContainer = document.getElementById("cart-list-container");
cartListContainer.addEventListener("click", e => {
    if (e.target.classList.contains("product-name")) {
        let slug = e.target.getAttribute("data-product-slug");
        window.location.replace(`/product/${slug}/`);
    }
    else if (e.target.classList.contains("product-remove")) {
        let productId = e.target.getAttribute("data-product-id")
        deleteCartItem(productId)
    }
});

function deleteCartItem(productId) {
    const xhr = new XMLHttpRequest();
    xhr.open("DELETE", `/api/carts/delete-cart-item/${productId}/`);
    xhr.responseType = "json"
    let csrftoken = getCookie("csrftoken");
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                handleRightSideBarCart(xhr.response)
                if (window.location.pathname === '/carts/') {
                    getCartData();
                }
            }
        }
    }
    xhr.send()
}

// // Example usage:
// const cartResponse = /* your cart response data */;
// handleCartPageData(cartResponse);

function toggleWishlist(product_id) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", `/api/wishlist/toggle/${product_id}/`);
    xhr.responseType = "json";
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                const response = xhr.response
                let message = response.message
                toastr.success(message)

            } else if (xhr.status === 200) {
                const response = xhr.response
                let message = response.message
                toastr.warning(message)
            }
        }
    }
    xhr.send();

}


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

