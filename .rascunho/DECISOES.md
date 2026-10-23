# Decisões do desenho da nova .claude

Registro passo a passo das decisões tomadas ao transformar os fluxos de `.rascunho` em skills. Objetivo geral: **fluxos rápidos e econômicos**, usando pacotes prontos sempre que possível e uma camada própria fina.

---

## Passo 1: espinha do fluxo 1 (spec-kit versus tlc-spec-driven)

**Status:** aprovado em 2026-10-23.

### O que foi lido

- `.tlc/.../tlc-spec-driven/SKILL.md` e a regra de modelos em `references/sub-agents.md`
- `.speckit/templates/commands/specify.md` (amostra do núcleo do spec-kit)
- `.speckit/extensions/assess/README.md` (extensão de avaliação de ideia)

### Comparação

| Critério | spec-kit (núcleo) | tlc-spec-driven | spec-kit `assess` |
|---|---|---|---|
| Cobre no fluxo 1 | Fases 6 a 9 (especificar, planejar, tarefas, implementar) | Fases 6 a 10 (especificar, desenhar, tarefas, executar, verificar) | Fases 1 a 3 e parte da 5 (ideia, pesquisa, problema, solução, decisão) |
| Economia de contexto | Baixa: cada comando carrega dezenas de linhas de regras de hooks, além de constituição, checklists e templates | Alta: meta de menos de 40 mil tokens, carrega referências sob demanda | Média: 5 comandos de cerca de 100 linhas |
| Rapidez | Fluxo fixo: sempre passa por todas as etapas | **Dimensiona sozinho**: tarefa pequena pula desenho e tarefas | Funil: a maioria das ideias para cedo, de propósito |
| Escolha de modelo | Não trata | **Tabela de modelo por papel** (desenho e domínio: forte; mecânico: barato; verificador: médio-alto) | Não trata |
| Garantias mecânicas | Checklist feito pela própria IA | **Scripts Python** validam spec, tarefas, commits e veredito final | Não tem |
| Verificação | Comando `analyze` e `converge` | **Verificador independente** (quem escreve não verifica), com injeção de falhas para testar os testes | Não se aplica |
| Instalação | CLI `specify` (Python 3.11+ e `uv`), cria `.specify/` e `specs/` | Uma skill: `npx @tech-leads-club/agent-skills install --skill tlc-spec-driven --agent claude-code` | Extensão do spec-kit, depende do CLI |
| Licença | MIT | CC-BY-4.0 | MIT |

### Proposta

1. **Entrega (fases 6 a 10): `tlc-spec-driven` como pacote instalado.** É o que melhor atende "rápido e econômico": dimensiona a profundidade pelo tamanho da tarefa, controla contexto e já sugere modelo por papel.
2. **Descoberta (fases 1 a 3 e 5): adaptar a estrutura do `assess` do spec-kit numa skill própria**, sem instalar o spec-kit inteiro. Instalar exigiria o CLI e a estrutura `.specify/` só para usar 5 comandos. A licença MIT permite reaproveitar com atribuição. Ganhamos o funil (intake, pesquisa, problema, forma, decisão) e acrescentamos o que ele não tem: viabilidade técnica e plano comercial.
3. **Superpowers como disciplina pontual**, sem duplicar o que o `tlc-spec-driven` já faz: `brainstorming` (ideia), `systematic-debugging` (bug), `using-git-worktrees` e `finishing-a-development-branch` (integração). TDD e verificação ficam com o `tlc-spec-driven`, que já os exige.
4. **Núcleo do spec-kit fica como referência**, não como dependência. Concorre com o `tlc-spec-driven` e pesa mais.

### Riscos

- `tlc-spec-driven` cria a pasta `.specs/` no projeto e escreve em inglês. Nossos fluxos precisam aceitar essa estrutura.
- Superpowers instalado impõe a skill `using-superpowers` em toda sessão. Precisamos decidir se ela fica ativa ou se nossos fluxos chamam as skills dele só quando precisam.
- O `assess` adaptado deixa de receber atualizações do spec-kit. Aceitável: são 5 comandos estáveis.

