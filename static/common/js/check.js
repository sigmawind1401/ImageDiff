// Webページ読込時の処理
window.addEventListener("load", function() {

    document.querySelector("#id_username").addEventListener("keyup", function(e) {
    // document.on('keyup', '#id_username', function(e){
        if(e.keyCode === 9 || e.keyCode === 16) return;
        this.value = this.value.replace(/[^0-9a-zA-Z]+/i,'');
    });
    
    document.querySelector("#id_username").addEventListener("blur", function(e) {
    // document.on('blur', '#id_username',function(){
        this.value = this.value.replace(/[^0-9a-zA-Z]+/i,'');
    });

});