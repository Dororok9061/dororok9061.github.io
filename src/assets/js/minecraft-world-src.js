import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { KTX2Loader } from "three/examples/jsm/loaders/KTX2Loader.js";

const ASSET_ROOT = "/assets/minecraft-world";
const clamp = THREE.MathUtils.clamp;
const MIN_LOADING_MS = 2200;

const sectionData = [
  {
    id: "intro",
    at: 0.02,
    kicker: "Research Blocks",
    title: "류형록 Engineering Research World",
    body: "기존 dororok9061.github.io 자료 위에 Minecraft 3D 템플릿을 겹쳐, 논문·프로젝트·블로그·Notion·GitHub로 바로 이어지는 입구를 만들었습니다.",
    chips: ["Radar", "Vision AI", "Embedded", "FPGA", "PCB"],
    href: "/blog/start-here/",
    label: "Research Blocks Hub",
    subtitle: "Homepage · GitHub · Notion",
    position: [1.25, 66.6, 38.2],
    color: "#f2c760"
  },
  {
    id: "projects",
    at: 0.34,
    kicker: "Selected Works",
    title: "프로젝트와 논문형 Case Study",
    body: "FMCW Radar, PCB Visual Inspection, FPGA Delay Logic, PPG-HRV, Drowsiness Monitor를 한 방 안의 액자로 배치했습니다.",
    chips: ["FMCW", "PCB Inspection", "PPG-HRV", "FPGA DV"],
    href: "/projects/",
    label: "Selected Works",
    subtitle: "Open project cases",
    position: [-9.0, 70.35, -3.7],
    color: "#6fb6d8"
  },
  {
    id: "about",
    at: 0.58,
    kicker: "About / Focus",
    title: "Radar · Vision AI · Sensor Fusion",
    body: "학부 연구, 전공 과제, 센서·신호처리·회로설계 기록을 직무 포트폴리오 흐름으로 묶었습니다.",
    chips: ["R&D 2027", "CES 2027", "Dankook", "H&S Lab"],
    href: "/about/",
    label: "About Ryu",
    subtitle: "Focus and profile",
    position: [-8.25, 68.95, 4.95],
    color: "#a7d06f"
  },
  {
    id: "blog",
    at: 0.72,
    kicker: "Blog Taxonomy",
    title: "주제별·일수별 공부 기록",
    body: "전공, RF/mmWave, STM32, PCB 설계, OUTTA AI, 방산, 반도체 회로설계 글을 하위 카테고리와 일차별 로그로 정리합니다.",
    chips: ["RF/mmWave", "STM32", "OUTTA", "PADS/KiCad"],
    href: "/blog/",
    label: "Study Logs",
    subtitle: "Topic and day routes",
    position: [-2.15, 70.4, 7.25],
    color: "#ef8f62"
  },
  {
    id: "resources",
    at: 0.88,
    kicker: "Source Routes",
    title: "GitHub · Notion · PaperBanana",
    body: "공개 GitHub Pages는 이 도메인을 유지하고, Notion 허브와 PaperBanana figure workflow는 별도 경로로 이어집니다.",
    chips: ["GitHub Pages", "Public Notion", "Paper Figures"],
    href: "https://github.com/Dororok9061",
    label: "GitHub · Notion",
    subtitle: "Code, papers, figures",
    position: [-3.05, 69.65, 0.9],
    color: "#d9b179"
  }
];

