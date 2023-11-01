const getPage = (number) => {
    let paginationURL = localStorage.getItem("paginationUrl");
    console.log('paginationURL: ', paginationURL)
    console.log('location.href: ', window.location)
    let url;
    if (paginationURL === 'null') {
        url = `${location.origin}/api/shop/get-products/?page=${number}`;
    } else {
        url = `${paginationURL}&page=${number}`;
    }
    let formData = null;
    getProducts(url, formData);
}

const handlePagination = (pagination) => {
    var formattedPagination = " ";
    var paginationContainer = document.getElementById("pagination");
    if (pagination.has_previous === true) {
        formattedPagination += `<li class="page-item"><a class="page-link" onclick="getPage(${parseInt(pagination.current_page_number) - 1})"><i class="fa fa-angle-left"></i></a></li>`;
    }
    for (i = 0; i <= pagination.number_of_pages; i++) {

        if (i !== 0) {

            if ((pagination.current_page_number - 2) === i) {
                formattedPagination += `<li class="page-item"><a class="page-link" onclick="getPage(${i})">${i}</a></li>`
            }
            if ((pagination.current_page_number - 3) === i) {
                formattedPagination += `<li class="page-item"><a class="page-link" onclick="getPage(${i})">${i}</a></li>`
            }
            if (pagination.current_page_number === i) {
                formattedPagination += `<li class="page-item active"><a class="page-link active">${pagination.current_page_number}</a></li>`
            }

            if ((pagination.current_page_number + 2) === i) {
                formattedPagination += `<li class="page-item"><a class="page-link" onclick="getPage(${i})">${i}</a></li>`
            }
            if ((pagination.current_page_number + 3) === i) {
                formattedPagination += `<li class="page-item"><a class="page-link" onclick="getPage(${i})">${i}</a></li>`
            }
        }
    }
    if (pagination.has_next === true) {
        formattedPagination += `<li class="page-item"><a class="page-link" onclick="getPage(${parseInt(pagination.current_page_number) + 1})"><i class="fa fa-angle-right"></i></a></li>`;
    }
    paginationContainer.innerHTML = formattedPagination;

}

function isNew(product) {
    const productTimestamp = product.created_at;
    const productDate = new Date(productTimestamp);
    const today = new Date();
    const diffInDays = Math.ceil((today - productDate) / (1000 * 60 * 60 * 24));
    if (diffInDays > 3) {
        if (product.discounted_percentage === null) {
            return ``
        }
        else {
            return `<div class="product-badge new-badge">-${product.discounted_percentage}%</div>`
        }
    } else {
        return `<div class="product-badge new-badge">New</div>`;
    }
}
function formatShopProducts(product) {
    const isInWishlist = (input) => (input === true ? 'active' : '');
    var value = isInWishlist(product.is_in_wishlist);
    return `<div div class="col-12 col-sm-6 col-lg-4" >
            <div class="single-product-wrapper">
                <div class="product-img">
                    <img src="${product.image}" alt="${product.slug}">

                        <img class="hover-img" src="${product.hover_image_url}" alt="">
                            ${isNew(product)}
                            <div class="product-favourite">
                                <a data-product-id="${product.id}" class="favme fa fa-heart ${value}"></a>
                            </div>
                        </div>
                        <div class="product-description">
                            <span>${product.brand}</span>
                            <a href="/product/${product.slug}/">
                                <h6>${product.name}</h6>
                            </a>
                            <p class=" product-price">
                                <span class="old-price">#${product.discounted_price}</span>
                                ${product.price}
                            </p>
                        </div>
                </div>
            </div> `
};

function getSingleProduct(data) {
    let productList = data;
    var productListContainer = document.getElementById("product_row");
    var productCountSpan = document.getElementById("product-count");
    if (productList.length > 0) {
        var finishedProducts = "";
        for (var i = 0; i < productList.length; i++) {
            var singleProduct = productList[i];
            var formattedShopProduct = formatShopProducts(singleProduct);
            finishedProducts += formattedShopProduct
            productListContainer.innerHTML = finishedProducts;
            productCountSpan.innerText = `${productList.length} products count`;

        }
    }
    else if (productList.length === 0) {
        productCountSpan.innerText = productList.length;
        productListContainer.innerHTML = `<h3> Oops! No Product matches this filter </h3> `
    }

}

function handleWishlistToggle(event) {
    const clickedElement = event.target;
    if (clickedElement.classList.contains("favme")) {
        const productId = clickedElement.getAttribute("data-product-id");
        toastr.info("Checking wishlist");
        toggleWishlist(productId);
        clickedElement.classList.toggle("active");

    }
}

const productRow = document.getElementById("product_row");
productRow.addEventListener("click", handleWishlistToggle);




function getProducts(url, formData) {
    $.ajax({
        type: 'GET',
        url: url,
        data: formData,
        dataType: 'json',
        success: function (response) {
            getSingleProduct(response.products);
            localStorage.setItem("paginationUrl", response.pagination.pagination_url);
            handlePagination(response.pagination);

        }
    })
}

$(document).ready(function () {
    let url = '/api/shop/get-products/';
    let formData = null;
    inWishlistData = localStorage.getItem("in-wishlist-data");
    subcategory_data = localStorage.getItem('shop-button-data');
    if (subcategory_data != null) {
        formData = subcategory_data;
        localStorage.removeItem('shop-button-data');
    }
    getProducts(url, formData);

    $('#filter-form').submit(function (event) {
        event.preventDefault();
        var formData = $(this).serialize();
        let url = '/api/shop/get-products/';
        getProducts(url, formData);

    })
})

