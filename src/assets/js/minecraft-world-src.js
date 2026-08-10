const MIN_LOADING_MS = 1700;
const MAX_LOADING_MS = 4200;

document.querySelectorAll("[data-minecraft-entry]").forEach((root) => {
  const enterButton = root.querySelector("[data-minecraft-enter]");
  const progressBar = root.querySelector("[data-minecraft-progress-bar]");
  const percentLabel = root.querySelector("[data-minecraft-percent]");
  const soundToggle = document.querySelector("[data-minecraft-sound-toggle]");
  const soundLabel = document.querySelector("[data-minecraft-sound-label]");
  const startedAt = performance.now();
  const clickSound = new Audio("/assets/minecraft-world/audio/sfx/ButtonClick.mp3");
  const music = new Audio("/assets/minecraft-world/audio/music/Sweden.mp3");
  clickSound.volume = 0.72;
  music.loop = true;
  music.volume = 0.34;

  let pageReady = document.readyState === "complete";
  let complete = false;
  let soundEnabled = true;

  document.body.classList.add("is-home-gated");
  window.addEventListener("load", () => {
    pageReady = true;
  }, { once: true });

  const update = () => {
    const elapsed = performance.now() - startedAt;
    const timedOut = elapsed >= MAX_LOADING_MS;
    const canEnter = elapsed >= MIN_LOADING_MS && (pageReady || timedOut);
    const progress = canEnter ? 100 : Math.min(99, Math.round((elapsed / MIN_LOADING_MS) * 94));

    if (progressBar) progressBar.style.width = `${progress}%`;
    if (percentLabel) percentLabel.textContent = `${progress}%`;

    if (canEnter) {
      complete = true;
      root.classList.add("is-loaded");
      if (enterButton) enterButton.hidden = false;
      return;
    }

    requestAnimationFrame(update);
  };

  enterButton?.addEventListener("click", () => {
    if (!complete) return;
    play(clickSound);
    if (soundEnabled) play(music);

    root.classList.add("is-entered");
    document.body.classList.remove("is-home-gated");
    document.body.classList.add("minecraft-home-active");
    if (soundToggle) soundToggle.hidden = false;
    window.setTimeout(() => {
      root.hidden = true;
    }, 850);
  });

  soundToggle?.addEventListener("click", () => {
    soundEnabled = !soundEnabled;
    soundToggle.setAttribute("aria-pressed", String(soundEnabled));
    if (soundLabel) soundLabel.textContent = soundEnabled ? "Sound On" : "Sound Off";
    play(clickSound);
    if (soundEnabled) play(music);
    else music.pause();
  });

  update();
});

function play(sound) {
  try {
    sound.currentTime = sound.loop ? sound.currentTime : 0;
    const pending = sound.play();
    if (pending?.catch) pending.catch(() => {});
  } catch (_error) {}
}
