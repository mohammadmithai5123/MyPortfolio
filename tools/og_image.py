"""Makes the 1200x630 picture shown when the site link is shared (WhatsApp, LinkedIn, Facebook, X).
usage: python tools/og_image.py .
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

root = sys.argv[1] if len(sys.argv) > 1 else '.'
W, H = 1200, 630


def font(size, bold=False):
    for f in (('seguisb.ttf', 'segoeuib.ttf', 'arialbd.ttf') if bold else ('segoeui.ttf', 'arial.ttf')):
        try:
            return ImageFont.truetype('C:/Windows/Fonts/' + f, size)
        except OSError:
            continue
    return ImageFont.load_default()


# studio-grey backdrop with a soft light behind the head and a vignette
bg = Image.new('RGB', (W, H), (152, 160, 166))
glow = Image.new('L', (W, H), 0)
ImageDraw.Draw(glow).ellipse((560, -120, 1160, 560), fill=110)
glow = glow.filter(ImageFilter.GaussianBlur(90))
bg.paste(Image.new('RGB', (W, H), (255, 255, 255)), (0, 0), glow)
vig = Image.new('L', (W, H), 0)
ImageDraw.Draw(vig).ellipse((-250, -200, W + 250, H + 200), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(120))
dark = Image.new('RGB', (W, H), (40, 46, 52))
bg = Image.composite(bg, Image.blend(bg, dark, .55), vig)

# person (cutout), right side, cropped by the bottom edge
cut = Image.open(os.path.join(root, 'assets', 'img', 'profile-cutout.webp')).convert('RGBA')
ph = int(H * 1.04)
cut = cut.resize((int(cut.width * ph / cut.height), ph), Image.LANCZOS)
canvas = bg.convert('RGBA')
canvas.alpha_composite(cut, (W - cut.width - 40, H - ph + 26))

d = ImageDraw.Draw(canvas)
d.text((70, 150), 'Mohammad', font=font(120, True), fill='white')
d.text((70, 262), 'Muslim', font=font(120, True), fill='white')
d.text((74, 420), 'Freelance Designer & Developer', font=font(36), fill=(255, 255, 255, 235))
# location pill
pill = (74, 492, 74 + 262, 492 + 58)
d.rounded_rectangle(pill, 29, fill=(28, 29, 32, 255))
d.ellipse((pill[0] + 20, pill[1] + 22, pill[0] + 34, pill[1] + 36), fill=(34, 197, 94, 255))
d.text((pill[0] + 48, pill[1] + 12), 'Based in the UAE', font=font(26), fill='white')

out = os.path.join(root, 'assets', 'img', 'og.jpg')
canvas.convert('RGB').save(out, 'JPEG', quality=86, optimize=True, progressive=True)
print('og.jpg', os.path.getsize(out) // 1024, 'KB')
