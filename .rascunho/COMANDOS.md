# Comandos possíveis

Registro dos comandos disponíveis neste conjunto de fluxos. Fontes: `.claude/skills/fluxo/SKILL.md`, `.claude/CLAUDE.md` e os cabeçalhos de `.claude/scripts/`.

## Comandos na conversa (`/`)

| Comando | O que faz | Quando usar |
|---|---|---|
| `/fluxo` | Abre o menu em dois cliques (categoria, depois fluxo); retoma o trabalho gravado em `.specs/STATE.md` | Começar ou retomar qualquer trabalho |
| `/fluxo <atalho ou número>` | Vai direto ao fluxo (ex.: `/fluxo bug`, `/fluxo 12`) | Quando já se sabe o fluxo |
| `/progresso` | Mostra tarefas concluídas e faltantes, com percentual, no item atual e no projeto (ex.: "Faltam 45 de 180 tarefas: 75% concluído") | A qualquer momento; também aparece no fim de cada fase e ao retomar a sessão |
| `/atualizacoes` | Verifica e, com aprovação, aplica atualizações das dependências de `.claude/fontes.json` | Aviso de início de sessão ou antes de um projeto novo |
| `/model opus` · `/model sonnet` | Troca o modelo da sessão | Planejamento no Opus; da preparação em diante no Sonnet |
| `/clear` | Limpa a conversa; depois `/fluxo` retoma pelos arquivos | Marcos de troca de sessão |

## Atalhos do `/fluxo`

| # | Fluxo | Atalhos |
|---|---|---|
| 1 | Projeto novo para vender | `novo`, `projeto`, `produto`, `ideia` |
| 2 | Aplicação para uso próprio | `pessoal`, `uso-proprio` |
| 3 | Feature em projeto feito com IA | `feature` |
| 4 | Feature em projeto legado | `legado` |
| 5 | Performance e escala | `performance`, `lento` |
| 6 | Integração com terceiros | `integracao`, `api` |
| 7 | Redesign de interface | `redesign`, `visual` |
| 8 | Aprendizado | `estudo`, `aprender`, `aprendizado` |
| 9 | Investigação de incidentes | `incidente`, `caiu` |
| 10 | Sugestão de melhoria de terceiros | `sugestao` |
| 11 | Solicitação de feature sob demanda | `pedido`, `solicitacao` |
| 12 | Correção de bug | `bug`, `erro` |
| 13 | Refatoração e dívida técnica | `refatorar`, `divida` |
| 14 | Documentar projeto existente | `documentar`, `docs` |
| 16 | Auditoria de segurança | `seguranca`, `auditoria` |
| 17 | Prova de conceito (spike) | `spike`, `poc` |
| 24 | Revisão de código | `revisao`, `review` |
| 25 | Escolha de tecnologia | `tecnologia`, `stack` |
| 27 | Avaliação de projeto de terceiros | `avaliar`, `terceiros` |
| 30 | Automação de processo | `automacao`, `automatizar` |
| 32 | Suporte ao cliente | `suporte`, `atendimento` |

## Scripts (`python .claude/scripts/...`)

| Comando | O que faz |
|---|---|
| `python .claude/scripts/progresso.py [--item PASTA] [--json]` | Conta as tarefas dos `tasks.md` de `.specs/` e mostra o percentual concluído; só lê |
| `python .claude/scripts/trava-testes.py --rodar` | Roda a suíte (comando de `.specs/projeto/testes.json`) e registra o resultado; exigido antes de integrar ou implantar |
| `python .claude/scripts/instalar.py <pasta>` | Leva a `.claude` para outro projeto |
| `python .claude/scripts/instalar.py <pasta> --atualizar` | Traz a versão nova dos fluxos, preservando o que o projeto mudou (`--simular` mostra antes) |
| `python .claude/scripts/instalar.py <pasta> --local` | Para repositório de terceiros: não sobrescreve nada, usa `CLAUDE.local.md` e `.claude/settings.local.json`, e registra em `.git/info/exclude` |
| `python .claude/scripts/verificar-atualizacoes.py` | Lê `fontes.json` e confere as atualizações; usar depois de mexer nele |
| `python .claude/scripts/checar-tokens.py <pasta ou arquivo>...` | Acha cores e fontes fora do `tokens.css` no código de interface (`--permitir` libera arquivos) |
| `python .claude/scripts/varredura-seguranca.py ferramentas --saida DIR` | Varredura de dependências, segredos no histórico e análise estática (usado na auditoria de segurança; há outros subcomandos para o teste ativo) |
| `python .claude/scripts/propriedade-git.py --repo <cópia> --saida <pasta>` | Fator ônibus e atividade pelo histórico do git (avaliação de terceiros) |
| `node .claude/scripts/comparar-visual.mjs` | Compara, tela a tela, o mockup aprovado com a aplicação rodando (`--so-app` captura só a aplicação) |

## Observações

- Os fluxos também podem ser acionados pelo nome da skill (ex.: `bug`, `feature`), mas o ponto de entrada recomendado é `/fluxo`.
- Os scripts `varredura-seguranca.py`, `propriedade-git.py` e `comparar-visual.mjs` têm mais opções; veja o cabeçalho de cada um.
- Hook: `git push`, `gh pr create` e `git merge <branch>` são bloqueados sem a suíte verde registrada no commit.
