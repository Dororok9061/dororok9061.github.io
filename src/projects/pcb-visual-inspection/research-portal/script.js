const ASSET_VERSION = "20260808-public-mirror-v1";

function clear(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
}

function textElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  element.textContent = text || "";
  return element;
}

function icon(name) {
  const span = document.createElement("span");
  span.className = "material-symbols-outlined";
  span.setAttribute("aria-hidden", "true");
  span.textContent = name || "article";
  return span;
}

function assetUrl(src) {
  const value = String(src || "");
  if (!value || value.startsWith("http") || value.startsWith("data:") || value.includes("?")) return value;
  return `${value}?v=${ASSET_VERSION}`;
}

function normaliseFigureItem(entry, index) {
  if (typeof entry === "object" && entry !== null) {
    return {
      src: entry.src || entry.url || "",
      label: entry.label || entry.caption || `Figure ${index + 1}`,
    };
  }
  const src = String(entry || "");
  const file = src.split("/").pop().replace(/[?].*$/, "");
  const stem = file.replace(/[.](png|jpe?g|webp|svg)$/i, "").replace(/^pcb_style_/, "");
  const label = stem
    .replace(/_/g, " ")
    .replace(/fig([0-9]+[a-z]?)/i, "Figure $1")
    .replace(/table([0-9]+[a-z]?)/i, "Table $1");
  return { src, label: label || `Figure ${index + 1}` };
}

function renderPage(data) {
  const safeData = data || {};
  document.title = safeData.paper_title || "Research Publication Workbench";
  document.querySelectorAll("[data-bind='paper_title']").forEach((element) => {
    element.textContent = safeData.paper_title || "";
  });

  const subtitle = document.querySelector("[data-bind='subtitle']");
  if (subtitle) subtitle.textContent = safeData.subtitle || safeData.header_note || "";

  renderBadges(safeData.conference_badges || []);
  renderActions(safeData.buttons || []);
  renderNav(safeData.sections || []);
  renderMetrics(safeData.metrics || []);
  renderSections(safeData.sections || []);
  setupInteractions();
  restoreHashTarget();
}

function restoreHashTarget() {
  if (!window.location.hash) return;
  const id = decodeURIComponent(window.location.hash.slice(1));
  const target = document.getElementById(id);
  if (!target) return;
  requestAnimationFrame(() => target.scrollIntoView({ block: "start" }));
}

function renderBadges(items) {
  const root = document.getElementById("badges");
  clear(root);
  items.forEach((item) => root.appendChild(textElement("span", "badge", item)));
}

function renderActions(items) {
  const root = document.getElementById("actions");
  clear(root);
  items.forEach((item) => {
    const link = document.createElement("a");
    link.href = item.url || "#";
    link.target = "_blank";
    link.rel = "noreferrer";
    link.append(icon(item.icon), textElement("span", "", item.label));
    root.appendChild(link);
  });
}

function renderNav(sections) {
  const root = document.getElementById("navLinks");
  clear(root);
  sections.forEach((section) => {
    const link = document.createElement("a");
    link.href = `#${section.id || ""}`;
    link.append(icon(section.icon), textElement("span", "", section.nav_label || section.title));
    root.appendChild(link);
  });
}

function renderMetrics(metrics) {
  const root = document.getElementById("metrics");
  clear(root);
  metrics.forEach((metric) => {
    const card = document.createElement("div");
    card.className = "metric";
    card.append(
      textElement("span", "", metric.label),
      textElement("strong", "", metric.value),
      textElement("small", "", metric.note),
    );
    root.appendChild(card);
  });
}

function renderSections(sections) {
  const root = document.getElementById("sections");
  clear(root);
  sections.forEach((section) => root.appendChild(renderSection(section)));
}

