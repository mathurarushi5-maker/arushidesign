(function () {
  const shelf = document.getElementById("shelf");
  if (!shelf) return;
  const pop = document.getElementById("bkPop"), n = document.getElementById("libN");
  const empty = document.querySelector(".lib-empty"), pills = document.querySelector(".lib-filters");
  const q = (s) => pop.querySelector(s);
  const EDIT = new URLSearchParams(location.search).has("edit");
  const KEY = "libEdits";
  let ed = { over: {}, added: [] };
  try { ed = Object.assign(ed, JSON.parse(localStorage.getItem(KEY) || "{}")); } catch (e) {}
  const save = () => localStorage.setItem(KEY, JSON.stringify(ed));
  const PAL = [["#d2f26f", "#16150f"], ["#ffb4a2", "#16150f"], ["#1f2bff", "#d2f26f"], ["#ffffff", "#16150f"], ["#ffe27a", "#16150f"], ["#c9c2ff", "#16150f"], ["#a9d8ff", "#16150f"]];

  function fill(btn, b) {
    const d = btn.dataset;
    d.title = b.title; d.author = b.author; d.genre = b.genre; d.status = b.status || "read";
    d.rating = b.rating == null ? "" : b.rating; d.note = b.note || ""; d.year = b.year || ""; d.cover = b.cover || "";
  }

  function addPill(g) {
    if (!pills || [...pills.children].some((x) => x.dataset.f === g)) return;
    const p = document.createElement("button");
    p.dataset.f = g; p.textContent = g;
    pills.appendChild(p);
  }

  function spine(b, i) {
    const [bg, fg] = PAL[(shelf.children.length + i) % PAL.length];
    const label = b.spine || b.title;
    const w = Math.max(32, Math.min(46, 28 + label.length * .75));
    const h = Math.max(240, Math.min(300, Math.round(200 + label.length * 4)));
    const wrap = document.createElement("div");
    wrap.className = "bk-w"; wrap.dataset.genre = b.genre;
    wrap.innerHTML = '<button class="bk"><span class="bk-t"></span><span class="bk-a"></span></button>';
    const btn = wrap.firstChild;
    btn.style.cssText = `--bg:${bg};--fg:${fg};--w:${w}px;--h:${h}px`;
    btn.querySelector(".bk-t").textContent = label;
    btn.querySelector(".bk-a").textContent = b.author.split(" ").pop();
    fill(btn, b);
    (shelf.querySelector(".srow:last-child") || shelf).appendChild(wrap);
    addPill(b.genre);
  }

  ed.added.forEach(spine);
  shelf.querySelectorAll(".bk").forEach((btn) => {
    const o = ed.over[btn.dataset.title];
    if (o) { btn.dataset.rating = o.rating == null ? "" : o.rating; btn.dataset.note = o.note || ""; }
  });
  const total = () => { n.textContent = shelf.querySelectorAll(".bk-w:not([hidden])").length; };
  total();

  if (pills) pills.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    pills.querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
    shelf.querySelectorAll(".bk-w").forEach((w) => { w.hidden = !!b.dataset.f && w.dataset.genre !== b.dataset.f; });
    total();
    if (empty) empty.hidden = +n.textContent > 0;
  });

  const stars = (r) => (r ? "★".repeat(Math.round(r)) + "☆".repeat(5 - Math.round(r)) : "");
  let cur = null, curRating = 0;
  const paintStars = () => q(".bk-stars").querySelectorAll("button").forEach((s, i) => { s.textContent = i < curRating ? "★" : "☆"; });

  const close = () => { pop.hidden = true; };
  shelf.addEventListener("click", (e) => {
    const b = e.target.closest(".bk");
    if (!b) return;
    cur = b;
    const d = b.dataset;
    q(".bk-g").textContent = d.genre + (d.year ? " · " + d.year : "");
    q(".bk-h").textContent = d.title;
    q(".bk-by").textContent = "by " + d.author;
    q(".bk-r").textContent = stars(parseFloat(d.rating));
    const cv = q(".bk-cv"), img = cv.querySelector("img");
    cv.classList.toggle("none", !d.cover);
    img.src = d.cover || ""; img.alt = "Cover of " + d.title;
    q(".bk-card").style.setProperty("--bg", b.style.getPropertyValue("--bg"));
    q(".bk-card").style.setProperty("--fg", b.style.getPropertyValue("--fg"));
    if (EDIT) {
      curRating = parseFloat(d.rating) || 0;
      paintStars();
    }
    pop.hidden = false;
    q(".bk-x").focus();
  });
  pop.addEventListener("click", (e) => { if (e.target === pop || e.target.closest(".bk-x")) close(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });

  if (!EDIT) return;

  const admin = document.querySelector(".lib-admin");
  admin.hidden = false;
  q(".bk-edit").hidden = false;
  q(".bk-r").style.display = "none";
  const sw = q(".bk-stars");
  for (let i = 1; i <= 5; i++) {
    const s = document.createElement("button");
    s.type = "button"; s.setAttribute("aria-label", i + " stars");
    s.onclick = () => { curRating = curRating === i ? 0 : i; paintStars(); };
    sw.appendChild(s);
  }
  q(".bk-save").onclick = () => {
    const rating = curRating || null;
    const t = cur.dataset.title;
    const a = ed.added.find((x) => x.title === t);
    if (a) a.rating = rating; else ed.over[t] = { rating };
    save();
    cur.dataset.rating = rating || "";
    q(".bk-r").textContent = stars(rating);
    close();
  };

  const res = admin.querySelector(".lib-res");
  admin.querySelector(".lib-add").addEventListener("submit", async (e) => {
    e.preventDefault();
    res.innerHTML = "<li>Searching…</li>";
    const term = new FormData(e.target).get("q");
    try {
      const r = await fetch("https://openlibrary.org/search.json?limit=6&fields=title,author_name,cover_i,first_publish_year&q=" + encodeURIComponent(term));
      const docs = (await r.json()).docs;
      res.innerHTML = "";
      if (!docs.length) res.innerHTML = "<li>No matches.</li>";
      docs.forEach((d) => {
        const li = document.createElement("li");
        const cover = d.cover_i ? `https://covers.openlibrary.org/b/id/${d.cover_i}-L.jpg` : "";
        li.innerHTML = `<img alt="" src="${cover}"><span></span><button type="button">Add</button>`;
        li.querySelector("span").textContent = `${d.title} — ${(d.author_name || ["Unknown"])[0]}${d.first_publish_year ? " (" + d.first_publish_year + ")" : ""}`;
        li.querySelector("button").onclick = () => {
          const genre = (prompt("Genre for this book?", "Fiction") || "").trim();
          if (!genre) return;
          const b = { title: d.title, author: (d.author_name || ["Unknown"])[0], genre, series: "", status: "read", rating: null, note: "", cover, year: d.first_publish_year || "" };
          ed.added.push(b); save(); spine(b, ed.added.length); total();
          li.remove();
          [...shelf.querySelectorAll(".bk")].pop().click();
        };
        res.appendChild(li);
      });
    } catch (err) { res.innerHTML = "<li>Search failed — check your connection.</li>"; }
  });

  admin.querySelector(".lib-export").onclick = () => {
    const books = window.__LIB.map((b) => Object.assign({}, b, ed.over[b.title] || {})).concat(ed.added);
    const out = { title: "Library", intro: document.querySelector(".lib-head .lede").textContent, books };
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)], { type: "application/json" }));
    a.download = "library.json"; a.click();
  };
  admin.querySelector(".lib-reset").onclick = () => { if (confirm("Discard all local edits?")) { localStorage.removeItem(KEY); location.reload(); } };
})();
