// Webページ読込時の処理
window.addEventListener("load", function() {

    $('#modal0').on('show.bs.modal', function (event) {
    });

    $('#switch').on('click', function () {
        $('.result1').toggle();
        $('.result2').toggle();
    });

    // document.querySelector("#viewDialog").addEventListener("click", function() {

    //     // 確認ダイアログ表示    
    //     $("#dialog").dialog({
    //     modal: true,
    //     title: "文字数設定",
    //     width: "auto",
    //     height: "auto",
    //     buttons: {
    //         "OK": function() {
    //         $(this).dialog("close");
    //         $('form input[name=config]').val($("#condLength").val());
    //         document.querySelector("#config").click();
    //         }
    //     }
    //     });
    // });
});
