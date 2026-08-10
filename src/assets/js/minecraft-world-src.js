import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { KTX2Loader } from "three/examples/jsm/loaders/KTX2Loader.js";

const ASSET_ROOT = "/assets/minecraft-world";
const MIN_LOADING_MS = 2200;
const clamp = THREE.MathUtils.clamp;

const cameraPoints = [
  [2, 65, 47.5],
  [1.4, 65, 39],
  [-2, 70, 17],
  [-2.6, 68.5, 4.8],
  [-2.45, 67.9, 0],
  [-3.42, 68.9, 0.145],
  [-8.05, 69.36, -0.875],
  [-10.05, 69.36, -0.88],
  [-7.148, 69.22, 0.37],
  [-9, 69.2, 1.22],
  [-7.8, 68.72, 3.04],
  [-8.01, 69.97, -1.72],
  [-3, 68.21, 0.308],
  [-2.4, 68.47, 7.1],
  [-2, 70, 17],
  [1.4, 65, 39]
].map((point) => new THREE.Vector3(...point));

const rotationTargets = [
  [0, [-0.12, 0.17, 0.02]],
  [0.14, [-0.11, 0.003, 0]],
  [0.2, [-0.11, 0.003, 0]],
  [0.24, [0.173, 1.042, -0.15]],
  [0.365, [0.023, 0.024, -0.001]],
  [0.42, [0.177, 0.972, -0.147]],
  [0.5, [-2.725, 1.02, 2.782]],
  [0.56, [-2.9, -0.069, -3.125]],
  [0.62, [-2.76, 0.21, 3.06]],
  [0.715, [-0.467, -0.681, -0.308]],
  [0.735, [-0.043, 0.012, 0.0005]],
  [0.85, [-0.043, 0.012, 0.0005]],
  [1, [-0.12, 0.17, 0.02]]
].map(([progress, rotation]) => ({
  progress,
  quaternion: new THREE.Quaternion().setFromEuler(new THREE.Euler(...rotation))
}));

const modelFiles = [
  "HouseT-transformed.glb",
  "BackGrassT-transformed.glb",
  "DetailT-v1.glb",
  "ExtrasT-transformed.glb",
  "ExtrasTwoT-transformed.glb",
  "ExtrasThreeT-v1.glb",
  "FrontGrassT-transformed.glb",
  "GrassBlocksT-transformed.glb",
  "GrassSidesT-transformed.glb",
  "MobsT-transformed.glb"
];

const modelPlacements = {
  "HouseT-transformed.glb": [["house_Baked", [-4.55, 71.054, 0.595], [Math.PI / 2, 0, 0]]],
  "BackGrassT-transformed.glb": [
    ["grass_back_Baked", [-6.777, 70.277, -25.075], [Math.PI / 2, 0, 0]],
    ["shrubs_Baked", [-6.036, 77.158, -55.567], [Math.PI / 2, 0, 0]],
    ["water_Baked", [-5.297, 60.772, 19.029], [Math.PI / 2, 0, 0]],
    ["actual_water_baked", [-5.297, 60.772, 19.029], [Math.PI / 2, 0, 0]]
  ],
  "DetailT-v1.glb": [
    ["detail_Baked", [-6.46, 69.669, -1.148], [Math.PI / 2, 0, 0]],
    ["About_Me_Pictures", [-8.164, 68.036, 4.408], [Math.PI / 2, 0, 0]],
    ["Project_One", [-10.528, 69.422, -4.13], [Math.PI / 2, 0, 0]],
    ["Project_Two", [-9.532, 69.422, -4.13], [Math.PI / 2, 0, 0]],
    ["Project_Three", [-8.536, 69.422, -4.13], [Math.PI / 2, 0, 0]],
    ["Project_Four", [-7.541, 69.422, -4.13], [Math.PI / 2, 0, 0]],
    ["about_me_text", [-8.524, 68.356, 4.727], [Math.PI / 2, 0, 0]]
  ],
  "ExtrasTwoT-transformed.glb": [["extras_two_Baked", [-8.228, 64.814, 1.892], [Math.PI / 2, 0, 0]]],
  "ExtrasThreeT-v1.glb": [
    ["extras_three_Baked", [0.597, 68.353, 2.812], [Math.PI / 2, 0, 0]],
    ["door", [-2.935, 67.848, 0.906], [Math.PI / 2, 0, 0]]
  ],
  "FrontGrassT-transformed.glb": [
    ["grass_center_Baked", [-6.777, 70.277, -25.075], [Math.PI / 2, 0, 0]],
    ["grass_right_Baked", [-6.777, 70.277, -25.075], [Math.PI / 2, 0, 0]],
    ["grass_left_Baked", [-6.777, 70.277, -25.075], [Math.PI / 2, 0, 0]]
  ],
  "GrassBlocksT-transformed.glb": [
    ["grass_block_first_half_right_Baked", [5.421, 67.409, -0.825], [Math.PI / 2, 0, 0]],
    ["grass_block_first_half_left_Baked", [5.421, 67.409, -0.825], [Math.PI / 2, 0, 0]],
    ["grass_block_second_half_Baked", [5.421, 67.409, -0.825], [Math.PI / 2, 0, 0]],
    ["grass_block_third_half_Baked", [5.421, 67.409, -0.825], [Math.PI / 2, 0, 0]]
  ],
  "GrassSidesT-transformed.glb": [
    ["grass_side_back_Baked", [-8.02, 70.438, -24.962], [Math.PI / 2, 0, 0]],
    ["grass_side_front_Baked", [-8.02, 70.438, -24.962], [Math.PI / 2, 0, 0]]
  ]
};

