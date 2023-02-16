$('#sendForm').click(function() {
    canvas = document.getElementById('sendImage');
    $('form input[name=imgData]').val(canvas.toDataURL("image/jpeg", 1));
    $('form').submit();
});