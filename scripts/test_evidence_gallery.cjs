/* Run with Node and Playwright available on NODE_PATH. Uses installed Chrome by default. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const src = path.join(root, "src");
const graphic = (width, height) => `data:image/svg+xml,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}"><rect width="100%" height="100%" fill="white"/></svg>`)}`;
const figure = (i, existingTrigger = true) => {
  const image = `<img src="${graphic(i === 2 ? 900 : 1600, i === 2 ? 1600 : 600)}" alt="Figure ${i}" width="1600" height="600">`;
  return `<figure>${existingTrigger ? `<button type="button" data-lightbox="${graphic(1600, 600)}" data-lightbox-alt="Figure ${i}" data-lightbox-caption="Caption ${i}">${image}</button>` : image}<figcaption>Caption ${i}</figcaption></figure>`;
};
const figures = [1, 2, 3].map((i) => figure(i)).join("");
const markup = (language) => `<!doctype html><html lang="${language}"><body class="minecraft-theme">
  <header class="site-header"><div class="site-header__inner">
    <a href="#main" class="site-brand">Hyeongrok Ryu</a>
    <button class="site-menu-toggle" id="site-menu-toggle" aria-expanded="false">Menu</button>
    <nav class="site-navigation" id="site-navigation"><ul class="site-navigation__list">
      ${["Projects & files", "Papers", "About", "Roles", "Research & blog", "Coursework", "External learning", "Contact", "한국어"].map((title) => `<li class="site-navigation__item"><a href="#main">${title}</a></li>`).join("")}
    </ul></nav>
  </div></header>
  <main style="max-width:1100px;margin:auto;padding:12px">
    <section class="project-gallery"><h2>FPGA</h2><div class="research-gallery-strip">${figures}</div></section>
    <section class="project-gallery dca-debug-gallery" aria-label="DCA capture"><div>${figures}</div></section>
    <div class="publication-figure-grid">${figures}</div>
    <div class="indra-gallery">${[1, 2, 3].map((i) => figure(i, false)).join("")}</div>
    <div class="gallery">${figures}</div>
    <section class="project-gallery"><div>${figure(1)}</div></section>
    <article class="post__content">${figure(4, false)}</article>
  </main>
  <dialog id="publication-lightbox" class="lightbox" aria-labelledby="lightbox-caption">
    <button data-lightbox-close class="lightbox__close" type="button">×</button>
    <figure><img class="lightbox__image"><figcaption id="lightbox-caption"></figcaption></figure>
  </dialog>
</body></html>`;

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.GALLERY_BROWSER ? { executablePath: process.env.GALLERY_BROWSER } : { channel: "chrome" }),
  });
  try {
    for (const width of [1600, 900, 390]) {
      for (const language of ["ko", "en"]) {
        const page = await browser.newPage({ viewport: { width, height: 950 } });
        const errors = [];
        page.on("pageerror", (error) => errors.push(error.message));
        await page.setContent(markup(language));
        for (const filename of ["portfolio.css", "research-case.css", "research-start.css", "minecraft-world.css", "portfolio-readability.css", "evidence-gallery.css"]) {
          await page.addStyleTag({ content: fs.readFileSync(path.join(src, "assets/css", filename), "utf8") });
        }

        // No-JavaScript fallback: complete figures remain in a normal, non-clipped grid.
        assert.equal(await page.locator("main figure:visible").count(), 17);
        assert.equal(await page.locator(".research-gallery-strip").evaluate((element) => element.scrollWidth <= element.clientWidth + 1), true);
        assert.equal(await page.locator("main").evaluate((element) => element.scrollWidth <= element.clientWidth + 1), true);

        await page.addScriptTag({ path: path.join(src, "assets/js/site.js") });
        await page.addScriptTag({ path: path.join(src, "assets/js/evidence-gallery.js") });
        if (width <= 1088) {
          await page.locator("#site-menu-toggle").click();
          assert.equal(await page.locator("#site-navigation").isVisible(), true);
          const navigationBounds = await page.locator("#site-navigation").boundingBox();
          assert.ok(navigationBounds.x >= 0 && navigationBounds.x + navigationBounds.width <= width);
          const mainBounds = await page.locator("main").boundingBox();
          assert.ok(navigationBounds.y + navigationBounds.height <= mainBounds.y);
          await page.keyboard.press("Escape");
          assert.equal(await page.locator("#site-navigation").isVisible(), false);
        }
        assert.equal(await page.locator(".evidence-gallery-controls").count(), 5);
        assert.equal(await page.locator(".evidence-gallery").count(), 6);
        for (const gallery of await page.locator(".evidence-gallery").all()) {
          assert.equal(await gallery.locator(":scope > figure:visible").count(), 1);
          assert.equal(await gallery.evaluate((element) => element.scrollWidth <= element.clientWidth + 1), true);
        }

        const controls = page.locator(".evidence-gallery-controls").first();
        const gallery = page.locator(".research-gallery-strip");
        await controls.locator(".evidence-gallery-next").click();
        assert.equal(await controls.locator(".evidence-gallery-count").textContent(), "2 / 3");
        assert.equal(await gallery.locator("figure:visible img").getAttribute("alt"), "Figure 2");
        await controls.locator(".evidence-gallery-next").press("ArrowRight");
        assert.equal(await controls.locator(".evidence-gallery-count").textContent(), "3 / 3");
        await controls.locator(".evidence-gallery-next").press("Home");
        assert.equal(await controls.locator(".evidence-gallery-count").textContent(), "1 / 3");
        await controls.locator(".evidence-gallery-prev").click();
        assert.equal(await controls.locator(".evidence-gallery-count").textContent(), "3 / 3");
        await controls.locator(".evidence-gallery-toggle").click();
        assert.equal(await gallery.locator("figure:visible").count(), 3);
        await controls.locator(".evidence-gallery-toggle").click();
        assert.equal(await gallery.locator("figure:visible").count(), 1);

        // Arrow navigation from the image itself keeps focus on the newly visible image.
        await gallery.locator("figure:visible [data-lightbox]").focus();
        await page.keyboard.press("ArrowLeft");
        await page.keyboard.press("ArrowRight");
        assert.equal(await gallery.locator("figure:visible [data-lightbox]").evaluate((element) => element === document.activeElement), true);
        assert.equal(await controls.locator(".evidence-gallery-count").textContent(), "3 / 3");

        await gallery.locator("figure:visible [data-lightbox]").click();
        const dialog = page.locator("#publication-lightbox");
        assert.equal(await dialog.evaluate((element) => element.open), true);
        assert.equal(await dialog.locator(".evidence-gallery-count").textContent(), "3 / 3");
        await dialog.locator(".evidence-lightbox-next").click();
        assert.equal(await dialog.locator(".lightbox__image").getAttribute("alt"), "Figure 1");
        await dialog.locator(".evidence-lightbox-next").press("ArrowRight");
        assert.equal(await dialog.locator(".lightbox__image").getAttribute("alt"), "Figure 2");
        assert.equal(await dialog.locator(".evidence-lightbox-original").getAttribute("href"), graphic(1600, 600));
        assert.equal(await dialog.evaluate((element) => element.scrollWidth <= element.clientWidth + 1), true);
        await page.keyboard.press("Escape");
        assert.equal(await dialog.evaluate((element) => element.open), false);
        assert.equal(await gallery.locator("figure:visible img").getAttribute("alt"), "Figure 2");
        await page.waitForFunction(() => document.activeElement?.matches(".research-gallery-strip figure:not([hidden]) [data-lightbox]"));
        assert.equal(await gallery.locator("figure:visible [data-lightbox]").evaluate((element) => element === document.activeElement), true);

        // Bare article figures are enlarged without changing their source pixels.
        const articleImage = page.locator(".post__content img");
        const originalSource = await articleImage.getAttribute("src");
        await page.locator(".post__content [data-lightbox]").click();
        assert.equal(await dialog.locator(".lightbox__image").getAttribute("src"), originalSource);
        assert.equal(await dialog.locator(".evidence-lightbox-next").isVisible(), false);
        await dialog.locator("[data-lightbox-close]").click();
        assert.deepEqual(errors, []);
        await page.close();
        console.log(`PASS: ${language}, ${width}px: fallback, gallery, keys, modal, focus, original image`);
      }
    }

    // Exercise the actual standalone PCB portal, which bypasses Jekyll's shared layout.
    const portal = await browser.newPage({ viewport: { width: 390, height: 950 } });
    const portalErrors = [];
    portal.on("pageerror", (error) => portalErrors.push(error.message));
    await portal.route("http://portfolio.test/**", (route) => {
      const file = path.resolve(src, `.${decodeURIComponent(new URL(route.request().url()).pathname)}`);
      const target = fs.existsSync(file) && fs.statSync(file).isDirectory() ? path.join(file, "index.html") : file;
      if (!target.startsWith(src + path.sep) || !fs.existsSync(target)) return route.fulfill({ status: 404, body: "Not found" });
      return route.fulfill({ path: target });
    });
    await portal.goto("http://portfolio.test/projects/pcb-visual-inspection/research-portal/", { waitUntil: "networkidle" });
    assert.equal(await portal.title(), "PCB Visual Inspection Studio");
    assert.equal(await portal.locator("h1").textContent(), "PCB Visual Inspection Studio");
    assert.equal(await portal.locator(".material-symbols-outlined:visible").count(), 0);
    assert.equal(await portal.locator("#actions a[href*='PCB-Visual-Inspection-Studio']").count(), 0);
    assert.equal(await portal.locator("#actions a[href^='#'][target='_blank']").count(), 0);
    assert.equal(await portal.locator("body").evaluate((element) => element.scrollWidth <= window.innerWidth + 1), true);
    const portalGallery = portal.locator(".evidence-gallery").first();
    assert.equal(await portalGallery.locator("figure:visible").count(), 1);
    const portalCount = portal.locator(".evidence-gallery-count").first();
    const firstCount = await portalCount.textContent();
    await portal.locator(".evidence-gallery-next").first().click();
    assert.notEqual(await portalCount.textContent(), firstCount);
    for (const gallery of await portal.locator(".evidence-gallery").all()) {
      assert.equal(await gallery.evaluate((element) => element.scrollWidth <= element.clientWidth + 1), true);
    }
    await portalGallery.locator("figure:visible [data-lightbox]").click();
    assert.equal(await portal.locator("#publication-lightbox").evaluate((element) => element.open), true);
    await portal.locator(".evidence-lightbox-next").click();
    await portal.keyboard.press("Escape");
    assert.deepEqual(portalErrors, []);
    await portal.close();
    console.log("PASS: actual standalone PCB portal, 390px: gallery, no clipping, modal, Escape");
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