const modalByMesh = {
  About_Me_Pictures: "about",
  Project_One: "fmcw",
  Project_Two: "pcb",
  Project_Three: "cics",
  Project_Four: "outta"
};

const portfolioCards = [
  ["fmcw", "/assets/minecraft-world/images/mmwave-signal-overview.png", [-10.528, 69.422, -4.02], [0.72, 0.54]],
  ["pcb", "/assets/minecraft-world/images/pcb-inspection-heatmap.png", [-9.532, 69.422, -4.02], [0.72, 0.54]],
  ["cics", "/assets/minecraft-world/images/cics-hrv-timeseries.jpg", [-8.536, 69.422, -4.02], [0.72, 0.54]],
  ["outta", "/assets/minecraft-world/images/outta-deep-learning.png", [-7.541, 69.422, -4.02], [0.72, 0.54]],
  ["about", "/assets/minecraft-world/images/pcb-kicad-board.jpg", [-8.164, 68.036, 4.52], [1.35, 0.84]]
];

const modalContent = {
  info: {
    title: "Minecraft Research Portfolio",
    image: "/assets/minecraft-world/images/hero-research-world.png",
    sections: [
      ["Template", "andrewwoan/woan-minecraft-folio의 로딩 화면, 카메라 경로, Blender GLB 모델, 사운드 구조를 기반으로 홈페이지 첫 화면을 구성했습니다."],
      ["Routes", "홈페이지의 기존 연구·프로젝트·블로그·논문·Notion·GitHub 자료는 아래 Jekyll 섹션과 3D 액자 모달에서 이어집니다."]
    ],
    actions: [
      ["GitHub", "https://github.com/Dororok9061"],
      ["Notion", "https://bronzed-dragonfly-3ca.notion.site/2025-257518ac7a59807c9193f243e059fb9a"],
      ["Blog", "/blog/"]
    ]
  },
  about: {
    title: "류형록",
    image: "/assets/minecraft-world/images/pcb-kicad-board.jpg",
    sections: [
      ["Focus", "Radar, Vision AI, Embedded, PCB 설계, STM32, RF/mmWave 학습 기록을 연구 포트폴리오 흐름으로 묶었습니다."],
      ["Current Direction", "방산·반도체 회로설계·센서 신호처리 직무와 연결되는 프로젝트, 과제, 논문 기록을 계속 정리합니다."]
    ],
    actions: [["About", "/about/"], ["Contact", "/contact/"]]
  },
  fmcw: {
    title: "FMCW Radar Cardiac Timing",
    image: "/assets/minecraft-world/images/mmwave-signal-overview.png",
    sections: [
      ["Problem", "ECG, SCG, Radar 기반 심장 타이밍을 한 흐름에서 비교하고 정리한 mmWave/RF 연구 기록입니다."],
      ["Materials", "FMCW radar, Infineon 계열 radar study, RF/mmWave 신호처리, 논문형 발표 자료를 함께 연결합니다."]
    ],
    actions: [["Open Project", "/projects/fmcw-radar/"], ["RF Blog", "/blog/category/rf-mmwave/"]]
  },
  pcb: {
    title: "PCB Visual Inspection",
    image: "/assets/minecraft-world/images/pcb-inspection-heatmap.png",
    sections: [
      ["Problem", "PCB 검사 이미지의 ROI 정렬, anomaly heatmap, mask, 리뷰 흐름을 공개 프로젝트 페이지로 정리했습니다."],
      ["Stack", "Python, OpenCV, PyTorch, PatchCore/FR-PatchCore, DINO 계열 특징 추출, GitHub Pages를 함께 사용합니다."]
    ],
    actions: [["Open Project", "/projects/pcb-visual-inspection/"], ["Research Portal", "/projects/pcb-visual-inspection/research-portal/"]]
  },
  cics: {
    title: "PPG-HRV Cognitive Load",
    image: "/assets/minecraft-world/images/cics-hrv-timeseries.jpg",
    sections: [
      ["Paper", "PPG 기반 HRV와 인지부하 분석을 CNN/Transformer 계열 모델 관점에서 정리한 CICS 발표 기록입니다."],
      ["Reuse", "논문, 포스터, 실험 기록, 코드 정리를 포트폴리오와 GitHub 자료로 이어둡니다."]
    ],
    actions: [["Publication", "/publications/cics25-cnn-hrv/"], ["Projects", "/projects/ppg-hrv/"]]
  },
  outta: {
    title: "OUTTA AI Study",
    image: "/assets/minecraft-world/images/outta-deep-learning.png",
    sections: [
      ["Study", "OUTTA 딥러닝 basic 부트캠프와 Kaggle/실습 기록을 주제별·일차별 학습 로그로 정리했습니다."],
      ["Direction", "Vision AI, 딥러닝 기초, 모델 평가, 실습 파일의 공개 가능한 부분만 학습 포트폴리오에 연결합니다."]
    ],
    actions: [["Learning", "/learning/bootcamps/outta-basic-2024/"], ["Blog", "/blog/"]]
  }
};

