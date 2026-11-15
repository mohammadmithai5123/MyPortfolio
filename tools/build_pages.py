"""Generates the five HTML pages (shared nav / menu / footer live here).
Usage:  python tools/build_pages.py .
Every visible string carries data-i18n="key"; Arabic text lives in assets/js/i18n.js.
"""
import sys, os, re

import hashlib
SITE_URL = 'https://mohammadmithai5123.github.io/MyPortfolio/'   # change when you attach your own domain
PAGE_FILES = {'home': '', 'work': 'work.html', 'about': 'about.html', 'contact': 'contact.html', 'project': 'project.html'}
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
OUT = _args[0] if _args else '.'
DEV = '--dev' in sys.argv   # --dev: point pages at the readable sources instead of assets/dist


def ver(path):
    try:
        return hashlib.md5(open(os.path.join(OUT, path), 'rb').read()).hexdigest()[:8]
    except OSError:
        return '0'


ARROW = ('<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">'
         '<path d="M2.5 11.5l9-9M3.5 2.5h8v8" stroke="currentColor" stroke-width="1.5"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='14' fill='%231c1d20'/%3E"
           "%3Ctext x='32' y='45' font-size='36' text-anchor='middle' fill='white' "
           "font-family='Arial' font-weight='700'%3EM%3C/text%3E%3C/svg%3E")

HERO_PRELOAD = ('<link rel="preload" as="image" href="assets/img/profile-cutout-640.webp" '
                'imagesrcset="assets/img/profile-cutout-640.webp 640w, assets/img/profile-cutout.webp 1024w" '
                'imagesizes="(max-width:1000px) 86vw, 40vw" fetchpriority="high">\n')

# href, English label, page key, i18n key
LINKS = [('index.html', 'Home', 'home', 'nav.home'), ('work.html', 'Work', 'work', 'nav.work'),
         ('about.html', 'About', 'about', 'nav.about'), ('contact.html', 'Contact', 'contact', 'nav.contact')]

LOADER_WORDS = ['Hello', 'नमस्ते', 'Hola', 'Bonjour', 'Ciao', 'Hallo', 'السلام عليكم', 'مرحبا']


def magnetic_link(href, text, key, active=False, s=20, st=10):
    return ('<li class="btn btn-link%s"><a href="%s" class="btn-click magnetic" data-strength="%d" '
            'data-strength-text="%d"><span class="btn-text"><span class="btn-text-inner" data-i18n="%s">%s</span></span></a></li>'
            % (' active' if active else '', href, s, st, key, text))


def nav_bar(page):
    links = ''.join(magnetic_link(h, t, k, active=(p == page)) for h, t, p, k in LINKS[1:])
    cls = 'nav-bar on-dark' if page == 'home' else 'nav-bar'
    return ('<div class="' + cls + '">'
            '<div class="credits-top"><div class="btn btn-credit"><a href="index.html" class="btn-click magnetic nav-logo" '
            'data-strength="20" data-strength-text="10"><i class="avatar" aria-hidden="true"></i><span class="btn-text">'
            '<span class="btn-text-inner" data-i18n="name">Mohammad Muslim</span></span></a></div></div>'
            '<ul class="links-wrap">' + links +
            '<li class="btn btn-link btn-lang"><button type="button" class="btn-click magnetic" data-lang-toggle data-strength="20" data-strength-text="10">'
            '<span class="btn-text"><span class="btn-text-inner">&#1575;&#1604;&#1593;&#1585;&#1576;&#1610;&#1577;</span></span></button></li>'
            '<li class="btn btn-cta"><a href="contact.html" class="btn-click magnetic" data-strength="30" data-strength-text="15">'
            '<span class="btn-text"><span class="btn-text-inner change" data-i18n="nav.talk">Let&rsquo;s talk</span></span></a></li></ul></div>')


