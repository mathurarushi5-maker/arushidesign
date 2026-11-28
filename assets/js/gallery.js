(function () {
  const wall = document.getElementById("glWall");
  if (!wall) return;
  const lb = document.getElementById("glLb"), n = document.getElementById("glN"), empty = document.querySelector(".gl-empty");
  const q = (s) => lb.querySelector(s);
  const P = new URLSearchParams(location.search), EDIT = P.has("edit"), DEMO = P.has("demo");
  const KEY = "artEdits";
  let ed = { added: [], removed: [] };
  try { ed = Object.assign(ed, JSON.parse(localStorage.getItem(KEY) || "{}")); } catch (e) {}
  const save = () => localStorage.setItem(KEY, JSON.stringify(ed));
  const SAMPLE = [["Sample sketch", "pencil"], ["Sample canvas", "paint"], ["Sample study", "pencil"], ["Sample landscape", "paint"], ["Sample portrait", "pencil"], ["Sample abstract", "paint"]]
    .map(([title, medium], i) => ({ title, medium, year: "Demo", note: "Placeholder piece.", wip: i === 2 }));
  if (DEMO) window.__ART = SAMPLE;
  const list = () => window.__ART.concat(ed.added).filter((p) => !ed.removed.includes(p.title));
  let filter = "all", shown = [], cur = 0;
  const vis = () => list().filter((p) => filter === "all" || p.medium === filter);

  function art(p, big) {
    const d = document.createElement("div");
    d.className = "gl-art";
    if (p.image) { const i = document.createElement("img"); i.src = p.image; i.alt = p.title; i.loading = "lazy"; d.appendChild(i); }
    else d.innerHTML = p.medium === "paint"
      ? '<svg viewBox="0 0 120 90" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="120" height="90" fill="#a9d8ff"/><circle cx="92" cy="22" r="11" fill="#ffe27a"/><path d="M0 70 Q30 40 60 62 T120 52 V90 H0Z" fill="#bfeed6"/><path d="M0 78 Q40 60 120 74 V90 H0Z" fill="#6fb04a"/></svg>'
      : '<svg viewBox="0 0 120 90" aria-hidden="true"><path d="M20 70 C30 20 50 20 60 45 S90 70 100 25" fill="none" stroke="#3a2f22" stroke-width="2.2" stroke-linecap="round"/><path d="M24 74 C34 28 52 30 62 50 S88 72 98 32" fill="none" stroke="#3a2f22" stroke-width="1" opacity=".5" stroke-linecap="round"/></svg>';
    return d;
  }

  function render() {
    shown = vis();
    wall.innerHTML = "";
    shown.forEach((p, i) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "gl-piece " + (p.medium === "paint" ? "is-paint" : "is-pencil");
      b.style.setProperty("--r", ((i * 37) % 7 - 3) * 0.7 + "deg");
      b.appendChild(art(p));
      const c = document.createElement("span");
      c.className = "gl-cap";
      c.textContent = p.title + (p.year ? " · " + p.year : "");
      b.appendChild(c);
      if (p.wip) { const w = document.createElement("span"); w.className = "gl-wip"; w.textContent = "work in progress"; b.appendChild(w); }
      b.onclick = () => open(i);
      wall.appendChild(b);
    });
    n.textContent = shown.length;
    empty.hidden = list().length > 0;
    document.querySelector(".gl-filters").hidden = list().length === 0;
  }

  function open(i) {
    cur = (i + shown.length) % shown.length;
    const p = shown[cur];
    q(".gl-img").replaceChildren(art(p, true));
    q("h2").textContent = p.title;
    q(".gl-meta").textContent = [p.medium === "paint" ? "Colors" : "Pen", p.year, p.wip ? "work in progress" : ""].filter(Boolean).join(" · ");
    q(".gl-note").textContent = p.note || "";
    q(".gl-del").hidden = !EDIT;
    lb.hidden = false;
    document.body.style.overflow = "hidden";
  }
  const close = () => { lb.hidden = true; document.body.style.overflow = ""; };
  q(".gl-x").onclick = close;
  q(".gl-prev").onclick = () => open(cur - 1);
  q(".gl-next").onclick = () => open(cur + 1);
  lb.addEventListener("click", (e) => { if (e.target === lb) close(); });
  document.addEventListener("keydown", (e) => {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") open(cur - 1);
    if (e.key === "ArrowRight") open(cur + 1);
  });
  document.querySelectorAll(".gl-filters [data-f]").forEach((b) => b.onclick = () => {
    filter = b.dataset.f;
    document.querySelectorAll(".gl-filters [data-f]").forEach((x) => x.classList.toggle("on", x === b));
    render();
  });

  const admin = document.querySelector(".gl-admin");
  if (EDIT) {
    admin.hidden = false;
    admin.querySelector("form").onsubmit = (e) => {
      e.preventDefault();
      const f = new FormData(e.target);
      ed.added.push({ title: f.get("title").trim(), image: f.get("image").trim(), medium: f.get("medium"), year: f.get("year").trim(), note: f.get("note").trim(), wip: !!f.get("wip") });
      save(); e.target.reset(); render();
    };
    q(".gl-del").onclick = () => {
      const t = shown[cur].title;
      const k = ed.added.findIndex((x) => x.title === t);
      if (k > -1) ed.added.splice(k, 1); else ed.removed.push(t);
      save(); close(); render();
    };
    admin.querySelector(".gl-export").onclick = () => {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([JSON.stringify({ title: "Paint & pencil", intro: document.querySelector(".lede").textContent, items: list() }, null, 2)], { type: "application/json" }));
      a.download = "gallery.json"; a.click();
    };
    admin.querySelector(".gl-reset").onclick = () => { if (confirm("Discard all local edits?")) { localStorage.removeItem(KEY); location.reload(); } };
  }
  render();
})();
