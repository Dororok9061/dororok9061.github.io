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
    lightboxImage.alt = trigger.dataset.lightboxAlt || "Publication first-page preview";
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

const blogSearch = document.querySelector("[data-blog-search]");

if (blogSearch) {
  const input = blogSearch.querySelector("[data-blog-search-input]");
  const results = blogSearch.querySelector("[data-blog-search-results]");
  const status = blogSearch.querySelector("[data-blog-search-status]");
  const language = blogSearch.dataset.lang || "ko";
  let index = [];

  const renderResults = (query) => {
    if (!input || !results || !status) return;
    results.replaceChildren();
    const normalized = query.trim().toLocaleLowerCase();
    if (normalized.length < 2) return;

    const matches = index.filter((item) => {
      if (item.lang !== language) return false;
      const searchable = [item.title, item.description, item.category, item.subcategory, item.series, item.tools, item.tags, item.headings]
        .filter(Boolean)
        .join(" ")
        .toLocaleLowerCase();
      return searchable.includes(normalized);
    }).slice(0, 12);

    status.textContent = language === "en" ? `${matches.length} result(s)` : `${matches.length}개 결과`;
    matches.forEach((item) => {
      const row = document.createElement("li");
      const link = document.createElement("a");
      const meta = document.createElement("small");
      const summary = document.createElement("p");
      link.href = item.url;
      link.textContent = item.title;
      meta.textContent = `${item.date} · ${item.category || ""}`;
      summary.textContent = item.description;
      row.append(link, meta, summary);
      results.append(row);
    });
  };

  if (input && results && status) {
    fetch(blogSearch.dataset.indexUrl, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw new Error("search index unavailable");
        return response.json();
      })
      .then((items) => { index = Array.isArray(items) ? items : []; })
      .catch(() => { status.textContent = language === "en" ? "Search unavailable; use categories or archive." : "검색을 불러오지 못했습니다. 카테고리나 Archive를 이용하세요."; });
    input.addEventListener("input", () => renderResults(input.value));
  }
}