const imageCards = [
  {
    title: "FMCW Radar",
    image: "/assets/minecraft-world/images/mmwave-signal-overview.png",
    href: "/projects/fmcw-radar/",
    position: [-10.55, 69.45, -3.72],
    scale: [1.15, 0.78, 1]
  },
  {
    title: "PCB Vision AI",
    image: "/assets/minecraft-world/images/pcb-inspection-heatmap.png",
    href: "/projects/pcb-visual-inspection/",
    position: [-9.55, 69.45, -3.72],
    scale: [1.15, 0.78, 1]
  },
  {
    title: "CICS HRV",
    image: "/assets/minecraft-world/images/cics-hrv-timeseries.jpg",
    href: "/publications/cics25-cnn-hrv/",
    position: [-8.55, 69.45, -3.72],
    scale: [1.15, 0.78, 1]
  },
  {
    title: "OUTTA AI",
    image: "/assets/minecraft-world/images/outta-deep-learning.png",
    href: "/learning/bootcamps/outta-basic-2024/",
    position: [-7.55, 69.45, -3.72],
    scale: [1.15, 0.78, 1]
  },
  {
    title: "PCB / KiCad",
    image: "/assets/minecraft-world/images/pcb-kicad-board.jpg",
    href: "/coursework/",
    position: [-8.55, 68.18, 4.7],
    scale: [1.55, 1.08, 1]
  }
];

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
  "ExtrasT-transformed.glb",
  "ExtrasTwoT-transformed.glb",
  "ExtrasThreeT-v1.glb",
  "FrontGrassT-transformed.glb",
  "GrassBlocksT-transformed.glb",
  "GrassSidesT-transformed.glb",
  "MobsT-transformed.glb"
];

