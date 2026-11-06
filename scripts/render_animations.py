"""Animações GIF locais para o perfil, sem SVG servido ao visitante.

python3 scripts/render_art.py && python3 scripts/render_animations.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import render_art

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
RED = (225, 29, 46)
BG = (11, 14, 20)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
LINES = [
    'Oi, eu sou o RTPySystems',
    'Programador BR · sites, bots e APIs',
    'Construo projetos pra clientes',
    'Fundador da RTCloud',
]


def save_gif(name, frames, durations):
    # Paleta compartilhada: texto e fundo não mudam de cor entre quadros.
    sample = Image.new('RGB', (frames[0].width, frames[0].height * 3))
    for i, index in enumerate([0, len(frames)//3, 2*len(frames)//3]):
        sample.paste(frames[index].convert('RGB'), (0, i*frames[0].height))
    palette = sample.quantize(colors=256)
    indexed = [frame.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE)
               for frame in frames]
    target = ASSETS / name
    indexed[0].save(target, save_all=True, append_images=indexed[1:],
                    duration=durations, loop=0, optimize=True, disposal=1)
    with Image.open(target) as image:
        assert image.is_animated and image.info['loop'] == 0
        assert image.n_frames > 1
        print(f'{name}: {image.n_frames} frames, {target.stat().st_size/1024:.0f} KiB')
    assert target.stat().st_size < 1_500_000, f'GIF acima do orçamento: {name}'


def dot(draw, x, y, color, radius=3):
    for r, a in [(radius+9, 12), (radius+5, 25), (radius+2, 55), (radius, 230)]:
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(*color, a))


def hero():
    base = Image.open(ASSETS / 'hero-developer.png').convert('RGB').resize((1200, 440), Image.Resampling.LANCZOS)
    frames = []
    for i in range(48):
        phase = i / 48
        layer = Image.new('RGBA', base.size)
        d = ImageDraw.Draw(layer)
        # Pulso lento no contorno e pacotes no caminho do deploy.
        alpha = round(48 + 32*math.sin(phase*math.tau))
        d.rounded_rectangle((1, 1, 1198, 438), radius=24, outline=(*RED, alpha), width=2)
        t = (phase * 2) % 1
        distance = t * 220
        if distance < 33:
            x, y = 891, 350+distance
        else:
            x, y = 891+distance-33, 383
        dot(d, x, y, RED, 3)
        # Linha de varredura somente no rodapé vazio do editor.
        x = 685 + phase*421
        d.line((x, 291, min(x+32, 1105), 291), fill=(251, 113, 133, 120), width=2)
        frames.append(Image.alpha_composite(base.convert('RGBA'), layer).convert('RGB'))
    save_gif('hero-developer-animated.gif', frames, 100)


def cloud():
    base = Image.open(ASSETS / 'rtcloud-platform.png').convert('RGB').resize((1200, 455), Image.Resampling.LANCZOS)
    frames = []
    offsets = [(0, 36), (18, 28), (31, 33), (47, 14), (60, 20), (78, 8), (96, 13), (118, 4)]
    for i in range(48):
        layer = Image.new('RGBA', base.size)
        d = ImageDraw.Draw(layer)
        phase = i/48
        for row, color in enumerate([RED, (96, 165, 250), (167, 139, 250)]):
            t = (phase + row/3) % 1
            pos = t*(len(offsets)-1)
            index = min(int(pos), len(offsets)-2)
            frac = pos-index
            x1, y1 = offsets[index]
            x2, y2 = offsets[index+1]
            dot(d, 974+x1+(x2-x1)*frac, 121+row*68+y1+(y2-y1)*frac, color, 2)
        alpha = round(50+25*math.sin(phase*math.tau))
        d.rounded_rectangle((1, 1, 1198, 453), radius=24, outline=(*RED, alpha), width=2)
        frames.append(Image.alpha_composite(base.convert('RGBA'), layer).convert('RGB'))
    save_gif('rtcloud-platform-animated.gif', frames, 100)


def typing():
    font = ImageFont.truetype(FONT, 34)
    small = ImageFont.truetype(FONT, 11)
    frames, timings = [], []

    def add(line, cursor, duration):
        image = Image.new('RGB', (1100, 116), BG)
        d = ImageDraw.Draw(image)
        d.rounded_rectangle((1, 1, 1098, 114), radius=16, outline=(39, 43, 54), width=1)
        d.text((24, 16), '>_', font=small, fill=(251, 113, 133))
        width = d.textlength(line, font=font)
        x = (1100-width)/2
        d.text((x, 41), line, font=font, fill=(244, 246, 250))
        if cursor:
            d.rectangle((x+width+7, 47, x+width+10, 80), fill=RED)
        d.line((430, 102, 670, 102), fill=(86, 31, 45), width=2)
        frames.append(image)
        timings.append(duration)

    # Primeiro quadro completo: continua legível se o app suspender animações.
    add(LINES[0], True, 900)
    for line_index in range(4):
        current = LINES[line_index]
        add(current, False, 300)
        add(current, True, 500)
        for end in range(len(current)-1, -1, -2):
            add(current[:end], True, 40)
        add('', True, 220)
        following = LINES[(line_index+1) % len(LINES)]
        for end in range(1, len(following)+1):
            add(following[:end], True, 60)
        add(following, True, 900)
    save_gif('typing-intro.gif', frames, timings)


def divider():
    frames = []
    for i in range(48):
        image = Image.new('RGB', (1200, 30), BG)
        d = ImageDraw.Draw(image)
        d.line((0, 15, 1200, 15), fill=(39, 35, 45))
        for j in range(2):
            x = (i/48*1200 + j*600) % 1200
            for dx in range(-90, 91):
                weight = max(0, 1-abs(dx)/90)
                color = tuple(round(39+(c-39)*weight*.7) for c in RED)
                d.point((int(x+dx), 15), fill=color)
        d.polygon([(592, 15), (600, 7), (608, 15), (600, 23)], fill=BG, outline=(139, 39, 53))
        d.rectangle((598, 13, 602, 17), fill=RED)
        frames.append(image)
    save_gif('section-divider.gif', frames, 100)


def rich_svg():
    # Mesma arte vetorial do GIF: o navegador recebe vetores + SMIL,
    # enquanto o <img> oferece um fallback animado rasterizado.
    render_art.main()
    pulse = '<rect x="1" y="1" width="1198" height="438" rx="24" fill="none" stroke="#e11d2e" stroke-width="2"><animate attributeName="opacity" values=".2;.5;.2" dur="4.8s" repeatCount="indefinite"/></rect>'
    packet = '<circle r="4" fill="#fb7185"><animateMotion path="M891 350V383H1078" dur="2.4s" repeatCount="indefinite"/></circle>'
    scan = '<path d="M685 291h32" stroke="#fb7185" stroke-width="2" opacity=".5"><animateTransform attributeName="transform" type="translate" values="0 0;390 0;0 0" dur="4.8s" repeatCount="indefinite"/></path>'
    source = (ASSETS/'hero-developer.svg').read_text()
    (ASSETS/'hero-developer-animated.svg').write_text(source.replace('</svg>', pulse+packet+scan+'</svg>'))
    additions = ''
    for row, color in enumerate(['#e11d2e', '#60a5fa', '#a78bfa']):
        y = 121 + row*68
        path = f'M974 {y+36}l18 -8 13 5 16 -19 13 6 18 -12 18 5 22 -9'
        additions += f'<circle r="3" fill="{color}"><animateMotion path="{path}" dur="4.8s" begin="-{row*1.6}s" repeatCount="indefinite"/></circle>'
    source = (ASSETS/'rtcloud-platform.svg').read_text()
    (ASSETS/'rtcloud-platform-animated.svg').write_text(source.replace('</svg>',additions+'</svg>'))
    (ASSETS/'section-divider.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="30" viewBox="0 0 1200 30">
<defs><linearGradient id="trail"><stop stop-color="#e11d2e" stop-opacity="0"/><stop offset=".5" stop-color="#e11d2e"/><stop offset="1" stop-color="#e11d2e" stop-opacity="0"/></linearGradient></defs>
<rect width="1200" height="30" fill="#0b0e14"/><path d="M0 15H1200" stroke="#27232d"/>
<path d="M-100 15H100" stroke="url(#trail)" stroke-width="2"><animateTransform attributeName="transform" type="translate" from="-100 0" to="1300 0" dur="4.8s" repeatCount="indefinite"/></path>
<path d="M592 15l8 -8 8 8 -8 8z" fill="#0b0e14" stroke="#8b2735"/><path d="M598 13h4v4h-4z" fill="#e11d2e"/></svg>''')


if __name__ == '__main__':
    rich_svg()
    hero()
    cloud()
    typing()
    divider()
