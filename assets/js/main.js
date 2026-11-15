/* ==========================================================================
   Mohammad Muslim — portfolio interactions
   Needs (loaded before this file): gsap, ScrollTrigger, Lenis, config.js, data.js
   Everything degrades gracefully: without GSAP/Lenis the site still works,
   and with prefers-reduced-motion the loader, smooth scroll and parallax are skipped.
   ========================================================================== */
(function () {
  'use strict';

  var S = window.SITE || {};
  var P = window.PROJECTS || [];
  var A = window.ARCHIVE || [];
  var html = document.documentElement;
  var page = document.body.getAttribute('data-page');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var hasGSAP = !!window.gsap && !!window.ScrollTrigger;
  var lenis = null;
  var leaving = false;
  var syncHamburger = function () {};
  var lang = html.getAttribute('lang') === 'ar' ? 'ar' : 'en';
  var rtl = lang === 'ar';
  var D = (window.I18N && window.I18N.ar) || {};

  /* i18n helpers: English is whatever is written in the HTML / code, Arabic comes from i18n.js */
  function t(key, en) { return rtl && D[key] != null ? D[key] : en; }
  function m(s) { return rtl && D.map && D.map[s] ? D.map[s] : s; }
  function pText(p) {
    var a = rtl && D.projects && D.projects[p.slug];
    return { title: a ? a.title : p.title, desc: a ? a.desc : p.desc, services: m(p.services) };
  }
  function applyI18n() {
    if (!rtl) return;
    $$('[data-i18n]').forEach(function (el) {
      var k = el.getAttribute('data-i18n'); if (D[k] == null) return;
      if (el.hasAttribute('data-i18n-html')) el.innerHTML = D[k]; else el.textContent = D[k];
    });
    $$('[data-i18n-placeholder]').forEach(function (el) {
      var k = el.getAttribute('data-i18n-placeholder'); if (D[k] != null) el.setAttribute('placeholder', D[k]);
    });
    if (D['title.' + page]) document.title = D['title.' + page];
    var md = document.querySelector('meta[name="description"]');
    if (md && D['desc.' + page]) md.setAttribute('content', D['desc.' + page]);
  }

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (m) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]; }); }
  function safeStore(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); if (v === null) sessionStorage.removeItem(k); else sessionStorage.setItem(k, v); } catch (e) { return null; } }

  var ARROW = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2.5 11.5l9-9M3.5 2.5h8v8" stroke="currentColor" stroke-width="1.5"/></svg>';

  if (hasGSAP) gsap.registerPlugin(ScrollTrigger);

  /* ------------------------------------------------------------------ */
  /* Site settings → DOM (email, phone, WhatsApp, socials, time)         */
  /* ------------------------------------------------------------------ */
  function bindSite() {
    $$('[data-bind="email"]').forEach(function (a) {
      a.href = 'mailto:' + S.email;
      var t = $('.btn-text-inner', a) || a;
      t.textContent = S.email;
    });
    var phoneText = S.phone ? S.phone.replace(/^(\+\d{3})(\d{2})(\d{3})(\d{4})$/, '$1 $2 $3 $4') : (S.phonePlaceholder || '');
    $$('[data-bind="phone"]').forEach(function (a) {
      var t = $('.btn-text-inner', a) || a;
      t.textContent = phoneText;
      if (S.phone) { a.href = 'tel:' + S.phone; }
      else { a.removeAttribute('href'); a.setAttribute('aria-disabled', 'true'); a.title = 'Phone number coming soon'; }
    });
    var wa = String(S.whatsapp || S.phone || '').replace(/\D/g, '');
    $$('[data-bind="whatsapp"]').forEach(function (a) {
      if (wa) { a.href = 'https://wa.me/' + wa; a.target = '_blank'; a.rel = 'noopener'; }
      else { a.hidden = true; }
    });
    $$('[data-socials]').forEach(function (ul) {
      ul.innerHTML = (S.socials || []).map(function (s) {
        return '<li class="btn btn-link btn-link-external"><a href="' + esc(s.url) + '" target="_blank" rel="noopener" class="btn-click magnetic" data-strength="20" data-strength-text="10"><span class="btn-text"><span class="btn-text-inner">' + esc(s.label) + '</span></span></a></li>';
      }).join('');
    });
    $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
    $$('[data-lang-toggle]').forEach(function (b) {
      var inner = $('.btn-text-inner', b) || b;
      inner.textContent = rtl ? 'English' : 'العربية';
      b.setAttribute('lang', rtl ? 'en' : 'ar');
      b.setAttribute('aria-label', rtl ? 'Switch to English' : 'التبديل إلى العربية');
      b.addEventListener('click', switchLang);
    });
  }

  /* Language switch: store the choice, play the page curtain, reload in the new language. */
  function switchLang() {
    var next = rtl ? 'en' : 'ar';
    try { localStorage.setItem('lang', next); } catch (e) { /* storage blocked: fall back to a plain reload */ }
    if (leaving) return;
    var c = $('.curtain');
    if (!hasGSAP || reduce || !c) { location.reload(); return; }
    leaving = true;
    var label = next === 'ar' ? 'العربية' : 'English';
    safeStore('ptLabel', label);
    $('#curtainLabel').textContent = label;
    html.classList.remove('menu-open');
    c.classList.add('is-active');
    gsap.fromTo(c, { y: '112vh' }, { y: 0, duration: .9, ease: 'power3.inOut', onComplete: function () { safeStore('pt', '1'); location.reload(); } });
  }

  function initClock() {
    var els = $$('[data-time]');
    if (!els.length) return;
    var fmt;
    try { fmt = new Intl.DateTimeFormat(rtl ? 'ar-AE-u-nu-latn' : 'en-US', { hour: '2-digit', minute: '2-digit', hour12: true, timeZone: S.timezone || 'Asia/Dubai' }); } catch (e) { return; }
    var tz = t('clock.gst', S.timezoneLabel || 'GST');
    function tick() { var txt = fmt.format(new Date()) + ' ' + tz; els.forEach(function (el) { el.textContent = txt; }); }
    tick(); setInterval(tick, 20000);
  }

  function setRollText() {
    $$('.btn-text-inner').forEach(function (el) {
      var t = Array.prototype.filter.call(el.childNodes, function (n) { return n.nodeType === 3; }).map(function (n) { return n.textContent; }).join('').trim();
      if (t) el.setAttribute('data-text', t);
    });
  }

  /* ------------------------------------------------------------------ */
  /* Renderers (data.js → markup)                                        */
  /* ------------------------------------------------------------------ */
  function tileHTML(p) {
    var x = pText(p);
    return '<article class="tile" data-kinds="' + p.kinds.join(' ') + '" data-cursor="view">' +
      '<a href="project.html?p=' + p.slug + '" data-label="' + esc(x.title) + '">' +
      '<div class="tile-image" style="background:' + p.color + '"><img src="' + p.cover + '" width="' + p.coverW + '" height="' + p.coverH + '" alt="' + esc(x.title) + '" loading="lazy" decoding="async"></div>' +
      '<div class="tile-meta"><h4>' + esc(x.title) + '</h4><p>' + esc(x.services) + (p.year ? ' &middot; ' + p.year : '') + '</p></div></a></article>';
  }

  function byGroup(g) { return P.filter(function (p) { return p.group === g; }); }

  function rowHTML(p, i) {
    var x = pText(p);
    return '<li data-i="' + i + '" data-cursor="view"><div class="stripe animate"></div>' +
      '<a href="project.html?p=' + p.slug + '" class="row" data-label="' + esc(x.title) + '"><div class="flex-col"><h4>' + esc(x.title) + '</h4></div><div class="flex-col"><p>' + esc(x.services) + '</p></div></a></li>';
  }

  function renderHome() {
    var ld = $('#workListDesign'); if (!ld) return;
    /* a few from each side, so design and development are shown separately */
    var design = byGroup('design').slice(0, 4), dev = byGroup('development').slice(0, 4);
    var all = design.concat(dev);
    var end = '<li aria-hidden="true"><div class="stripe animate"></div></li>';
    ld.innerHTML = design.map(function (p, i) { return rowHTML(p, i); }).join('') + end;
    $('#workListDev').innerHTML = dev.map(function (p, i) { return rowHTML(p, design.length + i); }).join('') + end;
    $('#tilesDesign').innerHTML = design.map(tileHTML).join('');
    $('#tilesDev').innerHTML = dev.map(tileHTML).join('');
    $('#floatImgs').innerHTML = all.map(function (p) { return '<div class="float-img"><img data-src="' + p.cover + '" alt=""></div>'; }).join('');
    $$('[data-count-projects]').forEach(function (el) { el.textContent = P.length; });
  }

  function renderWork() {
    var wrap = $('#workGroups'); if (!wrap) return;
    var groups = [['design', 'Design'], ['development', 'Development']];
    wrap.innerHTML = groups.map(function (g) {
      var list = byGroup(g[0]);
      return '<section class="work-group" data-group="' + g[0] + '"><h3 class="group-title">' + esc(t('filter.' + g[0], g[1])) + '<sup>' + list.length + '</sup></h3>' +
        '<div class="tiles">' + list.map(tileHTML).join('') + '</div></section>';
    }).join('');
    var bar = $('#filterBar');
    var opts = [['all', 'All', P.length], ['design', 'Design', byGroup('design').length], ['development', 'Development', byGroup('development').length]];
    var want = new URLSearchParams(location.search).get('f');
    if (!opts.some(function (o) { return o[0] === want; })) want = 'all';
    bar.innerHTML = '<h5>' + esc(t('work.services', 'Services')) + '</h5>' + opts.map(function (o) {
      return '<button class="filter-btn' + (o[0] === want ? ' active' : '') + '" data-f="' + o[0] + '">' + esc(t('filter.' + o[0], o[1])) + '<sup>' + o[2] + '</sup></button>';
    }).join('');
    function show(f) { $$('.work-group', wrap).forEach(function (g) { g.classList.toggle('is-hidden', f !== 'all' && g.getAttribute('data-group') !== f); }); }
    show(want);
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('.filter-btn'); if (!b) return;
      $$('.filter-btn', bar).forEach(function (x) { x.classList.toggle('active', x === b); });
      var f = b.getAttribute('data-f');
      function apply() {
        show(f);
        if (hasGSAP) { gsap.to(wrap, { opacity: 1, y: 0, duration: .6, ease: 'power3.out' }); ScrollTrigger.refresh(); }
      }
      if (hasGSAP) gsap.to(wrap, { opacity: 0, y: 24, duration: .3, ease: 'power2.in', onComplete: apply }); else apply();
    });
    var arch = $('#archiveList');
    if (arch) arch.innerHTML = A.map(function (a) {
      return '<li><a href="' + esc(a.url) + '" target="_blank" rel="noopener"><span class="a-name">' + esc(a.name) + '</span><span class="a-type">' + esc(m(a.type)) + '</span><span class="a-plat">' + esc(m(a.platform)) + '</span><span class="a-arrow">' + ARROW + '</span></a></li>';
    }).join('');
    $$('[data-count-projects]').forEach(function (el) { el.textContent = P.length; });
    $$('[data-count-archive]').forEach(function (el) { el.textContent = A.length; });
  }

  function renderProject() {
    var g = $('#gallery'); if (!g) return;
    var slug = new URLSearchParams(location.search).get('p');
    var i = P.findIndex(function (p) { return p.slug === slug; }); if (i < 0) i = 0;
    var p = P[i], n = P[(i + 1) % P.length], x = pText(p), nxt = pText(n);
    var who = t('name', S.name);
    document.title = x.title + ' — ' + who;
    var md = $('meta[name="description"]'); if (md) md.setAttribute('content', x.title + ' — ' + who + '. ' + x.desc);
    $('#pTitle').textContent = x.title;
    $('#pServices').textContent = x.services;
    $('#pYear').textContent = p.year || '';
    $('#pYear').parentNode.hidden = !p.year;
    var vis = $('#pVisit');
    if (vis && p.url) { vis.href = p.url; $('#pVisitWrap').hidden = false; }
    $('#pCount').textContent = p.images.length + ' ' + t('proj.pieces', 'pieces');
    $('#pDesc').textContent = x.desc;
    g.innerHTML = p.images.map(function (im, k) {
      return '<figure class="shot"><div class="frame" style="background:' + p.color + '"><img src="' + im.src + '" width="' + im.w + '" height="' + im.h + '" alt="' + esc(x.title + ' — ' + (im.caption || (k + 1))) + '" loading="lazy" decoding="async"></div>' +
        (im.caption ? '<figcaption>' + esc(im.caption) + '</figcaption>' : '') + '</figure>';
    }).join('');
    var nx = $('#nextProject');
    nx.href = 'project.html?p=' + n.slug; nx.setAttribute('data-label', nxt.title);
    $('#nextTitle').textContent = nxt.title;
    $('#nextImg').src = n.cover;
  }

  /* ------------------------------------------------------------------ */
  /* Text splitting + reveal on scroll                                   */
  /* ------------------------------------------------------------------ */
  function splitWords() {
    $$('.span-lines').forEach(function (el) {
      var txt = el.textContent.trim().replace(/\s+/g, ' ');
      el.setAttribute('aria-label', txt);
      el.innerHTML = txt.split(' ').map(function (w, i) {
        return '<span class="w" aria-hidden="true"><span style="transition-delay:' + (i * 0.028).toFixed(3) + 's">' + esc(w) + '</span></span>';
      }).join(' ');
    });
  }

  var io = null;
  function startReveals() {
    var targets = $$('.fade-in, .stripe.animate, .span-lines, .shot, .tile');
    if (!('IntersectionObserver' in window)) { targets.forEach(function (t) { t.classList.add('is-in'); }); return; }
    if (!io) io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    targets.forEach(function (t) { if (!t.classList.contains('is-in')) io.observe(t); });
  }

  /* ------------------------------------------------------------------ */
  /* Smooth scroll                                                       */
  /* ------------------------------------------------------------------ */
  function initScroll() {
    if (!window.Lenis || reduce) return;
    lenis = new Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true });
    if (hasGSAP) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(0);
    }
  }
  function lockScroll(lock) {
    if (lenis) { lock ? lenis.stop() : lenis.start(); }
    document.body.classList.toggle('is-locked', lock);
  }
  function currentY() { return lenis ? lenis.scroll : window.pageYOffset; }

  /* ------------------------------------------------------------------ */
  /* Menu + hamburger                                                    */
  /* ------------------------------------------------------------------ */
  function initMenu() {
    var hb = $('.btn-hamburger'), btn = hb && $('.btn-click', hb), label = hb && $('.btn-text-inner', hb);
    if (!hb) return;
    function setMenu(open) {
      html.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      label.textContent = open ? t('nav.close', 'Close') : t('nav.menu', 'Menu');
      lockScroll(open);
    }
    btn.addEventListener('click', function () { setMenu(!html.classList.contains('menu-open')); });
    $$('.btn-menu .btn-click').forEach(function (b) { b.addEventListener('click', function () { setMenu(true); }); });
    $('.fixed-nav-back').addEventListener('click', function () { setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    $$('.fixed-nav a').forEach(function (a) { a.addEventListener('click', function () { if (!a.target) html.classList.remove('menu-open'); }); });

    syncHamburger = function () {
      var nav = $('.nav-bar');
      hb.classList.toggle('is-visible', (nav && nav.classList.contains('is-hidden')) || window.innerWidth <= 1000);
    };
    syncHamburger();
  }

  /* ------------------------------------------------------------------ */
  /* Navigation bar: white over the hero, frosted over content, hides on scroll down */
  /* ------------------------------------------------------------------ */
  function initNav() {
    var nav = $('.nav-bar'); if (!nav) return;
    var hero = $('.home-header'), last = 0;
    function update(y) {
      var overHero = page === 'home' && !!hero && y < hero.offsetHeight - 90;
      nav.classList.toggle('on-dark', overHero);
      nav.classList.toggle('is-solid', y > 30 && !overHero);
      if (y > 260 && y > last + 4) nav.classList.add('is-hidden');
      else if (y < last - 4 || y <= 260) nav.classList.remove('is-hidden');
      last = y;
      syncHamburger();
    }
    if (lenis) lenis.on('scroll', function (e) { update(e.scroll); });
    else window.addEventListener('scroll', function () { update(window.pageYOffset); }, { passive: true });
    window.addEventListener('resize', function () { update(currentY()); });
    update(currentY());
  }

  /* ------------------------------------------------------------------ */
  /* Magnetic buttons, "View" cursor, floating work image                */
  /* ------------------------------------------------------------------ */
  function initMagnetic() {
    if (!hasGSAP || !fine || reduce) return;
    $$('.magnetic').forEach(function (el) {
      var s = parseFloat(el.getAttribute('data-strength')) || 20;
      var st = parseFloat(el.getAttribute('data-strength-text')) || s / 2;
      var t = $('.btn-text', el);
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - (r.left + r.width / 2)) / r.width, y = (e.clientY - (r.top + r.height / 2)) / r.height;
        gsap.to(el, { x: x * s, y: y * s, duration: 1, ease: 'power3.out', overwrite: 'auto' });
        if (t) gsap.to(t, { x: x * st, y: y * st, duration: 1, ease: 'power3.out', overwrite: 'auto' });
      });
      el.addEventListener('mouseleave', function () {
        gsap.to(el, { x: 0, y: 0, duration: 1.2, ease: 'elastic.out(1, .4)', overwrite: 'auto' });
        if (t) gsap.to(t, { x: 0, y: 0, duration: 1.2, ease: 'elastic.out(1, .4)', overwrite: 'auto' });
      });
    });
  }

  function initCursor() {
    var v = $('.cursor-view');
    if (!v || !hasGSAP || !fine) return;
    var xt = gsap.quickTo(v, 'x', { duration: .35, ease: 'power3' }), yt = gsap.quickTo(v, 'y', { duration: .35, ease: 'power3' });
    window.addEventListener('mousemove', function (e) { xt(e.clientX); yt(e.clientY); }, { passive: true });
    document.addEventListener('mouseover', function (e) { v.classList.toggle('on', !!e.target.closest('[data-cursor="view"]')); });
    document.addEventListener('mouseleave', function () { v.classList.remove('on'); });
  }

  function initFloat() {
    var wrap = $('.float-wrap'), list = $('#workWrap');
    if (!wrap || !list || !hasGSAP || !fine) return;
    var imgs = $$('.float-img', wrap);
    /* the hover previews are not needed to paint the page: fetch them once the page is idle */
    function loadFloat(i) { var im = $('img', imgs[i]); if (im && !im.src) im.src = im.getAttribute('data-src'); }
    function loadAllFloat() { imgs.forEach(function (_, i) { loadFloat(i); }); }
    if (document.readyState === 'complete') setTimeout(loadAllFloat, 1200); else window.addEventListener('load', function () { setTimeout(loadAllFloat, 1200); });
    var xt = gsap.quickTo(wrap, 'x', { duration: .8, ease: 'power3' }), yt = gsap.quickTo(wrap, 'y', { duration: .8, ease: 'power3' }), rt = gsap.quickTo(wrap, 'rotation', { duration: .6, ease: 'power3' });
    var lx = 0;
    list.addEventListener('mousemove', function (e) {
      xt(e.clientX); yt(e.clientY); rt(gsap.utils.clamp(-10, 10, (e.clientX - lx) * .35)); lx = e.clientX;
    });
    $$('li[data-i]', list).forEach(function (li) {
      li.addEventListener('mouseenter', function () { var k = +li.getAttribute('data-i'); loadFloat(k); imgs.forEach(function (im, i) { im.classList.toggle('visible', i === k); }); });
    });
    list.addEventListener('mouseleave', function () { imgs.forEach(function (im) { im.classList.remove('visible'); }); });
  }

  /* ------------------------------------------------------------------ */
  /* Scroll-linked effects                                               */
  /* ------------------------------------------------------------------ */
  function initScrollFX() {
    if (!hasGSAP || reduce) return;
    if (page === 'home') {
      var hdr = '.home-header';
      gsap.to('.big-name h1', { x: function () { return -window.innerWidth * 0.12; }, ease: 'none', scrollTrigger: { trigger: hdr, start: 'top top', end: 'bottom top', scrub: 0.6 } });
      gsap.to('.personal-image', { yPercent: 7, ease: 'none', scrollTrigger: { trigger: hdr, start: 'top top', end: 'bottom top', scrub: true } });
      gsap.to('.hero-title-block, .hanger', { yPercent: -25, autoAlpha: 0, ease: 'none', scrollTrigger: { trigger: hdr, start: 'top top', end: 'bottom top', scrub: true } });
    }
    $$('[data-parallax]').forEach(function (el) {
      var v = parseFloat(el.getAttribute('data-parallax')) || 8;
      gsap.fromTo(el, { yPercent: -v }, { yPercent: v, ease: 'none', scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
    $$('.drift').forEach(function (el) {
      var d = parseFloat(el.getAttribute('data-drift')) || 40;
      gsap.fromTo(el, { y: d }, { y: -d, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
    if ($('.footer-wrap')) {
      gsap.fromTo('.footer-inner', { yPercent: -16 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: '.footer-wrap', start: 'top bottom', end: 'bottom bottom', scrub: true } });
      gsap.fromTo('.footer-rounded-div .rd', { scaleY: 1 }, { scaleY: 0, ease: 'none', scrollTrigger: { trigger: '.footer-rounded-div', start: 'top bottom', end: 'bottom 55%', scrub: true } });
    }
    window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  }

  /* ------------------------------------------------------------------ */
  /* Entry animations                                                    */
  /* ------------------------------------------------------------------ */
  /* ------------------------------------------------------------------ */
  /* Small UX touches: progress bar, back-to-top, counters, hero parallax */
  /* ------------------------------------------------------------------ */
  function onScrollY(fn) {
    if (lenis) lenis.on('scroll', function (e) { fn(e.scroll); });
    else window.addEventListener('scroll', function () { fn(window.pageYOffset); }, { passive: true });
  }

  function initUX() {
    var bar = $('.progress i'), top = $('.to-top');
    if (top) {
      top.setAttribute('aria-label', t('ui.top', 'Back to top'));
      top.addEventListener('click', function () {
        if (lenis) lenis.scrollTo(0, { duration: 1.6 }); else window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      });
    }
    function upd(y) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (bar) bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
      if (top) top.classList.toggle('is-visible', y > window.innerHeight * 1.1);
    }
    onScrollY(upd); window.addEventListener('resize', function () { upd(currentY()); }); upd(currentY());
  }

  function initCounters() {
    var els = $$('.stat-n[data-count]'); if (!els.length) return;
    function run(el) {
      var end = +el.getAttribute('data-count'), suf = el.getAttribute('data-suffix') || '';
      if (!hasGSAP || reduce) { el.textContent = end + suf; return; }
      var o = { v: 0 };
      gsap.to(o, { v: end, duration: 1.8, ease: 'power3.out', onUpdate: function () { el.textContent = Math.round(o.v) + suf; } });
    }
    if (!('IntersectionObserver' in window)) return;
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { run(e.target); io2.unobserve(e.target); } });
    }, { threshold: 0.6 });
    els.forEach(function (el) { el.textContent = '0' + (el.getAttribute('data-suffix') || ''); io2.observe(el); });
  }

  function initHeroParallax() {
    if (!hasGSAP || !fine || reduce || page !== 'home') return;
    var hero = $('.home-header'), img = $('.personal-image'), bg = $('.hero-bg');
    if (!hero || !img || !bg) return;
    var xi = gsap.quickTo(img, 'x', { duration: 1.2, ease: 'power3' });
    var xb = gsap.quickTo(bg, 'x', { duration: 1.4, ease: 'power3' }), yb = gsap.quickTo(bg, 'y', { duration: 1.4, ease: 'power3' });
    hero.addEventListener('mousemove', function (e) {
      var r = hero.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width - 0.5, ny = (e.clientY - r.top) / r.height - 0.5;
      xi(nx * -22); xb(nx * 16); yb(ny * 12);
    });
    hero.addEventListener('mouseleave', function () { xi(0); xb(0); yb(0); });
  }

  /* the two marquees speed up while you scroll, then settle back */
  function initMarqueeBoost() {
    if (reduce) return;
    var anims = [];
    $$('.name-track, .marquee-track').forEach(function (el) { var a = el.getAnimations && el.getAnimations()[0]; if (a) anims.push(a); });
    if (!anims.length) return;
    var rate = 1, target = 1, last = currentY();
    onScrollY(function (y) { target = 1 + Math.min(Math.abs(y - last) * 0.12, 7); last = y; });
    (function tick() {
      target += (1 - target) * 0.06; rate += (target - rate) * 0.08;
      if (Math.abs(rate - 1) > 0.01 || Math.abs(anims[0].playbackRate - 1) > 0.01) anims.forEach(function (a) { a.playbackRate = rate; });
      requestAnimationFrame(tick);
    })();
  }

  function heroIn() {
    if (!hasGSAP || reduce) return;
    var tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
    tl.from('.personal-image', { yPercent: 10, autoAlpha: 0, duration: 1.7 }, 0.05)
      .from('.big-name h1', { yPercent: 105, duration: 1.6 }, 0.25)
      .from('.hero-title-block > *', { y: 40, autoAlpha: 0, duration: 1.2, stagger: .12 }, 0.5)
      .from('.hanger', { xPercent: rtl ? 100 : -100, duration: 1.3 }, 0.7)
      .from('.nav-bar .credits-top, .nav-bar .btn-link, .nav-bar .btn-cta', { y: -20, autoAlpha: 0, duration: 1, stagger: .06 }, 0.6);
  }
  function innerIn() {
    if (!hasGSAP || reduce) return;
    gsap.from('.page-header .eyebrow, .project-header .eyebrow, .nav-bar .credits-top, .nav-bar .btn-link', { y: -18, autoAlpha: 0, duration: 1, stagger: .05, ease: 'power4.out' });
  }
  function pageIn() { startReveals(); if (page === 'home') heroIn(); else innerIn(); }

  function runLoader(done) {
    var L = $('.loader');
    if (!L || !html.classList.contains('show-loader') || !hasGSAP || reduce) { html.classList.remove('show-loader'); if (L) L.remove(); done(); return; }
    lockScroll(true);
    var words = $$('.loader-words h2', L);
    var tl = gsap.timeline({ onComplete: function () { L.remove(); html.classList.remove('show-loader'); safeStore('seen', '1'); lockScroll(false); } });
    words.forEach(function (w, i) {
      tl.set(words, { autoAlpha: 0 }).set(w, { autoAlpha: 1 }).to({}, { duration: i === 0 ? 0.8 : 0.2 });
    });
    tl.to('.loader-words', { yPercent: -40, autoAlpha: 0, duration: .55, ease: 'power2.in' }, '+=.1')
      .to(L, { y: '-112vh', duration: 1.2, ease: 'power4.inOut' }, '<.05')
      .add(done, '-=.65');
  }

  /* ------------------------------------------------------------------ */
  /* Page transitions (curtain)                                          */
  /* ------------------------------------------------------------------ */
  function labelFor(a) {
    if (a.getAttribute('data-label')) return a.getAttribute('data-label');
    var f = (a.getAttribute('href') || '').split('?')[0].split('#')[0].split('/').pop();
    var pair = { 'index.html': ['nav.home', 'Home'], '': ['nav.home', 'Home'], 'work.html': ['nav.work', 'Work'], 'about.html': ['nav.about', 'About'], 'contact.html': ['nav.contact', 'Contact'] }[f] || ['nav.work', 'Work'];
    return t(pair[0], pair[1]);
  }
  function initTransitions() {
    var c = $('.curtain'); if (!c) return;
    if (html.classList.contains('pt-in')) {
      safeStore('pt', null);
      if (hasGSAP && !reduce) {
        gsap.set(c, { y: 0 });
        gsap.to(c, { y: '-112vh', duration: 1.1, ease: 'power4.inOut', delay: .2, onComplete: function () { html.classList.remove('pt-in'); gsap.set(c, { clearProps: 'all' }); } });
        gsap.delayedCall(.55, pageIn);
      } else { html.classList.remove('pt-in'); pageIn(); }
    }
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a'); if (!a || !hasGSAP || reduce) return;
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || a.target === '_blank' || a.hasAttribute('download') || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
      if (/^(mailto:|tel:)/.test(href)) return;
      if (/^https?:/i.test(a.href) && new URL(a.href).origin !== location.origin) return;
      if (a.hasAttribute('aria-disabled')) { e.preventDefault(); return; }
      e.preventDefault();
      if (leaving) return;
      leaving = true;
      var label = labelFor(a);
      safeStore('ptLabel', label);
      $('#curtainLabel').textContent = label;
      html.classList.remove('menu-open');
      c.classList.add('is-active');
      gsap.fromTo(c, { y: '112vh' }, { y: 0, duration: .9, ease: 'power3.inOut', onComplete: function () { safeStore('pt', '1'); location.href = a.href; } });
    });
    window.addEventListener('pageshow', function (e) {
      if (e.persisted) { leaving = false; c.classList.remove('is-active'); html.classList.remove('pt-in'); if (hasGSAP) gsap.set(c, { clearProps: 'all' }); lockScroll(false); }
    });
  }

  /* ------------------------------------------------------------------ */
  /* Contact form (no backend: opens the visitor's email app)            */
  /* ------------------------------------------------------------------ */
  function initForm() {
    var f = $('#contactForm'); if (!f) return;
    var st = $('#formStatus');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(f);
      var name = (d.get('name') || '').trim(), email = (d.get('email') || '').trim(), org = (d.get('org') || '').trim(), msg = (d.get('message') || '').trim();
      var services = d.getAll('services').join(', ');
      st.classList.remove('err');
      if (!name || !email || !msg) { st.textContent = t('err.fill', 'Please add your name, email and a short message.'); st.classList.add('err'); return; }
      if (!/^\S+@\S+\.\S+$/.test(email)) { st.textContent = t('err.email', 'That email address does not look right.'); st.classList.add('err'); return; }
      /* The email itself is always written in English so it reads the same in the inbox. */
      var subject = 'Project enquiry from ' + name;
      var body = 'Name: ' + name + '\nEmail: ' + email + '\nOrganisation: ' + (org || '-') + '\nServices: ' + (services || '-') + '\nSite language: ' + (rtl ? 'Arabic' : 'English') + '\n\n' + msg;
      st.textContent = t('ok.mail', 'Your email app should open with the message ready to send. If nothing opens, write to ') + S.email + (rtl ? '' : '.');
      window.location.href = 'mailto:' + S.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }

  /* ------------------------------------------------------------------ */
  /* Boot                                                                */
  /* ------------------------------------------------------------------ */
  function boot() {
    applyI18n();
    bindSite();
    renderHome(); renderWork(); renderProject();
    splitWords();
    setRollText();
    initClock();
    initScroll();
    initMenu();
    initNav();
    initMagnetic(); initCursor(); initFloat();
    initScrollFX();
    initUX(); initCounters(); initHeroParallax(); initMarqueeBoost();
    initForm();
    initTransitions();
    if (!html.classList.contains('pt-in')) {
      if (page === 'home') runLoader(pageIn); else pageIn();
    }
    // Safety: never leave content hidden if something above failed.
    setTimeout(function () { if (!io) startReveals(); }, 7000);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