def menu(page):
    links = ''.join(magnetic_link(h, t, k, active=(p == page), s=24, st=12) for h, t, p, k in LINKS)
    return ('<div class="btn btn-hamburger"><button type="button" class="btn-click magnetic" data-strength="50" data-strength-text="25" '
            'aria-label="Menu" aria-expanded="false" aria-controls="menu"><span class="btn-fill"></span>'
            '<span class="btn-text"><span class="btn-bars"></span><span class="btn-text-inner" data-i18n="nav.menu">Menu</span></span></button></div>\n'
            '<div class="fixed-nav-back"></div>\n'
            '<aside class="fixed-nav theme-dark" id="menu" aria-label="Main menu"><div class="fixed-nav-inner">'
            '<div><h5 data-i18n="menu.navigation">Navigation</h5><div class="stripe"></div><ul class="links-wrap">' + links + '</ul></div>'
            '<div class="menu-foot"><div><h5 data-i18n="nav.contact">Contact</h5><a href="#" data-bind="email" class="menu-mail">email</a></div><div class="socials"><h5 data-i18n="menu.socials">Socials</h5><ul data-socials></ul></div>'
            '<div class="lang-row"><h5 data-i18n="menu.language">Language</h5><button type="button" class="lang-btn" data-lang-toggle>&#1575;&#1604;&#1593;&#1585;&#1576;&#1610;&#1577;</button></div></div>'
            '</div></aside>')


def pill(inner_attrs, key, text, extra=''):
    return ('<div class="btn btn-normal"><a href="#" %s class="btn-click magnetic" data-strength="25" data-strength-text="15">'
            '<span class="btn-fill"></span><span class="btn-text"><span class="btn-text-inner change"%s>%s</span></span></a></div>'
            % (inner_attrs, (' data-i18n="%s"' % key) if key else '', text))


def footer():
    return ('''<div class="footer-rounded-div" aria-hidden="true"><div class="rd"></div></div>
<div class="footer-wrap theme-dark">
  <footer class="footer"><div class="footer-inner">
    <div class="container medium">
      <div class="eyebrow"><i class="live"></i><span data-i18n="eyebrow.footer">Have a project in mind?</span></div>
      <h2><span><i class="profile-picture" role="img" aria-label="Mohammad"></i> <span data-i18n="footer.lets">Let&rsquo;s work</span></span><span data-i18n="footer.together">together</span></h2>
      <div class="stripe-row">
        <div class="stripe animate"></div>
        <div class="btn btn-round"><a href="contact.html" class="btn-click magnetic" data-strength="100" data-strength-text="50"><span class="btn-fill"></span><span class="btn-text"><span class="btn-text-inner" data-i18n="footer.touch">Get in touch</span></span></a></div>
      </div>
      <div class="contact-links">
        ''' + pill('data-bind="email"', '', 'email') + '''
        ''' + pill('data-bind="phone"', '', 'phone') + '''
        ''' + pill('data-bind="whatsapp"', 'footer.whatsapp', 'WhatsApp') + '''
      </div>
    </div>
    <div class="container">
      <div class="bottom-footer">
        <div class="meta">
          <div><h5 data-i18n="footer.based">Based in</h5><p data-i18n="footer.uae">United Arab Emirates</p></div>
          <div><h5 data-i18n="footer.time">Local time</h5><p data-time>--:-- --</p></div>
        </div>
        <div class="socials"><h5 data-i18n="footer.socials">Socials</h5><ul data-socials></ul></div>
      </div>
      <div class="credit-line"><p>&copy; <span data-year>2026</span> <span data-i18n="footer.rights">Mohammad Muslim. All rights reserved.</span></p>
        <ul><li><a href="work.html" data-i18n="nav.work">Work</a></li><li><a href="about.html" data-i18n="nav.about">About</a></li><li><a href="contact.html" data-i18n="nav.contact">Contact</a></li></ul></div>
    </div>
  </div></footer>
</div>''')



if DEV:
    HEAD_ASSETS = '<link rel="stylesheet" href="assets/css/fonts.css">\n<link rel="stylesheet" href="assets/css/style.css">'
    SCRIPTS = ''.join('<script src="assets/%s" defer></script>\n' % f for f in (
        'vendor/gsap.min.js', 'vendor/ScrollTrigger.min.js', 'vendor/lenis.min.js',
        'js/config.js', 'js/i18n.js', 'js/data.js', 'js/main.js'))
