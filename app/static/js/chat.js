$(document).ready(function () {
  var popup = $(".chat-popup");
  var chatBtn = $(".chat-btn");

  chatBtn.on("click", () => {
    popup.toggleClass("show");
  });
});


