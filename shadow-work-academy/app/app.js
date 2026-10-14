(function () {
  'use strict';
  var M = SWA.modules.sort(function (a, b) { return a.id - b.id; });
  var KEY = SWA.meta.storageKey;
  var memory = null, storageOK = true;

  // ---------- state (localStorage only; nothing leaves the browser) ----------
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : { v: 1, name: '', done: {}, doneAt: {}, a: {}, last: null, started: null };
    } catch (e) { storageOK = false; return memory || { v: 1, name: '', done: {}, doneAt: {}, a: {}, last: null, started: null }; }
  }
  var S = load();
  memory = S;
  var timer;
  function save() {
    clearTimeout(timer);
    timer = setTimeout(function () {
      try { localStorage.setItem(KEY, JSON.stringify(S)); storageOK = true; }
      catch (e) { storageOK = false; }
      var n = document.getElementById('saveNote');
      if (n) n.textContent = storageOK ? 'Saved on this device' : 'Could not save — your browser is blocking storage. Use Backup to keep your work.';
    }, 250);
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function mod(n) { return M.filter(function (m) { return m.id === +n; })[0]; }
  function doneCount() { return M.filter(function (m) { return S.done[m.id]; }).length; }

  // ---------- reusable field renderers ----------
  function field(id, label, rows) {
    return '<div class="field"><label for="f_' + id + '">' + esc(label) + '</label><textarea id="f_' + id + '" data-k="' + id + '" rows="' + (rows || 3) + '">' + esc(S.a[id] || '') + '</textarea></div>';
  }
  function table(id, cols, rows) {
    var h = '<div class="tablewrap"><table class="grid"><thead><tr>' + cols.map(function (c) { return '<th scope="col">' + esc(c.label) + '</th>'; }).join('') + '</tr></thead><tbody>';
    for (var r = 0; r < rows; r++) {
      h += '<tr>' + cols.map(function (c) {
        var k = id + '.' + r + '.' + c.id;
        return '<td data-label="' + esc(c.label) + '"><textarea aria-label="' + esc(c.label) + ', row ' + (r + 1) + '" data-k="' + k + '" rows="2">' + esc(S.a[k] || '') + '</textarea></td>';
      }).join('') + '</tr>';
    }
    return h + '</tbody></table></div>';
  }
  function checks(id, label, opts) {
    return '<fieldset class="field"><legend>' + esc(label) + '</legend>' + opts.map(function (o, i) {
      var k = id + '.' + i;
      return '<label class="chk"><input type="checkbox" data-k="' + k + '" data-bool="1"' + (S.a[k] ? ' checked' : '') + '> <span>' + esc(o) + '</span></label>';
    }).join('') + '</fieldset>';
  }
  function scale(id, label, items) {
    return '<fieldset class="field"><legend>' + esc(label) + '</legend>' + items.map(function (it, i) {
      var k = id + '.' + i;
      return '<div class="scale"><span>' + esc(it) + '</span><span class="opts" role="radiogroup" aria-label="' + esc(it) + '">' + [1, 2, 3, 4, 5].map(function (n) {
        return '<label><input type="radio" name="' + k + '" data-k="' + k + '" value="' + n + '"' + (String(S.a[k]) === String(n) ? ' checked' : '') + '><span>' + n + '</span></label>';
      }).join('') + '</span></div>';
    }).join('') + '<p class="muted small" id="auditTotal_' + id + '"></p></fieldset>';
  }
  function worksheet(m) {
    var w = m.worksheet, id = 'm' + m.id + 'tbl', h = '<h3>' + esc(w.title) + '</h3><p>' + esc(w.intro) + '</p>';
    if (w.scale) h += scale(w.scale.id, w.scale.label, w.scale.items);
    if (w.checks) h += checks(w.checks.id, w.checks.label, w.checks.options);
    if (w.columns) h += table(id, w.columns, w.rows);
    (w.summary || []).forEach(function (f) { h += field(f.id, f.label, 3); });
    return h;
  }
  function scriptsHTML(m) {
    var areas = {}; m.scripts.forEach(function (s) { (areas[s.area] = areas[s.area] || []).push(s); });
    return Object.keys(areas).map(function (a) {
      return '<h4>' + esc(a) + '</h4>' + areas[a].map(function (s) {
        return '<div class="script"><strong>' + esc(s.situation) + '</strong><p>“' + esc(s.text) + '”</p></div>';
      }).join('');
    }).join('');
  }
  function paras(arr) { return (arr || []).map(function (p) { return '<p>' + esc(p) + '</p>'; }).join(''); }
  function lessonHTML(m) {
    return m.lesson.map(function (s) {
      return '<section class="lesson-sec"><h3>' + esc(s.h) + '</h3>' + paras(s.p) + (s.list ? '<ul>' + s.list.map(function (l) { return '<li>' + esc(l) + '</li>'; }).join('') + '</ul>' : '') + '</section>';
    }).join('');
  }
  function moduleBody(m, opts) {
    opts = opts || {};
    var h = '';
    h += '<section id="lesson"><h2>Lesson</h2>' + lessonHTML(m) + '</section>';
    h += '<section id="scenario" class="callout"><h2>' + esc(m.scenario.title) + '</h2>' + paras(m.scenario.text) + '</section>';
    h += '<section id="reflect"><h2>Guided reflection</h2><p class="muted">Take your time. Short, honest answers are enough. Skip anything that feels like too much today.</p>' +
      m.reflection.map(function (r, i) { return field(r.id, (i + 1) + '. ' + r.q, 4); }).join('') + '</section>';
    h += '<section id="worksheet"><h2>Worksheet</h2>' + worksheet(m) + '</section>';
    if (m.scripts) h += '<section id="scripts"><h2>Boundary script examples</h2><p class="muted">Adapt the wording to sound like you. The full library is in Resources.</p>' + scriptsHTML(m) + '</section>';
    h += '<section id="action" class="callout sage"><h2>' + esc(m.action.title) + '</h2><p>' + esc(m.action.text) + '</p>' +
      field('m' + m.id + 'act', 'What I did, what happened, what I noticed:', 4) + '</section>';
    h += '<section id="recap"><h2>Module recap</h2><ul>' + m.recap.map(function (r) { return '<li>' + esc(r) + '</li>'; }).join('') + '</ul></section>';
    return h;
  }

  // ---------- views ----------
  function pct() { return Math.round(doneCount() / M.length * 100); }
  function banner() { return storageOK ? '' : '<div class="warn" role="alert">Your browser is blocking local storage, so progress cannot be saved between visits. You can still work here and use Backup on the Progress page to keep a copy.</div>'; }

  function vWelcome() {
    return '<div class="wrap narrow"><p class="eyebrow">Welcome</p><h1>From self-doubt to self-trust.</h1>' +
      '<p class="lead">This academy is a six-module, self-paced program for understanding the patterns behind people-pleasing, self-criticism, and difficulty with boundaries — and practicing different choices.</p>' +
      '<div class="card"><h2>How it works</h2><ol class="steps"><li><strong>Learn.</strong> Each module opens with a lesson and a real-life scenario.</li><li><strong>Reflect.</strong> Answer the guided questions and complete the worksheet in your own words.</li><li><strong>Practice.</strong> Try one real-world action step, then record what happened.</li><li><strong>Record.</strong> Mark the module complete and note your key insight.</li></ol>' +
      '<p class="muted">Plan on roughly 45–60 minutes per module plus a week of practice. One module a week works well.</p></div>' +
      '<div class="card"><h2>Before you begin</h2><ul><li>This is educational self-reflection, not therapy, diagnosis, or medical advice.</li><li>Go at your own pace and skip anything that feels like too much. If you are struggling, please reach out to a licensed professional.</li><li><strong>Where your answers live:</strong> they are saved in this browser on this device only. Clearing browser data erases them, so use <em>Backup</em> on the Progress page now and then. <a href="#/help">Details</a></li></ul></div>' +
      '<div class="field"><label for="nm">What should we call you? (optional)</label><input id="nm" type="text" autocomplete="given-name" value="' + esc(S.name) + '"></div>' +
      '<p><button class="btn" id="begin">' + (S.started ? 'Continue' : 'Begin Module 1') + '</button> <a class="btn ghost" href="#/dashboard">Go to dashboard</a></p></div>';
  }

  function vDashboard() {
    var next = M.filter(function (m) { return !S.done[m.id]; })[0];
    var last = S.last && mod(S.last);
    var cont = last && !S.done[last.id] ? last : next;
    var h = '<div class="wrap">' + banner() + '<p class="eyebrow">Dashboard</p><h1>' + (S.started ? (S.name ? 'Welcome back, ' + esc(S.name) + '.' : 'Welcome back.') : 'Your dashboard.') + '</h1>';
    h += '<div class="bar" role="progressbar" aria-valuenow="' + pct() + '" aria-valuemin="0" aria-valuemax="100" aria-label="Course progress"><span style="width:' + pct() + '%"></span></div><p class="muted">' + doneCount() + ' of ' + M.length + ' modules complete</p>';
    if (cont) h += '<div class="card feature"><p class="eyebrow">' + (S.started ? 'Continue where you left off' : 'Start here') + '</p><h2>Module ' + cont.id + ': ' + esc(cont.title) + '</h2><p>' + esc(cont.tagline) + '</p><a class="btn" href="#/module/' + cont.id + '">' + (S.started ? 'Resume' : 'Start') + ' module</a></div>';
    else h += '<div class="card feature"><h2>All six modules complete</h2><p>Keep going with your weekly review. Open the tracker in Resources.</p><a class="btn" href="#/resource/weekly">Open weekly tracker</a></div>';
    h += '<h2>Your six modules</h2><div class="grid3">' + M.map(function (m) {
      var st = S.done[m.id] ? 'Complete' : (S.last === m.id ? 'In progress' : 'Not started');
      return '<a class="card mod' + (S.done[m.id] ? ' done' : '') + '" href="#/module/' + m.id + '"><span class="num">' + m.id + '</span><h3>' + esc(m.title) + '</h3><p>' + esc(m.tagline) + '</p><p class="meta">' + m.minutes + ' min · ' + st + '</p></a>';
    }).join('') + '</div></div>';
    return h;
  }

  function vModule(n) {
    var m = mod(n); if (!m) return vDashboard();
    S.last = m.id; if (!S.started) S.started = new Date().toISOString(); save();
    var prev = mod(m.id - 1), nxt = mod(m.id + 1);
    var h = '<div class="wrap">' + banner() + '<p class="eyebrow">Module ' + m.id + ' of ' + M.length + ' · about ' + m.minutes + ' minutes</p><h1>' + esc(m.title) + '</h1><p class="lead">' + esc(m.tagline) + '</p>';
    h += '<nav class="toc" aria-label="In this module"><a href="#lesson" data-jump>Lesson</a><a href="#scenario" data-jump>Scenario</a><a href="#reflect" data-jump>Reflection</a><a href="#worksheet" data-jump>Worksheet</a><a href="#action" data-jump>Action</a><a href="#recap" data-jump>Recap</a><a href="#complete" data-jump>Complete</a></nav>';
    h += moduleBody(m);
    h += '<section id="complete" class="card feature"><h2>Complete this module</h2>' + field('m' + m.id + 'insight', 'My key insight from this module:', 3) +
      '<label class="chk big"><input type="checkbox" id="doneBox"' + (S.done[m.id] ? ' checked' : '') + '> <span>I have finished Module ' + m.id + '</span></label>' +
      '<p class="muted small" id="doneAt">' + (S.doneAt[m.id] ? 'Completed ' + new Date(S.doneAt[m.id]).toLocaleDateString() : '') + '</p>' +
      '<p class="actions"><button class="btn ghost" onclick="window.print()">Print this module</button> ' +
      (nxt ? '<a class="btn" href="#/module/' + nxt.id + '">Next: Module ' + nxt.id + '</a>' : '<a class="btn" href="#/progress">See my progress</a>') + '</p></section>';
    h += '<p class="pager">' + (prev ? '<a href="#/module/' + prev.id + '">← Module ' + prev.id + '</a>' : '<span></span>') + '<a href="#/dashboard">Dashboard</a>' + (nxt ? '<a href="#/module/' + nxt.id + '">Module ' + nxt.id + ' →</a>' : '<span></span>') + '</p>';
    return h + '<p class="muted small" id="saveNote">Saved on this device</p></div>';
  }

  function vProgress() {
    var filled = Object.keys(S.a).filter(function (k) { return S.a[k]; }).length;
    var h = '<div class="wrap">' + banner() + '<p class="eyebrow">Progress</p><h1>Your progress</h1><div class="bar" role="progressbar" aria-valuenow="' + pct() + '" aria-valuemin="0" aria-valuemax="100" aria-label="Course progress"><span style="width:' + pct() + '%"></span></div>' +
      '<p>' + doneCount() + ' of ' + M.length + ' modules complete · ' + filled + ' fields filled in</p><h2>Insights by module</h2>';
    h += M.map(function (m) {
      var ins = S.a['m' + m.id + 'insight'];
      return '<div class="card"><h3>Module ' + m.id + ': ' + esc(m.title) + ' <span class="pill ' + (S.done[m.id] ? 'ok' : '') + '">' + (S.done[m.id] ? 'Complete' : 'Not complete') + '</span></h3><p>' + (ins ? esc(ins).replace(/\n/g, '<br>') : '<span class="muted">No insight recorded yet.</span>') + '</p><a href="#/module/' + m.id + '">Open module</a></div>';
    }).join('');
    h += '<h2>Backup &amp; restore</h2><div class="card"><p>Your answers are stored only in this browser. Download a backup file to keep them safe or to move to another device. The file contains everything you have written, so store it somewhere private.</p>' +
      '<p class="actions"><button class="btn" id="exp">Download backup</button> <label class="btn ghost" for="imp">Restore from backup</label><input id="imp" type="file" accept="application/json,.json" hidden></p><p class="muted small" id="impMsg" role="status"></p></div>' +
      '<h2>Erase my data</h2><div class="card"><p>Remove all answers and progress from this browser. This cannot be undone, so download a backup first.</p><button class="btn danger" id="wipe">Erase everything</button></div></div>';
    return h;
  }

  function vResources() {
    var h = '<div class="wrap">' + banner() + '<p class="eyebrow">Resource library</p><h1>Your resources</h1><p class="lead">Use each one online in this academy or download the printable PDF. Your complete workbook includes every module and worksheet.</p>';
    h += '<div class="card feature"><h2>Complete Academy Workbook (PDF)</h2><p>All six modules with lessons, scenarios, reflections, and worksheets, formatted for print or tablet.</p><a class="btn" href="../resources/00-complete-academy-workbook.pdf" download>Download workbook</a></div><div class="grid2">';
    h += SWA.resources.map(function (r) {
      var link = r.type === 'ref' ? '#/module/' + r.ref.module + '" data-jump-ws="1' : '#/resource/' + r.id;
      return '<div class="card"><h3>' + esc(r.title) + '</h3><p>' + esc(r.blurb) + '</p><p class="actions"><a class="btn small" href="' + link + '">Open online</a> <a class="btn ghost small" href="../resources/' + r.file + '" download>PDF</a></p></div>';
    }).join('') + '</div></div>';
    return h;
  }

  function vResource(id) {
    var r = SWA.resources.filter(function (x) { return x.id === id; })[0];
    if (!r) return vResources();
    var h = '<div class="wrap">' + banner() + '<p class="eyebrow"><a href="#/resources">← Resources</a></p><h1>' + esc(r.title) + '</h1><p class="lead">' + esc(r.blurb) + '</p>';
    if (r.type === 'guide') h += r.sections.map(function (s) { return '<section><h2>' + esc(s.h) + '</h2>' + paras(s.p) + (s.list ? '<ul>' + s.list.map(function (l) { return '<li>' + esc(l) + '</li>'; }).join('') + '</ul>' : '') + '</section>'; }).join('');
    if (r.type === 'prompts') h += r.prompts.map(function (p, i) { return field('sw' + i, (i + 1) + '. ' + p, 4); }).join('');
    if (r.type === 'table') h += table('res_' + r.id, r.columns, r.rows);
    if (r.type === 'scripts') h += scriptsHTML(mod(5)) + '<h2>My own scripts</h2>' + [0, 1, 2].map(function (i) { return field('myscript' + i, 'Situation and script ' + (i + 1) + ':', 4); }).join('');
    if (r.type === 'values') {
      h += checks('vals', 'Part A — Circle (tick) the values that feel most like you, then narrow to your top three below.', SWA.values);
      h += field('vtop', 'My top three values and what each means to me in practice:', 4);
      h += checks('needs', 'Part B — Which needs matter most to you right now?', SWA.needs);
      h += field('vgap', 'Which of these values or needs is least honored in my current week?', 3);
      h += field('vact', 'One small, specific change that would honor it:', 3);
    }
    if (r.type === 'weekly') {
      for (var w = 1; w <= r.weeks; w++) {
        h += '<details class="week"' + (w === 1 ? ' open' : '') + '><summary>Week ' + w + '</summary>' + SWA.weeklyPrompts.map(function (p) { return field('wk' + w + '_' + p.id, p.label, 2); }).join('') +
          '<label class="chk"><input type="checkbox" data-k="wk' + w + '_done" data-bool="1"' + (S.a['wk' + w + '_done'] ? ' checked' : '') + '> <span>Review completed</span></label></details>';
      }
    }
    h += '<p class="actions"><button class="btn ghost" onclick="window.print()">Print</button> <a class="btn ghost" href="../resources/' + r.file + '" download>Download blank PDF</a></p><p class="muted small" id="saveNote">Saved on this device</p></div>';
    return h;
  }

  function vHelp() {
    return '<div class="wrap narrow">' + banner() + '<p class="eyebrow">Help &amp; privacy</p><h1>Help &amp; privacy</h1>' +
      '<h2>Where is my information stored?</h2><p>Everything you type is saved in your browser’s local storage on this device. This academy page does not include any analytics, forms, or code that sends your answers to a server. Fonts are loaded from Google Fonts when you are online, which means your browser contacts Google to download them. If you open the academy from a folder on your computer, no answers are uploaded.</p>' +
      '<p>Because the data lives only in this browser: it is not available on other devices, it can be erased if you clear site data or use a private window, and anyone with access to this browser profile could open it. Use Backup regularly, and store backup files privately.</p>' +
      '<h2>Printing</h2><p>Every module and resource has a Print button that produces a clean layout. Printed pages and backup files are your responsibility to store safely.</p>' +
      '<h2>Support</h2><p>For access or download problems, contact <a href="mailto:' + SWA.meta.supportEmail + '">' + SWA.meta.supportEmail + '</a>.</p>' +
      '<h2>Important</h2><p>The Shadow Work Academy is educational and not a substitute for therapy or medical advice. If you are in crisis or may harm yourself, contact local emergency services or a crisis line in your country.</p></div>';
  }

  // ---------- routing ----------
  var main = document.getElementById('main');
  function route() {
    var p = (location.hash || '#/').replace(/^#\/?/, '').split('/');
    var view, key = p[0] || 'welcome';
    if (key === 'welcome') view = vWelcome();
    else if (key === 'dashboard') view = vDashboard();
    else if (key === 'module') view = vModule(p[1]);
    else if (key === 'progress') view = vProgress();
    else if (key === 'resources') view = vResources();
    else if (key === 'resource') view = vResource(p[1]);
    else if (key === 'help') view = vHelp();
    else view = vWelcome();
    if (!location.hash && S.started) { location.replace('#/dashboard'); return; }
    main.innerHTML = view;
    document.title = 'The Shadow Work Academy';
    Array.prototype.forEach.call(document.querySelectorAll('[data-nav]'), function (a) { a.classList.toggle('on', a.getAttribute('data-nav') === key || (key === 'module' && a.getAttribute('data-nav') === 'dashboard')); });
    document.getElementById('nav').classList.remove('open'); document.getElementById('menuBtn').setAttribute('aria-expanded', 'false');
    window.scrollTo(0, 0); main.focus({ preventScroll: true });
    bind(key);
    updateAudit();
  }
  function updateAudit() {
    Array.prototype.forEach.call(document.querySelectorAll('[id^=auditTotal_]'), function (el) {
      var id = el.id.replace('auditTotal_', ''), t = 0, c = 0;
      for (var i = 0; i < 20; i++) { var v = S.a[id + '.' + i]; if (v) { t += +v; c++; } }
      el.textContent = c ? 'Your total so far: ' + t + ' across ' + c + ' answered. Higher totals suggest this pattern shows up often; this is a reflection aid, not a diagnostic score.' : '';
    });
  }
  function bind(key) {
    main.addEventListener('input', onInput); main.addEventListener('change', onInput);
    var b = document.getElementById('begin');
    if (b) b.onclick = function () { S.name = document.getElementById('nm').value.trim(); save(); location.hash = '#/module/' + (S.last || 1); };
    var d = document.getElementById('doneBox');
    if (d) d.onchange = function () {
      var id = +location.hash.split('/')[2];
      S.done[id] = d.checked; if (d.checked) S.doneAt[id] = new Date().toISOString(); else delete S.doneAt[id]; save();
      document.getElementById('doneAt').textContent = d.checked ? 'Completed ' + new Date().toLocaleDateString() : '';
    };
    Array.prototype.forEach.call(document.querySelectorAll('[data-jump]'), function (a) {
      a.onclick = function (e) { e.preventDefault(); var t = document.querySelector(a.getAttribute('href')); if (t) { t.scrollIntoView({ behavior: 'smooth', block: 'start' }); } };
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-jump-ws]'), function (a) {
      a.onclick = function () { setTimeout(function () { var t = document.getElementById('worksheet'); if (t) t.scrollIntoView(); }, 50); };
    });
    var e = document.getElementById('exp');
    if (e) e.onclick = function () {
      var blob = new Blob([JSON.stringify(S, null, 2)], { type: 'application/json' }), a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'shadow-work-academy-backup-' + new Date().toISOString().slice(0, 10) + '.json'; a.click();
    };
    var im = document.getElementById('imp');
    if (im) im.onchange = function () {
      var f = im.files[0]; if (!f) return; var rd = new FileReader();
      rd.onload = function () {
        try { var o = JSON.parse(rd.result); if (!o || o.v !== 1 || typeof o.a !== 'object') throw 0; S = o; memory = S; save(); document.getElementById('impMsg').textContent = 'Backup restored.'; setTimeout(route, 400); }
        catch (x) { document.getElementById('impMsg').textContent = 'That file is not a valid Shadow Work Academy backup.'; }
      }; rd.readAsText(f);
    };
    var w = document.getElementById('wipe');
    if (w) w.onclick = function () { if (confirm('Erase all your answers and progress from this browser? This cannot be undone.')) { S = { v: 1, name: '', done: {}, doneAt: {}, a: {}, last: null, started: null }; memory = S; try { localStorage.removeItem(KEY); } catch (x) {} route(); } };
  }
  var bound = false;
  function onInput(ev) {
    var t = ev.target, k = t.getAttribute && t.getAttribute('data-k');
    if (!k) return;
    S.a[k] = t.getAttribute('data-bool') ? t.checked : t.value;
    if (t.type === 'radio') S.a[k] = t.value;
    save(); updateAudit();
  }
  // main listeners are re-added per render; avoid duplicates by cloning guard
  var origRoute = route;
  route = function () { main.removeEventListener('input', onInput); main.removeEventListener('change', onInput); origRoute(); };
  var mb = document.getElementById('menuBtn');
  if (mb) mb.onclick = function () { var n = document.getElementById('nav'); var o = n.classList.toggle('open'); this.setAttribute('aria-expanded', o); };
  if (!window.SWA_PRINT) window.addEventListener('hashchange', route);
  window.SWA_UI = { vResource: vResource, worksheet: worksheet, mod: mod, moduleBody: moduleBody, table: table, field: field, lessonHTML: lessonHTML, scriptsHTML: scriptsHTML, checks: checks, esc: esc, paras: paras };
  if (!window.SWA_PRINT) route();
})();