else:
    HEAD_ASSETS = '<link rel="stylesheet" href="assets/dist/style.min.css?v=%s">' % ver('assets/dist/style.min.css')
    SCRIPTS = ('<script src="assets/dist/vendor.min.js?v=%s" defer></script>\n'
               '<script src="assets/dist/app.min.js?v=%s" defer></script>\n' % (ver('assets/dist/vendor.min.js'), ver('assets/dist/app.min.js')))


def shell(page, title, desc, body_main, extra_head='', loader=False, float_block=False):
    loader_html = ''
    if loader:
        words = ''.join('<h2>%s<i class="dot"></i></h2>' % w for w in LOADER_WORDS)
        loader_html = '<div class="loader" aria-hidden="true"><div class="loader-words">%s</div></div>\n' % words
    cursor = '<div class="cursor-view" aria-hidden="true">View</div>\n'
    float_html = '<div class="float-wrap" id="floatImgs" aria-hidden="true"></div>\n' if float_block else ''
    boot = ("<script>(function(d){var h=d.documentElement;h.classList.add('js');"
            "try{if(localStorage.getItem('lang')==='ar'){h.lang='ar';h.dir='rtl'}}catch(e){}"
            "try{if(sessionStorage.getItem('pt')==='1'){h.classList.add('pt-in')}"
            "else if('%s'==='home'&&!sessionStorage.getItem('seen')){h.classList.add('show-loader')}}catch(e){}"
            "setTimeout(function(){h.classList.remove('pt-in','show-loader')},9000);"
            "if(location.protocol==='file:'){var l=d.createElement('link');l.rel='stylesheet';"
            "l.href='https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300..600&family=Noto+Sans+Arabic:wght@400..600&family=Noto+Sans+Devanagari:wght@400..500&display=swap';d.head.appendChild(l)}"
            "else{var p=d.createElement('link');p.rel='preload';p.as='font';p.type='font/woff2';p.crossOrigin='anonymous';p.href='assets/fonts/inter-tight-latin.woff2';d.head.appendChild(p)}"
            "})(document)</script>" % page)
    return '''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<meta property="og:url" content="%(page_url)s">
<meta property="og:site_name" content="Mohammad Muslim">
<meta property="og:image" content="%(site)sassets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="%(page_url)s">
<meta name="theme-color" content="#1c1d20">
<link rel="icon" href="%(favicon)s">
%(head_assets)s
%(boot)s
%(extra_head)s<noscript><style>.loader,.curtain{display:none!important}.fade-in,.shot{opacity:1!important;transform:none!important}.span-lines .w>span{transform:none!important}.stripe.animate{transform:none!important}</style></noscript>
</head>
<body data-page="%(page)s">
<a class="skip" href="#main" data-i18n="ui.skip">Skip to content</a>
<div class="progress" aria-hidden="true"><i></i></div>
%(loader)s<div class="curtain" aria-hidden="true"><div class="curtain-label"><span id="curtainLabel"></span><i class="dot"></i></div></div>
<script>try{document.getElementById('curtainLabel').textContent=sessionStorage.getItem('ptLabel')||''}catch(e){}</script>
%(cursor)s%(float)s%(menu)s
<main id="main">
%(main)s
</main>
<button type="button" class="to-top" aria-label="Back to top"><svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2.5 11.5l9-9M3.5 2.5h8v8" stroke="currentColor" stroke-width="1.5"/></svg></button>
%(scripts)s
</body>
</html>
''' % dict(title=title, desc=desc, favicon=FAVICON, head_assets=HEAD_ASSETS, scripts=SCRIPTS, site=SITE_URL, page_url=SITE_URL + PAGE_FILES[page], boot=boot, extra_head=extra_head, page=page,
           loader=loader_html, cursor=cursor, float=float_html, menu=menu(page), main=body_main)



