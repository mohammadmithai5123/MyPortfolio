import os, sys, json, statistics, datetime
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
SRC = sys.argv[1]            # portfolio source root
OUT = sys.argv[2]            # repo root
EXT = {'.jpg', '.jpeg', '.png', '.webp', '.jfif', '.avif'}


def listdir_imgs(sub):
    d = os.path.join(SRC, sub)
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if os.path.splitext(f)[1].lower() in EXT]


P = []


def add(slug, title, services, kinds, files, cover, captions=None, desc=''):
    P.append(dict(slug=slug, title=title, services=services, kinds=kinds, files=files,
                  cover=cover, captions=captions or {}, desc=desc))


# (Development work now comes from tools/mockups.py: one project per live client site, see SITES below.)

wd = listdir_imgs('Website Design')
add('web-design', 'Web Design Concepts', 'Design', ['design'], wd, 0,
    {i: os.path.splitext(os.path.basename(f))[0] for i, f in enumerate(wd)},
    'Landing pages and website concepts with strong hierarchy, bold type and conversion in mind.')

ux = listdir_imgs('UI UX')
ux = [f for i, f in enumerate(ux) if i != 7]
add('ui-ux-design', 'UI / UX Design', 'Design', ['design'], ux, 8, {},
    'Product interfaces, dashboards and design systems for web platforms and SaaS.')

ma = listdir_imgs('Mobile App Design')
add('mobile-apps', 'Mobile Apps', 'Design', ['design'], ma, 4,
    {i: os.path.splitext(os.path.basename(f))[0].replace(' Design', '') for i, f in enumerate(ma)},
    'Mobile app interfaces across banking, health, sports, and AI products.')

bi = listdir_imgs('Brand Identity Design')
bi = [f for i, f in enumerate(bi) if i != 15]
add('brand-identity', 'Brand Identity', 'Design', ['design'], bi, 7, {},
    'Complete brand systems: logo, colour, typography, and the touchpoints that bring them to life.')

lg = listdir_imgs('Logo Design')
add('logo-design', 'Logo Design', 'Design', ['design'], lg, 7, {},
    'Logos and marks for startups, sports teams and consumer brands.')

pk = listdir_imgs('Packaging Designs')
add('packaging', 'Packaging', 'Design', ['design'], pk, 2, {},
    'Packaging and dielines for food, wellness, and healthcare products.')

pdk = listdir_imgs('Pitch Deck Design')
pdk = [f for i, f in enumerate(pdk) if i not in (6, 12)]
add('pitch-decks', 'Pitch Decks', 'Design', ['design'], pdk, 2, {},
    'Investor and sales decks that make complex stories easy to follow.')

sm = listdir_imgs('Social Media Design')
sm = [f for i, f in enumerate(sm) if i != 4]
add('social-media', 'Social Media', 'Design', ['design'], sm, 15, {},
    'Social posts, carousels, and banners built as consistent campaign systems.')

ad = listdir_imgs('ADs')
ad = [f for i, f in enumerate(ad) if i not in (20, 22)]
add('ads-campaigns', 'Ads & Campaigns', 'Design', ['design'], ad, 14, {},
    'Paid-social ad creative designed to stop the scroll and drive action.')

# Which side of the portfolio each collection belongs to, and the order they appear in.
GROUP = {
    'brand-identity': 'design', 'logo-design': 'design', 'packaging': 'design', 'ui-ux-design': 'design',
    'mobile-apps': 'design', 'web-design': 'design', 'pitch-decks': 'design', 'social-media': 'design',
    'ads-campaigns': 'design',
}
ORDER = ['brand-identity', 'logo-design', 'packaging', 'ui-ux-design', 'mobile-apps', 'web-design', 'pitch-decks',
         'social-media', 'ads-campaigns']

