(function () {
  const icons = document.getElementById("lbIcons");
  if (!icons) return;
  const win = document.getElementById("lbWin"), q = (s) => win.querySelector(s);
  const P = new URLSearchParams(location.search), EDIT = P.has("edit"), DEMO = P.has("demo");
  const KEY = "labEdits";
  let ed = { added: [], removed: [] };
  try { ed = Object.assign(ed, JSON.parse(localStorage.getItem(KEY) || "{}")); } catch (e) {}
  const save = () => localStorage.setItem(KEY, JSON.stringify(ed));
  const T = { prototype: ["Pr", "#bfeed6"], image: ["Im", "#ffb4a2"], agent: ["Ag", "#a9d8ff"], workflow: ["Wf", "#ffe27a"] };
  const ST = { works: "works", cooking: "still cooking", broken: "broken" };
  const SAMPLE = [["Sample prototype", "prototype", "works"], ["Sample image study", "image", "cooking"], ["Sample agent", "agent", "broken"], ["Sample workflow", "workflow", "works"], ["Sample UI remix", "prototype", "cooking"], ["Sample poster", "image", "works"], ["Sample helper", "agent", "works"]]
    .map(([title, type, status], i) => ({ title, type, status, date: "Demo " + (i + 1), tools: ["Tool A", "Tool B"], what: "Placeholder: what I tried.", learned: "Placeholder: what I learned.", link: "" }));
  if (DEMO || !(window.__LAB || []).length) window.__LAB = SAMPLE;
  const list = () => window.__LAB.concat(ed.added).filter((p) => !ed.removed.includes(p.title));
  const mk = (tag, cls, txt) => { const x = document.createElement(tag); if (cls) x.className = cls; if (txt != null) x.textContent = txt; return x; };
  let shown = [], cur = 0;

  function render() {
    shown = list();
    icons.innerHTML = "";
    shown.forEach((p, i) => {
      const [sym, col] = T[p.type] || ["??", "#fff"];
      const b = mk("button", "lb-ico st-" + p.status);
      b.type = "button";
      b.style.setProperty("--c", col);
      b.append(mk("div", "lb-app", sym), mk("span", "", p.title));
      b.onclick = () => open(i);
      icons.appendChild(b);
    });
    document.querySelector(".lb-empty").hidden = shown.length > 0;
  }

  function open(i) {
    cur = i;
    const p = shown[i];
    q(".lb-wt").textContent = p.title;
    q("h2").textContent = p.title;
    q(".lb-meta").textContent = [p.type, ST[p.status], p.date].filter(Boolean).join(" · ");
    q(".lb-tools").textContent = (p.tools || []).join(" · ");
    q(".lb-what").textContent = p.what || "";
    q(".lb-learn").textContent = p.learned || "";
    const s = q(".lb-shot"); s.innerHTML = ""; s.hidden = !(p.embed || p.image);
    if (p.embed) { const f = mk("iframe"); f.src = p.embed; f.title = p.title; f.loading = "lazy"; s.appendChild(f); }
    else if (p.image) { const im = mk("img"); im.src = p.image; im.alt = p.title; s.appendChild(im); }
    const a = q(".lb-try"); a.hidden = !p.link; if (p.link) a.href = p.link;
    q(".lb-del").hidden = !EDIT;
    win.hidden = false;
    win.classList.remove("full");
    win.style.animation = "none"; win.offsetWidth; win.style.animation = "";
  }
  const home = win.parentNode;
  function setFull(on) {
    if (on) document.body.appendChild(win); else home.appendChild(win);
    win.classList.toggle("full", on);
    document.body.style.overflow = on ? "hidden" : "";
    q(".lb-fs").textContent = on ? "⤡ exit full screen" : "⤢ full screen";
  }
  const closeAll = () => { setFull(false); win.hidden = true; };
  q(".d-r").onclick = closeAll;
  q(".d-y").onclick = closeAll;
  q(".d-g").onclick = () => setFull(!win.classList.contains("full"));
  q(".lb-fs").onclick = () => setFull(!win.classList.contains("full"));
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape" || win.hidden) return;
    if (win.classList.contains("full")) setFull(false); else closeAll();
  });

  const clock = document.getElementById("lbClock");
  const tick = () => { clock.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }); };
  tick(); setInterval(tick, 30000);

  const admin = document.querySelector(".lb-admin");
  if (EDIT) {
    admin.hidden = false;
    admin.querySelector("form").onsubmit = (e) => {
      e.preventDefault();
      const f = Object.fromEntries(new FormData(e.target));
      f.tools = (f.tools || "").split(",").map((s) => s.trim()).filter(Boolean);
      ed.added.push(f); save(); e.target.reset(); render();
    };
    q(".lb-del").onclick = () => {
      const t = shown[cur].title, k = ed.added.findIndex((x) => x.title === t);
      if (k > -1) ed.added.splice(k, 1); else ed.removed.push(t);
      save(); closeAll(); render();
    };
    admin.querySelector(".lb-export").onclick = () => {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([JSON.stringify({ title: "Lab", intro: document.querySelector(".lede").textContent, items: list() }, null, 2)], { type: "application/json" }));
      a.download = "lab.json"; a.click();
    };
    admin.querySelector(".lb-reset").onclick = () => { if (confirm("Discard all local edits?")) { localStorage.removeItem(KEY); location.reload(); } };
  }
  render();
})();

/* map the live desktop onto the laptop screen of the room image */
(function () {
  var sc = document.querySelector('.lb-scene'), lp = sc && sc.querySelector('.sc-laptop');
  if (!lp) return;
  var W = 460, H = 400, Q = [[612, 548], [880, 520], [916, 722], [648, 750]];
  function solve(A, b) {
    var n = b.length, i, j, k, f, t;
    for (i = 0; i < n; i++) {
      t = i; for (j = i + 1; j < n; j++) if (Math.abs(A[j][i]) > Math.abs(A[t][i])) t = j;
      var r = A[i]; A[i] = A[t]; A[t] = r; var q = b[i]; b[i] = b[t]; b[t] = q;
      for (j = i + 1; j < n; j++) { f = A[j][i] / A[i][i]; for (k = i; k < n; k++) A[j][k] -= f * A[i][k]; b[j] -= f * b[i]; }
    }
    var x = new Array(n);
    for (i = n - 1; i >= 0; i--) { var s = b[i]; for (j = i + 1; j < n; j++) s -= A[i][j] * x[j]; x[i] = s / A[i][i]; }
    return x;
  }
  function fit() {
    var s = sc.clientWidth / 1536, src = [[0, 0], [W, 0], [W, H], [0, H]], A = [], b = [];
    for (var i = 0; i < 4; i++) {
      var x = src[i][0], y = src[i][1], u = Q[i][0] * s, v = Q[i][1] * s;
      A.push([x, y, 1, 0, 0, 0, -x * u, -y * u]); b.push(u);
      A.push([0, 0, 0, x, y, 1, -x * v, -y * v]); b.push(v);
    }
    var h = solve(A, b);
    lp.style.transform = 'matrix3d(' + [h[0], h[3], 0, h[6], h[1], h[4], 0, h[7], 0, 0, 1, 0, h[2], h[5], 0, 1].join(',') + ')';
  }
  fit(); window.addEventListener('resize', fit);
})();