document.querySelectorAll("[data-minecraft-world]").forEach((root) => startWorld(root));

function startWorld(root) {
  const canvas = root.querySelector("[data-minecraft-world-canvas]");
  const fallback = root.querySelector("[data-minecraft-fallback]");
  const enterButton = root.querySelector("[data-minecraft-enter]");
  const progressBar = root.querySelector("[data-minecraft-progress-bar]");
  const progressWrap = root.querySelector("[data-minecraft-progress]");
  const percentLabel = root.querySelector("[data-minecraft-percent]");
  const audioToggle = root.querySelector("[data-minecraft-audio-toggle]");
  const audioLabel = root.querySelector("[data-minecraft-audio-label]");
  const infoButton = root.querySelector("[data-minecraft-info]");
  const modal = root.querySelector("[data-minecraft-modal]");
  const modalTitle = root.querySelector("[data-minecraft-modal-title]");
  const modalBody = root.querySelector("[data-minecraft-modal-body]");
  const modalCloseButtons = root.querySelectorAll("[data-minecraft-modal-close]");

  const state = {
    entered: false,
    progress: 0,
    targetProgress: 0,
    mouseOffset: new THREE.Vector2(),
    isDragging: false,
    lastPointerY: 0,
    pointerMoved: 0,
    audioEnabled: true,
    modalOpen: false,
    doorState: "closed",
    door: null,
    enterShown: false,
    assetsReady: false,
    loadingPercentage: 0
  };

  const audio = createAudio();
  const hotspots = [];
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
  } catch (_error) {
    showFallback(root, fallback);
    return;
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new THREE.Scene();
  const cameraGroup = new THREE.Group();
  const camera = new THREE.PerspectiveCamera(70, 1, 0.1, 400);
  const worldGroup = new THREE.Group();
  const overlayGroup = new THREE.Group();
  const cameraCurve = new THREE.CatmullRomCurve3(cameraPoints, true);
  const rotationBuffer = rotationTargets[0].quaternion.clone();

  scene.background = new THREE.Color(0x131311);
  cameraGroup.add(camera);
  scene.add(cameraGroup, worldGroup, overlayGroup);

  const manager = new THREE.LoadingManager();
  const loadingStartedAt = performance.now();
  manager.onProgress = (_url, loaded, total) => {
    state.loadingPercentage = total > 0 ? Math.min(99, Math.round((loaded / total) * 100)) : 0;
  };
  manager.onLoad = () => {
    state.assetsReady = true;
    state.loadingPercentage = 100;
    const elapsed = performance.now() - loadingStartedAt;
    window.setTimeout(showEnterButton, Math.max(450, MIN_LOADING_MS - elapsed));
  };

  const textureLoader = new THREE.TextureLoader(manager);
  const cubeLoader = new THREE.CubeTextureLoader(manager).setPath(`${ASSET_ROOT}/cubemap/`);
  cubeLoader.load(["px.webp", "nx.webp", "py.webp", "ny.webp", "pz.webp", "nz.webp"], (texture) => {
    texture.colorSpace = THREE.SRGBColorSpace;
    scene.background = texture;
    scene.environment = texture;
  });

  const ktx2Loader = new KTX2Loader(manager).setTranscoderPath(`${ASSET_ROOT}/basis/`).detectSupport(renderer);
  const gltfLoader = new GLTFLoader(manager);
  gltfLoader.setKTX2Loader(ktx2Loader);

  loadModels(gltfLoader, worldGroup, hotspots, state);
  addPortfolioCards(overlayGroup, hotspots, textureLoader);
  resize(root, renderer, camera);
  tickLoading();

  enterButton?.addEventListener("click", () => {
    state.entered = true;
    root.classList.add("is-entered");
    enterButton.hidden = true;
    if (progressWrap) progressWrap.hidden = true;
    if (percentLabel) percentLabel.hidden = true;
    play(audio.buttonClick, state);
    play(audio.music, state);
  });

  audioToggle?.addEventListener("click", () => {
    state.audioEnabled = !state.audioEnabled;
    audioToggle.setAttribute("aria-pressed", String(state.audioEnabled));
    if (audioLabel) audioLabel.textContent = state.audioEnabled ? "Sound On" : "Sound Off";
    if (state.audioEnabled && state.entered) play(audio.music, state);
    else audio.music.pause();
  });

  infoButton?.addEventListener("click", () => openModal("info", { modal, modalTitle, modalBody }, state, audio));
  modalCloseButtons.forEach((button) => button.addEventListener("click", () => closeModal({ modal }, state, audio)));

  root.addEventListener("wheel", (event) => {
    if (!state.entered || state.modalOpen) return;
    event.preventDefault();
    const direction = Math.sign(event.deltaY);
    state.targetProgress += direction * 0.12 * Math.min(Math.abs(event.deltaY) / 100, 1);
    if (state.targetProgress > 1) state.targetProgress = 0;
    if (state.targetProgress < 0) state.targetProgress = 1;
  }, { passive: false });

  root.addEventListener("pointerdown", (event) => {
    if (!state.entered || state.modalOpen) return;
    state.isDragging = true;
    state.pointerMoved = 0;
    state.lastPointerY = event.clientY;
    root.setPointerCapture?.(event.pointerId);
  });

  root.addEventListener("pointermove", (event) => {
    const bounds = root.getBoundingClientRect();
    const localX = bounds.width ? (event.clientX - bounds.left) / bounds.width : 0.5;
    const localY = bounds.height ? (event.clientY - bounds.top) / bounds.height : 0.5;
    state.mouseOffset.x = (localX * 2 - 1) * 0.25;
    state.mouseOffset.y = (localY * 2 - 1) * 0.25;

    if (!state.isDragging || !state.entered || state.modalOpen) return;
    const deltaY = event.clientY - state.lastPointerY;
    state.pointerMoved += Math.abs(deltaY);
    state.targetProgress = clamp(state.targetProgress + Math.sign(deltaY) * 0.006, 0, 1);
    state.lastPointerY = event.clientY;
  });

  root.addEventListener("pointerup", (event) => {
    state.isDragging = false;
    if (!state.entered || state.modalOpen || state.pointerMoved > 6) return;
    const match = pickHotspot(event, root, camera, hotspots, raycaster, pointer);
    if (match?.userData?.modalId) {
      openModal(match.userData.modalId, { modal, modalTitle, modalBody }, state, audio);
    }
  });

  window.addEventListener("keydown", (event) => {
    if (!state.entered) return;
    if (event.key === "Escape" && state.modalOpen) closeModal({ modal }, state, audio);
    if (state.modalOpen) return;
    if (event.key === "ArrowDown" || event.key === "PageDown") state.targetProgress = clamp(state.targetProgress + 0.055, 0, 1);
    if (event.key === "ArrowUp" || event.key === "PageUp") state.targetProgress = clamp(state.targetProgress - 0.055, 0, 1);
  });

  window.addEventListener("resize", () => resize(root, renderer, camera));

  function tickLoading() {
    const elapsed = performance.now() - loadingStartedAt;
    const simulated = Math.min(99, Math.round((elapsed / MIN_LOADING_MS) * 100));
    const percentage = state.assetsReady ? 100 : Math.max(state.loadingPercentage, simulated);
    updateLoading(percentage, progressBar, percentLabel);
    if (!state.enterShown) window.requestAnimationFrame(tickLoading);
  }

  function showEnterButton() {
    state.enterShown = true;
    root.classList.add("is-loaded");
    updateLoading(100, progressBar, percentLabel);
    if (enterButton) enterButton.hidden = false;
  }

  function animate() {
    requestAnimationFrame(animate);
    state.progress = THREE.MathUtils.lerp(state.progress, state.targetProgress, 0.1);
    const point = cameraCurve.getPoint(state.progress);
    cameraGroup.position.lerp(point, 0.1);
    camera.position.x = THREE.MathUtils.lerp(camera.position.x, state.mouseOffset.x, 0.1);
    camera.position.y = THREE.MathUtils.lerp(camera.position.y, -state.mouseOffset.y, 0.1);
    camera.position.z = 0;
    rotationBuffer.slerp(getRotation(state.progress), 0.1);
    cameraGroup.quaternion.copy(rotationBuffer);
    updateDoor(state, audio);
    renderer.render(scene, camera);
  }

  animate();
}

