$(document).ready(function () {
  // if (localStorage.getItem("darkmode") === "true") {
  //   $(".contact-form").addClass("switch-color");
  // }

  $(".toggle-darkmode").click(function () {
    $(".contact-form").toggleClass("switch-color");

    var getBorderColor = $("form input[type='text']").css("border-color");

    if (getBorderColor === "rgb(255, 255, 255)") {
      $("form input[type='text'], form input[type='number'], form textarea, form input[type='email']").css(
        "border-color",
        "black"
      );
    } else {
      $("form input[type='text'], form input[type='number'], form input[type='email'], form textarea").css(
        "border-color",
        "white"
      );
    }
  });
});
