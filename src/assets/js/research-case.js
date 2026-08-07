"use strict";

const researchNavs = document.querySelectorAll("[data-research-nav]");

researchNavs.forEach((nav) => {
  const links = Array.from(nav.querySelectorAll("[data-research-nav-link]"));
  const targets = links
    .map((link) => document.getElementById(link.dataset.researchNavLink || ""))
    .filter(Boolean);

  if (!links.length || !targets.length || !("IntersectionObserver" in window)) return;

  const activate = (id) => {
    links.forEach((link) => {
      const active = link.dataset.researchNavLink === id;
      link.classList.toggle("is-active", active);
      if (active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };

  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
    if (visible[0]) activate(visible[0].target.id);
  }, { rootMargin: "-25% 0px -60% 0px", threshold: [0.05, 0.2, 0.5] });

  targets.forEach((target) => observer.observe(target));
});

document.querySelectorAll("[data-copy-target]").forEach((button) => {
  button.addEventListener("click", async () => {
    const target = document.getElementById(button.dataset.copyTarget || "");
    if (!target) return;
    const text = target.textContent || "";
    try {
      await navigator.clipboard.writeText(text.trim());
      const original = button.textContent;
      button.textContent = button.dataset.copiedLabel || "Copied";
      window.setTimeout(() => { button.textContent = original; }, 1600);
    } catch (_) {
      if (typeof target.focus === "function") target.focus();
    }
  });
});

const paperShell = document.querySelector("[data-indra-shell]");

if (paperShell) {
  const themeButton = paperShell.querySelector("[data-paper-theme-toggle]");
  const language = document.documentElement.lang === "en" ? "en" : "ko";
  const storageKey = "engineering-research-paper-theme";

  const applyTheme = (dark) => {
    paperShell.classList.toggle("is-dark", dark);
    if (!themeButton) return;
    themeButton.setAttribute("aria-pressed", String(dark));
    themeButton.textContent = dark
      ? (language === "en" ? "Light mode" : "밝은 화면")
      : (language === "en" ? "Dark mode" : "어두운 화면");
  };

  let savedTheme = "";
  try {
    savedTheme = window.localStorage.getItem(storageKey) || "";
  } catch (_) {
    savedTheme = "";
  }
  applyTheme(savedTheme === "dark");

  if (themeButton) {
    themeButton.addEventListener("click", () => {
      const dark = !paperShell.classList.contains("is-dark");
      applyTheme(dark);
      try {
        window.localStorage.setItem(storageKey, dark ? "dark" : "light");
      } catch (_) {
        // The page still works when storage is unavailable.
      }
    });
  }

  paperShell.querySelectorAll("[data-paper-carousel]").forEach((carousel) => {
    const track = carousel.querySelector("[data-carousel-track]");
    const previous = carousel.querySelector("[data-carousel-prev]");
    const next = carousel.querySelector("[data-carousel-next]");
    if (!track) return;

    const step = () => Math.max(track.clientWidth * 0.76, 280);
    if (previous) previous.addEventListener("click", () => {
      track.scrollBy({ left: -step(), behavior: "smooth" });
    });
    if (next) next.addEventListener("click", () => {
      track.scrollBy({ left: step(), behavior: "smooth" });
    });
  });

  const scrollTopButton = paperShell.querySelector("[data-scroll-top]");
  if (scrollTopButton) {
    const updateScrollButton = () => {
      scrollTopButton.classList.toggle("is-visible", window.scrollY > 420);
    };
    window.addEventListener("scroll", updateScrollButton, { passive: true });
    updateScrollButton();
    scrollTopButton.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
}