const modelPlacements = {
  "HouseT-transformed.glb": [
    ["house_Baked", [-4.55, 71.054, 0.595], [Math.PI / 2, 0, 0]]
  ],
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
  "ExtrasTwoT-transformed.glb": [
    ["extras_two_Baked", [-8.228, 64.814, 1.892], [Math.PI / 2, 0, 0]]
  ],
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

const roots = document.querySelectorAll("[data-minecraft-world]");
roots.forEach((root) => startWorld(root));

function startWorld(root) {
  const canvas = root.querySelector("[data-minecraft-world-canvas]");
  const fallback = root.querySelector("[data-minecraft-fallback]");
  const enterButton = root.querySelector("[data-minecraft-enter]");
  const progressBar = root.querySelector("[data-minecraft-progress-bar]");
  const progressWrap = root.querySelector("[data-minecraft-progress]");
  const percentLabel = root.querySelector("[data-minecraft-percent]");
  const audioToggle = root.querySelector("[data-minecraft-audio-toggle]");
  const audioLabel = root.querySelector("[data-minecraft-audio-label]");
  const meter = root.querySelector("[data-minecraft-meter]");
  const hud = {
    kicker: root.querySelector("[data-minecraft-section-kicker]"),
    title: root.querySelector("[data-minecraft-section-title]"),
    body: root.querySelector("[data-minecraft-section-body]"),
    chips: root.querySelector("[data-minecraft-section-chips]"),
    link: root.querySelector("[data-minecraft-section-link]")
  };

  const state = {
    entered: false,
    progress: 0,
    targetProgress: 0,
    mouseOffset: new THREE.Vector2(),
    isDragging: false,
    lastPointerY: 0,
    pointerMoved: 0,
    activeId: "",
    audioEnabled: true,
    doorState: "closed",
    door: null,
    animationId: 0,
    assetsReady: false,
    enterShown: false,
    loadingPercentage: 0
  };

  const audio = createAudio();

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: false,
      powerPreference: "high-performance"
    });
  } catch (error) {
    showFallback(root, fallback);
    return;
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x101110);

  const cameraGroup = new THREE.Group();
  scene.add(cameraGroup);

  const camera = new THREE.PerspectiveCamera(70, 1, 0.1, 400);
  cameraGroup.add(camera);

  const worldGroup = new THREE.Group();
  scene.add(worldGroup);

  const hotspotGroup = new THREE.Group();
  scene.add(hotspotGroup);

  const hotspots = [];
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  const cameraCurve = new THREE.CatmullRomCurve3(cameraPoints, true);
  const rotationBuffer = rotationTargets[0].quaternion.clone();

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

  const tickLoading = () => {
    const elapsed = performance.now() - loadingStartedAt;
    const simulated = Math.min(99, Math.round((elapsed / MIN_LOADING_MS) * 100));
    const percentage = state.assetsReady ? 100 : Math.max(state.loadingPercentage, simulated);
    updateLoading(percentage, progressBar, percentLabel);
    if (!state.enterShown) {
      window.requestAnimationFrame(tickLoading);
    }
  };

  const showEnterButton = () => {
    state.enterShown = true;
    root.classList.add("is-loaded");
    updateLoading(100, progressBar, percentLabel);
    if (enterButton) {
      enterButton.hidden = false;
    }
    window.setTimeout(() => {
      if (!state.entered) {
        return;
      }
      if (progressWrap) {
        progressWrap.hidden = true;
      }
      if (percentLabel) {
        percentLabel.hidden = true;
      }
    }, 180);
  };

  tickLoading();

  const textureLoader = new THREE.TextureLoader(manager);
  const cubeLoader = new THREE.CubeTextureLoader(manager).setPath(`${ASSET_ROOT}/cubemap/`);
  cubeLoader.load(["px.webp", "nx.webp", "py.webp", "ny.webp", "pz.webp", "nz.webp"], (texture) => {
    texture.colorSpace = THREE.SRGBColorSpace;
    scene.background = texture;
    scene.environment = texture;
  });

  const ktx2Loader = new KTX2Loader(manager)
    .setTranscoderPath(`${ASSET_ROOT}/basis/`)
    .detectSupport(renderer);

  const gltfLoader = new GLTFLoader(manager);
  gltfLoader.setKTX2Loader(ktx2Loader);

  addResearchRoom(worldGroup, textureLoader);
  addResearchSprites(hotspotGroup, hotspots, textureLoader);
  loadModels(gltfLoader, worldGroup, state);

  updateHud(sectionData[0], hud);
  resize(root, renderer, camera);

  enterButton?.addEventListener("click", () => {
    state.entered = true;
    root.classList.add("is-entered");
    if (enterButton) {
      enterButton.hidden = true;
    }
    if (progressWrap) {
      progressWrap.hidden = true;
    }
    if (percentLabel) {
      percentLabel.hidden = true;
    }
    play(audio.buttonClick, state);
    play(audio.music, state);
  });

  audioToggle?.addEventListener("click", () => {
    state.audioEnabled = !state.audioEnabled;
    if (audioToggle) {
      audioToggle.setAttribute("aria-pressed", String(state.audioEnabled));
    }
    if (audioLabel) {
      audioLabel.textContent = state.audioEnabled ? "Sound On" : "Sound Off";
    }
    if (state.audioEnabled && state.entered) {
      play(audio.music, state);
    } else {
      audio.music.pause();
    }
  });

  root.addEventListener("wheel", (event) => {
    if (!state.entered) {
      return;
    }
    const direction = Math.sign(event.deltaY);
    const atEnd = state.targetProgress >= 0.985 && direction > 0;
    const atStart = state.targetProgress <= 0.015 && direction < 0;
    if (!atEnd && !atStart) {
      event.preventDefault();
    }
    state.targetProgress = clamp(
      state.targetProgress + direction * 0.07 * Math.min(Math.abs(event.deltaY) / 90, 1),
      0,
      1
    );
  }, { passive: false });

  root.addEventListener("pointerdown", (event) => {
    if (!state.entered) {
      return;
    }
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

    if (!state.isDragging || !state.entered) {
      return;
    }
    const deltaY = event.clientY - state.lastPointerY;
    state.pointerMoved += Math.abs(deltaY);
    state.targetProgress = clamp(state.targetProgress + Math.sign(deltaY) * 0.01, 0, 1);
    state.lastPointerY = event.clientY;
  });

  root.addEventListener("pointerup", (event) => {
    state.isDragging = false;
    if (!state.entered || state.pointerMoved > 6) {
      return;
    }
    const match = pickHotspot(event, root, camera, hotspots, raycaster, pointer);
    if (match?.userData?.href) {
      play(audio.buttonClick, state);
      window.location.assign(match.userData.href);
    }
  });

  window.addEventListener("keydown", (event) => {
    if (!state.entered) {
      return;
    }
    if (event.key === "ArrowDown" || event.key === "PageDown") {
      state.targetProgress = clamp(state.targetProgress + 0.055, 0, 1);
    }
    if (event.key === "ArrowUp" || event.key === "PageUp") {
      state.targetProgress = clamp(state.targetProgress - 0.055, 0, 1);
    }
  });

  window.addEventListener("resize", () => resize(root, renderer, camera));

  const animate = () => {
    state.animationId = requestAnimationFrame(animate);

    state.progress = THREE.MathUtils.lerp(state.progress, state.targetProgress, 0.09);
    const point = cameraCurve.getPoint(state.progress);
    cameraGroup.position.lerp(point, 0.1);
    camera.position.x = THREE.MathUtils.lerp(camera.position.x, state.mouseOffset.x, 0.1);
    camera.position.y = THREE.MathUtils.lerp(camera.position.y, -state.mouseOffset.y, 0.1);
    camera.position.z = 0;
    rotationBuffer.slerp(getRotation(state.progress), 0.1);
    cameraGroup.quaternion.copy(rotationBuffer);

    updateDoor(state, audio);
    updateActiveSection(state, hud, meter);
    pulseHotspots(hotspots, state.progress, performance.now() * 0.001);

    renderer.render(scene, camera);
  };

  animate();
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
  if (!state.audioEnabled || !sound) {
    return;
  }
  try {
    sound.currentTime = sound.loop ? sound.currentTime : 0;
    const pending = sound.play();
    if (pending?.catch) {
      pending.catch(() => {});
    }
  } catch (_error) {
    // Browsers may reject audio until an explicit user gesture.
  }
}

