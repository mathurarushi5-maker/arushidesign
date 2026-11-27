(function(){
const D=(window.__LAB&&window.__LAB.length)?window.__LAB:[
 {t:'Sample: Prompt-to-prototype',y:2026,k:'Prototype',tools:['Claude','Figma'],c:'c1',d:'Turning a one-line idea into a clickable flow.',w:'Fast first draft',b:'Spacing was off',l:'Be specific about layout'},
 {t:'Sample: Brand voice bot',y:2026,k:'Prompt',tools:['GPT'],c:'c2',d:'Tone-of-voice checker for UX copy.',w:'Caught jargon',b:'Too literal',l:'Give examples, not rules'},
 {t:'Sample: Design critique agent',y:2025,k:'Tool',tools:['Copilot'],c:'c3',d:'An agent that reviews screens against heuristics.',w:'Consistent notes',b:'Missed context',l:'Feed it the brief'},
 {t:'Sample: Icon set generator',y:2025,k:'Prototype',tools:['Midjourney'],c:'c4',d:'A cohesive doodle icon family.',w:'Great mood',b:'Uneven weights',l:'Lock a style reference'},
 {t:'Sample: Research synthesiser',y:2025,k:'Tool',tools:['Claude'],c:'c1',d:'Clustering interview notes into themes.',w:'Saved hours',b:'Invented quotes',l:'Always verify sources'},
 {t:'Sample: Motion moodboard',y:2024,k:'Prompt',tools:['Runway'],c:'c2',d:'Exploring motion directions from words.',w:'Surprising ideas',b:'Hard to control',l:'Iterate in small steps'}
];
const V=[['mq',''],['sb','']];
const views=document.getElementById('views');
const nm=p=>p.t.replace('Sample: ','');
const shot=p=>`<div class="shot ${p.c}">${nm(p)}</div>`;
const tg=p=>p.tools.map(x=>`<span class="tag">${x}</span>`).join('');
const wbl=p=>`<div class="wbl"><span class="w">✓ worked<br>${p.w}</span><span class="b">✗ broke<br>${p.b}</span><span class="l">★ learned<br>${p.l}</span></div>`;
const chips=()=>`<div class="chips">`+['All','Prototype','Prompt','Tool'].map((c,i)=>`<button class="${i?'':'on'}">${c}</button>`).join('')+'</div>';
const R=[-1.6,1.2,-.8,1.8,-1.2,.9];
const html={
 nb:()=>chips()+`<div class="nb"><div class="nb-grid">${D.map((p,i)=>`<article class="nb-card" data-i="${i}" data-k="${p.k}" style="--r:${R[i]}deg">${shot(p)}<h3>${nm(p)}</h3><p>${p.d}</p>${wbl(p)}<div class="tags"><span class="tag">${p.k}</span>${tg(p)}</div></article>`).join('')}</div></div>`,
 sb:()=>{
  const CP=[[3,48,-3],[27,78,2],[51,36,-2],[75,66,3],[14,372,2],[38,392,-2]];
  const TG=['wip','done','','now tinkering ✦','','done'];
  const cards=D.map((p,i)=>{const c=CP[i%6];return `<div class="stk pl" data-i="${i}" style="--x:${c[0]}%;--y:${c[1]}px;--r:${c[2]}deg" role="button" aria-label="Open ${nm(p)}">${shot(p)}${TG[i]?`<span class="tag t${i%3}">${TG[i]}</span>`:''}<span class="open">open ↗</span>${nm(p)}</div>`}).join('');
  const sw=['#1f2bff','#c8f560','#ff9db8','#ffd23f','#16150f'].map(c=>`<i style="background:${c}"></i>`).join('');
  const cal=Array.from({length:28},(_,i)=>`<u class="${i===17?'ring':''}">${i+1}</u>`).join('');
  const S=[
   [0.5,10,-40,'sn-washi',''],[94,660,-38,'sn-washi w2',''],
   [85.6,513,-3,'sn-yellow','<span>Sample reminder: ship small, then iterate.</span>'],
   [25.2,320,0,'sn-btn','v1.0'],
   [73.2,629,-3,'sn-fails','<b>wall of fails</b><span>✗ sample: prompt too vague</span><span>✗ sample: wrong aspect</span>'],
   [70,392,3,'sn-blue','<span>Sample idea: what if it explained itself?</span>'],
   [10.2,304,-3,'sn-badge2','now tinkering ✦'],
   [69.7,507,2,'sn-idx','<b>Sample prompt</b><span>“act as a patient design coach…”</span>'],
   [84.2,389,3,'sn-fort','<span>Sample fortune: the bug is the feature.</span>'],
   [60.4,649,-3,'sn-tix','<b>ADMIT ONE</b><span>sample event · 2026</span>'],
   [1.4,392,2,'sn-list2','<b>testing now</b><label><i></i>sample flow</label><label><i></i>sample prompt</label><label><i></i>sample tool</label>'],
   [1.4,599,2,'sn-award','<div class="ros">★</div><b>GenAI Hackathon 2026</b><span>award</span>'],
   [86.7,619,-2,'sn-pink','<span>“Sample quote goes here.”</span><em>— someone worth quoting</em>'],
   [12.7,649,3,'sn-biz','<b>Arushi</b><span>product designer</span>'],
   [90,40,-6,'sn-doodle2','<svg viewBox="0 0 120 80" fill="none" stroke="#1f2bff" stroke-width="3" stroke-linecap="round"><path d="M8 60C30 10 70 10 104 44"/><path d="M88 36L106 46L92 60"/></svg>']
  ].map(x=>`<div class="sn pl ${x[3]}" style="--x:${x[0]}%;--y:${x[1]}px;--r:${x[2]}deg">${x[4]}</div>`).join('');
  const string=`<svg class="string" viewBox="0 0 1000 740" preserveAspectRatio="none" aria-hidden="true"><g fill="none" stroke="#c8262b" stroke-width="2.4" vector-effect="non-scaling-stroke" stroke-linecap="round"><path d="M135 56Q255 8 375 86"/><path d="M375 86Q495 14 615 44"/><path d="M615 44Q735 6 855 74"/><path d="M375 86Q250 220 245 380"/><path d="M245 380Q365 340 485 400"/></g></svg>`;
  return `<p class="note" style="margin-bottom:16px">click a card to open it · drag the little things around</p><div class="cork">${S}${cards}</div>`},
 tl:()=>`<div class="tl">${D.map(p=>`<div class="tl-i"><div><div class="tl-d">${p.y}</div>${shot(p)}</div><div><h3>${nm(p)}</h3><p>${p.d}</p><div class="tags">${tg(p)}</div><div class="tl-l">→ ${p.l}</div></div></div>`).join('')}</div>`,
 ix:()=>`<div class="ix">${D.map((p,i)=>`<div class="ix-r" data-i="${i}"><span>0${i+1}</span><h3>${nm(p)}</h3><span>${p.k}</span><span>${p.y}</span></div>`).join('')}</div><p class="note" style="margin-top:14px">hover a row for a peek</p>`,
 mq:()=>{const m=['ai tinkering','small experiments','what worked','what broke','what I learned'];const s=m.map(x=>`<span>${x}</span><b>✦</b>`).join('');return `<div class="mq"><div>${s}${s}${s}</div></div>`}
};
V.forEach(([id,h])=>{const v=document.createElement('section');v.className='lab-sec';v.id='v-'+id;v.innerHTML=(h?`<h2>${h}</h2>`:'')+html[id]();views.appendChild(v);});
document.querySelectorAll('.chips').forEach(c=>c.onclick=e=>{if(e.target.tagName!=='BUTTON')return;c.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b===e.target));
 const k=e.target.textContent;document.querySelectorAll('#v-nb .nb-card').forEach(a=>a.style.display=(k==='All'||a.dataset.k===k)?'':'none')});
