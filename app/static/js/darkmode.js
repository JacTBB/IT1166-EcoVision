$(document).ready(function () {
    if (localStorage.getItem("darkmode") === "true") {
        $(".contact-form").addClass("switch-color");
    }
    $(".toggle-darkmode").click(function () {
        $(".contact-form").toggleClass("switch-color");

        var borderColor = $("form input[type='text']").css("border-color");
        if (borderColor === 'rgb(255, 255, 255)') { // white in rgb
            $("form input[type='text']").css("border-color", "black");
        } else {
            $("form input[type='text']").css("border-color", "white");
        }
    });
});