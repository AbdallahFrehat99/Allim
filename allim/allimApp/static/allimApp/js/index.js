
  const container = document.getElementById("cardContainer");
  const slider = document.getElementById("cardSlider");
  let cardWidth = 0;
  let scrollSpeed = 4;
  let isUserScrolling = false;

  function cloneCardsForLoop() {
    const cards = [...slider.children];
    if (!cards.length) return;

    cardWidth = cards[0].offsetWidth + 20;

    // Clone start and end for loop
    cards.forEach(card => slider.appendChild(card.cloneNode(true)));
    cards.reverse().forEach(card => slider.insertBefore(card.cloneNode(true), slider.firstChild));

    // Center scroll
    container.scrollLeft = cards.length * cardWidth;
  }

  function highlightCenterCard() {
    const cards = slider.querySelectorAll(".custom-carad");
    const centerX = container.offsetLeft + container.offsetWidth / 2;

    let closestCard = null;
    let closestDist = Infinity;

    cards.forEach(card => {
      const rect = card.getBoundingClientRect();
      const cardCenter = rect.left + rect.width / 2;
      const dist = Math.abs(centerX - cardCenter);

      card.classList.remove("highlight");

      if (dist < closestDist) {
        closestDist = dist;
        closestCard = card;
      }
    });

    if (closestCard) closestCard.classList.add("highlight");
  }

  function autoScroll() {
    if (!isUserScrolling) {
      container.scrollLeft += scrollSpeed;

      const maxScroll = slider.scrollWidth;
      const half = maxScroll / 2;
      const visible = container.offsetWidth;

      if (container.scrollLeft >= maxScroll - visible - 1) {
        container.scrollLeft = half - visible;
      }

      if (container.scrollLeft <= 1) {
        container.scrollLeft = half;
      }

      highlightCenterCard();
    }

    requestAnimationFrame(autoScroll);
  }

  function scrollSlider(dir) {
    isUserScrolling = true;
    container.scrollLeft += dir * cardWidth;
    setTimeout(() => isUserScrolling = false, 500);
  }

  window.addEventListener("load", () => {
    setTimeout(() => {
      cloneCardsForLoop();
      requestAnimationFrame(autoScroll);
    }, 10); // Delay ensures layout is stable
  });

