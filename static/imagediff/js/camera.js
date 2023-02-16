// 画面サイズに合わせてvideoサイズを変更
function chgSize() {

  // 定数
  const video = document.querySelector("#camera");
  const shutter = document.querySelector("#shutter");

  // videoサイズ変更
  video.width = shutter.offsetWidth;
  video.height = shutter.offsetHeight;

}

// リサイズ時の処理
window.addEventListener("resize", chgSize);

// Webページ読込時の処理
window.addEventListener("load", function() {

  // 定数
  const video = document.querySelector("#camera");
  const reviewImage = document.querySelector("#reviewImage");
  // const sendImage1 = document.querySelector("#sendImage1");
  // const sendImage2 = document.querySelector("#sendImage2");
  const shutter = document.querySelector("#shutter");
  const facingMode = document.querySelector("input[name='facingMode']").value;
  const send = document.querySelector("button[name='send']");
  const constraints = {
    audio: false,
    video: {
        width: { ideal: 1280 },  // TEXT_DETECTIONの推奨画像サイズ[1024x768]より高く設定
        // facingMode: { exact: "environment" }
    }
  };

  if (facingMode == "True") {
    constraints.video.facingMode = { exact: "environment" };
  }

  // 変数
  let ctx = null;
  let step = 1;
  let sendImage = null;
  let dl = document.querySelector("#download");
  let date = null;
  let fileName = null;
  
  // ビデオに属性付与
  video.setAttribute('autoplay', '');
  video.setAttribute('muted', '');
  video.setAttribute('playsinline', '');

  // カメラ
  navigator.mediaDevices.getUserMedia(constraints)
  .then( (mediaStream) => {
    video.srcObject = mediaStream;
    video.onloadedmetadata = (e) => {
      video.play();
    };
  })
  .catch( (err) => {
    console.log(err.name + ": " + err.message);
  });

  // 画面サイズに変更
  chgSize();

  $('#modal0').on('show.bs.modal', function (event) {});
  send.addEventListener("click", function() {
    date = new Date();
    fileName = date.getFullYear() + ('0' + (date.getMonth() + 1)).slice(-2) + ('0' + date.getDate()).slice(-2) + ('0' + date.getHours()).slice(-2) + ('0' + date.getMinutes()).slice(-2) + ('0' + date.getSeconds()).slice(-2) + date.getMilliseconds() + ".jpg";
    dl.download = fileName;
    dl.href = sendImage.toDataURL("image/jpeg");
    dl.click();
    switch(step) {
      case 1:
        $('form input[name=imgData1]').val(sendImage.toDataURL("image/jpeg", 1));
        step = 2;
        $('#modal0').modal('hide')
        break;
      case 2:
        $('form input[name=imgData2]').val(sendImage.toDataURL("image/jpeg", 1));
        step = 1;
        $('#modal0').modal('hide')
        // $('form').submit();
        document.querySelector("#viewResult").click();
        break;
    }
  });

  // 画面クリック時の処理
  shutter.addEventListener("click", function() {

    video.pause();  // カメラ一時停止
  
    // canvas描画処理 (確認用Image)
    // reviewImage.width = video.width * 0.8;
    // reviewImage.height = (reviewImage.width / video.videoWidth) * video.videoHeight;
    reviewImage.width = 350;
    reviewImage.height = (reviewImage.width / video.videoWidth) * video.videoHeight;
    ctx = reviewImage.getContext("2d");
    ctx.drawImage(video, 0, 0, reviewImage.width, reviewImage.height);

    // canvas描画処理 (送信用Image)
    switch(step) {
      case 1:
        sendImage = document.querySelector("#sendImage1");
        break;
      case 2:
        sendImage = document.querySelector("#sendImage2");
        break;
    }
    sendImage.width = video.videoWidth;
    sendImage.height = video.videoHeight;
    ctx = sendImage.getContext("2d");
    ctx.drawImage(video, 0, 0, sendImage.width, sendImage.height);

    video.play(); // カメラ再開

    // // 確認ダイアログ表示
    // $("#dialog").dialog({
    //   modal: true,
    //   title: "撮影画像確認",
    //   width: video.width,
    //   height: video.height,
    //   buttons: {
    //     "NG": function() {
    //       $(this).dialog("close");
    //     },
    //     "OK": function() {
    //       $(this).dialog("close");
    //       switch(step) {
    //         case 1:
    //           $('form input[name=imgData1]').val(sendImage.toDataURL("image/jpeg", 1));
    //           step = 2;
    //           break;
    //         case 2:
    //           $('form input[name=imgData2]').val(sendImage.toDataURL("image/jpeg", 1));
    //           step = 1;
    //           // $('form').submit();
    //           document.querySelector("#viewResult").click();
    //           break;
    //       }
    //     }
    //   }
    // });

  });

});