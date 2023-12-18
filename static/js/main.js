$(document).ready(function ($) {
  $(window).scroll(function () {
    var scrollTopPosition =
      document.documentElement.scrollTop || document.body.scrollTop;
    console.log(scrollTopPosition);
    if (scrollTopPosition > 1) {
      $("nav").addClass("nav-background ");
    } else {
      $("nav").removeClass("nav-background ");
    }
  });
});