---

## Passo 2: política de modelos

**Status:** aprovado em 2026-10-23, com duas decisões:

1. Verificador independente em **Sonnet** (effort high).
2. Troca de modelo da sessão **manual** (`/model opus` nas fases 1 a 7, `/model sonnet` depois). As skills avisam quando trocar.

### O que a documentação garante (consultada em 2026-10-23)

| Peça | Fixa modelo? | Detalhe | Fonte |
|---|---|---|---|
| Agente (`.claude/agents/*.md`) | Sim, `model` e `effort` | `opus`, `sonnet`, `haiku`, ID completo ou `inherit`. É a forma garantida. | code.claude.com/docs/en/sub-agents.md |
| Skill na sessão principal | Só na resposta atual | O `model` da skill vale até o fim do turno; na próxima mensagem volta o modelo da sessão | code.claude.com/docs/en/skills.md |
| Skill com `context: fork` | Sim | Roda num subagente com o modelo escolhido, mas não vê a conversa e não dialoga com o usuário | code.claude.com/docs/en/skills.md |
| Chamada de agente | Sim, parâmetro `model` | Tem a maior prioridade: chamada, depois agente, depois `CLAUDE_CODE_SUBAGENT_MODEL`, depois sessão | code.claude.com/docs/en/model-config.md |
| Sessão | `/model`, `settings.json` ou `opusplan` | `opusplan` usa Opus no plan mode e Sonnet na execução | code.claude.com/docs/en/model-config.md |
| Hooks | Podem bloquear | `Stop`, `PreToolUse`, `UserPromptSubmit`, `SubagentStop` e outros, por código de saída 2 ou JSON | code.claude.com/docs/en/hooks.md |

### Regra geral

- **Conversa usa o modelo da sessão. Trabalho usa subagente com modelo fixo.**
- **Opus** onde o erro é caro e a decisão é difícil de desfazer: discovery, decisão de seguir, MVP, desenho, segurança.
- **Sonnet** como padrão de trabalho: pesquisa, especificação, tarefas, implementação, verificação.
- **Haiku** para o mecânico: busca e leitura de arquivos, rodar scripts de validação, formatar, commits, resumos de estado.
- **Effort** acompanha o modelo: `high` para decisão e verificação, `medium` para implementação, `low` para o mecânico.
- **Na dúvida, subir e não descer.** Um modelo fraco em lógica ambígua gera erro que custa mais para corrigir (regra do `tlc-spec-driven`).
- O verificador nunca fica no modelo mais barato.

### Modelo por fase do fluxo 1

| # | Fase | Onde roda | Modelo | Effort |
|---|---|---|---|---|
| 1 | Ideia | Sessão (conversa) | Opus | high |
| 2 | Discovery: pesquisa | Subagente | Sonnet | medium |
| 2 | Discovery: síntese e decisão | Sessão | Opus | high |
| 3 | Solução e valor | Sessão | Opus | high |
| 4 | Viabilidade técnica: spike | Subagente | Sonnet | medium |
| 4 | Viabilidade técnica: veredito | Sessão | Opus | high |
| 5 | Viabilidade de negócio: levantamento de concorrentes e preços | Subagente | Sonnet | medium |
| 5 | Viabilidade de negócio: conta e decisão | Sessão | Opus | high |
| 6 | MVP (especificação) | Sessão | Opus | high |
| 7 | Desenho | Sessão | Opus | high |
| 8 | Preparação: quebra em tarefas | Sessão | Sonnet | high |
| 8 | Preparação: repositório, CI/CD, esqueleto | Subagente | Sonnet | medium |
| 9 | Construção: tarefa mecânica (CRUD, configuração, ligações) | Subagente | Sonnet | low |
| 9 | Construção: tarefa de domínio ou ambígua | Subagente | Opus | medium |
| 10 | Validação: verificador independente | Subagente | Sonnet | high |
| 10 | Validação: auditoria de segurança | Subagente | Opus | high |
| 11 | Lançamento | Sessão | Sonnet | medium |
| 12 | Operação e aprendizado | Sessão | Sonnet | medium |
| — | Busca e leitura de código, rodar validadores, commits | Subagente | Haiku | low |

