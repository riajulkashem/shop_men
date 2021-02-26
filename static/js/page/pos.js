$(document).ready(function () {
    var shop_name = $('#userInfo').data('shop');
    var address = $('#userInfo').data('address');
    var phone = $('#userInfo').data('phone');
    var email = $('#userInfo').data('email');
    var customer_name = ''
    var invoiceBiller = $('#userInfo').data('biller');
    $('#paymentBtn').click(function () {
        total = $('#total').text();
        customer = $('#customer').children("option:selected").val();
        customer_name = $('#customer').children("option:selected").text();
        items = $('#total_qt').text();
        discount = $('#discount').val();
        netTotal = $('#amount').text();
        payment = $('#payment').children("option:selected").val();
        paid = $('#total_paid').val();
        due = parseInt(total) - parseInt(paid);
        status = '';
        if (parseInt(paid) === 0) {
            status = 'due';
        } else if (parseInt(due) === 0) {
            status = 'paid';
        } else {
            status = 'partial';
        }
        let product_info = new Array() ;
        prod = '';
        // All Product ID Storing into product_info[]
        $('tbody#productRow').find('tr').each(function () {
            var name = $(this).find('.productName').text();
            var id = $(this).find('.productName').attr('idnt');
            var stock = $(this).find('.qt').attr('max');
            var qt = $(this).find('.qt').val();
            var up = $(this).find('.unit_price').val();
            var st = $(this).find('.subTotal').text();
            product_info.push(
                {'quantity':qt, 'stock':stock, 'price':up, 'total':st, 'product_id':id}
            );
            prod += '<tr style="border-bottom:1px solid #000;"><td>' 
            + name + '</td><td>' + qt + '</td><td>' + up + '</td><td>'
             + st + '</td></tr>';
        });

        if (payment == '' || paid == 0 || product_info.length <= 0) {
            swal("Check Missing Input", "You may forget to select product or payment", {
                icon: "warning",
                buttons: {
                    confirm: {
                        className: 'btn btn-warning'
                    }
                },
            });
        } else if (customer == 0 && netTotal != paid) {
            swal("Walk in customer should paid fully", {
                icon: "warning",
                buttons: {
                    confirm: {
                        className: 'btn btn-warning'
                    }
                },
            });
        } else {
            data = {
                'people_id':customer, 'quantity':items,
                 'discount_total':discount, 'grand_total': total, 
                 'payment_type_id':payment, 'paid':paid, 'due':due,
                  'items':JSON.stringify(product_info), 'status':status,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            };
            console.log(data)
            var URL = window.location.href;
            // if (customer == 'walk-in-customer') { URL += '/sale/pos/'; }
            // else { URL += '/sale/add/'; }
            $.ajax({
                method: "POST",
                url: URL,
                data: data,
                success: function (pk) {
                    customer_name
                    var d = new Date();
                    var Html = '<div id="invoice-POS"><div style="text-align: center; max-width: 250px; margin:0 auto; border:1px solid"><h4 style="margin:0;"><strong>' + shop_name + '</strong></h4><p style="margin: 0;font-size: 12px;">Address:' + address + ' <br>Email: ' + email + ' <br>Phone: ' + phone + ' <br></p><hr><p style="margin: 0;font-size: 12px;">Invoice ID: <strong>' + pk.pk + '</strong><br>Date: <strong>' + d.getDate() + "-" + (d.getMonth() + 1) + "-" + d.getFullYear() + " " + d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds() + '</strong><br>Biller: <strong>' + invoiceBiller + '</strong><br>'
if(customer_name !== '') Html += 'Customer: <strong>' + customer_name + '</strong><br>'
                    Html +='</p><hr><table  style="font-size: 12px; margin: 0 auto; max-width: 250px;"><thead><tr style="border-bottom:1 px solid;"><th>Item</th><th>Qty</th><th>Price</th><th>Total</th> </tr></thead><tbody>' + prod + '</tbody><tfoot><tr style="border-bottom:1px solid #000;"><th colspan="3">Total</th><th>' + total + '</th> </tr><tr style="border-bottom:1px solid #000;"><th colspan="3">Discount</th><th>' + discount + '</th></tr><tr style="border-bottom:1px solid #000;"><th colspan="3">Net Total</th><th>' + netTotal + '</th></tr><tr style="border-bottom:1px solid #000;"><th colspan="3">Paid</th><th>' + paid + '</th></tr></tfoot></table><hr><p style="margin: 0 auto; font-size: 10px;">A Software By ROYAL IT LTD. <br>+880 1777824258<br> riajulkashem@gmail.com</p></div></div>';

                    var a = window.open('', '', 'width = 600, height = 1000');
                    a.document.write('<html><title>ROYAL IT POS Invoice</title><style>table, th, td {border: 1px solid black;border-collapse: collapse;}</style>');
                    a.document.write('<body>' + Html + '</body></html>');
                    a.document.close();
                    a.print();
                    window.location.reload();
                },
                error: function (error) { alert(error); }
            });

        }
    });
    // Filter Product By Category
    $('#category').on('change', function () {
        var cat = $(this).val();
        all_product = document.getElementById("all-product");
        product = all_product.getElementsByClassName('col-md-3');

        // Loop through all product list items, and hide those who don't match the search query
        for (i = 0; i < product.length; i++) {
            product_cat = product[i].getElementsByClassName("category")[0];
            value = product_cat.textContent || product_cat.innerText;
            if (value == cat || cat == 'all') {
                product[i].style.display = "";
            } else {
                product[i].style.display = "none";
            }
        }
    });

    // Add Product For Sale
    $('.product').click(function () {
        var name = $(this).find('.name').text();
        var quantity = $(this).find('.quantity').text();
        var price = $(this).find('.price').text();
        var buy_price = $(this).data('buy')
        var id = $(this).find('.name').data('id');
        if (quantity == 0) {
            swal("Product Out of Stock!", {
                icon: "warning",
                buttons: {
                    confirm: {
                        className: 'btn btn-warning'
                    }
                },
            });
        } else {
            code = '<tr class="textFormate"><td class="productName" id = "name' + id + '" idnt="' + id + '">' + name + '</td><td><input type="number" max="' + quantity + '" id="quantity' + id + '" style="width: 50%" class="qt" idnt="' + id + '" value="1"></td><td><input type="number" min="' + buy_price + '" id="unit_price' + id + '" class="unit_price" idnt="' + id + '" style="width: 50%" value="'+price+'"></td><td id="sub_total' + id + '" class="subTotal" idnt="' + id + '">' + price + '</td><td><span class="btn btn-sm btn-danger delete"><i class="fa fa-trash"></i></span></td></tr>';

            var productExist = false;
            $('.productName').each(function () {
                if ($(this).attr('idnt') == id) { productExist = true; }
            });
            if (productExist) {
                pq = parseInt($('#quantity' + id).val());
                if (quantity == pq) {
                    swal("Product Out of Stock!", {
                        icon: "warning",
                        buttons: {
                            confirm: {
                                className: 'btn btn-warning'
                            }
                        },
                    });
                } else {
                    $('#quantity' + id).val(pq + 1);
                }
                rowUpdate(id);
            } else {
                $('#productRow').append(code);
                rowUpdate(id);
            }
        }
    });

    // Add New Customer
    $('a.addPeople').click(function () {
        url = window.location.origin;
        url += '/sale/add/customer/';
        var input = $("<input>").attr("type", "hidden").attr("name", "pos").val("pos");
        $('form').append(input);
        $('form').attr('action', url);
    });

    // Search Product
    $('#search').on('keyup', function () {
        searchProduct();
    });
    // Search Products
    function searchProduct() {
        // Declare variables
        var input, filter, all_product, product, product_name, i, txtValue;
        input = document.getElementById('search');
        filter = input.value.toUpperCase();
        all_product = document.getElementById("all-product");
        product = all_product.getElementsByClassName('col-md-6');

        // Loop through all product list items, and hide those who don't match the search query
        for (i = 0; i < product.length; i++) {
            product_name = product[i].getElementsByTagName("p")[0];
            txtValue = product_name.textContent || product_name.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                product[i].style.display = "";
            } else {
                product[i].style.display = "none";
            }
        }
    }

    // Update Product Price
    function rowUpdate(id) {
        q = parseFloat($('#quantity' + id).val());
        up = parseFloat($('#unit_price' + id).val());
        q = q * up;
        $('#sub_total' + id).text(q);
        grandTotal();
    }

    $('body').on('mousedown', '.qt', function () {
        var id = $(this).attr('idnt');
        var max = $(this).attr('max');
        $(this).on('keyup change', function () {
            var value = $(this).val();
            if ((value !== '') && (value.indexOf('.') === -1)) {
                $(this).val(Math.max(Math.min(value, max), -max));
                rowUpdate(id);
            }
        });
    });

    $('body').on('mousedown', '.unit_price', function () {
        var id = $(this).attr('idnt');
        var min = $(this).attr('min');
        $(this).on('keyup kedown', function () {
            var value = $(this).val();
            if (value < min) $(this).val(min)
            if ((value !== '') && (value.indexOf('.') === -1)) {
                rowUpdate(id);
            }
        });
    });

    $('#discount').on('keyup', function () {
        t = $('#total').text();
        d = $('#discount').val();
        if (d != '') {
            d = t - d;
            $('#amount').text(d);
            $('#total_paid').val($('#amount').text());
        }
    });
    function grandTotal() {
        var t = 0;
        $('.subTotal').each(function () {
            t += parseFloat($(this).text());
        });
        $('#total').text(t);
        d = $('#discount').val();
        d = t - d;
        $('#amount').text(d);
        $('#total_paid').val($('#amount').text());

        t = 0;
        $('.qt').each(function () {
            t += parseFloat($(this).val());
        });
        $('#total_qt').text(t);
    }
    $(document).on("click", '.delete', function () {
        $(this).closest('tr').remove();
        grandTotal();
    });


});