$(document).ready(function () {
  $(".toggle-darkmode").on("click", function () {
    if ($(".contact-form").css("color") == "rgb(255, 255, 255)") {
      $(".error-message").css("color", "lightgreen");
    } else {
      $(".error-message").css("color", "darkgreen");
    }
  });
});
