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
    const move = (m) => {
      ox = m.clientX - sx; oy = m.clientY - sy;
      el.style.translate = `${ox}px ${oy}px`;
    };
    const up = () => {
      el.classList.remove("dragging");
      el.removeEventListener("pointermove", move);
      el.removeEventListener("pointerup", up);
    };
    el.addEventListener("pointermove", move);
    el.addEventListener("pointerup", up);
  });
});

// 3D tilt on project art
if (!reduce) {
  document.querySelectorAll("[data-tilt]").forEach((el) => {
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
