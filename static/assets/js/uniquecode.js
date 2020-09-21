    function uniquecode(){
        $.ajax({
            url:'/customersmacid/',
            dataType:'json',
            success: function(data){
                sidecart()
            }
        });
    }
    function sidecart(){
        $.ajax({
            url:'/sidecart/',
            dataType:'json',
            success: function(data){
                var container = `<a href="#" class="dropdown-toggle" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-display="static">
                                <i class="icon-shopping-cart"></i>
                                <span class="cart-count">${data.count}</span>
                                <span class="cart-txt">$${data.price}</span>
                                </a>
                                <div class="dropdown-menu dropdown-menu-right">`
                var last = `<div class="dropdown-cart-total">
                                    <span>Total</span>

                                    <span class="cart-total-price">$${data.price}</span>
                                </div>

                                <div class="dropdown-cart-action">
                                    <a ></a>
                                    <a href="checkout.html" class="btn btn-outline-primary-2"><span>View Cart</span><i class="icon-long-arrow-right"></i></a>
                                </div><!-- End .dropdown-cart-total -->
                            </div>`
                for(var i=0; i<data.lists.length; i++){
                        var info = `
                                        <div class="dropdown-cart-products">
                                            <div class="product">
                                                <div class="product-cart-details">
                                                    <h4 class="product-title">
                                                        <a href="/productsingle/?id2=${data.lists[i].productid}">${data.lists[i].name}</a>
                                                    </h4>
                                                    <span class="cart-product-info">
                                                        <span class="cart-product-qty"></span>
                                                         ${data.lists[i].size}
                                                    </span>
                                                    <br>
                                                    <span class="cart-product-info">
                                                        <span class="cart-product-qty"></span>
                                                         $${data.lists[i].price}
                                                    </span>
                                                </div><!-- End .product-cart-details -->

                                                <figure class="product-image-container">
                                                    <a href="/productsingle/?id2=${data.lists[i].productid}" class="product-image">
                                                        <img src="${data.lists[i].link}" alt="product">
                                                    </a>
                                                </figure>
                                                <a href="#" class="btn-remove" title="Remove Product"><i class="icon-close"></i></a>
                                            </div>
                                        </div>`
                        container += info
                }
                $('#sidecart').append(container+last)
            }
        })
    }

