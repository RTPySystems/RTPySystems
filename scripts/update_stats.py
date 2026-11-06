"""Atualiza os cards PNG usando somente repositórios públicos próprios.

CI: GITHUB_TOKEN é lido do ambiente. Local: usa a sessão já aberta do gh.
Nenhum token ou payload da API é gravado nos arquivos gerados.
"""
import json
import os
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from render_art import frame, rect, text
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
COLORS = ['#e11d2e', '#60a5fa', '#fbbf24', '#a78bfa', '#34d399', '#fb923c']


def api(endpoint):
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        return json.loads(subprocess.check_output(['gh', 'api', endpoint], text=True))
    request = Request('https://api.github.com/' + endpoint, headers={
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'RTPySystems-profile',
    })
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def public_repositories(username):
    result = []
    page = 1
    while True:
        batch = api(f'users/{username}/repos?type=owner&per_page=100&page={page}')
        result.extend(repo for repo in batch if not repo['private'] and not repo['fork'])
        if len(batch) < 100:
            return result
        page += 1


def language_rows(languages, limit=5):
    """Agrupa o restante para manter o card legível sem descartar bytes."""
    rows = languages.most_common(limit)
    remainder = sum(languages.values()) - sum(value for _, value in rows)
    if remainder:
        rows.append(('Outras', remainder))
    return rows


def write_card(name, body):
    cairosvg.svg2png(bytestring=frame(600, 340, body).encode(),
                     write_to=str(ROOT / 'assets' / name), scale=2)


def main():
    username = os.environ.get('PROFILE_USERNAME', 'RTPySystems')
    repositories = public_repositories(username)
    languages = Counter()
    for repo in repositories:
        languages.update(api(f"repos/{repo['full_name']}/languages"))
    stamp = datetime.now(ZoneInfo('America/Recife')).strftime('%d/%m/%Y')
    common = text(30, 47, 'CÓDIGO PÚBLICO', 15, '#fb7185', 700)
    metrics = [(len(repositories), 'repositórios próprios'),
               (sum(repo['stargazers_count'] for repo in repositories), 'estrelas recebidas'),
               (sum(repo['forks_count'] for repo in repositories), 'forks recebidos'),
               (len(languages), 'linguagens no código')]
    for i, (value, label) in enumerate(metrics):
        x, y = 30 + (i % 2)*282, 72 + (i // 2)*103
        common += rect(x, y, 258, 87, '#141922', '#282d39', 10)
        common += text(x+17, y+39, value, 31, '#f4f6fa', 700)
        common += text(x+17, y+65, label, 13)
    common += text(30, 303, f'GitHub API · {stamp} · sem forks ou repositórios privados', 11, '#818b9d')
    write_card('github-stats.png', common)

    body = text(30, 47, 'LINGUAGENS NOS REPOSITÓRIOS', 15, '#fb7185', 700)
    rows = language_rows(languages)
    total = sum(languages.values())
    x = 30
    for i, (_, value) in enumerate(rows):
        width = 540*value/total
        body += rect(x, 72, width, 13, COLORS[i], COLORS[i], 0)
        x += width
    for i, (language, value) in enumerate(rows):
        y = 120 + i*27
        body += f'<circle cx="36" cy="{y-5}" r="4" fill="{COLORS[i]}"/>'
        body += text(50, y, language, 15, '#e0e5ef')
        body += text(503, y, f'{value/total:.1%}', 14, '#a7b0bf')
    if not rows:
        body += text(30, 135, 'Nenhuma linguagem identificada pela API.', 16)
    body += text(30, 303, 'Proporção em bytes · não representa domínio ou experiência', 11, '#818b9d')
    write_card('github-languages.png', body)
    print(f'Cards atualizados: {len(repositories)} repositórios públicos, {len(languages)} linguagens.')


if __name__ == '__main__':
    main()