# ---- platform logos (inline SVG, paths from assets/img/platforms/*.svg) -------------------
def _logo(name):
    svg = open(os.path.join(OUT, 'assets', 'img', 'platforms', name + '.svg'), encoding='utf-8').read()
    return '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">' + ''.join(re.findall(r'<path[^>]*/>', svg)) + '</svg>'


PLATFORM_DEFS = [
    ('shopify', 'Shopify', '#95BF47', 'plat.shopify', 'Themes, apps and high-converting stores'),
    ('wordpress', 'WordPress', '#21759B', 'plat.wp', 'Custom sites, Elementor and WooCommerce'),
    ('react', 'React / Node', '#149ECA', 'plat.react', 'MERN apps and API-driven platforms'),
    ('magento', 'Magento', '#F26322', 'plat.magento', 'Legacy builds and clean migrations out'),
]
PLATFORMS_HTML = ''.join(
    '<div class="platform fade-in" style="--brand:%s">%s<h4>%s</h4><p data-i18n="%s">%s</p></div>' % (c, _logo(n), t, k, d)
    for n, t, c, k, d in PLATFORM_DEFS)

# ---------------------------------------------------------------- HOME
marq_items = [('Shopify', ''), ('WordPress', ''), ('Magento', ''), ('Brand identity', 'marq.brand'),
              ('UI / UX', 'marq.uiux'), ('Packaging', 'marq.pack'), ('Migrations', 'marq.migr'), ('Pitch decks', 'marq.pitch')]
marq = ''.join('<span%s>%s</span><i></i>' % ((' data-i18n="%s"' % k) if k else '', w) for w, k in marq_items) * 2

NAME_ITEMS = ''.join('<span class="name-item" aria-hidden="true"><span data-i18n="name">Mohammad Muslim</span><span class="spacer">&mdash;</span></span>' for _ in range(4))

home_main = '''<header class="home-header theme-dark">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="personal-image"><img src="assets/img/profile-cutout.webp" srcset="assets/img/profile-cutout-640.webp 640w, assets/img/profile-cutout.webp 1024w" sizes="(max-width:1000px) 86vw, 40vw" alt="Portrait of Mohammad Muslim" width="1024" height="1536" fetchpriority="high" decoding="async"></div>
  ''' + nav_bar('home') + '''
  <div class="hero-title-block"><div class="eyebrow"><i class="live"></i><span data-i18n="eyebrow.available">Available for new projects</span></div><h4 data-i18n="hero.title" data-i18n-html><span>Freelance</span> Designer &amp; Developer</h4></div>
  <div class="hanger"><p><span data-i18n="hero.located1">Located</span><span data-i18n="hero.located2">in the UAE</span></p>
    <div class="globe" aria-hidden="true"><div class="globe-wrap"><div class="circle"></div><div class="circle"></div><div class="circle"></div><div class="circle-hor"></div><div class="circle-hor-middle"></div></div></div></div>
  <div class="big-name"><h1 aria-label="Mohammad Muslim"><span class="name-track">''' + NAME_ITEMS + '''</span></h1></div>
  <div class="hero-curve" aria-hidden="true"></div>
</header>

<section class="section home-intro">
  <div class="container medium"><div class="row">
    <div class="flex-col"><h4 class="span-lines" data-i18n="intro.h4">Helping brands in the UAE and beyond stand out online. Sharp design, clean code and stores that sell. No nonsense, always on the cutting edge.</h4></div>
    <div class="flex-col">
      <div class="fade-in"><p data-i18n="intro.p">I blend design, development and e-commerce know-how to take a brand from first idea to a website or store that is ready to grow.</p></div>
      <div class="btn btn-round"><a href="about.html" class="btn-click magnetic" data-strength="100" data-strength-text="50"><span class="btn-fill"></span><span class="btn-text"><span class="btn-text-inner" data-i18n="intro.about">About me</span></span></a></div>
    </div>
  </div></div>
</section>

<section class="section home-work" id="work">
  <div class="container">
    <div class="work-items-wrap" id="workWrap">
      <div class="work-group">
        <div class="grid-sub-title group-head"><h5 data-i18n="filter.design">Design</h5><a href="work.html?f=design" class="view-all"><span data-i18n="work.viewall">View all</span> ''' + ARROW + '''</a></div>
        <ul class="work-items" id="workListDesign"></ul>
      </div>
      <div class="work-group">
        <div class="grid-sub-title group-head"><h5 data-i18n="filter.development">Development</h5><a href="work.html?f=development" class="view-all"><span data-i18n="work.viewall">View all</span> ''' + ARROW + '''</a></div>
        <ul class="work-items" id="workListDev"></ul>
      </div>
    </div>
    <div class="work-tiles">
      <div class="work-group"><div class="grid-sub-title group-head"><h5 data-i18n="filter.design">Design</h5></div><div class="tiles" id="tilesDesign"></div></div>
      <div class="work-group"><div class="grid-sub-title group-head"><h5 data-i18n="filter.development">Development</h5></div><div class="tiles" id="tilesDev"></div></div>
    </div>
  </div>
</section>

<section class="section center-grid-btn">
  <div class="container"><div class="btn btn-normal"><a href="work.html" class="btn-click magnetic" data-strength="25" data-strength-text="15"><span class="btn-fill"></span><span class="btn-text"><span class="btn-text-inner change" data-i18n="work.more">More work</span></span><span class="count-nr" data-count-projects>12</span></a></div></div>
</section>

<section class="marquee" aria-hidden="true"><div class="marquee-track">''' + marq + '''</div></section>

''' + footer()

