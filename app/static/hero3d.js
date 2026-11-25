// YojanaSetu — first-load 3D signature (J8).
// A real Three.js district skyline in the masthead: one bar per district
// (all 13, from the live /api/dashboard register), bar height = enrolment
// volume — the same data as the dashboard map below, in real 3D.
// Auto-initialises on load, no click needed. Drag to rotate; click a bar
// to filter the whole dashboard to that district (same action as the map
// blocks). Reduced-motion and no-WebGL fall back gracefully.
import * as THREE from 'three';

const canvas = document.getElementById('hero3d-canvas');
const fallback = document.getElementById('hero3d-fallback');
const caption = document.getElementById('hero3d-caption');
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const lowMotion = () =>
  document.body.classList.contains('low-motion') || reduced;

function showFallback(msg) {
  if (canvas) canvas.hidden = true;
  if (fallback) {
    fallback.hidden = false;
    if (msg) fallback.textContent = msg;
  }
}

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
} catch (err) {
  showFallback();
  throw err;
}
if (!renderer) { showFallback(); }
else {
  const wrap = document.getElementById('hero3d');
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a2a1f);

  const camera = new THREE.PerspectiveCamera(38, 2, 0.1, 100);
  camera.position.set(0, 4.4, 8.2);
  camera.lookAt(0, 1.1, 0);

  scene.add(new THREE.AmbientLight(0xffffff, 0.8));
  const key = new THREE.DirectionalLight(0xffffff, 1.5);
  key.position.set(4, 8, 5);
  scene.add(key);

  const skyline = new THREE.Group();
  scene.add(skyline);

  // Ground slab.
  const ground = new THREE.Mesh(
    new THREE.BoxGeometry(13.4, 0.18, 3.4),
    new THREE.MeshStandardMaterial({ color: 0x14213d, roughness: 0.6, metalness: 0.2 })
  );
  ground.position.y = -0.09;
  skyline.add(ground);

  const barMat = new THREE.MeshStandardMaterial({ color: 0x2e7d5b, roughness: 0.5, metalness: 0.1 });
  const selMat = new THREE.MeshStandardMaterial({ color: 0xc2410c, roughness: 0.5, metalness: 0.1 });
  const bars = []; // {mesh, district}
  let selectedMesh = null;

  async function build() {
    let counts = null;
    try {
      const res = await fetch('/api/dashboard');
      const data = await res.json();
      counts = data.dashboard && data.dashboard.by_district;
    } catch (err) { counts = null; }
    if (!counts || !Object.keys(counts).length) {
      showFallback('District enrolments could not be loaded — see the Officer Dashboard below.');
      return;
    }
    const entries = Object.entries(counts);
    const max = Math.max(1, ...entries.map(([, n]) => n));
    const step = 12.6 / Math.max(1, entries.length - 1 || 1);
    entries.forEach(([district, count], i) => {
      const h = 0.35 + (count / max) * 2.6;
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(0.72, h, 1.5), barMat);
      mesh.position.set(-6.3 + i * step, h / 2, 0);
      mesh.userData.district = district;
      mesh.userData.count = count;
      skyline.add(mesh);
      bars.push(mesh);
    });
    const top = entries.reduce((a, b) => (b[1] > a[1] ? b : a));
    if (caption) {
      caption.textContent = `Enrolment volume as height — all ${entries.length} districts, tallest bar ${top[0]} (${top[1]} enrolments). Click a bar to filter the dashboard to that district.`;
    }
  }
  build();

  // Drag to rotate; click (no drag) on a bar filters the dashboard.
  let dragging = false, moved = 0, lastX = 0;
  let rotY = 0, autoSpin = !lowMotion();
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  canvas.addEventListener('pointerdown', (e) => {
    dragging = true; moved = 0; lastX = e.clientX; autoSpin = false;
    canvas.setPointerCapture(e.pointerId);
  });
  canvas.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    const dx = e.clientX - lastX;
    moved += Math.abs(dx);
    rotY = Math.max(-0.9, Math.min(0.9, rotY + dx * 0.006));
    lastX = e.clientX;
  });
  canvas.addEventListener('pointerup', (e) => {
    dragging = false;
    if (moved < 6) {
      const rect = canvas.getBoundingClientRect();
      pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(pointer, camera);
      const hit = raycaster.intersectObjects(bars, false)[0];
      if (hit && typeof selectDistrict === 'function') {
        const district = hit.object.userData.district;
        if (selectedMesh) selectedMesh.material = barMat;
        selectedMesh = hit.object;
        selectedMesh.material = selMat;
        selectDistrict(district);
        document.getElementById('panel-dashboard').scrollIntoView();
      }
    }
  });
  canvas.addEventListener('pointercancel', () => { dragging = false; });
  canvas.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') { rotY = Math.max(-0.9, rotY - 0.15); autoSpin = false; }
    if (e.key === 'ArrowRight') { rotY = Math.min(0.9, rotY + 0.15); autoSpin = false; }
  });
  canvas.tabIndex = 0;

  function resize() {
    const w = wrap.clientWidth || 640;
    const h = 280;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  const clock = new THREE.Clock();
  function tick() {
    requestAnimationFrame(tick);
    const dt = Math.min(clock.getDelta(), 0.05);
    if (autoSpin && !dragging && !lowMotion()) {
      rotY = Math.sin(clock.elapsedTime * 0.25) * 0.45;
    }
    skyline.rotation.y = rotY;
    renderer.render(scene, camera);
  }
  tick();
}