function updateLoading(percentage, bar, label) {
  if (bar) {
    bar.style.width = `${percentage}%`;
  }
  if (label) {
    label.textContent = `${percentage}%`;
  }
}

function resize(root, renderer, camera) {
  const width = Math.max(root.clientWidth, 320);
  const height = Math.max(root.clientHeight, 320);
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function loadModels(loader, group, state) {
  modelFiles.forEach((file) => {
    loader.load(
      `${ASSET_ROOT}/models/${file}`,
      (gltf) => {
        const model = createPlacedModel(file, gltf.scene);
        model.traverse((object) => {
          if (object.isMesh) {
            object.frustumCulled = true;
            if (object.material) {
              object.material = Array.isArray(object.material)
                ? object.material.map((material) => toBakedMaterial(material))
                : toBakedMaterial(object.material);
            }
          }
          if (object.name === "door") {
            state.door = object;
          }
        });
        group.add(model);
      },
      undefined,
      () => {}
    );
  });
}

function createPlacedModel(file, scene) {
  const placements = modelPlacements[file];
  if (!placements) {
    return scene;
  }
  const byName = new Map();
  scene.traverse((object) => {
    if (object.name) {
      byName.set(object.name, object);
    }
  });

  const group = new THREE.Group();
  group.name = file.replace(/\.glb$/i, "");
  placements.forEach(([name, position, rotation]) => {
    const object = byName.get(name);
    if (!object?.isMesh) {
      return;
    }
    const mesh = new THREE.Mesh(object.geometry, object.material);
    mesh.name = object.name;
    mesh.position.set(...position);
    mesh.rotation.set(...rotation);
    mesh.scale.copy(object.scale);
    group.add(mesh);
  });
  return group;
}

function toBakedMaterial(material) {
  const map = material.emissiveMap || material.map || null;
  if (map) {
    map.colorSpace = THREE.SRGBColorSpace;
  }
  const bakedMaterial = new THREE.MeshBasicMaterial({
    map,
    color: material.color || new THREE.Color(0xffffff),
    transparent: true,
    opacity: material.opacity,
    alphaMap: material.alphaMap || null,
    alphaTest: material.alphaTest || 0.55,
    side: material.side
  });
  bakedMaterial.name = material.name || "minecraft-baked";
  bakedMaterial.toneMapped = false;
  return bakedMaterial;
}

function addResearchRoom(group, textureLoader) {
  const wallMaterial = makePixelMaterial("#b48a61", "#9a714c", 0.18);
  const woodMaterial = makePixelMaterial("#8f541f", "#6d3e16", 0.25);
  const darkWoodMaterial = makePixelMaterial("#4a2610", "#2b1608", 0.32);
  const floorMaterial = makePixelMaterial("#8a551f", "#6c3f16", 0.16);
  const frameMaterial = new THREE.MeshBasicMaterial({ color: "#17120d" });
  const lanternMaterial = new THREE.MeshBasicMaterial({ color: "#ffd98c" });
  const plantMaterial = new THREE.MeshBasicMaterial({ color: "#5c8f36" });
  const potMaterial = new THREE.MeshBasicMaterial({ color: "#a45524" });

  addBlock(group, [-8.7, 67.04, -0.2], [7.4, 0.18, 9.6], floorMaterial);
  addBlock(group, [-8.7, 69.35, -4.78], [7.4, 4.15, 0.2], wallMaterial);
  addBlock(group, [-8.7, 69.35, 4.85], [7.4, 4.15, 0.2], wallMaterial);
  addBlock(group, [-12.42, 69.35, 0.05], [0.22, 4.15, 9.6], wallMaterial);
  addBlock(group, [-5.02, 69.35, 0.05], [0.22, 4.15, 9.6], wallMaterial);
  addBlock(group, [-8.7, 71.42, 0.05], [7.4, 0.2, 9.6], darkWoodMaterial);

  addBlock(group, [-8.7, 67.55, -4.25], [6.65, 0.62, 0.62], woodMaterial);
  addBlock(group, [-8.7, 68.05, -4.25], [6.65, 0.2, 0.62], darkWoodMaterial);
  for (let i = 0; i < 18; i += 1) {
    const hue = ["#b33a2d", "#d5b340", "#2d6aa0", "#4b8c45", "#8a3f8f"][i % 5];
    addBlock(group, [-11.65 + i * 0.34, 67.82, -4.03], [0.2, 0.46, 0.1], new THREE.MeshBasicMaterial({ color: hue }));
  }

  addBlock(group, [-8.6, 67.54, 4.28], [6.8, 0.42, 0.72], woodMaterial);
  addBlock(group, [-8.6, 67.95, 4.24], [6.8, 0.22, 0.72], darkWoodMaterial);
  addBlock(group, [-6.0, 68.34, 4.2], [0.52, 0.64, 0.52], lanternMaterial);
  addBlock(group, [-6.0, 68.82, 4.2], [0.44, 0.18, 0.44], new THREE.MeshBasicMaterial({ color: "#8cb5d9" }));
  addPlant(group, [-11.15, 68.15, 4.26], potMaterial, plantMaterial);
  addPlant(group, [-5.85, 68.15, -4.25], potMaterial, plantMaterial);

  const selectedSign = makeWallSign("Selected Works", "FMCW Radar · PCB Vision · HRV · OUTTA AI", "#6fb6d8");
  selectedSign.position.set(-8.7, 70.2, -4.53);
  selectedSign.scale.set(2.9, 0.82, 1);
  group.add(selectedSign);

  const aboutSign = makeWallSign("About Ryu", "Radar · Vision AI · Embedded · PCB Design", "#a7d06f");
  aboutSign.position.set(-7.15, 69.9, 4.62);
  aboutSign.scale.set(2.75, 0.78, 1);
  group.add(aboutSign);

  const aboutImages = [
    ["pcb-kicad-board.jpg", -7.85, 68.92, 4.63],
    ["paper-session.jpg", -6.55, 68.92, 4.63]
  ];
  aboutImages.forEach(([image, x, y, z]) => {
    addBlock(group, [x, y, z - 0.02], [1.02, 0.72, 0.06], frameMaterial);
    const plane = makeImagePlane(textureLoader, image, [0.9, 0.6]);
    plane.position.set(x, y, z + 0.02);
    group.add(plane);
  });

  const images = [
    ["mmwave-signal-overview.png", -10.95, 69.25, -4.52],
    ["pcb-inspection-heatmap.png", -9.45, 69.25, -4.52],
    ["cics-hrv-timeseries.jpg", -7.95, 69.25, -4.52],
    ["outta-deep-learning.png", -6.45, 69.25, -4.52]
  ];
  images.forEach(([image, x, y, z]) => {
    addBlock(group, [x, y, z - 0.02], [1.12, 0.78, 0.06], frameMaterial);
    const plane = makeImagePlane(textureLoader, image, [1.0, 0.66]);
    plane.position.set(x, y, z + 0.02);
    group.add(plane);
  });
}

function addBlock(group, position, scale, material) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), material);
  mesh.position.set(...position);
  mesh.scale.set(...scale);
  mesh.frustumCulled = false;
  group.add(mesh);
  return mesh;
}

