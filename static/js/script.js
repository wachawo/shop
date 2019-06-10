$(document).ready(function() {
   console.log('loaded.');
   var cart_sum = getCookie("CART_SUM");
   if (cart_sum != "") {
       $('#cart_sum').text(cart_sum);
   }
});

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function getCookie(cname) {
    var r = document.cookie.match("(^|;) ?" + cname + "=([^;]*)(;|$)");
    if (r) return r[2];
    else return "";
}
function deleteCookie(cname) {
    var date = new Date(); // Берём текущую дату
    date.setTime(date.getTime() - 1); // Возвращаемся в "прошлое"
    document.cookie = cname += "=; expires=" + date.toGMTString(); // Устанавливаем cookie пустое значение и срок действия до прошедшего уже времени
}

function productAddToCart(product_id) {
    console.log('productAddToCart ' + product_id);
    var proto = window.location.protocol;
    var host = window.location.hostname;
    var port = window.location.port;
    var url = proto + '//' + host + ':' + port + '/cart/product/';
    console.log(url);
    $.ajax({
        type: 'POST',
        url: url,
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {'product_id': product_id},
        async: true,
        success: function (data) {
            console.log('success: ' + data);
            $('#cart_sum').text(data);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function productDeleteFromCart(product_id) {
    console.log('productDeleteFromCart ' + product_id);
    var proto = window.location.protocol;
    var host = window.location.hostname;
    var port = window.location.port;
    var url = proto + '//' + host + ':' + port + '/cart/product/';
    console.log(url);
    $.ajax({
        type: 'DELETE',
        url: url,
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {'product_id': product_id},
        async: true,
        success: function (data) {
            console.log('success: ' + data);
            if (data == 0) {
                // При удалении последнего товара из корзины
                window.location.reload();
            } else {
                $('#cart_sum').text(data);
                $('tr.' + product_id).remove();
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

$("#invoice_submit").click(function(){
    var name = $('#invoice .name').val();
    var phone = $('#invoice .phone').val();
    var proto = window.location.protocol;
    var host = window.location.hostname;
    var port = window.location.port;
    var url = proto + '//' + host + ':' + port + '/invoice/';
    console.log(url);
    $.ajax({
        type: 'POST',
        url: url,
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'name': name,
            'phone': phone
        },
        async: true,
        success: function (data) {
            console.log('success: ' + data);
            $('#cart_sum').text(0);
            $('#work').html("Номер заказа: <b>" + data + "</b>");
        },
        error: function (data) {
            console.log(data);
            $('#error').text("Ошибка");
        }
    });
});