ld = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"Mohammad Muslim","jobTitle":"Freelance Designer & Developer","address":{"@type":"PostalAddress","addressCountry":"AE"},"knowsAbout":["Shopify","WordPress","Magento","Brand identity","UI/UX design"]}</script>
'''

pages = {}
pages['index.html'] = shell('home', 'Mohammad Muslim — Freelance Designer & Developer in the UAE',
                            'Freelance designer and developer based in the UAE. Shopify, WordPress and Magento builds, brand identity, UI/UX and packaging for brands in the Gulf and worldwide.',
                            home_main, extra_head=HERO_PRELOAD + ld, loader=True, float_block=True)

# ---------------------------------------------------------------- WORK
work_main = nav_bar('work') + '''
<header class="page-header"><div class="container">
  <div class="eyebrow"><span data-i18n="eyebrow.work">Selected work</span></div>
  <h1 class="span-lines wide" data-i18n="work.h1">Selected work in design and development</h1>
</div></header>
<section class="container" style="padding-bottom:var(--sec)">
  <div class="filters" id="filterBar"></div>
  <div id="workGroups"></div>
  <div class="archive">
    <h5><span data-i18n="archive.title">Archive</span> &middot; <span data-count-archive>15</span> <span data-i18n="archive.sub">live websites</span></h5>
    <ul id="archiveList"></ul>
  </div>
</section>
''' + footer()
pages['work.html'] = shell('work', 'Work — Mohammad Muslim',
                           'Selected design and development work by Mohammad Muslim: Shopify and WordPress builds, websites, UI/UX, brand identity, packaging and more.',
                           work_main)

# ---------------------------------------------------------------- ABOUT
about_main = nav_bar('about') + '''
<header class="page-header"><div class="container">
  <div class="eyebrow"><span data-i18n="eyebrow.about">About me</span></div>
  <h1 class="span-lines wide" data-i18n="about.h1">Brands that look sharp and sell online</h1>
