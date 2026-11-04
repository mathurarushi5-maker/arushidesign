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