# Development projects: one per live client site. Images are made by tools/mockups.py from real screenshots.
# slug, title, platform (shown as the service), url, description
SITES = [
    ('tetongear', 'Teton Gear', 'Shopify', 'https://tetongear.com/',
     'Premium outdoor gear e-commerce with custom filtering and performance-optimized pages.'),
    ('ex1cosmetics', 'EX1 Cosmetics', 'Shopify', 'https://ex1cosmetics.com/',
     'Luxury beauty brand with editorial product pages and custom Shopify theme.'),
    ('kiefer', 'Kiefer', 'Shopify', 'https://www.kiefer.com/',
     'Aquatic sports retailer with large catalog management and performance-tuned storefront.'),
    ('vsg', 'Very Special Games', 'Shopify Plus', 'https://www.veryspecialgames.com/',
     'Custom gaming studio site with dynamic title showcases and interactive visuals.'),
    ('mymochi', 'My Mochi Ice Cream', 'WordPress / WooCommerce', 'https://www.mymochi.com/',
     'National ice cream brand with flavor explorer, store finder, and subscription.'),
    ('liralearning', 'Lira Learning', 'WordPress / WooCommerce', 'https://liralearning.com/',
     'Education platform with course management, student portals, and LMS integration.'),
    ('usjewelry', 'US Jewelry Factory', 'Magento', 'https://www.usjewelryfactory.com/',
     'Custom jewelry platform with product configurator and wholesale trade portal.'),
    ('silvermirror', 'Silver Mirror Facial Bar', 'WordPress / Custom', 'https://silvermirror.com/',
     'Luxury facial bar brand with AI-powered booking and editorial UX.'),
    ('temptu', 'Temptu', 'Magento to Shopify', 'https://temptu.com/',
     'Magento to Shopify migration preserving product data and order history.'),
    ('bioeffect', 'Bioeffect', 'Magento to Shopify', 'https://bioeffect.de/',
     'Skincare re-platformed from Magento to Shopify with multi-currency.'),
    ('trafalgar', 'Trafalgar Travel', 'WordPress', 'https://www.trafalgar.com/en-us',
     'Enterprise travel platform with tour listings, booking flows, and itinerary management.'),
    ('automationwerks', 'Automation Werks', 'WordPress', 'https://www.automationwerks.com/',
     'B2B industrial automation website with product catalog and lead generation.'),
    ('rogerkallen', 'Roger Kallen', 'Custom', 'https://www.rogerkallen.com/',
     'Fine art photographer portfolio with gallery management and print ordering.'),
]

# Live client websites (Archive list on the Work page). name, url, type, platform
ARCHIVE = [
    ('Teton Gear', 'https://tetongear.com/', 'Outdoor / E-Commerce', 'Shopify'),
    ('EX1 Cosmetics', 'https://ex1cosmetics.com/', 'Beauty', 'Shopify'),
    ('Kiefer', 'https://www.kiefer.com/', 'Sports', 'Shopify'),
    ('My Mochi Ice Cream', 'https://www.mymochi.com/', 'Food & Beverage', 'WordPress / WooCommerce'),
    ('Trafalgar Travel', 'https://www.trafalgar.com/en-us', 'Travel', 'WordPress'),
    ('Westcott Press', 'https://westcottpress.com/', 'Publishing', 'WordPress'),
    ('US Jewelry Factory', 'https://www.usjewelryfactory.com/', 'Jewelry', 'Magento'),
    ('Lira Learning', 'https://liralearning.com/', 'EdTech', 'WordPress / WooCommerce'),
    ('Automation Werks', 'https://www.automationwerks.com/', 'Industrial B2B', 'WordPress'),
    ('New South Botanicals', 'http://newsouthbotanicals.com/', 'Wellness', 'WordPress'),
    ('Very Special Games', 'https://www.veryspecialgames.com/', 'Gaming', 'Shopify Plus'),
    ('Roger Kallen', 'https://www.rogerkallen.com/', 'Art / Portfolio', 'Custom'),
    ('Silver Mirror Facial Bar', 'https://silvermirror.com/', 'Beauty', 'WordPress / Custom'),
    ('Temptu', 'https://temptu.com/', 'Pro Makeup', 'Magento to Shopify'),
    ('Bioeffect', 'https://bioeffect.de/', 'Skincare', 'Magento to Shopify'),
]