</div></header>
<section class="container" style="padding-bottom:var(--sec)">
  <div class="about-grid">
    <div class="about-photo"><img src="assets/img/profile-cutout.webp" srcset="assets/img/profile-cutout-640.webp 640w, assets/img/profile-cutout.webp 1024w" sizes="(max-width:1000px) 92vw, 46vw" alt="Mohammad Muslim" width="1024" height="1536" loading="lazy" decoding="async"></div>
    <div class="about-copy fade-in">
      <h4 data-i18n="about.hi">Hi, I&rsquo;m Mohammad.</h4>
      <p data-i18n="about.p1">I&rsquo;m a freelance designer and developer based in the UAE, working with brands across the Gulf and around the world.</p>
      <p data-i18n="about.p2">I build high-converting e-commerce and custom web platforms, blending clean design with solid engineering to craft seamless digital experiences. I design intuitive interfaces and develop user-centric solutions that scale.</p>
      <div class="btn btn-normal" style="margin-top:1rem"><a href="contact.html" class="btn-click magnetic" data-strength="25" data-strength-text="15"><span class="btn-fill"></span><span class="btn-text"><span class="btn-text-inner change" data-i18n="about.start">Start a project</span></span></a></div>
    </div>
  </div>

  <div class="services-list">
    <h5 style="margin-bottom:1.4em" data-i18n="about.help">I can help you with&hellip;</h5>
    <div class="service fade-in"><span class="n">01</span><h3 data-i18n="about.s1t">Design</h3><p data-i18n="about.s1d">Brand identity, logos, packaging, UI/UX and social creative that look sharp and make the message clear.</p></div>
    <div class="service fade-in"><span class="n">02</span><h3 data-i18n="about.s2t">Development</h3><p data-i18n="about.s2d">Shopify, WooCommerce, Magento and WordPress builds plus custom MERN apps. Clean front-ends, solid back-ends, and migrations that keep your SEO and data intact.</p></div>
    <div class="service fade-in"><span class="n">03</span><h3 data-i18n="about.s3t">The full package</h3><p data-i18n="about.s3d">One person from brand to launch: design the identity, build the site or store, and ship it with care.</p></div>
  </div>

  <div class="stats-row">
    <div class="fade-in"><div class="stat-n" data-count="8" data-suffix="+">8+</div><div class="stat-l" data-i18n="about.stat1">Years of experience</div></div>
    <div class="fade-in"><div class="stat-n" data-count="100" data-suffix="+">100+</div><div class="stat-l" data-i18n="about.stat2">Projects delivered</div></div>
    <div class="fade-in"><div class="stat-n" data-count="8" data-suffix="">8</div><div class="stat-l" data-i18n="about.stat3">Platform migrations</div></div>
  </div>

  <div class="platforms-wrap">
    <h3 class="group-title" data-i18n="about.platforms">Platforms I work with</h3>
    <div class="platforms">
''' + PLATFORMS_HTML + '''
    </div>
  </div>
</section>
''' + footer()
pages['about.html'] = shell('about', 'About — Mohammad Muslim',
                            'Mohammad Muslim is a freelance designer and developer in the UAE. Design, Shopify, WordPress and Magento development, and migrations that keep your SEO intact.',
                            about_main)

# ---------------------------------------------------------------- CONTACT
chip_defs = [('Brand identity', 'chip.brand'), ('UI / UX design', 'chip.uiux'), ('Shopify', 'chip.shopify'),
             ('WordPress', 'chip.wp'), ('Magento migration', 'chip.magento'), ('Something else', 'chip.other')]
chips = ''.join('<label class="chip"><input type="checkbox" name="services" value="%s"><span data-i18n="%s">%s</span></label>' % (c, k, c)
                for c, k in chip_defs)
contact_main = nav_bar('contact') + '''
<header class="page-header"><div class="container">
  <div class="eyebrow"><span data-i18n="eyebrow.contact">Contact</span></div>
  <h1 class="span-lines wide" data-i18n="contact.h1">Let&rsquo;s start a project together</h1>
