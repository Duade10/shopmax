function AddToCart(event) {
    let formDataDictionary = {}
    const addToCartForm = event.target

    const formData = new FormData(addToCartForm);
    for (var pair of formData.entries()) {
        formDataDictionary[pair[0]] = pair[1];
    }
    var data = JSON.stringify(formDataDictionary)
    let csrftoken = getCookie("csrftoken")
    toastr.info('Adding to cart')
    const xhr = new XMLHttpRequest();
    xhr.open("POST", '/api/carts/add-to-cart/');
    xhr.responseType = "json"
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            toastr.clear();
            toastr.success('Added successfully');
            getContextData();
            if (xhr.status === 201) {
            }
        }
    }
    xhr.send(data)
}


const wishlistHeart = document.getElementById("wishlist-heart");
wishlistHeart.addEventListener("click", (e) => {
    var productId = e.target.getAttribute("data-product-id");
    toastr.info("Checking wishlist");
    toggleWishlist(productId);
});

const addToCartForm = document.getElementById('add-to-cart-form')
addToCartForm.addEventListener('submit', (e) => {
    e.preventDefault();
    AddToCart(e);
})