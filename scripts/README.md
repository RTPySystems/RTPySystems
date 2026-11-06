# Artes e cards do perfil

As imagens exibidas no README são PNGs do próprio GitHub, com endereço absoluto. Isso evita depender de serviços de cards em tempo de visualização e mantém a compatibilidade com o app do GitHub.

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
python3 scripts/render_art.py
```

Os SVGs são montados em memória e convertidos com CairoSVG. O README referencia apenas os PNGs. A ilustração da plataforma representa um fluxo de uso, não um painel com métricas reais.

Os badges locais de `assets/stack/` são versões PNG dos badges do Shields.io com ícones Simple Icons; grammY usa o ícone do Telegram, Baileys o do WhatsApp e SQL o do MySQL.