function loadModels(loader, group, hotspots, state) {
  modelFiles.forEach((file) => {
    loader.load(`${ASSET_ROOT}/models/${file}`, (gltf) => {
      const model = createPlacedModel(file, gltf.scene, hotspots);
      model.traverse((object) => {
        if (object.isMesh && object.material) {
          object.frustumCulled = true;
          object.material = Array.isArray(object.material)
            ? object.material.map((material) => toBakedMaterial(material))
            : toBakedMaterial(object.material);
        }
        if (object.name === "door") state.door = object;
      });
      group.add(model);
    });
  });
}

function createPlacedModel(file, scene, hotspots) {
  const placements = modelPlacements[file];
  if (!placements) return scene;

  const byName = new Map();
  scene.traverse((object) => {
    if (object.name) byName.set(object.name, object);
  });

  const group = new THREE.Group();
  group.name = file.replace(/\.glb$/i, "");
  placements.forEach(([name, position, rotation]) => {
    const source = byName.get(name);
    if (!source?.isMesh) return;
    const mesh = new THREE.Mesh(source.geometry, source.material);
    mesh.name = name;
    mesh.position.set(...position);
    mesh.rotation.set(...rotation);
    mesh.scale.copy(source.scale);
    if (modalByMesh[name]) {
      mesh.userData.modalId = modalByMesh[name];
      hotspots.push(mesh);
    }
    group.add(mesh);
  });
  return group;
}

