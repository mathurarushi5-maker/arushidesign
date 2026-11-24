// always land on the hero after a refresh
if (document.getElementById("jv")) {
  history.scrollRestoration = "manual";
  if (location.hash) history.replaceState(null, "", location.pathname + location.search);
  window.scrollTo(0, 0);
}

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

// off the clock iframe: auto height, fullscreen while inside a room
(function () {
  const f = document.querySelector(".otc");
  if (!f) return;
  addEventListener("message", (e) => {
    if (e.source !== f.contentWindow || !e.data || !e.data.otc) return;
    const was = f.classList.contains("full");
    f.classList.toggle("full", e.data.room);
    document.documentElement.style.overflow = e.data.room ? "hidden" : "";
    if (!e.data.room && e.data.h) f.style.height = e.data.h + "px";
    if (was && !e.data.room) document.getElementById("life").scrollIntoView({ block: "start" });
  });
})();

// pop library / poems up over the page
(function () {
  const f = document.querySelector(".otc");
  if (!f) return;
  addEventListener("message", (e) => {
    if (e.data && typeof e.data === "object" && "diaryOpen" in e.data) { const x = document.querySelector(".pop-x"); if (x) x.hidden = !!e.data.diaryOpen; return; }
    if (e.data && e.data.popClose) { const o = document.querySelector(".pop"); if (o) o.click(); return; }
    if (e.source !== f.contentWindow || !e.data || !e.data.otcOpen) return;
    if (document.querySelector(".pop")) return;
    const m = document.createElement("div");
    m.className = "pop";
    m.innerHTML = '<button class="pop-x" aria-label="Close">×</button><iframe title="Popup" src="' + e.data.otcOpen + '?embed&t=' + Date.now() + '"></iframe>';
    const fit = () => {
      try {
        const d = m.querySelector("iframe").contentDocument, c = d.querySelectorAll(".rl-card");
        const t = c.length ? c[c.length - 1] : d.querySelector(".es-canvas");
        if (!t) return;
        const x = m.querySelector(".pop-x"), es = d.querySelector(".es-stage");
        if (es) {
          const h = Math.min(innerHeight * 0.86, 860), w = Math.min(h * 2 / 3, innerWidth * 0.94);
          x.style.left = innerWidth / 2 + w / 2 + 4 + "px";
          x.style.top = Math.max(8, innerHeight / 2 - h / 2 + 8) + "px";
          return;
        }
        const r = t.getBoundingClientRect();
        x.style.left = r.right - 24 + "px"; x.style.top = Math.max(6, r.top - 20) + "px";
      } catch (_) {}
    };
    m.querySelector("iframe").addEventListener("load", () => { fit(); setTimeout(fit, 900); });
    addEventListener("resize", fit);
    const close = () => { m.remove(); document.documentElement.style.overflow = ""; removeEventListener("keydown", esc); };
    const esc = (k) => k.key === "Escape" && close();
    m.addEventListener("click", (k) => { if (k.target === m || k.target.classList.contains("pop-x")) close(); });
    addEventListener("keydown", esc);
    document.documentElement.style.overflow = "hidden";
    document.body.appendChild(m);
  });
})();

if (document.documentElement.classList.contains("embed"))
  addEventListener("click", (e) => { if (!e.target.closest(".rl-card,.pm-desk,.pop-x,.es-stage")) parent.postMessage({popClose: 1}, "*"); });
