window.addEventListener("load", function() {

    $('#modal0').on('show.bs.modal', function (event) {
    });

    $('#modal1').on('show.bs.modal', function (event) {
    });

    // $('#modal2').on('show.bs.modal', function (event) {

    //     var button = $(event.relatedTarget)
    //     var word = button.data('word')
    //     var comment = button.data('comment')
    //     var key = button.data('key')
    //     var modal = $(this)

    //     modal.find('.modal-body input[name="alertWord2"]').val(word)
    //     modal.find('.modal-body textarea').val(comment)
    //     modal.find('.modal-body input[name="key2"]').val(key)

    // });

    $('#modal3').on('show.bs.modal', function (event) {

        var button = $(event.relatedTarget)
        var word = button.data('word')
        var comment = button.data('comment')
        var key = button.data('key')
        var modal = $(this)

        modal.find('.modal-body input[name="alertWord3"]').val(word)
        modal.find('.modal-body textarea').val(comment)
        modal.find('.modal-body input[name="key3"]').val(key)

    });

    $('#modal4').on('show.bs.modal', function (event) {
    });

});