</div></header>
<section class="container"><div class="contact-grid">
  <form id="contactForm" novalidate>
    <div class="field"><span class="n">01</span><label for="f-name" data-i18n="contact.q1">What&rsquo;s your name?</label><input id="f-name" name="name" type="text" autocomplete="name" placeholder="John Doe *" data-i18n-placeholder="contact.ph1"></div>
    <div class="field"><span class="n">02</span><label for="f-email" data-i18n="contact.q2">What&rsquo;s your email?</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="john@doe.com *" data-i18n-placeholder="contact.ph2"></div>
    <div class="field"><span class="n">03</span><label for="f-org" data-i18n="contact.q3">What&rsquo;s the name of your organisation?</label><input id="f-org" name="org" type="text" autocomplete="organization" placeholder="John &amp; Doe &trade;" data-i18n-placeholder="contact.ph3"></div>
    <div class="field"><span class="n">04</span><span class="label" data-i18n="contact.q4">What services are you looking for?</span><div class="chips">''' + chips + '''</div></div>
    <div class="field"><span class="n">05</span><label for="f-msg" data-i18n="contact.q5">Your message</label><textarea id="f-msg" name="message" rows="4" placeholder="Hello Mohammad, can you help me with&hellip; *" data-i18n-placeholder="contact.ph5"></textarea></div>
    <div class="form-foot">
      <div class="btn btn-round"><button type="submit" class="btn-click magnetic" data-strength="100" data-strength-text="50"><span class="btn-fill"></span><span class="btn-text"><span class="btn-text-inner" data-i18n="contact.send">Send it</span></span></button></div>
      <p class="form-note" data-i18n="contact.note">This opens your email app with everything filled in, so you can review it before sending.</p>
    </div>
    <p class="form-status" id="formStatus" role="status" aria-live="polite"></p>
  </form>
  <aside class="side-info">
    <div class="block fade-in"><h5 data-i18n="contact.details">Contact details</h5>
      <a href="#" data-bind="email">email</a>
      <a href="#" data-bind="phone">phone</a>
      <a href="#" data-bind="whatsapp" class="wa-link" data-i18n="contact.wa">Chat on WhatsApp</a></div>
    <div class="block fade-in"><h5 data-i18n="contact.based">Based in</h5><p data-i18n="contact.uae">United Arab Emirates</p><p class="sub" data-i18n="contact.working">Working with clients across the UAE, the Gulf and worldwide.</p></div>
    <div class="block fade-in"><h5 data-i18n="contact.time">Local time</h5><p data-time>--:-- --</p></div>
    <div class="block fade-in socials"><h5 data-i18n="contact.socials">Socials</h5><ul data-socials></ul></div>
  </aside>
</div></section>
''' + footer()
pages['contact.html'] = shell('contact', 'Contact — Mohammad Muslim',
                              'Start a project with Mohammad Muslim, a freelance designer and developer in the UAE. Tell me what you need and I will get back to you.',
                              contact_main)

# ---------------------------------------------------------------- PROJECT
project_main = nav_bar('work') + '''
<header class="project-header"><div class="container">
  <div class="eyebrow"><span data-i18n="eyebrow.project">Project</span></div>
  <h1 id="pTitle">Project</h1>
  <div class="project-meta">
    <div><h5 data-i18n="proj.services">Services</h5><p id="pServices"></p></div>
    <div><h5 data-i18n="proj.year">Year</h5><p id="pYear"></p></div>
    <div class="desc"><h5 data-i18n="proj.about">About this collection</h5><p id="pDesc"></p></div>
    <div><h5 data-i18n="proj.scope">Scope</h5><p id="pCount"></p></div>
  </div>
  <div class="btn btn-normal project-visit" id="pVisitWrap" hidden><a id="pVisit" href="#" target="_blank" rel="noopener" class="btn-click magnetic" data-strength="25" data-strength-text="15"><span class="btn-fill"></span><span class="btn-text"><span class="btn-text-inner change" data-i18n="proj.visit">Visit live site</span></span></a></div>
</div></header>
<section class="container"><div class="gallery" id="gallery"></div></section>
<a class="next-project" id="nextProject" href="work.html" data-cursor="view">
  <div class="np-img"><img id="nextImg" src="" alt="" loading="lazy"></div>
  <h5 data-i18n="proj.next">Next project</h5>
  <h2 id="nextTitle"></h2>
</a>
''' + footer()
pages['project.html'] = shell('project', 'Project — Mohammad Muslim',
                              'A collection of design and development work by Mohammad Muslim.', project_main)

for name, content in pages.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(content)
    print('wrote', name, len(content))
