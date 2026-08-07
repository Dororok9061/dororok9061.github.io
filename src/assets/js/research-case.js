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
      target.focus?.();
    }
  });
});
