$(document).ready(function () {
    let slider = $('.form-range');
    $('.text-center').text(slider.val())
    slider.on('input', function (event) {
        let id = event.target.id;
        let value = $(this).val();
        $(`#${id}-value`).text(value);
    })
})