### Como aplicar na prática

- **Sessão:** padrão Sonnet em `settings.json`. As skills das fases 1 a 7 declaram `model: opus`, que vale para o primeiro turno, e avisam no início: "esta fase rende melhor em Opus; use `/model opus` durante a conversa". Ao terminar a fase, a skill lembra de voltar ao Sonnet.
- **Subagentes:** agentes próprios com `model` e `effort` fixos (ex.: pesquisador Sonnet, leitor de código Haiku, verificador Sonnet high, auditor Opus).
- **Sem variável global forçada.** `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` anularia a escolha por fase.

---

## Passo 3: estrutura da .claude para o fluxo 1

**Status:** aprovado em 2026-10-23, com as decisões:

1. **Projeto primeiro, plugin depois:** montar e testar na `.claude` do Rascunho; empacotar como plugin quando estável.
2. **Superpowers continua ativo.** A própria skill `using-superpowers` diz que instruções do usuário (CLAUDE.md) têm precedência sobre ela. O `CLAUDE.md` define que o fluxo comanda e em que pontos chamar cada skill do superpowers.
3. **Tudo em português**, inclusive os artefatos gerados pelo `tlc-spec-driven` (instrução no `CLAUDE.md`).

---

## Passo 4: conteúdo de cada peça

**Status:** aprovado em 2026-10-23. Detalhe em [DESENHO-FLUXO-1.md](DESENHO-FLUXO-1.md).

**Plano comercial (fase 5) é opcional.** O orquestrador pergunta se a fase será feita; se pulada, `decisao.md` registra "viabilidade comercial: não avaliada" e o veredito não depende dela.

Acréscimo: **verificação de atualizações** (peça 11), aprovada em 2026-10-23 com aviso **automático** semanal (hook `SessionStart`) e script em **Python**. Verificar é automático; atualizar é sempre decisão do usuário; código adaptado nunca é sobrescrito.

### Construção (registro)

