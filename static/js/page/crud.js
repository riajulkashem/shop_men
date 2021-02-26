$(document).ready(function () {
    let NOTIFICATION_TITLE = 'EduCom';
    let searchParams = new URLSearchParams(window.location.search)
    if (searchParams.has('search')) $('#searchbar').val(searchParams.get('search'))

    function init_plugins() {
        // re init Function where data loaded via ajax
        $('select').select2({
            tags: true,
            placeholder: "Select an Option",
            allowClear: true,
            width: '100%',
            // dropdownParent: $('#crud_modal')
        });

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

    }

    init_plugins()

    function add_item(selector) {
        $(selector).click(function (e) {
            e.preventDefault()
            let data_type = 'json'
            let id = {'id': ''}
            let url = window.location.href
            ajax_html_load(id, url, data_type)
        })
    }

    function edit_item(selector) {
        $(selector).click(function (e) {
            e.preventDefault()
            let id = $(this).data('id')
            let url = "update/" + id + "/"
            let data_type = 'json'
            ajax_html_load({'id': id}, url, data_type)
        })
    }

    function delete_item(selector) {
        $(selector).click(function (e) {
            e.preventDefault()
            $(this);
            $('.prefix_text').text('Delete')
            let id = $(this).data('id')
            $('#object_name').text($(this).data('name'))
            let url = String(window.location.href + 'delete/' + id + '/').replace('#', '')
            console.log('URL = ', url)

            $('#confirm_delete').click(() => {
                $('#delete_modal').modal("hide");

                function remove_tr() {
                    window.location.reload()
                }

                ajax_post({'confirm_delete': true}, remove_tr, url)
            })
        });
    }

    function change_status(selector) {
        $(selector).click(function (e) {
            e.preventDefault()
            let id = $(this).data('id')
            let url = String(window.location.href + 'status/' + id + '/').replace('#', '')

            function change_status(data) {
                let status = $('#status_' + id)
                if (status.prop("checked") === true) {
                    status.prop('checked', false);
                } else {
                    status.prop('checked', true);
                }
            }

            ajax_post({'status': $(this).val()}, change_status, url)
        })
    }

    function login_to_user(selector) {
        $(selector).click(function (e) {
            e.preventDefault()
            let id = $(this).data('user_id')

            console.log('requesting authorisation for user_id', id)

            function goto_dashboard(data) {
                if (data['success']) window.location.assign(window.location.origin)
            }

            ajax_post({'id': id}, goto_dashboard, '/user/sign_in/')
        })
    }

    add_item('#add_button')
    edit_item('.edit')
    delete_item('.delete')
    change_status('.status')
    login_to_user('.login_as_user')


    let infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        onBeforePageLoad: function () {
            $('.loading').show();
            console.log('onBeforePageLoad On Loading Data...')
        },
        onAfterPageLoad: function ($items) {
            $('.loading').hide();
            console.log('onAfterPageLoad On Loading Data...');
            $items.each(function () {
                add_item($(this).find('#add_button'))
                edit_item($(this).find('.edit'))
                delete_item($(this).find('.delete'))
                change_status($(this).find('.status'))
                login_to_user($(this).find('.login_as_user'))
                init_plugins()
            })
        }
    });

    function ajax_html_load(id, url, data_type) {
        console.log('url = ', url)
        if (data_type !== null) {
            $.ajax({
                method: 'GET',
                url: url,
                dataType: 'json',
                success: function (data) {
                    console.log(data)
                    if (data['error']) {
                        toastr.error(data['error'], NOTIFICATION_TITLE)
                        $('#crud_modal').close();
                    } else {
                        $('#modal-content').html(data['html_form'])
                        $('#crud_modal').modal("show");
                        init_plugins()
                    }

                },
                error: function (jqXHR, textStatus, errorThrown) {
                    toastr.error(String(errorThrown), NOTIFICATION_TITLE)
                    $('#crud_modal').close();
                }
            });
        } else {
            $.ajax({
                method: 'GET',
                url: url,
                data: {'id': id},
                success: function (data) {
                    console.log(data)
                    if (data['error']) toastr.error(data['error'], NOTIFICATION_TITLE)
                    else {
                        $('#modal-content').html(data['html_form'])
                        $('#crud_modal').modal("show");
                        init_plugins()
                    }

                },
                error: function (jqXHR, textStatus, errorThrown) {
                    toastr.error(String(errorThrown), NOTIFICATION_TITLE)
                    $('#crud_modal').close();
                }
            });
        }
    }

    function ajax_post(sendData, successTodo, url) {
        sendData['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val()
        $.ajax({
            type: "POST",
            url: url,
            data: sendData,
            success: function (data) {
                if (data['error']) {
                    toastr.error(data['error'], NOTIFICATION_TITLE)
                    $('#crud_modal').modal('hide');
                } else {
                    toastr.success(data['success'], NOTIFICATION_TITLE)
                    successTodo(data)
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                toastr.error(errorThrown, NOTIFICATION_TITLE)
                $('#crud_modal').modal('hide');
            }
        });
    }

    function ajax_load(sendData, url, selector) {
        $.ajax({
            method: 'GET',
            url: url,
            data: sendData,
            success: function (data) {
                console.log(data)
                if (data['error']) {
                    toastr.error(data['error'], NOTIFICATION_TITLE)
                } else {
                    $(selector).html(data['html_options'])
                    $('select').select2({
                        tags: true,
                        placeholder: "Select an Option",
                        allowClear: true,
                        width: '100%',
                    });
                }

            },
            error: function (jqXHR, textStatus, errorThrown) {
                toastr.error(String(errorThrown), NOTIFICATION_TITLE)
            }
        });
    }


})