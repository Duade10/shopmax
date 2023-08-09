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

function AddToCart(event) {
    event.preventDefault();
    let formDataDictionary = {}
    const new_event = event
    console.log(new_event)
    const addToCartForm = event.target
    console.log(addToCartForm)

    const formData = new FormData(addToCartForm);
    for (var pair of formData.entries()) {
        formDataDictionary[pair[0]] = pair[1];
    }
    var data = JSON.stringify(formDataDictionary)
    console.log(data)
    let csrftoken = getCookie("csrftoken")
    const xhr = new XMLHttpRequest();
    xhr.open("POST", '/api/carts/add-to-cart/');
    xhr.responseType = "json"
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = xhr.response
            console.log(response)
        }
    }
    xhr.send(data)
}

const addToCartForm = document.getElementById('add-to-cart-form')
addToCartForm.addEventListener('submit', AddToCart)

