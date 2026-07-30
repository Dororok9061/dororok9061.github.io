(() => {
  const root = document.documentElement;
  const button = document.querySelector("[data-theme-toggle]");
  const storageKey = "portfolio-theme";
  const stored = localStorage.getItem(storageKey);

  if (stored === "light" || stored === "dark") {
    root.dataset.theme = stored;
  }

  const updateLabel = () => {
    if (!button) return;
    const isLight = root.dataset.theme === "light";
    button.textContent = isLight ? "DARK" : "LIGHT";
    button.setAttribute(
      "aria-label",
      isLight ? button.dataset.darkLabel : button.dataset.lightLabel,
    );
  };

  updateLabel();

  button?.addEventListener("click", () => {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    localStorage.setItem(storageKey, next);
    updateLabel();
  });
})();