function renderSection(section) {
  const wrapper = document.createElement("section");
  wrapper.className = "section";
  wrapper.id = section.id || "";

  const heading = document.createElement("h2");
  heading.append(icon(section.icon), textElement("span", "", section.title));
  wrapper.appendChild(heading);

  if (section.content) wrapper.appendChild(textElement("p", "", section.content));
  renderComponents(wrapper, section.components || []);
  renderSubsections(wrapper, section.subsections || []);
  renderCards(wrapper, section.cards || []);
  renderTable(wrapper, section.table || []);
  if (section.bibtex) renderBibtex(wrapper, section.bibtex);
  return wrapper;
}

function renderSubsections(root, items) {
  items.forEach((item) => {
    const subsection = document.createElement("div");
    subsection.className = "subsection";
    subsection.appendChild(textElement("h3", "", item.title));
    if (item.content) subsection.appendChild(textElement("p", "", item.content));
    renderList(subsection, item.list || []);
    renderComponents(subsection, item.components || []);
    root.appendChild(subsection);
  });
}

function renderList(root, items) {
  if (!items.length) return;
  const list = document.createElement("ul");
  list.className = "check-list";
  items.forEach((item) => list.appendChild(textElement("li", "", item)));
  root.appendChild(list);
}

function renderComponents(root, items) {
  items.forEach((component) => {
    if (component.type === "image_gallery") renderGallery(root, component);
    if (component.type === "image_carousel") renderCarousel(root, component);
  });
}

function renderGallery(root, component) {
  const items = (component.images || []).map(normaliseFigureItem);
  root.appendChild(textElement("h3", "component-title", component.title || "Gallery"));

  const gallery = document.createElement("div");
  gallery.className = "gallery";
  gallery.dataset.count = String(items.length);

  items.forEach((item, index) => {
    const src = assetUrl(item.src);
    const label = item.label || `Figure ${index + 1}`;
    const figure = document.createElement("figure");
    figure.className = "figure-card";

    const button = document.createElement("button");
    button.className = "figure-thumb";
    button.type = "button";
    button.dataset.full = src;
    button.setAttribute("aria-label", label);

    const image = document.createElement("img");
    image.src = src;
    image.alt = label;
    image.width = 900;
    image.height = 900;
    image.loading = "lazy";
    image.decoding = "async";

    button.appendChild(image);
    figure.append(button, textElement("figcaption", "", label));
    gallery.appendChild(figure);
  });

  root.appendChild(gallery);
}

function renderCarousel(root, component) {
  const carousel = document.createElement("div");
  carousel.className = "carousel";
  carousel.appendChild(textElement("h3", "component-title", component.title || "Carousel"));

  const windowElement = document.createElement("div");
  windowElement.className = "carousel-window";
  const track = document.createElement("div");
  track.className = "carousel-track";

  (component.images || []).forEach((src) => {
    const slide = document.createElement("div");
    slide.className = "carousel-slide";
    const button = document.createElement("button");
    button.className = "figure-thumb";
    button.type = "button";
    button.dataset.full = assetUrl(src);
    button.setAttribute("aria-label", "Open enlarged figure");
    const image = document.createElement("img");
    image.src = assetUrl(src);
    image.alt = component.title || "carousel image";
    image.width = 900;
    image.height = 900;
    image.loading = "lazy";
    image.decoding = "async";
    button.appendChild(image);
    slide.appendChild(button);
    track.appendChild(slide);
  });

  windowElement.appendChild(track);
  const controls = document.createElement("div");
  controls.className = "carousel-controls";
  const previous = document.createElement("button");
  previous.className = "icon-button prev";
  previous.type = "button";
  previous.setAttribute("aria-label", "Previous");
  previous.appendChild(icon("chevron_left"));
  const next = document.createElement("button");
  next.className = "icon-button next";
  next.type = "button";
  next.setAttribute("aria-label", "Next");
  next.appendChild(icon("chevron_right"));
  controls.append(previous, next);
  carousel.append(windowElement, controls);
  root.appendChild(carousel);
  setupCarousel(carousel);
}