CAPTION_SLUGS = ('shopify-stores', 'wordpress-builds', 'business-websites', 'web-design', 'mobile-apps')


def to_rgb(im):
    im = ImageOps.exif_transpose(im)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert('RGB')


def save(im, path, maxw, q):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(path, 'WEBP', quality=q, method=5)
    return im.size


out_data = []
total = 0
for p in P:
    d = os.path.join(OUT, 'assets', 'img', 'work', p['slug'])
    os.makedirs(d, exist_ok=True)
    years = [datetime.datetime.fromtimestamp(os.path.getmtime(f)).year for f in p['files']]
    year = statistics.median_low(years)
    imgs = []
    cim = None
    for i, f in enumerate(p['files']):
        im = to_rgb(Image.open(f))
        fn = '%02d.webp' % (i + 1)
        w, h = save(im, os.path.join(d, fn), 1500, 76)
        cap = p['captions'].get(i, '') if p['slug'] in CAPTION_SLUGS else ''
        imgs.append(dict(src='assets/img/work/%s/%s' % (p['slug'], fn), w=w, h=h, caption=cap))
        total += os.path.getsize(os.path.join(d, fn))
        if i == p['cover']:
            cim = im
    cw, ch = save(cim, os.path.join(d, 'cover.webp'), 1200, 74)
    total += os.path.getsize(os.path.join(d, 'cover.webp'))
    avg = cim.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    out_data.append(dict(slug=p['slug'], title=p['title'], group=GROUP[p['slug']], services=p['services'], kinds=p['kinds'],
                         year=year, desc=p['desc'],
                         cover='assets/img/work/%s/cover.webp' % p['slug'], coverW=cw, coverH=ch,
                         color='#%02x%02x%02x' % avg, images=imgs))
    print('%-20s %3d imgs  year~%s' % (p['slug'], len(imgs), year))

prof = to_rgb(Image.open(os.path.join(OUT, 'assets', 'images', 'profile', '111.png')))
pw, ph = save(prof, os.path.join(OUT, 'assets', 'img', 'profile.webp'), 900, 80)
print('profile', pw, ph)

os.makedirs(os.path.join(OUT, 'assets', 'js'), exist_ok=True)
out_data.sort(key=lambda d: ORDER.index(d['slug']))
for slug, title, platform, url, desc in SITES:
    d = os.path.join(OUT, 'assets', 'img', 'work', slug)
    files = sorted(f for f in os.listdir(d) if f.endswith('.webp') and f != 'cover.webp')
    imgs = []
    for f in files:
        w, h = Image.open(os.path.join(d, f)).size
        imgs.append(dict(src='assets/img/work/%s/%s' % (slug, f), w=w, h=h, caption=''))
    cim = Image.open(os.path.join(d, 'cover.webp')).convert('RGB')
    avg = cim.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    out_data.append(dict(slug=slug, title=title, group='development', services=platform, kinds=['development'],
                         year=None, desc=desc, url=url, cover='assets/img/work/%s/cover.webp' % slug,
                         coverW=cim.width, coverH=cim.height, color='#%02x%02x%02x' % avg, images=imgs))
with open(os.path.join(OUT, 'assets', 'js', 'data.js'), 'w', encoding='utf-8') as fh:
    fh.write('/* Project data. Edit titles, years and descriptions here. '
             'Images live in assets/img/work/<slug>/ */\nwindow.PROJECTS = ')
    json.dump(out_data, fh, ensure_ascii=False, separators=(',', ':'))
    fh.write(';\n\n/* Live client websites shown in the Archive list on the Work page. */\nwindow.ARCHIVE = ')
    json.dump([dict(name=a, url=b, type=c, platform=d) for a, b, c, d in ARCHIVE], fh, ensure_ascii=False, separators=(',', ':'))
    fh.write(';\n')
print('total webp MB:', round(total / 1e6, 1))
