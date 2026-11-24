(function () {
  const grid = document.getElementById("poemGrid");
  if (!grid) return;
  const pop = document.getElementById("pmPop"), n = document.getElementById("poemN"), empty = document.querySelector(".pm-empty");
  const q = (s) => pop.querySelector(s);
  const EDIT = new URLSearchParams(location.search).has("edit");
  const KEY = "poemEdits";
  let ed = { added: [], removed: [] };
  try { ed = Object.assign(ed, JSON.parse(localStorage.getItem(KEY) || "{}")); } catch (e) {}
  const save = () => localStorage.setItem(KEY, JSON.stringify(ed));
  const slug = (t) => (t || "untitled").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const TONES = ["lime", "salmon", "white", "yellow", "blue"];
  const list = () => window.__POEMS.concat(ed.added).filter((p) => !ed.removed.includes(p.title));
  const DEMO = new URLSearchParams(location.search).has("demo");
  const SAMPLE = ["Sample one", "Sample two", "Sample three", "Sample four"].map((t, i) => ({ title: t, date: "Demo", published: i % 2 === 0, text: "Placeholder line one\nPlaceholder line two\nPlaceholder line three\nPlaceholder line four" }));
  if (DEMO) window.__POEMS = SAMPLE;
  grid.className = "pm-grid s-note";
  let shown = [], cur = 0;

  function render() {
    shown = list();
    if (BOOK && shown.length > 1) shown = [shown[Math.floor(Math.random() * shown.length)]];
    grid.innerHTML = "";
    shown.forEach((p, i) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "pm-card t-" + TONES[i % TONES.length];
      b.style.setProperty("--r", ((i % 3) - 1) * 1.2 + "deg");
      const prev = (p.text || "").trim().split("\n").slice(0, 4).join("\n");
      b.innerHTML = '<span class="pm-badge" hidden>★ published</span><h3></h3><pre></pre><small></small>';
      b.querySelector("h3").textContent = p.title;
      b.querySelector("pre").textContent = prev;
      b.querySelector("small").textContent = p.date || "";
      if (p.published) b.querySelector(".pm-badge").hidden = false;
      b.onclick = () => open(i);
      b.onfocus = () => { const { step, n } = geo(); tgt = -(i - (n - 1) / 2) * step; kick(); };
      grid.appendChild(b);
    });
    n.textContent = shown.length;
    empty.hidden = shown.length > 0;
    document.querySelector(".pm-count").hidden = shown.length === 0;
    layout();
    if (typeof BOOK !== "undefined" && BOOK && desk) buildBook();
  }

  let mx = 0.5, off = 0, tgt = 0, running = false;
  const geo = () => { const vw = window.innerWidth; return { step: vw < 700 ? 56 : 104, n: shown.length }; };
  function frame() {
    const { step, n } = geo(), cards = grid.children;
    off += (tgt - off) * 0.12;
    for (let i = 0; i < cards.length; i++) {
      const x = (i - (n - 1) / 2) * step + off, d = Math.abs(x) / step;
      const c = cards[i];
      c.style.transform = "translateX(" + x.toFixed(1) + "px) rotate(" + (x / step * 1.6).toFixed(2) + "deg) scale(" + (d < 0.5 ? 1.03 : 1) + ")";
      c.style.zIndex = 1000 - Math.round(d * 10);
    }
    if (Math.abs(tgt - off) > 0.2) requestAnimationFrame(frame); else running = false;
  }
  function kick() { if (!running) { running = true; requestAnimationFrame(frame); } }
  function layout() {
    const { step, n } = geo();
    tgt = (0.5 - mx) * (n - 1) * step;
    kick();
  }
  window.addEventListener("pointermove", (e) => { mx = e.clientX / window.innerWidth; layout(); });
  window.addEventListener("resize", layout);

  function open(i) {
    cur = (i + shown.length) % shown.length;
    const p = shown[cur];
    q(".pm-h").textContent = p.title;
    q(".pm-d").textContent = p.date || "";
    q(".pm-t").textContent = p.text;
    q(".pm-b").hidden = !p.published;
    const l = q(".pm-l");
    l.hidden = !(p.published && typeof p.published === "string");
    if (!l.hidden) l.href = p.published;
    q(".pm-nav").hidden = shown.length < 2;
    const del = q(".pm-del");
    if (del) del.hidden = !EDIT;
    pop.hidden = false;
    pop.querySelector(".pm-x").focus();
    try { history.replaceState(null, "", "#" + slug(p.title) + (EDIT ? "" : "")); } catch (e) {}
  }
  const close = () => { pop.hidden = true; try { history.replaceState(null, "", location.pathname + location.search); } catch (e) {} };
  pop.addEventListener("click", (e) => {
    if (e.target === pop || e.target.closest(".pm-x")) close();
    else if (e.target.closest(".pm-prev")) open(cur - 1);
    else if (e.target.closest(".pm-next")) open(cur + 1);
  });
  document.addEventListener("keydown", (e) => {
    if (pop.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") open(cur - 1);
    if (e.key === "ArrowRight") open(cur + 1);
  });

  function removePoem(p) {
    if (!confirm("Remove “" + p.title + "” from this browser's view?")) return;
    const ai = ed.added.indexOf(p);
    if (ai >= 0) ed.added.splice(ai, 1); else ed.removed.push(p.title);
    save(); close(); render();
  }

  // notebook on the desk
  const BOOK = !new URLSearchParams(location.search).has("stack");
  const desk = document.getElementById("pmDesk");
  let turned = 0, leaves = [], bookEl = null, deskReady = false;
  const el = (tag, cls, txt) => { const x = document.createElement(tag); if (cls) x.className = cls; if (txt != null) x.textContent = txt; return x; };
  const nudge = (label, act, cls) => { const b = el("button", "bk-nudge " + (cls || ""), label); b.dataset.act = act; b.type = "button"; return b; };
  function buildBook() {
    desk.querySelectorAll(".pm-bookwrap").forEach((x) => x.remove());
    const wrap = el("div", "pm-bookwrap");
    bookEl = el("div", "pm-book");
    bookEl.appendChild(el("div", "bk-base"));
    const mk = (front, backNode) => {
      const lf = el("div", "bk-leaf"), f = el("div", "bk-face bk-front"), b = el("div", "bk-face bk-back");
      front(f); if (backNode) backNode(b);
      lf.append(f, b); return lf;
    };
    const total = shown.length + 3;
    const page = (f, i) => { f.classList.add("bk-paper"); f.appendChild(el("span", "bk-no", i)); };
    const back = (b) => b.classList.add("bk-paper");
    const L = [];
    L.push(mk((f) => {
      f.classList.add("bk-cover");
      f.append(el("i", "bk-band"), el("div", "bk-ctitle", "Poems"), el("div", "bk-csub", "by arushi"), el("span", "bk-hint", "click to open"));
      f.setAttribute("role", "button"); f.tabIndex = 0; f.dataset.act = "next";
    }, (b) => b.classList.add("bk-inside")));
    if (!shown.length) L.push(mk((f) => {
      page(f, "");
      f.append(el("h2", "bk-hi", "Poems are on their way."), el("p", "bk-sub", "Check back soon."), nudge("close the diary ↺", "close"));
    }, back));
    shown.forEach((p, i) => {
      L.push(mk((f) => {
        page(f, i + 1);
        const hd = el("div", "bk-hd");
        hd.append(el("h3", "", p.title));
        if (p.published) hd.append(el("span", "pm-badge", "★ published"));
        f.append(hd);
        if (p.date) f.append(el("div", "bk-date", p.date));
        f.append(el("pre", "bk-text", p.text));
        if (typeof p.published === "string") { const a = el("a", "bk-link", "read it where it was published →"); a.href = p.published; a.target = "_blank"; a.rel = "noopener"; f.append(a); }
        if (EDIT) { const d = el("button", "bk-del", "remove"); d.type = "button"; d.onclick = (ev) => { ev.stopPropagation(); removePoem(p); }; f.append(d); }
        f.append(nudge("close the diary ↺", "close"));
      }, back));
    });
    leaves = L;
    L.forEach((x) => bookEl.appendChild(x));
    wrap.appendChild(bookEl);
    desk.appendChild(wrap);
    wrap.addEventListener("click", (e) => {
      const t = e.target.closest("[data-act]"); if (!t) return;
      const a = t.dataset.act;
      if (a === "close") { go(0); if (list().length > 1) setTimeout(buildBook0, 1000); } else if (a === "next") go(turned + 1); else if (a === "prev") go(turned - 1);
    });
    wrap.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.target.dataset && e.target.dataset.act === "next") go(turned + 1); });
    turned = 0; paint(true);
  }
  function buildBook0() { render(); }
  function paint(instant) {
    const N = leaves.length;
    bookEl.classList.toggle("open", turned > 0);
    if (parent !== window) parent.postMessage({ diaryOpen: turned > 0 }, "*");
    leaves.forEach((lf, i) => {
      const was = lf.classList.contains("turned"), is = i < turned;
      lf.classList.toggle("turned", is);
      lf.style.transitionDelay = "0s";
      if (instant || was === is) { lf.style.zIndex = is ? i + 1 : N - i; return; }
      lf.style.zIndex = 500;
      clearTimeout(lf._z);
      lf._z = setTimeout(() => { lf.style.zIndex = is ? i + 1 : N - i; }, 460);
    });
  }
  function go(t) {
    t = Math.max(0, Math.min(leaves.length - 1, t));
    if (t === turned) return;
    turned = t; paint();
  }
  if (BOOK && desk) {
    desk.hidden = false; grid.hidden = true;
    document.querySelector(".pm-hint").hidden = true;
    document.addEventListener("keydown", (e) => {
      if (!pop.hidden || /INPUT|TEXTAREA/.test((e.target.tagName || ""))) return;
      if (e.key === "ArrowRight") go(turned + 1);
      if (e.key === "ArrowLeft") go(turned - 1);
    });
    document.body.classList.add("pm-diary");
  }

  render();
  const h = location.hash.slice(1);
  if (h) { const i = shown.findIndex((p) => slug(p.title) === h); if (i >= 0) { if (BOOK && desk) go(1); else open(i); } }

  if (!EDIT) return;
  const admin = document.querySelector(".pm-admin");
  admin.hidden = false;
  const form = admin.querySelector("form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const link = (f.get("link") || "").trim();
    const p = { title: f.get("title").trim(), date: f.get("date").trim(), published: f.get("published") ? (link || true) : false, text: f.get("text").replace(/\s+$/, "") };
    ed.added.push(p); save(); form.reset(); render();
  });
  q(".pm-del").onclick = () => removePoem(shown[cur]);
  admin.querySelector(".pm-export").onclick = () => {
    const out = { title: "Poems", intro: document.querySelector(".pm-head .lede").textContent, poems: list() };
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)], { type: "application/json" }));
    a.download = "poems.json"; a.click();
  };
  admin.querySelector(".pm-reset").onclick = () => { if (confirm("Discard all local edits?")) { localStorage.removeItem(KEY); location.reload(); } };
})();
