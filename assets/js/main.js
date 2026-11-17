const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

// scroll reveal
const io = new IntersectionObserver((entries) => {
  entries.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
  });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// draggable stickers
document.querySelectorAll("[data-drag]").forEach((el) => {
  let sx, sy, ox = 0, oy = 0, base = getComputedStyle(el).transform;
  if (base === "none") base = "";
  el.addEventListener("pointerdown", (ev) => {
    el.setPointerCapture(ev.pointerId);
    el.classList.add("dragging");
    sx = ev.clientX - ox; sy = ev.clientY - oy;
    cancelAnimationFrame(el._raf);
    let vx = 0, vy = 0, lx = ox, ly = oy;
    const move = (m) => {
      ox = m.clientX - sx; oy = m.clientY - sy;
      vx = ox - lx; vy = oy - ly; lx = ox; ly = oy;
      el.style.translate = `${ox}px ${oy}px`;
    };
    const up = () => {
      el.classList.remove("dragging");
      if (el.hasAttribute("data-pop") && Math.abs(vx) + Math.abs(vy) < 3) burst(ev.clientX, ev.clientY);
      if (!reduce) {
        const glide = () => {
          vx *= 0.93; vy *= 0.93;
          ox += vx; oy += vy;
          el.style.translate = `${ox}px ${oy}px`;
          if (Math.abs(vx) + Math.abs(vy) > 0.4) el._raf = requestAnimationFrame(glide);
        };
        glide();
      }
      el.removeEventListener("pointermove", move);
      el.removeEventListener("pointerup", up);
    };
    el.addEventListener("pointermove", move);
    el.addEventListener("pointerup", up);
  });
});

// 3D tilt on project art
if (!reduce) {
  document.querySelectorAll(".lock[data-tilt]").forEach((el) => {
    el.addEventListener("pointermove", (ev) => {
      const r = el.getBoundingClientRect();
      const x = (ev.clientX - r.left) / r.width - 0.5;
      const y = (ev.clientY - r.top) / r.height - 0.5;
      el.style.transform = `perspective(900px) rotateY(${x * 7}deg) rotateX(${-y * 7}deg) scale(1.02)`;
    });
    el.addEventListener("pointerleave", () => { el.style.transform = ""; });
  });
}

// lightbox for case study images
const lb = document.querySelector(".lightbox");
if (lb) {
  const big = lb.querySelector("img");
  document.querySelectorAll(".shot img").forEach((img) => {
    img.addEventListener("click", () => { big.src = img.src; big.alt = img.alt; lb.hidden = false; });
  });
  lb.addEventListener("click", () => { lb.hidden = true; });
  addEventListener("keydown", (e) => { if (e.key === "Escape") lb.hidden = true; });
}

// confetti burst
function burst(x, y) {
  if (reduce) return;
  const cols = ["#c8f560", "#1f2bff", "#ffb4a2", "#f6f1e7"];
  for (let i = 0; i < 24; i++) {
    const c = document.createElement("i");
    c.className = "confetti";
    c.style.cssText = `left:${x}px;top:${y}px;background:${cols[i % 4]}`;
    document.body.appendChild(c);
    const a = Math.random() * Math.PI * 2, d = 60 + Math.random() * 120;
    c.animate([
      { transform: "translate(0,0) rotate(0)", opacity: 1 },
      { transform: `translate(${Math.cos(a) * d}px,${Math.sin(a) * d + 80}px) rotate(${Math.random() * 720}deg)`, opacity: 0 },
    ], { duration: 900 + Math.random() * 400, easing: "cubic-bezier(.2,.7,.3,1)" }).onfinish = () => c.remove();
  }
}
document.querySelectorAll(".btn, .s2, .big-link").forEach((el) =>
  el.addEventListener("click", (e) => burst(e.clientX, e.clientY)));

// copy email
document.querySelectorAll("a[href^='mailto:']").forEach((a) => {
  if (!a.classList.contains("big-link")) return;
  a.addEventListener("click", (e) => {
    if (!navigator.clipboard) return;
    e.preventDefault();
    navigator.clipboard.writeText(a.getAttribute("href").slice(7).split("?")[0]).then(() => {
      const t = document.createElement("div");
      t.className = "toast"; t.textContent = "email copied ✓";
      document.body.appendChild(t); setTimeout(() => t.remove(), 1700);
    });
  });
});

// project filters
const chips = document.querySelectorAll(".chip[data-filter]");
const applyFilter = (f) => {
  chips.forEach((c) => c.classList.toggle("on", c.dataset.filter === f));
  let n = 0;
  document.querySelectorAll(".tile[data-cat]").forEach((el) => {
    const show = f === "all" || el.dataset.cat.split(" ").includes(f);
    el.hidden = !show;
    if (show) n++;
  });
  const em = document.querySelector(".empty");
  if (em) em.hidden = n > 0;
};
chips.forEach((c) => c.addEventListener("click", () => applyFilter(c.dataset.filter)));