function addPlant(group, position, potMaterial, plantMaterial) {
  addBlock(group, position, [0.5, 0.38, 0.5], potMaterial);
  addBlock(group, [position[0], position[1] + 0.44, position[2]], [0.14, 0.75, 0.14], plantMaterial);
  addBlock(group, [position[0] - 0.25, position[1] + 0.78, position[2]], [0.5, 0.14, 0.14], plantMaterial);
  addBlock(group, [position[0] + 0.25, position[1] + 0.95, position[2]], [0.48, 0.14, 0.14], plantMaterial);
}

function makePixelMaterial(base, stripe, density) {
  const canvas = document.createElement("canvas");
  canvas.width = 64;
  canvas.height = 64;
  const context = canvas.getContext("2d");
  context.fillStyle = base;
  context.fillRect(0, 0, 64, 64);
  context.fillStyle = stripe;
  for (let y = 0; y < 64; y += 16) {
    context.fillRect(0, y + 4, 64, 4);
  }
  for (let x = 0; x < 64; x += 16) {
    if (Math.random() < density) {
      context.fillRect(x, 0, 4, 64);
    }
  }
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2, 2);
  texture.magFilter = THREE.NearestFilter;
  texture.minFilter = THREE.NearestFilter;
  return new THREE.MeshBasicMaterial({ map: texture });
}

