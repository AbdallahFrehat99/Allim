document.addEventListener("DOMContentLoaded", function () {
  const slider = document.getElementById("reviewSlider");
  const card = slider.querySelector(".review-card");
  const cardWidth = card.offsetWidth + 20; // Include margin or gap if needed

  window.slideReviews = function (direction) {
    slider.scrollBy({
      left: direction * cardWidth,
      behavior: "smooth"
    });
  };
});
