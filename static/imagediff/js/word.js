window.addEventListener("load", function() {

    $('#modal0').on('show.bs.modal', function (event) {
    });

    $('#modal1').on('show.bs.modal', function (event) {
    });

    $('#modal2').on('show.bs.modal', function (event) {
    });

    $('#modal3').on('show.bs.modal', function (event) {

        var button = $(event.relatedTarget)
        var before = button.data('before')
        var after = button.data('after')
        var key = button.data('key')
        var modal = $(this)

        modal.find('.modal-body input[name="wordBefore3"]').val(before)
        modal.find('.modal-body input[name="wordAfter3"]').val(after)
        modal.find('.modal-body input[name="key3"]').val(key)

    });

    $('#modal4').on('show.bs.modal', function (event) {
    });

});