function makeImagePlane(textureLoader, image, scale) {
  const texture = textureLoader.load(resolveWorldImage(image));
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.magFilter = THREE.NearestFilter;
  const material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(scale[0], scale[1]), material);
  return mesh;
}

function makeWallSign(title, subtitle, accent) {
  const sprite = makeTextSprite(title, subtitle, accent);
  sprite.material.depthTest = false;
  return sprite;
}

function addResearchSprites(group, hotspots, textureLoader) {
  sectionData.forEach((section) => {
    const sprite = makeTextSprite(section.label, section.subtitle, section.color);
    sprite.position.set(...section.position);
    sprite.scale.set(4.0, 1.45, 1);
    sprite.userData.href = section.href;
    sprite.userData.sectionId = section.id;
    group.add(sprite);
    hotspots.push(sprite);
  });

  imageCards.forEach((card) => {
    const texture = textureLoader.load(resolveWorldImage(card.image));
    texture.colorSpace = THREE.SRGBColorSpace;
    const material = new THREE.SpriteMaterial({
      map: texture,
      transparent: false,
      depthTest: false
    });
    const sprite = new THREE.Sprite(material);
    sprite.position.set(...card.position);
    sprite.scale.set(...card.scale);
    sprite.userData.href = card.href;
    sprite.userData.title = card.title;
    group.add(sprite);
    hotspots.push(sprite);
  });
}

