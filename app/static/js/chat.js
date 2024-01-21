$(document).ready(function () {
  var popup = $(".chat-popup");
  var chatBtn = $(".chat-btn");
  var contactForm = $(".contact-form"); // replace "form" with your form's selector

  contactForm.on("submit", function(e) {
    e.preventDefault(); // prevent the form from submitting normally
    chatBtn.toggleClass("show");
  });
  
  chatBtn.on("click", () => {
    popup.toggleClass("show");
  });
});