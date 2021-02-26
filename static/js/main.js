$(document).ready(() => {
    // Active Menu Class
    let url = window.location;
    let element = $('ul.navigation-main a').filter(function () {
        return this.href === url || url.href.indexOf(this.href) === 0;
    });

    $(element).toString().replace('#', '')
    $(element).closest('a').addClass('active');
    $(element).parentsUntil('ul.navigation-main', 'li').addClass('open');

    $('.timeinput').flatpickr({
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i:s",
    });

    if (document.formHasErrors) {
        $('#crud_modal').modal('show');
    }
    $('select').select2({
        tags: true,
        placeholder: "Select an Option",
        allowClear: true,
        width: '100%',
    });

})