function addPortfolioCards(group, hotspots, textureLoader) {
  portfolioCards.forEach(([modalId, image, position, scale]) => {
    const frame = new THREE.Mesh(
      new THREE.PlaneGeometry(scale[0] + 0.12, scale[1] + 0.12),
      new THREE.MeshBasicMaterial({ color: 0x131311, side: THREE.DoubleSide })
    );
    frame.position.set(position[0], position[1], position[2] - 0.015);
    group.add(frame);

    const texture = textureLoader.load(image);
    texture.colorSpace = THREE.SRGBColorSpace;
    texture.magFilter = THREE.NearestFilter;
    const plane = new THREE.Mesh(
      new THREE.PlaneGeometry(scale[0], scale[1]),
      new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide })
    );
    plane.position.set(...position);
    plane.userData.modalId = modalId;
    group.add(plane);
    hotspots.push(plane);
  });
}

function toBakedMaterial(material) {
  const map = material.emissiveMap || material.map || null;
  if (map) map.colorSpace = THREE.SRGBColorSpace;
  const baked = new THREE.MeshBasicMaterial({
    map,
    color: material.color || new THREE.Color(0xffffff),
    transparent: true,
    opacity: material.opacity,
    alphaMap: material.alphaMap || null,
    alphaTest: material.alphaTest || 0.55,
    side: material.side
  });
  baked.toneMapped = false;
  return baked;
}

