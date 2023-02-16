// Webページ読込時の処理
window.addEventListener("load", function() {

    document.querySelector("#fade1").addEventListener("click", function() {

        // ターゲットフェードインフェードアウト
        $("#target1").fadeOut("slow", function(){ $("#target2").fadeIn("slow"); });
        $("#target3").fadeOut("slow", function(){ $("#target4").fadeIn("slow"); });
        $("#target5").fadeOut("slow", function(){ $("#target6").fadeIn("slow"); });
        $("#target7").fadeOut("slow", function(){ $("#target8").fadeIn("slow"); });
        $("#target9").fadeOut("slow", function(){ $("#target10").fadeIn("slow"); });

    });

    document.querySelector("#fade2").addEventListener("click", function() {

        // ターゲットフェードインフェードアウト
        $("#target10").fadeOut("slow", function(){ $("#target9").fadeIn("slow"); });
        $("#target8").fadeOut("slow", function(){ $("#target7").fadeIn("slow"); });
        $("#target6").fadeOut("slow", function(){ $("#target5").fadeIn("slow"); });
        $("#target4").fadeOut("slow", function(){ $("#target3").fadeIn("slow"); });
        $("#target2").fadeOut("slow", function(){ $("#target1").fadeIn("slow"); });

    });
});