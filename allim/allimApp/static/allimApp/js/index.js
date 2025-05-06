// document.addEventListener("DOMContentLoaded", () => {
//   const container = document.getElementById("cardContainer");
//   const slider = document.getElementById("cardSlider");

//   let cardWidth = 0;
//   let scrollSpeed = 1.2;
//   let isUserScrolling = false;

//   function cloneCardsForLoop() {
//     const cards = Array.from(slider.children);
//     if (!cards.length) return;

//     // Get card width after DOM is fully painted
//     setTimeout(() => {
//       // cardWidth = cards[0].offsetWidth + 20;

//       // Clone at end and beginning
//       cards.forEach(card => slider.appendChild(card.cloneNode(true)));
//       cards.reverse().forEach(card => slider.insertBefore(card.cloneNode(true), slider.firstChild));

//       container.scrollLeft = cards.length * cardWidth;
//     }, 50);
//   }

//   function highlightCenterCard() {
//     const cards = slider.querySelectorAll(".custom-card"); // Fixed typo here
//     const containerCenter = container.getBoundingClientRect().left + container.offsetWidth / 2;

//     let closest = null;
//     let closestDist = Infinity;

//     cards.forEach(card => {
//       const rect = card.getBoundingClientRect();
//       const cardCenter = rect.left + rect.width / 2;
//       const dist = Math.abs(containerCenter - cardCenter);

//       card.classList.remove("highlight");

//       if (dist < closestDist) {
//         closestDist = dist;
//         closest = card;
//       }
//     });

//     if (closest) closest.classList.add("highlight");
//   }

//   function autoScroll() {
//     if (!isUserScrolling) {
//       container.scrollLeft += scrollSpeed;

//       const maxScroll = slider.scrollWidth;
//       const half = maxScroll / 2;
//       const visible = container.offsetWidth;

//       if (container.scrollLeft >= maxScroll - visible - 1) {
//         container.scrollLeft = half - visible;
//       }
//       if (container.scrollLeft <= 1) {
//         container.scrollLeft = half;
//       }

//       highlightCenterCard();
//     }

//     requestAnimationFrame(autoScroll);
//   }

//   cloneCardsForLoop();
//   requestAnimationFrame(autoScroll);
// });



// ///////Reviews


// function autoScroll() {
//   if (!isUserScrolling) {
//     container.scrollLeft += scrollSpeed;

//     const maxScroll = slider.scrollWidth;
//     const half = maxScroll / 2;
//     const visible = container.offsetWidth;

//     if (container.scrollLeft >= maxScroll - visible - 1) {
//       container.scrollLeft = half - visible;
//     }

//     if (container.scrollLeft <= 1) {
//       container.scrollLeft = half;
//     }

//     highlightCenterCard();
//   }

//   requestAnimationFrame(autoScroll);
// }

// function scrollSlider(dir) {
//   isUserScrolling = true;
//   container.scrollLeft += dir * cardWidth;
//   setTimeout(() => isUserScrolling = false, 500);
// }

// window.addEventListener("load", () => {
//   setTimeout(() => {
//     cloneCardsForLoop();
//     requestAnimationFrame(autoScroll);
//   }, 10); // Delay ensures layout is stable
// });








