$(document).ready(function () {
  let slideIndex = 0;
  const slides = $(".home-slider img");

  function setSlides(index) {
    if (index < 0) {
      slideIndex = slides.length - 1;
    } else if (index >= slides.length) {
      slideIndex = 0;
    }

    slides.css("transform", `translateX(-${slideIndex * 100}%)`); // Move all slides to the left
  }

  setInterval(() => {
    slideIndex++;
    setSlides(slideIndex);
  }, 3000);
});