- **Etapa 1:** `.claude/CLAUDE.md` e `.claude/settings.json` criados.
- **Etapa 2:** `tlc-spec-driven` 3.3.0 instalado por cópia em `.claude/skills/tlc-spec-driven/`. O lockfile do CLI fica em `.agents/.skill-lock.json` (precisa ir para o git). O pacote publicado está um commit atrás do GitHub (correção de exemplo em `sub-agents.md`, sem impacto). Achado: o superpowers instalado é o 6.3.0 e já existe o 7.0.1; as quatro skills citadas no `CLAUDE.md` continuam existindo no 7.0.1.
- **Etapa 3:** verificação de atualizações pronta e testada. `.claude/fontes.json` (2 dependências + 9 clones), `.claude/scripts/verificar-atualizacoes.py` (2,4 s, consultas em paralelo; pacote pelo hash do registro na CDN, plugin pelas tags, adaptado pela API de comparação do GitHub, clone por `ls-remote`), hook `SessionStart` (só no início de sessão, a cada 7 dias) e skill `/atualizacoes`. `.gitignore` regravado sem BOM e com `.claude/.cache/`.
- **Etapa 4:** 6 agentes criados em `.claude/agents/` (40 a 56 linhas cada), com modelo, effort e ferramentas conforme o passo 2. Ajuste ao desenho: `verificador` e `auditor-seguranca` têm `Write`, restrito por instrução ao próprio relatório (`validation.md`, `seguranca.md`). Os agentes foram carregados nesta mesma sessão depois de alguns minutos; `leitor-codigo` (Haiku) testado com sucesso (32 s, formato correto).
- **Etapa 5:** skills `descoberta` (fases 1 a 3, `SKILL.md` + 4 referências + atribuição MIT) e `decisao`, adaptadas do `assess` do spec-kit (commit `27d14e2`), registradas como `adaptado` em `fontes.json`.
- **Rules (aprovado em 2026-10-23):** usar só rules com `paths`, para carregar instrução apenas quando relevante. Criadas `.claude/rules/artefatos.md` (`.specs/**`) e `.claude/rules/manutencao-claude.md` (`.claude/**`); o `CLAUDE.md` foi enxugado. Ressalva: plugins não levam rules; ao empacotar como plugin, o essencial precisa virar skill ou hook. Confirmado na prática: a rule `manutencao-claude.md` carregou sozinha ao escrever em `.claude/`.
- **Etapa 6:** skills `viabilidade-tecnica` (incertezas por dimensão, resolvidas por pesquisa, spike ou risco aceito; custo mensal; veredito) e `plano-comercial` (7 seções do legado, método de ponto de equilíbrio, checklist de consistência; opcional). `plano-comercial` registrado em `fontes.json` como adaptado de origem local congelada.
- **Etapa 7:** skills `projeto-novo` (orquestrador: fase pelos arquivos, aviso de modelo, peça por fase, aprovação; lacunas de esqueleto/CI e segurança tratadas nas fases 8 e 10) e `fluxo` (roteador com os 21 fluxos; só o 1 pronto).
- **Total:** 1.264 linhas nossas em `.claude` (sem contar o pacote do TLC); maior `SKILL.md` com 101 linhas. **Pendente:** teste de ponta a ponta numa sessão nova (agentes, hook `SessionStart`, fluxo com uma ideia pequena e real).
- **Commit local** `281183c` na branch `novo-fluxo-claude` (sem push). `.specs/` do teste em andamento ficou fora.

---

## Passo 5: mockup visual enxuto

**Status:** aprovado e construído em 2026-10-23.

O legado era pesado demais (toda tela × 4 estados × PC e celular, respostas da API no formato do contrato, comparação pixel a pixel com Playwright). Princípio da versão nova: **o resultado não sai diferente porque todas as telas usam as mesmas peças**, não porque todas foram desenhadas.

- **Aprovação em três passos:** 2 ou 3 direções de uma tela-chave → guia de estilo (`tokens.css`, componentes base, padrões de vazio / carregando / erro, tabela de contraste) → 2 ou 3 telas-chave em PC e celular. Galeria publicada como Artifact.
- **Fidelidade sem pixel a pixel:** a implementação copia `tokens.css`; `.claude/scripts/checar-tokens.py` acusa cores e fontes soltas (roda antes do commit e no CI; espaçamentos ficam de fora por gerarem ruído); na fase 10, prints do app ao lado do mockup para aceite visual do usuário.
- **Peças:** skill `mockup-visual` (fase 7 depois do Design do tlc; etapa 3 na fase 10), em `.specs/mockup/`; `projeto-novo`, `fases.md` e os dois implementadores atualizados; `fontes.json` com a origem no legado.

## Passo 6: perguntas sempre com opções

**Status:** pedido do usuário em 2026-10-23.

Toda pergunta ao usuário usa `AskUserQuestion`, inclusive aprovações e perguntas abertas (com respostas de exemplo e "Other"). Gravado no `CLAUDE.md` (seção "Perguntas"), na rule de manutenção, nas skills `fluxo`, `descoberta` e `plano-comercial`, e na memória do Claude.

Reforços aprovados (1, 2 e 3): a regra vale também dentro do `tlc-spec-driven` e de outras skills instaladas; pergunta aberta leva a opção "Ainda não sei" (vira `[A ESCLARECER]`) mais uma sugestão, e a resposta livre vai em "Other"; subagentes nunca perguntam: devolvem "Perguntas para o usuário" e a sessão principal pergunta. O hook de verificação (barrar pergunta só em texto) foi **recusado** por ora; fica como opção se a regra falhar na prática.

