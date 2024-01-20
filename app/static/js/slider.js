$(document).ready(function () {
  let slideIndex = 0;
  const slides = $(".home-slider img");

  const sliderbtns = $(".slider-buttons span");

  const animationms = 3000;
  let animation;

  function setSlides(index) {
    if (index < 0) {
      slideIndex = slides.length - 1;
    } else if (index >= slides.length) {
      slideIndex = 0;
    }

    slides.css("transform", `translateX(-${slideIndex * 100}%)`); // Move all slides to the left

    sliderbtns.eq(index).addClass("btn-selected").siblings().removeClass("btn-selected");
  }

  sliderbtns.on("click", function () {
    slideIndex = $(this).index();
    $(this).addClass("btn-selected").siblings().removeClass("btn-selected");
    setSlides(slideIndex);
    clearInterval(animation);

    startAnimation();
  });

  function startAnimation() {
    animation = setInterval(() => {
      slideIndex++;
      setSlides(slideIndex);
    }, animationms);
  }

  startAnimation();
});
