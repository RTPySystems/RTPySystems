"""Artes do perfil. Gere com: python3 scripts/render_art.py."""
from pathlib import Path
from html import escape
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
FONT = 'DejaVu Sans, sans-serif'


def text(x, y, content, size=20, fill='#a7b0bf', weight=400):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(str(content))}</text>'


def rect(x, y, w, h, fill='#121720', stroke='#252c38', radius=16):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def frame(w, h, body):
    grid = ''.join(f'<path d="M{x} 0V{h}" stroke="#ffffff" opacity=".025"/>' for x in range(0, w, 40))
    grid += ''.join(f'<path d="M0 {y}H{w}" stroke="#ffffff" opacity=".025"/>' for y in range(0, h, 40))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
    <defs><radialGradient id="glow"><stop stop-color="#e11d2e" stop-opacity=".22"/><stop offset="1" stop-color="#e11d2e" stop-opacity="0"/></radialGradient></defs>
    <rect width="{w}" height="{h}" rx="24" fill="#0b0e14"/>{grid}
    <ellipse cx="{w*.8}" cy="{h*.3}" rx="{w*.5}" ry="{h*.9}" fill="url(#glow)"/>
    <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="24" fill="none" stroke="#2c2630"/>{body}</svg>'''


def save(name, w, h, body):
    cairosvg.svg2png(bytestring=frame(w, h, body).encode(), write_to=str(ROOT / 'assets' / name), scale=1.5)


def main():
    body = text(52, 62, 'DESENVOLVIMENTO  /  BRASIL', 14, '#fb7185', 700)
    body += text(48, 151, 'RTPySystems', 62, '#f4f6fa', 700)
    body += text(52, 202, 'Sites, bots e APIs.', 31, '#f4f6fa', 700)
    body += text(52, 241, 'Do código à aplicação no ar.', 22)
    body += rect(52, 292, 273, 45, '#25121a', '#65303c', 22)
    body += text(73, 321, 'FUNDADOR DA RTCLOUD', 15, '#fda4af', 700)
    body += text(52, 388, 'WEB  /  AUTOMAÇÃO  /  CLOUD', 13, '#758093', 700)
    body += rect(662, 67, 470, 283, '#11151e', '#34303b')
    body += '<path d="M662 109H1132" stroke="#34303b"/>'
    for x, c in [(684, '#e11d2e'), (703, '#fbbf24'), (722, '#34d399')]:
        body += f'<circle cx="{x}" cy="89" r="5" fill="{c}"/>'
    body += text(758, 94, 'workspace / projeto', 13, '#939baa')
    lines = [('01', 'const projeto = {', '#c4b5fd'), ('02', '  interface: "bem resolvida",', '#dce2ed'), ('03', '  backend: "organizado",', '#dce2ed'), ('04', '  deploy: "RTCloud"', '#fb7185'), ('05', '};', '#c4b5fd')]
    for i, (num, line, color) in enumerate(lines):
        body += text(685, 151+i*31, num, 14, '#535e70') + text(723, 151+i*31, line, 16, color)
    body += rect(684, 309, 424, 24, '#13241f', '#244c3b', 7)
    body += text(699, 326, '> build concluído  ·  aplicação publicada', 12, '#6ee7b7')
    body += '<path d="M891 350V383H1078" fill="none" stroke="#e11d2e" stroke-width="2"/>'
    body += '<circle cx="1078" cy="383" r="5" fill="#e11d2e"/>'
    body += text(678, 395, '&lt;/&gt;'.replace('&lt;', '<').replace('&gt;', '>'), 30, '#e11d2e', 700)
    save('hero-developer.png', 1200, 440, body)

    body = text(50, 57, 'MEU PRINCIPAL PROJETO', 14, '#fb7185', 700)
    body += text(46, 132, 'RTCloud', 64, '#f4f6fa', 700)
    body += text(50, 181, 'Hospedagem para quem cria.', 26, '#f4f6fa', 700)
    body += text(50, 222, 'Bots, sites e APIs em um painel em português.', 18)
    for i, label in enumerate(['DEPLOY PELO GITHUB', 'HTTPS AUTOMÁTICO', 'PIX AUTOMÁTICO']):
        body += text(50, 272+i*31, '↗  ' + label, 14, '#d2d9e5', 700)
    body += text(50, 400, 'rtcloud.com.br', 20, '#fb7185', 700)
    body += rect(662, 59, 482, 330, '#10151e', '#34303b')
    body += text(687, 93, 'RT / CLOUD', 14, '#f4f6fa', 700)
    body += rect(1012, 74, 107, 25, '#13241f', '#244c3b', 12)
    body += text(1028, 91, 'SEU PAINEL', 10, '#6ee7b7', 700)
    for i, (label, sub, color) in enumerate([('website', 'HTTPS · domínio próprio', '#e11d2e'), ('api', 'rotas · métricas · logs', '#60a5fa'), ('bot', 'console · reinício automático', '#a78bfa')]):
        y = 121 + i*68
        body += rect(686, y, 434, 57, '#161c27', '#273040', 9)
        body += f'<circle cx="706" cy="{y+28}" r="4" fill="{color}"/>'
        body += text(722, y+24, label, 15, '#f4f6fa', 700) + text(722, y+44, sub, 11)
        body += f'<path d="M974 {y+36}l18 -8 13 5 16 -19 13 6 18 -12 18 5 22 -9" fill="none" stroke="{color}" stroke-width="2"/>'
    body += text(687, 362, 'GITHUB → BUILD → DEPLOY → MONITOR', 13, '#939baa', 700)
    body += text(825, 420, 'ILUSTRAÇÃO DO FLUXO DA PLATAFORMA', 10, '#626e81')
    save('rtcloud-platform.png', 1200, 455, body)

    body = text(40, 51, 'COMO EU TRABALHO', 13, '#fb7185', 700)
    steps = [('01', 'Entender', 'O que o projeto precisa resolver.'), ('02', 'Construir', 'Interface, lógica e integrações.'), ('03', 'Publicar', 'Deploy, logs e acompanhamento.')]
    for i, (num, title, desc) in enumerate(steps):
        x = 40+i*390
        body += text(x, 112, num, 32, '#e11d2e', 700) + text(x+64, 110, title, 24, '#f4f6fa', 700)
        body += text(x, 152, desc, 15)
        if i < 2:
            body += f'<path d="M{x+310} 101h42m-8 -5 8 5 -8 5" fill="none" stroke="#4d3441" stroke-width="2"/>'
    save('workflow.png', 1200, 196, body)

if __name__ == '__main__':
    main()