Mudança em relação ao passo 1: as skills `brainstorming`, `writing-plans`, `executing-plans` e `subagent-driven-development` do superpowers **não** entram no fluxo 1, porque duplicariam `descoberta` e `tlc-spec-driven`. Do superpowers ficam `systematic-debugging`, `using-git-worktrees`, `verification-before-completion` e `finishing-a-development-branch`.

### Situação das dependências

| Pacote | Situação | Onde fica |
|---|---|---|
| superpowers | Já instalado como plugin do usuário, versão 6.3.0 | `~/.claude/plugins/` (vale para todos os projetos) |
| tlc-spec-driven | A instalar com `npx @tech-leads-club/agent-skills install -s tlc-spec-driven -a claude-code` | Projeto (`.claude/skills/tlc-spec-driven/`), por cópia, com lockfile; atualiza com `agent-skills update` |

### Árvore proposta

```
.claude/
  CLAUDE.md                     regras comuns: aprovação humana a cada fase, português,
                                política de modelos, onde ficam os artefatos
  settings.json                 model: sonnet; permissões
  skills/
    fluxo/                      roteador: pergunta o que você quer fazer e aciona o fluxo certo
    projeto-novo/               orquestrador do fluxo 1: estado atual, próxima fase,
                                aviso de troca de modelo, ponto de aprovação
      references/fases.md       as 12 fases, decisão e critério de passagem de cada uma
    descoberta/                 fases 1, 2 e 3 (adaptado do assess do spec-kit, MIT)
      references/               ideia.md, pesquisa.md, problema.md, solucao.md
    viabilidade-tecnica/        fase 4: riscos, spike, veredito
    plano-comercial/            fase 5: preço, canais, concorrentes, ponto de equilíbrio
                                (reaproveita ideias do agente dono do .claude_legado)
    decisao/                    fecha as fases 1 a 5: seguir, esclarecer ou matar,
                                e entrega ao tlc-spec-driven
    tlc-spec-driven/            PACOTE (fases 6 a 10), não editar
  agents/
    pesquisador.md              Sonnet, medium: pesquisa web, concorrentes, evidências
    leitor-codigo.md            Haiku, low: busca e leitura de código e documentos
    implementador.md            Sonnet, low: tarefa mecânica
    implementador-dominio.md    Opus, medium: tarefa de domínio ou ambígua
    verificador.md              Sonnet, high: verificação independente (quem escreve não verifica)
    auditor-seguranca.md        Opus, high: auditoria de segurança
```

### Onde ficam os artefatos de cada projeto

Uma pasta só, a mesma que o `tlc-spec-driven` já usa, para um fluxo ler o que o outro escreveu:

```
.specs/
  STATE.md                      decisões e ponto de retomada (formato do tlc-spec-driven)
  produto/                      fases 1 a 5 (nossas skills)
    ideia.md
    pesquisa.md
    problema.md
    solucao.md
    viabilidade-tecnica.md
    plano-comercial.md
    decisao.md                  veredito final; com "seguir", vira a entrada do MVP
  features/                     fases 6 a 10 (tlc-spec-driven)
```

### Fases sem dona ainda

- 11 (lançamento) e 12 (operação): ficam para depois do fluxo 1 funcionar até a fase 10.

### Pontos em aberto

1. **Projeto ou usuário?** Proposta: montar e testar no Rascunho (`.claude` do projeto) e, quando estável, empacotar como plugin para usar em qualquer projeto.
2. **Hook do superpowers.** Ele injeta `using-superpowers` em toda sessão, mandando invocar skill antes de qualquer resposta. Pode disputar com o orquestrador. Opções: manter (as skills dele ajudam), ou desativar o plugin neste projeto e chamar as skills dele só quando o fluxo mandar.
3. **Idioma dos artefatos.** O `tlc-spec-driven` gera em inglês por padrão. Nossas skills geram em português. Dá para instruir no `CLAUDE.md` que os artefatos saiam em português.