const pop=document.getElementById('pop'),popIn=document.getElementById('popIn');
const open=i=>{const p=D[i];popIn.innerHTML=(p.img?`<img src="${p.img}" alt="" style="border-radius:14px">`:shot(p))+`<div class="tags"><span class="tag">${p.k}</span><span class="tag">${p.y}</span>${tg(p)}</div><h3>${nm(p)}</h3><p>${p.d}</p><div style="margin-top:14px">${wbl(p)}</div>`+(p.url?`<p style="margin-top:16px"><a class="li-back" href="${p.url}" target="_blank" rel="noopener">View project ↗</a></p>`:'');pop.classList.add('on')};
document.querySelectorAll('.stk,.nb-card,.cg-c').forEach(c=>{c.style.cursor='pointer';c.tabIndex=0;c.onclick=()=>open(c.dataset.i);c.onkeydown=e=>{if(e.key==='Enter')open(c.dataset.i)}});
document.addEventListener('keydown',e=>{if(e.key==='Escape')pop.classList.remove('on')});
pop.onclick=e=>{if(e.target===pop||e.target.tagName==='BUTTON')pop.classList.remove('on')};

const ck=document.querySelector('.cork');
const fit=()=>{if(ck)ck.style.zoom=Math.max(.2,ck.parentNode.clientWidth/1100)};fit();addEventListener('resize',fit);
document.querySelectorAll('.sn').forEach(n=>{let x=0,y=0,sx,sy,d=false;n.style.touchAction='none';
 n.addEventListener('pointerdown',e=>{d=true;const z=+ck.style.zoom||1;sx=e.clientX-x*z;sy=e.clientY-y*z;n.setPointerCapture(e.pointerId);n.classList.add('drag')});
 n.addEventListener('pointermove',e=>{if(!d)return;const z=+ck.style.zoom||1;x=(e.clientX-sx)/z;y=(e.clientY-sy)/z;n.style.translate=x+'px '+y+'px'});
 n.addEventListener('pointerup',()=>{d=false;n.classList.remove('drag')})});
})();