function openModal(id, elements, state, audio) {
  const content = modalContent[id];
  if (!content || !elements.modal || !elements.modalTitle || !elements.modalBody) return;
  play(audio.buttonClick, state);
  state.modalOpen = true;
  elements.modal.hidden = false;
  elements.modalTitle.textContent = content.title;
  elements.modalBody.replaceChildren(renderModalContent(content));
}

function closeModal(elements, state, audio) {
  if (!elements.modal) return;
  play(audio.buttonClick, state);
  state.modalOpen = false;
  elements.modal.hidden = true;
}

function renderModalContent(content) {
  const fragment = document.createDocumentFragment();
  if (content.image) {
    const image = document.createElement("img");
    image.src = content.image;
    image.alt = content.title;
    fragment.append(image);
  }
  content.sections.forEach(([heading, body]) => {
    const h3 = document.createElement("h3");
    h3.textContent = heading;
    const p = document.createElement("p");
    p.textContent = body;
    fragment.append(h3, p);
  });
  if (content.actions?.length) {
    const actions = document.createElement("div");
    actions.className = "minecraft-world__modal-actions";
    content.actions.forEach(([label, href]) => {
      const link = document.createElement("a");
      link.className = "minecraft-world__modal-link";
      link.href = href;
      link.textContent = label;
      if (href.startsWith("http")) {
        link.target = "_blank";
        link.rel = "noopener noreferrer";
      }
      actions.append(link);
    });
    fragment.append(actions);
  }
  return fragment;
}

function createAudio() {
  const music = new Audio(`${ASSET_ROOT}/audio/music/Sweden.mp3`);
  music.loop = true;
  music.volume = 0.42;
  const buttonClick = new Audio(`${ASSET_ROOT}/audio/sfx/ButtonClick.mp3`);
  buttonClick.volume = 0.9;
  const doorOpening = new Audio(`${ASSET_ROOT}/audio/sfx/DoorOpening.mp3`);
  doorOpening.volume = 0.42;
  const doorClosing = new Audio(`${ASSET_ROOT}/audio/sfx/DoorClosing.mp3`);
  doorClosing.volume = 0.42;
  return { music, buttonClick, doorOpening, doorClosing };
}

function play(sound, state) {
  if (!state.audioEnabled || !sound) return;
  try {
    sound.currentTime = sound.loop ? sound.currentTime : 0;
    const pending = sound.play();
    if (pending?.catch) pending.catch(() => {});
  } catch (_error) {}
}

function updateLoading(percentage, bar, label) {
  if (bar) bar.style.width = `${percentage}%`;
  if (label) label.textContent = `${percentage}%`;
}

function resize(root, renderer, camera) {
  const width = Math.max(root.clientWidth, 320);
  const height = Math.max(root.clientHeight, 320);
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function getRotation(progress) {
  for (let index = 0; index < rotationTargets.length - 1; index += 1) {
    const start = rotationTargets[index];
    const end = rotationTargets[index + 1];
    if (progress >= start.progress && progress <= end.progress) {
      const factor = (progress - start.progress) / (end.progress - start.progress);
      const result = new THREE.Quaternion();
      result.slerpQuaternions(start.quaternion, end.quaternion, factor);
      return result;
    }
  }
  return rotationTargets[rotationTargets.length - 1].quaternion;
}

function updateDoor(state, audio) {
  if (!state.door) return;
  const shouldOpen = state.progress >= 0.17 && state.progress < 0.8;
  if (shouldOpen && state.doorState === "closed") {
    state.door.rotation.z = Math.PI / 2;
    state.doorState = "open";
    play(audio.doorOpening, state);
  }
  if (!shouldOpen && state.doorState === "open") {
    state.door.rotation.z = 0;
    state.doorState = "closed";
    play(audio.doorClosing, state);
  }
}

function pickHotspot(event, root, camera, hotspots, raycaster, pointer) {
  const rect = root.getBoundingClientRect();
  pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = -(((event.clientY - rect.top) / rect.height) * 2 - 1);
  raycaster.setFromCamera(pointer, camera);
  return raycaster.intersectObjects(hotspots, false)[0]?.object;
}

function showFallback(root, fallback) {
  root.classList.add("is-entered");
  if (fallback) fallback.hidden = false;
}
