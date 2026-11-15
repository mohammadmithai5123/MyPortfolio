"""Builds device mockups (laptop + phone, browser window, phone) from real site screenshots.

usage:  python tools/mockups.py <screenshots_dir> <repo_root>
Screenshots are named <slug>-d.png (desktop 1440x900) and <slug>-m.png (mobile 390x844 @2x).
Images are written to <repo_root>/assets/img/work/<slug>/01.webp, 02.webp, 03.webp and cover.webp.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, ROOT = sys.argv[1], sys.argv[2]

# slug -> (backdrop light, backdrop deep, has desktop, has mobile, domain shown in the browser bar)
SITES = {
    'tetongear':       ('#e6eadf', '#c9d6c4', True, True, 'tetongear.com'),
    'ex1cosmetics':    ('#f3e3dd', '#e3c3b8', True, True, 'ex1cosmetics.com'),
    'kiefer':          ('#dbe8f6', '#b3cde9', True, True, 'kiefer.com'),
    'vsg':             ('#d9ebef', '#a9d0d8', True, True, 'veryspecialgames.com'),
    'mymochi':         ('#e6d9f3', '#c8aee6', True, True, 'mymochi.com'),
    'liralearning':    ('#ebe0f4', '#cfb9e6', True, False, 'liralearning.com'),
    'usjewelry':       ('#efe9de', '#d8cdb8', True, True, 'usjewelryfactory.com'),
    'silvermirror':    ('#ece8e2', '#d3cbc0', True, True, 'silvermirror.com'),
    'temptu':          ('#e5ded7', '#c4b8ad', True, True, 'temptu.com'),
    'bioeffect':       ('#dcece3', '#b5d3c1', False, True, 'bioeffect.de'),
    'trafalgar':       ('#f4dedd', '#e3b4b2', True, True, 'trafalgar.com'),
    'automationwerks': ('#dbe3f3', '#b4c3e6', True, True, 'automationwerks.com'),
    'rogerkallen':     ('#e2e8f0', '#bccadd', True, True, 'rogerkallen.com'),
}


def font(size, bold=False):
    for f in ('segoeuib.ttf' if bold else 'segoeui.ttf', 'arialbd.ttf' if bold else 'arial.ttf'):
        try:
            return ImageFont.truetype('C:/Windows/Fonts/' + f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def backdrop(size, light, deep):
    w, h = size
    a, b = hex2rgb(light), hex2rgb(deep)
    base = Image.new('RGB', size)
    px = base.load()
    for y in range(h):
        for x in range(w):
            t = (x / w * 0.45 + y / h * 0.55)
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    glow = Image.new('L', size, 0)
    ImageDraw.Draw(glow).ellipse((w * .1, -h * .25, w * .9, h * .75), fill=120)
    glow = glow.filter(ImageFilter.GaussianBlur(w // 8))
    base.paste(Image.new('RGB', size, (255, 255, 255)), (0, 0), glow.point(lambda v: int(v * .35)))
    return base.convert('RGBA')


def rmask(size, r):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def soft_shadow(canvas, box, radius, blur, alpha, dy=0):
    x0, y0, x1, y1 = box
    pad = blur * 3
    layer = Image.new('RGBA', (x1 - x0 + pad * 2, y1 - y0 + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), radius, fill=(8, 12, 20, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(layer, (x0 - pad, y0 - pad + dy))


def fit_cover(img, size):
    w, h = size
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    return img.crop((0, 0, w, h))


def laptop(canvas, shot, x, y, sw):
    sh = round(sw * 10 / 16)
    b = round(sw * 0.022)
    lw, lh = sw + 2 * b, sh + b + round(b * 1.5)
    soft_shadow(canvas, (x + b, y + lh, x + lw - b, y + lh + b * 2), b, b * 3, 120, b * 2)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((x, y, x + lw, y + lh), round(lw * 0.018), fill=(15, 16, 18, 255))
    d.rounded_rectangle((x + 2, y + 2, x + lw - 2, y + lh - 2), round(lw * 0.018), outline=(60, 62, 68, 255), width=2)
    scr = fit_cover(shot.convert('RGB'), (sw, sh)).convert('RGBA')
    canvas.paste(scr, (x + b, y + b), rmask((sw, sh), 8))
    d.ellipse((x + lw // 2 - 4, y + b // 2 - 4, x + lw // 2 + 4, y + b // 2 + 4), fill=(40, 42, 48, 255))
    # base
    bw, bh = round(lw * 1.1), max(14, round(lw * 0.02))
    bx, by = x - (bw - lw) // 2, y + lh
    grad = Image.new('RGBA', (bw, bh))
    gd = ImageDraw.Draw(grad)
    for i in range(bh):
        t = i / max(1, bh - 1)
        gd.line((0, i, bw, i), fill=(int(226 - 40 * t), int(228 - 40 * t), int(233 - 38 * t), 255))
    m = Image.new('L', (bw, bh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, -bh, bw, bh - 1), bh, fill=255)
    canvas.paste(grad, (bx, by), m)
    nw = round(lw * 0.15)
    d.rounded_rectangle((x + (lw - nw) // 2, by, x + (lw + nw) // 2, by + round(bh * 0.55)), round(bh * 0.4), fill=(168, 171, 178, 255))
    return lw, lh + bh


def phone(canvas, shot, x, y, sw):
    sh = round(sw * 844 / 390)
    b = round(sw * 0.038)
    pw, ph = sw + 2 * b, sh + 2 * b
    r = round(sw * 0.2)
    soft_shadow(canvas, (x + b, y + b * 2, x + pw - b, y + ph), r, b * 3, 130, b * 3)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((x, y, x + pw, y + ph), r, fill=(16, 17, 20, 255))
    d.rounded_rectangle((x + 1, y + 1, x + pw - 1, y + ph - 1), r, outline=(70, 72, 78, 255), width=3)
    scr = fit_cover(shot.convert('RGB'), (sw, sh)).convert('RGBA')
    canvas.paste(scr, (x + b, y + b), rmask((sw, sh), round(sw * 0.15)))
    iw, ih = round(sw * 0.3), round(sw * 0.085)
    d.rounded_rectangle((x + (pw - iw) // 2, y + b + round(sw * 0.03), x + (pw + iw) // 2, y + b + round(sw * 0.03) + ih), ih // 2, fill=(8, 8, 10, 255))
    for yy, hh in ((0.22, 0.07), (0.32, 0.1), (0.45, 0.1)):
        d.rounded_rectangle((x - 3, y + round(ph * yy), x, y + round(ph * (yy + hh))), 2, fill=(40, 42, 48, 255))
    return pw, ph


def browser(canvas, shot, x, y, w, domain):
    bar = round(w * 0.04)
    sh = round((w) * 9 / 16 * 1.0)
    h = bar + sh
    r = round(w * 0.014)
    soft_shadow(canvas, (x + 20, y + 30, x + w - 20, y + h), r, w // 60, 110, w // 40)
    win = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    wd = ImageDraw.Draw(win)
    wd.rectangle((0, 0, w, bar), fill=(241, 242, 245, 255))
    cy = bar // 2
    for i, col in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        cx = round(bar * 0.6) + i * round(bar * 0.42)
        wd.ellipse((cx - bar * 0.12, cy - bar * 0.12, cx + bar * 0.12, cy + bar * 0.12), fill=col + (255,))
    uw, uh = round(w * 0.46), round(bar * 0.56)
    ux = (w - uw) // 2
    wd.rounded_rectangle((ux, cy - uh // 2, ux + uw, cy + uh // 2), uh // 2, fill=(255, 255, 255, 255))
    f = font(round(bar * 0.3))
    tw = wd.textlength(domain, font=f)
    wd.text((ux + (uw - tw) / 2, cy - bar * 0.19), domain, fill=(88, 92, 100, 255), font=f)
    win.paste(fit_cover(shot.convert('RGB'), (w, sh)), (0, bar))
    canvas.paste(win, (x, y), rmask((w, h), r))
    return w, h


def save_webp(img, path, width):
    img = img.convert('RGB')
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    img.save(path, 'WEBP', quality=84, method=5)
    return img.size


for slug, (c1, c2, has_d, has_m, domain) in SITES.items():
    d_path, m_path = os.path.join(SRC, slug + '-d.png'), os.path.join(SRC, slug + '-m.png')
    D = Image.open(d_path) if has_d and os.path.exists(d_path) else None
    M = Image.open(m_path) if has_m and os.path.exists(m_path) else None
    out = os.path.join(ROOT, 'assets', 'img', 'work', slug)
    os.makedirs(out, exist_ok=True)
    made = []

    # 01: hero mockup (laptop + phone)
    cv = backdrop((2000, 1500), c1, c2)
    if D and M:
        lw, lh = laptop(cv, D, 110, 330, 1360)
        phone(cv, M, 1500, 470, 270)
    elif D:
        lw, lh = laptop(cv, D, 220, 330, 1560)
    elif M:
        pw, ph = phone(cv, M, 560, 180, 430)
        phone(cv, M, 1010, 330, 400)
    made.append(save_webp(cv, os.path.join(out, '01.webp'), 1500))

    # 02: browser window
    if D:
        cv2 = backdrop((2000, 1400), c2, c1)
        browser(cv2, D, 150, 200, 1700, domain)
        made.append(save_webp(cv2, os.path.join(out, '02.webp'), 1500))
    # 03: phone portrait
    if M:
        cv3 = backdrop((1500, 1500), c1, c2)
        phone(cv3, M, 505, 120, 430) if False else phone(cv3, M, 520, 150, 400)
        made.append(save_webp(cv3, os.path.join(out, '03.webp'), 1200))

    cover = Image.open(os.path.join(out, '01.webp')).convert('RGB')
    cw, ch = save_webp(cover, os.path.join(out, 'cover.webp'), 1200)
    print('%-16s %d images, cover %dx%d' % (slug, len(made), cw, ch))
