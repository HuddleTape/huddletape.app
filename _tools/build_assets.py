"""Regenerates site assets from /workspace/huddletape-brand. Run: python3 _tools/build_assets.py
(Not part of the deployed site.)"""
import os, sys, shutil
BR = '/workspace/huddletape-brand'
sys.path.insert(0, os.path.join(BR, 'src'))
import r2logos as L
from fontTools import subset
from PIL import Image
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(SITE, 'assets'); IMG = os.path.join(A, 'img'); FN = os.path.join(A, 'fonts')
PINK = '#FF3EA5'

# ---- fonts -> woff2 (Latin subset) ----
fonts = {'anton/Anton-Regular.ttf': 'anton.woff2',
         'barlowsemicondensed/BarlowSemiCondensed-Medium.ttf': 'barlow-sc-500.woff2',
         'barlowsemicondensed/BarlowSemiCondensed-SemiBold.ttf': 'barlow-sc-600.woff2',
         'barlowsemicondensed/BarlowSemiCondensed-Bold.ttf': 'barlow-sc-700.woff2',
         'chakrapetch/ChakraPetch-Bold.ttf': 'chakra-700.woff2'}
for src, dst in fonts.items():
    subset.main([os.path.join(BR, 'fonts', src), '--flavor=woff2', f'--output-file={os.path.join(FN, dst)}',
                 '--unicodes=U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2190-2199,U+2212,U+2215,U+25B2,U+25BC,U+00B7',
                 '--layout-features=*'])
for d in ['anton', 'barlowsemicondensed', 'chakrapetch']:
    shutil.copy(os.path.join(BR, 'fonts', d, 'OFL.txt'), os.path.join(FN, f'OFL-{d}.txt'))

# ---- wordmark (slanted, outlined paths, no font needed) ----
body, ww, cap = L.a1_word(100, '#FFFFFF', PINK)
sk = cap * L.T10; pad = 6
tr = f'translate({pad + sk:.1f} {pad + cap:.1f}) skewX(-10)'
W, H = ww + 2 * pad + sk, cap + 2 * pad
wm = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="HuddleTape">'
      f'<g transform="{tr}">{body}</g></svg>')
open(os.path.join(IMG, 'wordmark.svg'), 'w').write(wm)

# ---- '#' mark (neon) for favicon.svg ----
mark = L.a1_mark(PINK, L.CYAN, L.LIME, neon=True)
s = 0.78
fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><defs>{L.glow(7)}</defs>'
       f'<rect width="400" height="400" rx="88" fill="#0A0614"/>'
       f'<g transform="translate({200 - 257 * s:.1f} {200 - 256 * s:.1f}) scale({s})">{mark}</g></svg>')
open(os.path.join(SITE, 'favicon.svg'), 'w').write(fav)
open(os.path.join(IMG, 'mark.svg'), 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="20 90 560 340"><defs>{L.glow(7)}</defs>{mark}</svg>')

# ---- raster icons from the 400px avatar ----
av = Image.open(os.path.join(BR, 'x-kit', 'huddletape-avatar-400.png')).convert('RGBA')
av.resize((180, 180), Image.LANCZOS).save(os.path.join(SITE, 'apple-touch-icon.png'), optimize=True)
for n in (192, 512):
    av.resize((n, n), Image.LANCZOS).save(os.path.join(IMG, f'icon-{n}.png'), optimize=True)
av.save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])

# ---- Tailer sprite sheets (half size, webp) ----
T = os.path.join(BR, 'tailer', 'sprites-T1')
for name in ('trot', 'wag'):
    im = Image.open(os.path.join(T, f'tailer-{name}-sheet.png'))
    im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    im.save(os.path.join(IMG, f'tailer-{name}.webp'), 'WEBP', quality=88, method=6)
Image.open(os.path.join(T, 'tailer-wag-0.png')).resize((220, 145), Image.LANCZOS).save(os.path.join(IMG, 'tailer.png'), optimize=True)
print('ok')