function makeTextSprite(title, subtitle, accent) {
  const canvas = document.createElement("canvas");
  canvas.width = 1024;
  canvas.height = 384;
  const context = canvas.getContext("2d");
  context.fillStyle = "#8a5523";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = "#6e401a";
  for (let y = 32; y < canvas.height; y += 70) {
    context.fillRect(0, y, canvas.width, 10);
  }
  context.strokeStyle = "#2a1608";
  context.lineWidth = 18;
  context.strokeRect(12, 12, canvas.width - 24, canvas.height - 24);
  context.fillStyle = accent;
  context.fillRect(36, 38, 18, canvas.height - 76);
  context.fillStyle = "#1c1208";
  context.font = '700 70px "Minecraft World", monospace';
  context.textBaseline = "top";
  context.fillText(title, 82, 86);
  context.font = '400 38px "Minecraft World", monospace';
  context.fillText(subtitle, 86, 188);

  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  const material = new THREE.SpriteMaterial({
    map: texture,
    transparent: true,
    depthTest: false
  });
  return new THREE.Sprite(material);
}

function resolveWorldImage(image) {
  return image.startsWith("/") ? image : `${ASSET_ROOT}/images/${image}`;
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
  if (!state.door) {
    return;
  }

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

function updateActiveSection(state, hud, meter) {
  const active = sectionData.reduce((best, current) => {
    return Math.abs(current.at - state.progress) < Math.abs(best.at - state.progress) ? current : best;
  }, sectionData[0]);

  if (active.id === state.activeId) {
    if (meter) {
      meter.style.width = `${Math.round(state.progress * 100)}%`;
    }
    return;
  }

  state.activeId = active.id;
  updateHud(active, hud);
}

function updateHud(section, hud) {
  if (hud.kicker) {
    hud.kicker.textContent = section.kicker;
  }
  if (hud.title) {
    hud.title.textContent = section.title;
  }
  if (hud.body) {
    hud.body.textContent = section.body;
  }
  if (hud.link) {
    hud.link.href = section.href;
    hud.link.textContent = section.href.startsWith("http") ? "Open GitHub" : "Open Route";
  }
  if (hud.chips) {
    hud.chips.replaceChildren();
    section.chips.forEach((chip) => {
      const span = document.createElement("span");
      span.textContent = chip;
      hud.chips.append(span);
    });
  }
}

function pulseHotspots(hotspots, progress, elapsed) {
  hotspots.forEach((hotspot) => {
    const target = sectionData.find((section) => section.id === hotspot.userData.sectionId);
    const near = target ? Math.max(0, 1 - Math.abs(target.at - progress) * 9) : 0.28;
    const pulse = 1 + near * (0.08 + Math.sin(elapsed * 3.4) * 0.025);
    hotspot.scale.x = THREE.MathUtils.lerp(hotspot.scale.x, hotspot.userData.baseScaleX || hotspot.scale.x, 0.1);
    hotspot.scale.y = THREE.MathUtils.lerp(hotspot.scale.y, hotspot.userData.baseScaleY || hotspot.scale.y, 0.1);
    if (!hotspot.userData.baseScaleX) {
      hotspot.userData.baseScaleX = hotspot.scale.x;
      hotspot.userData.baseScaleY = hotspot.scale.y;
    }
    hotspot.scale.x = hotspot.userData.baseScaleX * pulse;
    hotspot.scale.y = hotspot.userData.baseScaleY * pulse;
  });
}

function pickHotspot(event, root, camera, hotspots, raycaster, pointer) {
  const rect = root.getBoundingClientRect();
  pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = -(((event.clientY - rect.top) / rect.height) * 2 - 1);
  raycaster.setFromCamera(pointer, camera);
  const intersections = raycaster.intersectObjects(hotspots, false);
  return intersections[0]?.object;
}

function showFallback(root, fallback) {
  root.classList.add("is-entered");
  if (fallback) {
    fallback.hidden = false;
  }
}
