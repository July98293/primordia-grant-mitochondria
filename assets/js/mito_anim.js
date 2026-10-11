/* Cells passing mitochondria to each other.
   A well-stocked "hub" cell divides its mitochondria (fission) and donates them.
   Other cells slowly lose theirs (mitophagy) and receive new ones through
   tunneling nanotubes or vesicles. Cells look brighter the more mitochondria they hold. */
(() => {
  const canvas = document.getElementById("mito-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const INK = "#3a3fb8";
  const MITO_FILL = "#b3a2f7";
  const TAU = Math.PI * 2;
  const rand = (a, b) => a + Math.random() * (b - a);
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, k) => a + (b - a) * k;
  const angLerp = (a, b, k) => { let d = ((b - a + Math.PI) % TAU + TAU) % TAU - Math.PI; return a + d * k; };
  const ease = (x) => x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;

  // normalized home positions; index 2 is the hub
  const LAYOUT = [
    { x: 0.27, y: 0.18, s: 1.0, n: 3 },
    { x: 0.75, y: 0.27, s: 0.9, n: 2 },
    { x: 0.50, y: 0.52, s: 1.2, n: 7, hub: true },
    { x: 0.25, y: 0.82, s: 0.9, n: 2 },
    { x: 0.75, y: 0.80, s: 1.0, n: 3 },
  ];

  let W = 0, H = 0, LH = 0, unit = 50, cells = [], transfers = [], labels = [];
  let time = 0, last = 0, rafId = null, visible = true;
  let nextTransfer = 1.2, nextFission = 2.5, nextDecay = 4;

  function makeMito(cell, opts = {}) {
    return {
      a: opts.a ?? rand(0, TAU),
      d: opts.d ?? rand(0.5, 0.7),
      dT: rand(0.5, 0.7),
      w: rand(-0.35, 0.35),
      rot: rand(0, TAU),
      spin: rand(-0.6, 0.6),
      len: rand(0.9, 1.15),
      scale: opts.scale ?? 1,
      grow: opts.scale !== undefined && opts.scale < 1,
      dying: false,
      leaving: null,
    };
  }

  function build() {
    cells = LAYOUT.map((L, i) => {
      const c = {
        i, hub: !!L.hub, hx: L.x, hy: L.y, s: L.s, x: 0, y: 0, r: 0,
        ph: rand(0, TAU), pulse: 0, energy: 0.5, mitos: [], busy: 0,
      };
      for (let k = 0; k < L.n; k++) c.mitos.push(makeMito(c));
      c.energy = clamp(c.mitos.length / 6, 0, 1);
      return c;
    });
  }

  function resize() {
    const rect = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = rect.width; H = rect.height;
    const cap = canvas.parentElement.querySelector(".anim-caption");
    LH = Math.max(H * 0.55, H - (cap ? cap.offsetHeight : 0));
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    unit = Math.min(Math.min(W, LH) * 0.14, 92);
    placeCells();
    if (reduceMotion || !rafId) draw();
  }

  function placeCells() {
    for (const c of cells) {
      c.r = unit * c.s;
      c.x = c.hx * W + Math.sin(time * 0.31 + c.ph) * 6 + Math.sin(time * 0.17 + c.ph * 2) * 4;
      c.y = c.hy * LH + Math.cos(time * 0.27 + c.ph) * 6 + Math.sin(time * 0.13 + c.ph * 3) * 4;
    }
  }

  const membraneR = (c, th) =>
    c.r * (1 + 0.035 * Math.sin(3 * th + time * 0.8 + c.ph) + 0.025 * Math.sin(5 * th - time * 1.1 + c.ph * 2));
  const edgePoint = (c, th, k = 1) => {
    const rr = membraneR(c, th) * k;
    return { x: c.x + Math.cos(th) * rr, y: c.y + Math.sin(th) * rr };
  };
  const mitoPos = (c, m) => {
    const rr = c.r * m.d;
    return { x: c.x + Math.cos(m.a) * rr, y: c.y + Math.sin(m.a) * rr };
  };

  /* ---------- path between two cells (quadratic bezier) ---------- */
  function pathFor(tr) {
    const A = tr.from, B = tr.to;
    const th = Math.atan2(B.y - A.y, B.x - A.x);
    const p0 = edgePoint(A, th + tr.offA, 0.98);
    const p2 = edgePoint(B, th + Math.PI + tr.offB, 0.98);
    const mx = (p0.x + p2.x) / 2, my = (p0.y + p2.y) / 2;
    const dx = p2.x - p0.x, dy = p2.y - p0.y, dist = Math.hypot(dx, dy) || 1;
    const nx = -dy / dist, ny = dx / dist;
    const bend = tr.bend * dist + Math.sin(time * 1.3 + tr.seed) * dist * 0.03;
    const p1 = { x: mx + nx * bend, y: my + ny * bend };
    return { p0, p1, p2, exitAngle: th + tr.offA, entryAngle: th + Math.PI + tr.offB };
  }
  const bez = (P, s) => {
    const u = 1 - s;
    return {
      x: u * u * P.p0.x + 2 * u * s * P.p1.x + s * s * P.p2.x,
      y: u * u * P.p0.y + 2 * u * s * P.p1.y + s * s * P.p2.y,
    };
  };

  /* ---------- events ---------- */
  function startTransfer() {
    const hub = cells.find((c) => c.hub);
    const free = (c) => c.busy === 0;
    let donor = null;
    if (hub && free(hub) && hub.mitos.filter((m) => !m.dying && !m.grow).length >= 3 && Math.random() < 0.7) donor = hub;
    else {
      const rich = cells.filter((c) => free(c) && c.mitos.length >= 4);
      if (rich.length) donor = pick(rich);
    }
    if (!donor) return;
    const candidates = cells.filter((c) => c !== donor && free(c) && c.mitos.length < 6);
    if (!candidates.length) return;
    const minN = Math.min(...candidates.map((c) => c.mitos.length));
    const to = pick(candidates.filter((c) => c.mitos.length <= minN + 1));
    const movable = donor.mitos.filter((m) => !m.dying && !m.grow && !m.leaving);
    if (!movable.length) return;

    const dist = Math.hypot(to.x - donor.x, to.y - donor.y);
    // vesicles are the common route; a nanotube only forms between close neighbours
    const close = dist < (donor.r + to.r) * 1.35;
    const type = close && Math.random() < 0.45 ? "tube" : "vesicle";
    const tr = {
      type, from: donor, to, t: 0, seed: rand(0, 10),
      bend: type === "tube" ? rand(-0.18, 0.18) : rand(0.18, 0.32) * (Math.random() < 0.5 ? -1 : 1),
      offA: rand(-0.25, 0.25), offB: rand(-0.25, 0.25),
      mito: pick(movable), carried: false, done: false,
    };
    tr.mito.leaving = tr;
    donor.busy++; to.busy++;
    transfers.push(tr);
    const P = pathFor(tr);
    const mid = bez(P, 0.5);
    labels.push({ text: type === "tube" ? "nanotube" : "vesicle", tr, x: mid.x, y: mid.y, t: 0, life: type === "tube" ? 3.0 : 2.8 });
  }

  // timings (seconds)
  const TUBE = { grow: 0.9, travel: 1.7, retract: 0.7 };
  const VES = { exit: 0.7, travel: 2.4, fuse: 0.4 };

  function updateTransfer(tr, dt) {
    tr.t += dt;
    const P = pathFor(tr);
    const m = tr.mito;
    if (tr.type === "tube") {
      if (!tr.carried) {
        // move toward the exit while the tube grows
        m.a = angLerp(m.a, P.exitAngle, 1 - Math.exp(-dt * 4));
        m.d = lerp(m.d, 0.88, 1 - Math.exp(-dt * 4));
        if (tr.t >= TUBE.grow) { detach(tr); }
      } else if (tr.t < TUBE.grow + TUBE.travel) {
        tr.s = ease((tr.t - TUBE.grow) / TUBE.travel);
      } else if (!tr.done) {
        arrive(tr, P);
      }
      if (tr.t >= TUBE.grow + TUBE.travel + TUBE.retract) finish(tr);
    } else {
      if (!tr.carried) {
        m.a = angLerp(m.a, P.exitAngle, 1 - Math.exp(-dt * 4));
        m.d = lerp(m.d, 0.95, 1 - Math.exp(-dt * 4));
        if (tr.t >= VES.exit) detach(tr);
      } else if (tr.t < VES.exit + VES.travel) {
        tr.s = ease((tr.t - VES.exit) / VES.travel);
      } else if (!tr.done) {
        arrive(tr, P);
      }
      if (tr.t >= VES.exit + VES.travel + VES.fuse) finish(tr);
    }
  }
  function detach(tr) {
    const i = tr.from.mitos.indexOf(tr.mito);
    if (i >= 0) tr.from.mitos.splice(i, 1);
    tr.carried = true; tr.s = 0;
  }
  function arrive(tr, P) {
    tr.done = true; tr.s = 1;
    const m = tr.mito;
    m.leaving = null; m.a = P.entryAngle; m.d = 0.85; m.dT = rand(0.5, 0.7);
    tr.to.mitos.push(m);
    tr.to.pulse = 1;
  }
  function finish(tr) {
    tr.from.busy--; tr.to.busy--;
    transfers.splice(transfers.indexOf(tr), 1);
  }

  function fission() {
    const hub = cells.find((c) => c.hub);
    if (!hub || hub.mitos.length >= 7) return;
    const src = hub.mitos.filter((m) => !m.leaving && !m.dying && !m.grow);
    if (!src.length) return;
    const p = pick(src);
    hub.mitos.push(makeMito(hub, { a: p.a + 0.35, d: p.d, scale: 0.05 }));
  }
  function decay() {
    const pool = cells.filter((c) => !c.hub && c.mitos.filter((m) => !m.leaving && !m.dying).length >= 2);
    if (!pool.length) return;
    const c = pick(pool);
    const m = pick(c.mitos.filter((m) => !m.leaving && !m.dying));
    m.dying = true;
  }

  /* ---------- update ---------- */
  function update(dt) {
    time += dt;
    placeCells();

    nextTransfer -= dt; nextFission -= dt; nextDecay -= dt;
    if (nextTransfer <= 0) { if (transfers.length < 3) startTransfer(); nextTransfer = rand(0.9, 1.8); }
    if (nextFission <= 0) { fission(); nextFission = rand(2.2, 3.6); }
    if (nextDecay <= 0) { decay(); nextDecay = rand(4.5, 7); }

    for (const c of cells) {
      c.pulse = Math.max(0, c.pulse - dt * 0.8);
      const target = clamp(c.mitos.filter((m) => !m.dying).length / 6, 0.05, 1);
      c.energy = lerp(c.energy, target, 1 - Math.exp(-dt * 1.5));
      for (let k = c.mitos.length - 1; k >= 0; k--) {
        const m = c.mitos[k];
        if (m.grow) { m.scale = Math.min(1, m.scale + dt * 0.7); if (m.scale >= 1) m.grow = false; }
        if (m.dying) { m.scale -= dt * 0.6; if (m.scale <= 0) { c.mitos.splice(k, 1); continue; } }
        m.rot += m.spin * dt;
        if (!m.leaving) {
          m.a += m.w * dt * 0.6;
          m.d = lerp(m.d, m.dT, 1 - Math.exp(-dt * 0.8));
          if (Math.random() < dt * 0.15) m.dT = rand(0.5, 0.7);
        }
      }
    }
    for (const tr of [...transfers]) updateTransfer(tr, dt);
    for (const L of [...labels]) { L.t += dt; if (L.t > L.life) labels.splice(labels.indexOf(L), 1); }
  }

  /* ---------- drawing ---------- */
  function drawMito(x, y, rot, s, alpha = 1) {
    const L = unit * 0.46 * s, Wd = unit * 0.19 * s;
    if (L < 0.5) return;
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.translate(x, y); ctx.rotate(rot);
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(-L / 2, -Wd / 2, L, Wd, Wd / 2) : ctx.rect(-L / 2, -Wd / 2, L, Wd);
    ctx.fillStyle = MITO_FILL; ctx.fill();
    ctx.lineWidth = 1.4; ctx.strokeStyle = INK; ctx.stroke();
    // cristae: a wavy line inside
    ctx.beginPath();
    const n = 5;
    for (let i = 0; i <= n * 4; i++) {
      const u = i / (n * 4);
      const px = -L / 2 + Wd * 0.45 + u * (L - Wd * 0.9);
      const py = Math.sin(u * n * TAU) * Wd * 0.26;
      i ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
    }
    ctx.lineWidth = 1; ctx.stroke();
    ctx.restore();
  }

  function drawCell(c) {
    const N = 64;
    // soft glow when a mitochondrion arrives
    ctx.save();
    if (c.pulse > 0) { ctx.shadowColor = `rgba(140, 120, 255, ${0.85 * c.pulse})`; ctx.shadowBlur = 40 * c.pulse; }
    ctx.beginPath();
    for (let i = 0; i <= N; i++) {
      const th = (i / N) * TAU, p = edgePoint(c, th);
      i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y);
    }
    ctx.closePath();
    const e = c.energy;
    const r = Math.round(lerp(228, 243, e)), g = Math.round(lerp(229, 238, e)), b = Math.round(lerp(238, 255, e));
    ctx.fillStyle = `rgba(${r}, ${g}, ${b}, 0.9)`;
    ctx.fill();
    ctx.restore();
    ctx.lineWidth = 1.8; ctx.strokeStyle = INK; ctx.stroke();
    // second, offset stroke for a hand-drawn feel
    ctx.save();
    ctx.globalAlpha = 0.25; ctx.lineWidth = 1;
    ctx.beginPath();
    for (let i = 0; i <= N; i++) {
      const th = (i / N) * TAU, p = edgePoint(c, th, 0.965 + 0.01 * Math.sin(th * 7 + c.ph));
      i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y);
    }
    ctx.stroke();
    ctx.restore();

    // nucleus
    const nx = c.x + Math.cos(c.ph) * c.r * 0.06, ny = c.y + Math.sin(c.ph) * c.r * 0.06, nr = c.r * 0.27;
    ctx.beginPath(); ctx.arc(nx, ny, nr, 0, TAU);
    ctx.fillStyle = "rgba(170, 196, 250, 0.8)"; ctx.fill();
    ctx.lineWidth = 1.4; ctx.strokeStyle = INK; ctx.stroke();
    ctx.fillStyle = INK; ctx.globalAlpha = 0.45;
    for (let k = 0; k < 6; k++) {
      const a = c.ph * 3 + k * 2.4, rr = nr * (0.25 + 0.45 * ((k * 37) % 10) / 10);
      ctx.beginPath(); ctx.arc(nx + Math.cos(a) * rr, ny + Math.sin(a) * rr, Math.max(1, nr * 0.07), 0, TAU); ctx.fill();
    }
    ctx.globalAlpha = 1;

    for (const m of c.mitos) {
      const p = mitoPos(c, m);
      drawMito(p.x, p.y, m.a + Math.PI / 2 + 0.45 * Math.sin(m.rot), m.scale, m.dying ? Math.max(0, m.scale) : 1);
    }
  }

  function drawTube(tr) {
    const P = pathFor(tr);
    let a = 0, b = 1;
    if (tr.t < TUBE.grow) b = ease(tr.t / TUBE.grow);
    const retractStart = TUBE.grow + TUBE.travel;
    if (tr.t > retractStart) a = ease(clamp((tr.t - retractStart) / TUBE.retract, 0, 1));
    if (b - a < 0.01) return;
    const steps = 40, w = unit * 0.11;
    const left = [], right = [];
    for (let i = 0; i <= steps; i++) {
      const s = a + (b - a) * (i / steps);
      const p = bez(P, s), q = bez(P, Math.min(1, s + 0.01)), o = bez(P, Math.max(0, s - 0.01));
      const dx = q.x - o.x, dy = q.y - o.y, len = Math.hypot(dx, dy) || 1;
      const nx = -dy / len, ny = dx / len;
      const ww = w * (0.85 + 0.15 * Math.sin(s * 9 + time * 2));
      left.push({ x: p.x + nx * ww, y: p.y + ny * ww });
      right.push({ x: p.x - nx * ww, y: p.y - ny * ww });
    }
    ctx.beginPath();
    left.forEach((p, i) => i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y));
    for (let i = right.length - 1; i >= 0; i--) ctx.lineTo(right[i].x, right[i].y);
    ctx.closePath();
    ctx.fillStyle = "rgba(244, 241, 255, 0.8)"; ctx.fill();
    ctx.lineWidth = 1.3; ctx.strokeStyle = INK;
    ctx.beginPath(); left.forEach((p, i) => i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y)); ctx.stroke();
    ctx.beginPath(); right.forEach((p, i) => i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y)); ctx.stroke();
  }

  function drawCarried(tr) {
    if (!tr.carried || tr.done) return;
    const P = pathFor(tr);
    const p = bez(P, tr.s), q = bez(P, Math.min(1, tr.s + 0.02));
    const rot = Math.atan2(q.y - p.y, q.x - p.x);
    if (tr.type === "vesicle") {
      const bob = Math.sin(time * 3 + tr.seed) * unit * 0.05;
      const R = unit * 0.3;
      ctx.save();
      ctx.beginPath(); ctx.arc(p.x, p.y + bob, R, 0, TAU);
      ctx.fillStyle = "rgba(255,255,255,0.7)"; ctx.fill();
      ctx.setLineDash([4, 4]); ctx.lineWidth = 1.3; ctx.strokeStyle = INK; ctx.stroke();
      ctx.restore();
      drawMito(p.x, p.y + bob, rot + Math.sin(time * 2) * 0.3, 0.8);
    } else {
      drawMito(p.x, p.y, rot, 0.85);
    }
  }

  function drawLabels() {
    const size = Math.max(16, Math.round(unit * 0.32));
    ctx.font = `600 ${size}px Caveat, "Bradley Hand", cursive`;
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    for (const L of labels) {
      const fade = Math.min(1, L.t / 0.4, (L.life - L.t) / 0.5);
      if (fade <= 0) continue;
      let x = L.x, y = L.y - unit * 0.42;
      if (transfers.includes(L.tr)) {
        const mid = bez(pathFor(L.tr), 0.5);
        x = L.x = mid.x; y = (L.y = mid.y) - unit * 0.42;
      }
      x = clamp(x, 50, W - 50); y = clamp(y, 20, LH - 10);
      ctx.globalAlpha = fade;
      ctx.fillStyle = INK;
      ctx.fillText(L.text, x, y);
    }
    ctx.globalAlpha = 1;
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    for (const tr of transfers) if (tr.type === "tube") drawTube(tr);
    for (const c of cells) drawCell(c);
    for (const tr of transfers) drawCarried(tr);
    drawLabels();
  }

  /* ---------- loop ---------- */
  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000 || 0);
    last = now;
    update(dt);
    draw();
    rafId = requestAnimationFrame(frame);
  }
  function start() { if (reduceMotion || rafId || !visible || document.hidden) return; last = performance.now(); rafId = requestAnimationFrame(frame); }
  function stop() { if (rafId) cancelAnimationFrame(rafId); rafId = null; }

  build();
  resize();
  if (window.ResizeObserver) new ResizeObserver(resize).observe(canvas);
  else window.addEventListener("resize", resize);
  if (window.IntersectionObserver) {
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; visible ? start() : stop(); }).observe(canvas);
  }
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (!rafId) draw(); });
  start();
})();
