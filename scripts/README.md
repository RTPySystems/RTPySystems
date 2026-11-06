# Artes e cards do perfil

Os cards e badges são PNGs do próprio GitHub, com endereço absoluto. As artes usam `<picture>`: SVG animado em telas a partir de 768 px e GIF local como fallback. A digitação no desktop usa o readme-typing-svg; o fallback GIF reproduz as mesmas quatro frases sem depender do serviço externo. Cada bloco exibe uma única versão, sem duplicar as artes.

## Estatísticas

```sh
pip install -r scripts/requirements.txt
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/update_stats.py
```

Localmente, o script usa a sessão existente do `gh`. No Actions, lê `GITHUB_TOKEN` do ambiente, fornecido pelo próprio GitHub. Não salve tokens no repositório.

- Busca todos os repositórios públicos de RTPySystems, com paginação.
- Exclui forks e repositórios privados. Inclui os públicos arquivados.
- Soma estrelas e forks recebidos nos repositórios incluídos.
- Soma os bytes de cada linguagem retornados pela API. Não é uma medida de experiência, tempo de trabalho ou quantidade de commits.
- Em falha da API, o processo termina sem publicar alterações; os últimos PNGs permanecem disponíveis.
- O workflow roda diariamente às **09:29 (America/Recife)** e também por `workflow_dispatch`. O horário do cron do GitHub é UTC e pode sofrer atrasos. Repositórios públicos sem atividade por 60 dias podem ter schedules desativados pelo GitHub.

A permissão de escrita do workflow é usada somente para atualizar os dois cards. Nenhum serviço externo recebe o token. As imagens não contêm dados privados.

## Artes

```sh
pip install -r scripts/requirements-art.txt
python3 scripts/render_animations.py
```

As artes vetoriais são geradas por `render_art.py`, com conversão PNG via CairoSVG. `render_animations.py` acrescenta movimento aos SVGs e gera versões GIF com Pillow: cabeçalho, digitação, RTCloud e divisores. Os GIFs usam paleta compartilhada, primeiro quadro legível e loop infinito; cada arquivo fica abaixo de 1,5 MB. No Linux, a fonte usada é DejaVu Sans.

O fallback `<img>` é GIF para manter a arte disponível em leitores que ignoram `<source>` ou não exibem SVG. A seleção de fontes de `<picture>` foi conferida com o renderizador Markdown do GitHub; a reprodução no app nativo ainda depende do suporte do próprio app. A ilustração da plataforma representa um fluxo de uso, não um painel com métricas reais.

Os badges locais de `assets/stack/` são versões PNG dos badges do Shields.io com ícones Simple Icons; grammY usa o ícone do Telegram, Baileys o do WhatsApp e SQL o do MySQL.
