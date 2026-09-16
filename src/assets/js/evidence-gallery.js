/* Full-frame, keyboard-accessible evidence galleries; all figures remain visible without JS. */
(() => {
  "use strict";

  const english = document.documentElement.lang.startsWith("en");
  const labels = english ? {
    previous: "← Previous", next: "Next →", all: "All photos", single: "One at a time",
    enlarge: "Enlarge image", original: "Open original ↗", gallery: "Image gallery",
    position: (index, count) => `Image ${index + 1} of ${count}`,
  } : {
    previous: "← 이전", next: "다음 →", all: "사진 전체 보기", single: "한 장씩 보기",
    enlarge: "이미지 확대", original: "원본 열기 ↗", gallery: "사진 모음",
    position: (index, count) => `${count}장 중 ${index + 1}번째`,
  };
  const gallerySelector = ".research-gallery-strip, .project-gallery > div, .indra-gallery, .publication-figure-grid, .gallery";
  const galleryByTrigger = new WeakMap();

  const button = (text, className) => {
    const element = document.createElement("button");
    element.type = "button";
    element.className = className;
    element.textContent = text;
    return element;
  };

  const prepareFigure = (figure) => {
    const image = figure.querySelector("img");
    if (!image) return null;
    let trigger = figure.querySelector("[data-lightbox]");
    if (!trigger) {
      trigger = image.closest("button, a");
      if (!trigger) {
        trigger = button("", "evidence-image-trigger");
        const media = image.closest("picture") || image;
        media.before(trigger);
        trigger.append(media);
      }
      trigger.dataset.lightbox = trigger.dataset.full || image.currentSrc || image.src;
      trigger.dataset.lightboxAlt = image.alt;
      trigger.dataset.lightboxCaption = figure.querySelector("figcaption")?.textContent.trim() || image.alt;
    }
    trigger.classList.add("evidence-image-trigger");
    trigger.setAttribute("aria-haspopup", "dialog");
    trigger.setAttribute("aria-label", `${labels.enlarge}: ${image.alt || labels.gallery}`);
    const badge = trigger.querySelector(".project-gallery__zoom-badge");
    if (badge) badge.textContent = labels.enlarge;
    return trigger;
  };

  const setKeyboardNavigation = (element, move, home, end) => {
    element.addEventListener("keydown", (event) => {
      if (event.target.matches("input, select, textarea") || event.altKey || event.ctrlKey || event.metaKey) return;
      if (event.key === "ArrowLeft") move(-1);
      else if (event.key === "ArrowRight") move(1);
      else if (event.key === "Home") home();
      else if (event.key === "End") end();
      else return;
      event.preventDefault();
    });
  };

  document.querySelectorAll(gallerySelector).forEach((gallery, galleryIndex) => {
    const slides = Array.from(gallery.children).filter((child) => child.tagName === "FIGURE" && child.querySelector("img"));
    if (!slides.length) return;
    const triggers = slides.map(prepareFigure);
    let index = 0;
    let showAll = false;
    gallery.classList.add("evidence-gallery");
    gallery.id ||= `evidence-gallery-${galleryIndex + 1}`;
    gallery.setAttribute("role", "group");
    gallery.setAttribute("aria-label", gallery.closest("section")?.getAttribute("aria-label") || labels.gallery);

    const controls = document.createElement("div");
    controls.className = "evidence-gallery-controls";
    const previous = button(labels.previous, "evidence-gallery-prev");
    const next = button(labels.next, "evidence-gallery-next");
    const toggle = button(labels.all, "evidence-gallery-toggle");
    const status = document.createElement("span");
    status.className = "evidence-gallery-count";
    status.setAttribute("aria-live", "polite");
    status.setAttribute("aria-atomic", "true");
    [previous, next, toggle].forEach((control) => control.setAttribute("aria-controls", gallery.id));
    toggle.setAttribute("aria-pressed", "false");
    controls.append(previous, status, next, toggle);

    const select = (requested) => {
      const focusedSlide = slides.find((slide) => slide.contains(document.activeElement));
      index = (requested + slides.length) % slides.length;
      slides.forEach((slide, slideIndex) => {
        slide.hidden = !showAll && slideIndex !== index;
        slide.setAttribute("role", "group");
        slide.setAttribute("aria-label", labels.position(slideIndex, slides.length));
      });
      status.textContent = `${index + 1} / ${slides.length}`;
      status.setAttribute("aria-label", labels.position(index, slides.length));
      gallery.classList.toggle("evidence-gallery--all", showAll);
      if (focusedSlide?.hidden) triggers[index].focus({ preventScroll: true });
    };
    const state = { triggers, select };
    triggers.forEach((trigger) => galleryByTrigger.set(trigger, state));
    if (slides.length > 1) {
      gallery.before(controls);
      gallery.classList.add("evidence-gallery--ready");
      previous.addEventListener("click", () => select(index - 1));
      next.addEventListener("click", () => select(index + 1));
      toggle.addEventListener("click", () => {
        showAll = !showAll;
        toggle.textContent = showAll ? labels.single : labels.all;
        toggle.setAttribute("aria-pressed", String(showAll));
        select(index);
      });
      [gallery, controls].forEach((element) => setKeyboardNavigation(element,
        (step) => select(index + step), () => select(0), () => select(slides.length - 1)));
    }
    select(0);
  });

  // Standalone article and paper figures get the same enlarged viewer.
  document.querySelectorAll("main figure, #content figure").forEach((figure) => {
    if (!figure.closest("dialog") && !figure.querySelector("[data-lightbox]")) prepareFigure(figure);
  });

  const dialog = document.querySelector("#publication-lightbox");
  const image = dialog?.querySelector(".lightbox__image");
  const caption = dialog?.querySelector("figcaption");
  if (!dialog || !image || !caption) return;

  const navigation = document.createElement("div");
  navigation.className = "evidence-lightbox-controls";
  const previous = button(labels.previous, "evidence-lightbox-prev");
  const next = button(labels.next, "evidence-lightbox-next");
  const status = document.createElement("span");
  status.className = "evidence-gallery-count";
  status.setAttribute("aria-live", "polite");
  status.setAttribute("aria-atomic", "true");
  const original = document.createElement("a");
  original.className = "evidence-lightbox-original";
  original.textContent = labels.original;
  original.target = "_blank";
  original.rel = "noopener";
  navigation.append(previous, status, next, original);
  dialog.querySelector("figure").before(navigation);
  let active = [];
  let index = 0;
  let returnFocus = null;

  const show = (requested) => {
    index = (requested + active.length) % active.length;
    const trigger = active[index];
    image.src = trigger.dataset.lightbox;
    image.alt = trigger.dataset.lightboxAlt || trigger.querySelector("img")?.alt || "";
    caption.textContent = trigger.dataset.lightboxCaption || image.alt;
    original.href = trigger.dataset.lightbox;
    status.textContent = `${index + 1} / ${active.length}`;
    status.setAttribute("aria-label", labels.position(index, active.length));
    previous.hidden = next.hidden = active.length < 2;
    const gallery = galleryByTrigger.get(trigger);
    gallery?.select(gallery.triggers.indexOf(trigger));
    returnFocus = trigger;
  };

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest?.("[data-lightbox]");
    if (!trigger || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const gallery = galleryByTrigger.get(trigger);
    const scope = trigger.closest(".post__content, .publication-detail, main, #content") || document;
    active = gallery?.triggers || Array.from(scope.querySelectorAll("[data-lightbox]"));
    show(active.indexOf(trigger));
    if (!dialog.open) dialog.showModal();
    dialog.querySelector("[data-lightbox-close]")?.focus();
  });
  previous.addEventListener("click", () => show(index - 1));
  next.addEventListener("click", () => show(index + 1));
  setKeyboardNavigation(dialog, (step) => show(index + step), () => show(0), () => show(active.length - 1));
  dialog.querySelector("[data-lightbox-close]")?.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener("close", () => returnFocus?.focus({ preventScroll: true }));
})();
