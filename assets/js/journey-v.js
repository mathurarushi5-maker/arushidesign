// journey: renders the boarding-pass deck from the role list in the .exp markup
(function () {
  const about = document.getElementById("about"), box = document.getElementById("jv");
  if (!about || !box) return;
  const roles = [...document.querySelectorAll(".exp li")].map((li) => {
    const loc = (li.querySelector(".loc") || {}).textContent || "";
    const m = loc.match(/^(\S+)\s+(.*)$/);
    return {
      when: li.querySelector(".when2").textContent,
      title: li.querySelector("h4").childNodes[0].textContent.trim(),
      org: (li.querySelector("h4 em") || {}).textContent.replace(/^·\s*/, ""),
      flag: m ? m[1] : "", city: m ? m[2] : loc,
      text: (li.querySelector("p") || {}).textContent || "",
      edu: !!li.querySelector(".pin path[d^='M2 9']"),
    };
  });
  const esc = (t) => t.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  const yr = (w) => (w.match(/\d{4}/g) || [""])[0];
  const ICON = { edu: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-label="Studies"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/><path d="M22 9v6"/></svg>', work: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-label="Work"><rect x="5" y="5" width="14" height="10" rx="1.5"/><path d="M2 19h20l-2-4H4z"/></svg>' };
  const LOGO = (o) => (/adobe/i.test(o) ? "adobe" : /lloyds/i.test(o) ? "lloyds" : /punjab/i.test(o) ? "pnb" : /queen mary/i.test(o) ? "qmul" : /lucknow/i.test(o) ? "lucknow" : /freelance/i.test(o) ? "freelance" : "");
  const isEdu = (r) => r.edu || /university|college/i.test(r.org);
  const render = () => '<div class="jd"><button class="jd-n" data-d="-1" aria-label="Previous">‹</button><div class="jd-deck">' + roles.map((r, i) => {
      const prev = roles[i + 1];
      return `<article class="jd-t" data-i="${i}"><div class="jp-main">${LOGO(r.org) ? `<img class="jp-logo jp-logo-${LOGO(r.org)}" src="/assets/logos/${LOGO(r.org)}.png" alt="${esc(r.org)} logo">` : ""}<div class="jp-top"><i class="jp-ic">${isEdu(r) ? ICON.edu : ICON.work}</i><small>${esc(r.when)}</small></div><b>${esc(r.title)}</b><span>${esc(r.org)}</span><p>${esc(r.text)}</p></div><div class="jp-stub"><div class="jp-fl"><b>${prev ? prev.flag : "✦"}</b><i>→</i><b>${r.flag}</b></div><div class="jp-stamp"><small>arrived</small><em>${esc(r.city.split(",")[0])}</em><small>${esc(yr(r.when))}</small></div><div class="jp-bar" style="--s:${3 + (i * 5) % 7}px"></div></div></article>`;
    }).join("") + '</div><button class="jd-n" data-d="1" aria-label="Next">›</button></div>';
  box.hidden = false;
  box.className = "jv jv-pass";
  box.innerHTML = render();
  function deck(n) { const d = box.querySelector(".jd-deck"); if (!d) return; const c = Math.max(0, Math.min(roles.length - 1, (+d.dataset.i || 0) + n)); d.dataset.i = c; d.querySelectorAll(".jd-t").forEach((t) => { const o = +t.dataset.i - c; t.style.setProperty("--o", o); t.style.visibility = o < 0 ? "hidden" : ""; t.style.opacity = o > 2 ? 0 : 1; t.style.pointerEvents = o > 2 ? "none" : ""; }); box.querySelectorAll(".jd-n").forEach((b) => (b.disabled = (+b.dataset.d < 0 && c === 0) || (+b.dataset.d > 0 && c === roles.length - 1))); };
  box.addEventListener("click", (e) => {
    const nb = e.target.closest(".jd-n"); if (nb) return deck(+nb.dataset.d);
    if (e.target.closest(".jd-t")) return deck(1);
  });
  deck(0);
})();