function renderCards(root, cards) {
  if (!cards.length) return;
  const wrapper = document.createElement("div");
  wrapper.className = "cards";
  cards.forEach((card) => {
    const article = document.createElement("article");
    article.className = "track-card";
    article.append(
      icon(card.icon),
      textElement("h3", "", card.title),
      textElement("p", "", card.text),
      textElement("span", "badge", card.type),
    );
    wrapper.appendChild(article);
  });
  root.appendChild(wrapper);
}

function renderTable(root, rows) {
  if (!rows.length) return;
  const keys = Object.keys(rows[0]);
  const wrap = document.createElement("div");
  wrap.className = "table-wrap";
  const table = document.createElement("table");
  const thead = document.createElement("thead");
  const headRow = document.createElement("tr");
  keys.forEach((key) => headRow.appendChild(textElement("th", "", key)));
  thead.appendChild(headRow);
  const tbody = document.createElement("tbody");
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    keys.forEach((key) => tr.appendChild(textElement("td", "", row[key])));
    tbody.appendChild(tr);
  });
  table.append(thead, tbody);
  wrap.appendChild(table);
  root.appendChild(wrap);
}

function renderBibtex(root, text) {
  const wrapper = document.createElement("div");
  wrapper.className = "bibtex-section";
  const pre = document.createElement("pre");
  const code = document.createElement("code");
  code.textContent = text;
  pre.appendChild(code);
  const button = document.createElement("button");
  button.className = "icon-button";
  button.id = "copyBibtex";
  button.type = "button";
  button.setAttribute("aria-label", "Copy BibTeX");
  button.appendChild(icon("content_copy"));
  wrapper.append(pre, button);
  root.appendChild(wrapper);
}

function setupCarousel(root) {
  const track = root.querySelector(".carousel-track");
  const slides = root.querySelectorAll(".carousel-slide");
  let index = 0;
  const update = () => {
    if (track) track.style.transform = `translateX(${-index * 100}%)`;
  };
  root.querySelector(".prev")?.addEventListener("click", () => {
    index = (index + slides.length - 1) % slides.length;
    update();
  });
  root.querySelector(".next")?.addEventListener("click", () => {
    index = (index + 1) % slides.length;
    update();
  });
}

function setupInteractions() {
  document.getElementById("themeToggle")?.addEventListener("click", () => document.body.classList.toggle("dark"));
  document.getElementById("scrollTop")?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  const lightbox = document.getElementById("imageLightbox");
  const lightboxImage = lightbox?.querySelector("img");
  const closeLightbox = () => {
    if (!lightbox || !lightboxImage) return;
    lightbox.classList.remove("open");
    lightbox.setAttribute("aria-hidden", "true");
    lightboxImage.removeAttribute("src");
  };

  document.addEventListener("click", (event) => {
    const button = event.target.closest?.(".figure-thumb");
    if (!button || !lightbox || !lightboxImage) return;
    lightboxImage.src = button.dataset.full || "";
    lightbox.classList.add("open");
    lightbox.setAttribute("aria-hidden", "false");
  });
  lightbox?.querySelector(".lightbox-close")?.addEventListener("click", closeLightbox);
  lightbox?.addEventListener("click", (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeLightbox();
  });

  const copy = document.getElementById("copyBibtex");
  copy?.addEventListener("click", () => {
    const text = document.querySelector(".bibtex-section code")?.textContent || "";
    navigator.clipboard?.writeText(text);
  });

  const links = Array.from(document.querySelectorAll(".nav-links a"));
  const sections = links.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  const scrollTop = document.getElementById("scrollTop");
  window.addEventListener("scroll", () => {
    if (scrollTop) scrollTop.style.display = window.scrollY > 450 ? "grid" : "none";
    let current = sections[0]?.id;
    sections.forEach((section) => {
      if (section.offsetTop - 120 <= window.scrollY) current = section.id;
    });
    links.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === `#${current}`));
  });
}

renderPage(window.PORTAL_DATA);
