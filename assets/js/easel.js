// easel popup: shows one artwork at a time (only when the gallery is opened as a popup)
(function () {
  if (!document.documentElement.classList.contains("embed")) return;
  const es = document.getElementById("es");
  const list = (window.__ART || []).filter((p) => p.image);
  if (!es || !list.length) return;
  const img = document.getElementById("esImg"), cap = document.getElementById("esCap");
  let i = 0;
  const show = (n) => {
    i = (n + list.length) % list.length;
    const p = list[i];
    img.classList.remove("in");
    img.onload = () => img.classList.add("in");
    img.src = p.image;
    img.alt = p.title;
    cap.textContent = [p.title, p.year].filter(Boolean).join(" · ") + "  (" + (i + 1) + "/" + list.length + ")";
  };
  es.hidden = false;
  es.querySelector(".es-prev").onclick = () => show(i - 1);
  es.querySelector(".es-next").onclick = () => show(i + 1);
  addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
  let sx = null;
  es.addEventListener("pointerdown", (e) => { sx = e.clientX; });
  es.addEventListener("pointerup", (e) => {
    if (sx !== null && Math.abs(e.clientX - sx) > 40) show(i + (e.clientX < sx ? 1 : -1));
    sx = null;
  });
  show(0);
})();
