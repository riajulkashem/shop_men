$(document).ready(function () {
    $('.formset-table').find('tr').find('td a.delete-row')[0].remove()
    let NOTIFICATION_TITLE = 'ShopMan';
    $('#sub_total').text(
        $('#id_sub_total').val()
    )

    function calculate_sub_total() {
        let sub_total = 0
        let form_number = $('#id_shopping_products-TOTAL_FORMS').val()
        let len = parseInt(form_number)
        let i;
        for (i = 0; i < len; i++) {
            let total = parseFloat($('input[name="shopping_products-' + i + '-total"]').val())
            if (total) {
                sub_total += total
            }
            
        }
        
        $('#sub_total').text(Math.round(sub_total))
        $('#id_sub_total').val(Math.round(sub_total))
        calculate_grand_total()
    }

    function calculate_charge() {
        let charge = $('#id_other_charge').val()
        let charge_type = parseInt(
            $('#id_other_charge_type').children("option:selected").text().replace(/[^0-9.]/g, "")
        )
        if (charge_type && charge) {
            let charge_tax = parseFloat((charge * charge_type) / 100) + parseFloat(charge)

            console.log('Charge Tax ', charge_tax, '  Charge ', charge)
            $('#id_charge_total').val(charge_tax)
            $('#other_charges').text(charge_tax)
        } else if(charge) {
            $('#id_charge_total').val(charge)
            $('#other_charges').text(charge)
        }else{
            $('#id_charge_total').val(0)
            $('#other_charges').text(0)
        }
        calculate_sub_total()
    }

    function calculate_discount() {
        let discount = parseInt($('#id_discount').val())
        let discount_type = $('#id_discount_type').children("option:selected").val()
        console.log(discount_type)
        if (discount_type === 'percentage' && discount) {
            let sub_total = $('#id_sub_total').val()
            $('#discount_on_all').text((discount * sub_total) / 100)
            $('#id_discount_total').val((discount * sub_total) / 100)
        } else if (discount) {
            let sub_total = $('#id_sub_total').val()
            $('#discount_on_all').text(discount)
            $('#id_discount_total').val(discount)
        } else {
            $('#discount_on_all').text(0)
            $('#id_discount_total').val(0)
        }
        calculate_charge()
    }


    function calculate_grand_total() {
        let sub_total = parseFloat($('#id_sub_total').val())
        let charge = parseFloat($('#id_charge_total').val())
        let discount = parseFloat($('#id_discount_total').val())
        
        let grand_total = (sub_total + charge) - discount
        $('#id_grand_total').val(grand_total)
        $('#grand_total').text(grand_total)
        let paid = parseFloat($('#id_paid').val())
        if (paid){
            $('#id_due').val(grand_total - paid)
            $('#due').text(grand_total - paid)
        }else {
            $('#id_due').val(grand_total)
            $('#due').text(grand_total)
        }
        
        
    }

    $('#id_other_charge').one('change keyup', function () {
        calculate_charge()
    })
    $('#id_other_charge_type').on('change', function () {
        calculate_charge()
    })
    $('#id_discount').on('change keyup', function () {
        calculate_discount()
    })
    $('#id_discount_type').one('change', function () {
        calculate_discount()
    })

    $('#id_paid').on('change keyup', function () {
        let grand_total = $('#id_grand_total').val()
        $('#id_paid').attr('max', grand_total)
        calculate_discount()
    })


    calculate_sub_total()
    calculate_discount()

    function init_plugin() {
        $('.datetimeinput').flatpickr(
            {
                enableTime: true,
                dateFormat: "Y-m-d H:i",
                defaultHour: new Date().getHours(),
                defaultMinute: new Date().getMinutes(),
                defaultDate: new Date()
            }
        )
        $('.dateinput').flatpickr(
            {
                enableTime: false,
                dateFormat: "Y-m-d",
            }
        )
        $('.timeinput').flatpickr(
            {
                enableTime: true,
                noCalendar: true,
                dateFormat: "H:i:s",
            }
        );


        $('a.delete-row').click(function () {
            index = 0
            $('.serial').each(function () {
                index += 1
                $(this).text(index)
                $('#id_quantity').val(index)
            })
            index = 0
           init_plugin()
           calculate_sub_total()
        })

        $('.product').change(function () {
            let product_id = $(this).val()
            let form_number = parseInt($(this).attr('name').replace(/[^0-9.]/g, ""));
            console.log('product Change Form number ', form_number)
            $.ajax({
                method: 'GET',
                url: '/product/product_details/' + product_id + '/',
                dataType: 'json',
                success: function (data) {
                    console.log(data)
                    if (data['error']) {
                        toastr.error(data['error'], NOTIFICATION_TITLE)
                    } else {
                        $('input[name="shopping_products-' + form_number + '-price"]').attr('min', data['sale_price']).val(data['sell_price'])
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    toastr.error(String(errorThrown), NOTIFICATION_TITLE)
                }
            });
        })

        function calculate_total(form_number) {
            let q = $('input[name="shopping_products-' + form_number + '-quantity"]').val()
            let price = $('input[name="shopping_products-' + form_number + '-price"]').val()
            let tax_type = $('select[name="shopping_products-' + form_number + '-tax_type"]').val()
            let tax = parseInt($('select[name="shopping_products-' + form_number + '-tax"]').children("option:selected").text().replace(/[^0-9.]/g, ""));
            let total = parseInt(q) * parseFloat(price)
            console.log('TAX Type ', tax_type, 'exclusive is ', tax_type === 'exclusive', ' TAX amount ', tax)
            if (tax_type === 'exclusive' && tax) {
                console.log('Calculating Tax')
                total += (total * parseInt(tax)) / 100
            }
            total = Math.round(total)
            $('input[name="shopping_products-' + form_number + '-total"]').val(total)
            calculate_sub_total()
        }

        $('.price').on('keyup change', function () {
            let form_number = parseInt($(this).attr('name').replace(/[^0-9.]/g, ""));
            calculate_total(form_number)
        })
        $('.quantity').on('keyup change', function () {
            let form_number = parseInt($(this).attr('name').replace(/[^0-9.]/g, ""));
            calculate_total(form_number)
        })
        $('.product_tax').change(function () {
            let form_number = parseInt($(this).attr('name').replace(/[^0-9.]/g, ""));
            calculate_total(form_number)
        })
        $('.total').on('keyup change', function () {
            let form_number = parseInt($(this).attr('name').replace(/[^0-9.]/g, ""));
            calculate_total(form_number)
        })
        $('.product_tax_type').change(function () {
            let form_number = parseInt($(this).attr('name').replace(/[^0-9.]/g, ""));
            calculate_total(form_number)
        })
    }

    init_plugin()
    let index = 0
    $('.serial').each(function () {
        index += 1
        $(this).text(index)
        $('#id_quantity').val(index)
    })
    index = 0

    $('.add-more').click(function () {
        $('select').select2({
            tags: true,
            placeholder: "Select an Option",
            allowClear: true,
            width: '100%',
        })
        $('.serial').each(function () {
            index += 1
            $(this).text(index)
            $('#id_quantity').val(index)
        })
        index = 0
        init_plugin()
    })
})