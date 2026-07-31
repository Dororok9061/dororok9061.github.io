"use strict";

const menuButton = document.querySelector("#site-menu-toggle");
const navigation = document.querySelector("#site-navigation");

if (menuButton && navigation) {
  menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!isOpen));
    navigation.classList.toggle("is-open", !isOpen);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      menuButton.setAttribute("aria-expanded", "false");
      navigation.classList.remove("is-open");
      menuButton.focus();
    }
  });
}

const lightbox = document.querySelector("#publication-lightbox");
const lightboxImage = lightbox ? lightbox.querySelector(".lightbox__image") : null;
const lightboxCaption = lightbox ? lightbox.querySelector("figcaption") : null;

document.querySelectorAll("[data-lightbox]").forEach((trigger) => {
  trigger.addEventListener("click", () => {
    if (!lightbox || !lightboxImage || !lightboxCaption) return;
    lightboxImage.src = trigger.dataset.lightbox || "";
    lightboxImage.alt = trigger.dataset.lightboxAlt || "Publication evidence preview";
    lightboxCaption.textContent = trigger.dataset.lightboxCaption || "";
    lightbox.showModal();
  });
});

if (lightbox) {
  const closeButton = lightbox.querySelector("[data-lightbox-close]");
  if (closeButton) closeButton.addEventListener("click", () => lightbox.close());
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) lightbox.close();
  });
}
