function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// function AddToCart(event) {
//     event.preventDefault();
//     let formDataDictionary = {}
//     const new_event = event
//     const addToCartForm = event.target

//     const formData = new FormData(addToCartForm);
//     for (var pair of formData.entries()) {
//         formDataDictionary[pair[0]] = pair[1];
//     }
//     var data = JSON.stringify(formDataDictionary)
//     let csrftoken = getCookie("csrftoken")
//     const xhr = new XMLHttpRequest();
//     xhr.open("POST", '/api/carts/add-to-cart/');
//     xhr.responseType = "json"
//     xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
//     xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
//     xhr.setRequestHeader("Content-Type", "application/json")
//     xhr.setRequestHeader("X-CSRFToken", csrftoken)
//     xhr.onload = () => {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             const response = xhr.response;
//             getCartData();
//             if (xhr.status === 201) {
//             }
//         }
//     }
//     xhr.send(data)
// }

// const addToCartForm = document.getElementById('add-to-cart-form')
// addToCartForm.addEventListener('submit', AddToCart)

function decreaseCartQuantity(variation_id) {
    console.log("decreaseCartQuantity: ", variation_id)
}

function formatCartProductVariation(variation) {
    return `
    <tr class="Variation-table-row">
    <td>${variation.variation.size}</td>
        <td>
            <div class="input-group">
                <button class="btn btn-outline-primary js-btn-minus" data-action="decrease" data-variation-id="${variation.id}" type="button">
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

const cartBody = document.getElementById("cart-product-table-body");
cartBody.addEventListener('click', (e) => {
    if (e.target.tagName === "BUTTON") {
        if (e.target.getAttribute("data-action") === "decrease") {
            const variationId = e.target.getAttribute("data-variation-id")
            decreaseCartQuantity(variationId)
        }
    }
})

function loopAndReturnVariation(variations) {
    const formattedVariations = variations.map(variation => formatCartProductVariation(variation));
    return formattedVariations.join('');

}

function formatCartTableRow(item) {
    let product = item.product;
    return `
    <tr>
    <th class="cart-product-thumbnail"><img style="width:80px;" src="${product.image}" class="img-fluid" alt=""></th>
    <th class="cart-product-name">
        <h2 class="h6 text-black">${product.name}</h2>
    </th>
    <td class="cart-product-total">#${product.price}</td>
    <td class="cart-product-total">${item.total_quantity}</td>
    <td class="cart-product-total">#${item.sub_total}</td>
    <td class="cart-product-variation text-center">
        <table class="table Variation-table">
            <thead>
                <tr>
                    <th>Size</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            ${loopAndReturnVariation(item.cart_item_variations)}
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
    cartTableBody.innerHTML = formattedCartTable;
}



function getCartData() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/carts/get-cart-item-list/");
    xhr.responseType = "json"
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const response = xhr.response
                handleCartTableData(response)

            }
        }
    }
    xhr.send()
}

getCartData();