const themer = document.querySelector("[data-themer]");
if (themer) {
  const root = document.documentElement;
  const items = [...themer.querySelectorAll("[data-set-theme]")];
  const apply = (t) => { if (t === "cream") delete root.dataset.theme; else root.dataset.theme = t; };
  const cur = () => root.dataset.theme || "cream";
  let saved = cur();
  const mark = () => items.forEach((i) => i.classList.toggle("on", i.dataset.setTheme === saved));
  items.forEach((i) => {
    const t = i.dataset.setTheme;
    i.addEventListener("mouseenter", () => apply(t));
    i.addEventListener("mouseleave", () => apply(saved));
    i.addEventListener("click", () => {
      saved = t; apply(t); mark();
      try { localStorage.setItem("theme", t); } catch (e) {}
    });
  });
  mark();
}

// journey butterfly: scroll-driven trail
(() => {
  const wrap = document.querySelector(".exp-wrap");
  const bfly = document.querySelector(".bfly");
  const need = document.querySelector(".need");
  const about = document.querySelector(".about");
  const svg = wrap && wrap.querySelector(".exp-line");
  const path = svg && svg.querySelector(".trail-path");
  const mask = svg && svg.querySelector(".trail-mask");
  if (!bfly || !need || !path || matchMedia("(max-width: 860px)").matches) return;
  const lis = [...wrap.querySelectorAll(".exp li")].reverse();
  const total = path.getTotalLength();
  const N = 1600, pts = [];
  for (let i = 0; i <= N; i++) { const q = path.getPointAtLength((total * i) / N); pts.push([q.x, q.y]); }
  let prev = 0;
  const stops = lis.map((li) => {
    const x = parseFloat(li.style.left) || (li.offsetLeft / wrap.offsetWidth) * 1000;
    const y = parseFloat(li.style.top) || (li.offsetTop / wrap.offsetHeight) * 600;
    let best = prev, bd = Infinity;
    for (let i = prev; i <= N; i++) { const d = (pts[i][0] - x) ** 2 + (pts[i][1] - y) ** 2; if (d < bd) { bd = d; best = i; } }
    prev = best;
    return best / N;
  });
  window.__bf = () => ({ prog, stops, total, n: lis.length });
  wrap.classList.add("anim");
  mask.style.strokeDasharray = "1000";
  const clamp = (v) => Math.max(0, Math.min(1, v));
  const ease = (t) => t * t * (3 - 2 * t);
  let flyT, prog = reduce ? 1 : 0, playing = false, t0 = 0;
  const DUR = 7000;
  const frame = () => {
    const vh = innerHeight, r = wrap.getBoundingClientRect();
    const s = prog;
    const pf = clamp(s / 0.8), ff = ease(clamp((s - 0.8) / 0.2));
    mask.style.strokeDashoffset = String(1000 * (1 - pf));
    lis.forEach((li, i) => li.classList.toggle("seen", pf >= stops[i] - 0.005));
    const sr = svg.getBoundingClientRect(), ar = about.getBoundingClientRect();
    const at = (f) => { const q = path.getPointAtLength(total * f); return [sr.left + (q.x / 1000) * sr.width, sr.top + (q.y / 600) * sr.height]; };
    let [x, y] = at(pf);
    const a = at(Math.max(0, pf - 0.01)), b = at(Math.min(1, pf + 0.01));
    let tilt = Math.max(-25, Math.min(25, (Math.atan2(b[1] - a[1], b[0] - a[0]) * 180) / Math.PI * 0.35));
    if (ff > 0) {
      const nr = need.getBoundingClientRect();
      const tx = nr.right + 46, ty = nr.top + nr.height * 0.45;
      const cx = x, cy = ty;
      const u = 1 - ff;
      const nx = u * u * x + 2 * u * ff * cx + ff * ff * tx;
      const ny = u * u * y + 2 * u * ff * cy + ff * ff * ty;
      tilt = -14 * ff * u * 4 + 8 * ff;
      x = nx; y = ny;
    }
    bfly.style.transform = `translate(${x - ar.left - 36}px, ${y - ar.top - 29}px) rotate(${tilt}deg)`;
    bfly.classList.toggle("on", s > 0.001 || reduce);
  };
  const step = (now) => {
    prog = clamp((now - t0) / DUR);
    bfly.classList.add("fly"); clearTimeout(flyT);
    frame();
    if (prog < 1) requestAnimationFrame(step);
    else { playing = false; bfly.classList.remove("fly"); }
  };
  const play = () => { if (playing || prog >= 1) return; playing = true; t0 = performance.now(); requestAnimationFrame(step); };
  const watch = () => {
    const r = wrap.getBoundingClientRect(), vh = innerHeight;
    const vis = Math.min(r.bottom, vh) - Math.max(r.top, 0);
    if (!reduce && vis > r.height * 0.7) play();
    else if (!reduce && !playing && prog >= 1 && r.top > vh) { prog = 0; frame(); }
  };
  let tick = false;
  const onScroll = () => {
    watch();
    if (!tick) { tick = true; requestAnimationFrame(() => { tick = false; frame(); }); }
  };
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", frame);
  frame();
})();
