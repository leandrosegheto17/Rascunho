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

## Passo 7: primeiro teste real (fases 1 a 5 e decisão)

**Status:** concluído em 2026-10-23 com a ideia "registro compartilhado de cuidados entre familiares".

- **Resultado:** 14 minutos, 7 artefatos (462 linhas). Experiência do usuário: "fluiu bem". Veredito das notas: esclarecer (evidência e viabilidade comercial fracas); o usuário escolheu seguir mesmo assim, e a sessão registrou bem a escolha e as consequências. Conta do ponto de equilíbrio conferida.
- **Achados:** (1) pesquisa baseada em resumos de busca, sem abrir as páginas, com um link cortado; (2) "seguir contra o parecer" não estava previsto na skill `decisao` e foi improvisado; (3) validações pendentes ficavam só em texto, sem mecanismo para não serem esquecidas.
- **Ajustes aprovados:** 2 e 3. `decisao` agora prevê a decisão do usuário contra o parecer e cria a tabela "Validações pendentes", cada uma condição para construção, lançamento ou nenhuma. `projeto-novo` lembra as pendências a cada fase e bloqueia as fases 9 e 11 enquanto houver condição em aberto. O ajuste 1 (pesquisador abrir as fontes primárias) foi **recusado** por ora.

---

## Conclusão desta rodada (2026-10-23)

Teste encerrado por escolha do usuário. A sessão de teste chegou a gerar a spec do MVP (fase 6, `tlc-spec-driven`): `spec.md` com 9 histórias e 61 critérios EARS, títulos de seção em inglês (exigidos pelo validador) e conteúdo em português; `validate_spec.py` passou sem erros nem avisos. Artefatos arquivados em `.rascunho/teste-1-cuidados/` (removidos na limpeza de 2026-10-23; recuperáveis pelo histórico do git, commit anterior a essa limpeza). Branch `novo-fluxo-claude` juntada na `main` local (sem push).

**Pronto e testado:** fases 1 a 5 e decisão do fluxo 1 (skills `fluxo`, `projeto-novo`, `descoberta`, `viabilidade-tecnica`, `plano-comercial`, `decisao`), agentes (`leitor-codigo` testado isoladamente; `pesquisador` usado no teste), rules por `paths`, perguntas com opções, verificação de atualizações (script, skill e hook simulado).

**Pronto, ainda sem uso real:** fases 6 a 10 (`tlc-spec-driven` com nossos agentes `implementador`, `implementador-dominio`, `verificador`, `auditor-seguranca`), `mockup-visual` e `checar-tokens.py` (testado com arquivos de exemplo).

**Pendências para a próxima rodada:**

1. Testar as fases 6 a 10 de ponta a ponta (primeiro uso real do `tlc-spec-driven`, do mockup e dos agentes de construção e verificação).
2. Confirmar o hook `SessionStart` numa sessão aberta do zero.
3. Peças das fases 11 (lançamento) e 12 (operação).
4. Os outros 20 fluxos do catálogo, reaproveitando as peças do fluxo 1.
5. Atualizar o superpowers de 6.3.0 para 7.x (decisão do usuário, via `/plugin`).
6. Empacotar como plugin quando estável (rules precisam virar skill ou hook).
7. Opcionais recusados por ora: pesquisador abrir fontes primárias; hook que barra pergunta só em texto.

---

## Passo 8: menu do `/fluxo`

**Status:** aprovado e testado em 2026-10-23. `/fluxo` abre direto um menu em dois cliques (4 categorias, depois o fluxo; categorias com mais de 4 fluxos têm "Mais opções"), e aceita atalho por nome ou número (`/fluxo bug`, `/fluxo 12`). Motivo: com 21 fluxos, ninguém decora os nomes.

## Passo 9: fluxo 2, aplicação para uso próprio

**Status:** construído em 2026-10-23.

Decisões do usuário: **só ele usa** (sem login complexo); **Opus no planejamento** (fases 1 a 4) e Sonnet depois, como no fluxo 1; fases 1 a 3 num **único artefato com uma aprovação**; implantação **local com Docker ou nuvem gratuita, decidida por projeto**.

| Fases | Peça | Origem |
|---|---|---|
| 1 a 3 | skill `necessidade` → `.specs/produto/necessidade.md` (pesquisa de alternativas prontas pelo `pesquisador`; veredito construir / adaptar algo pronto / desistir) | nova |
| 4 a 7 | `tlc-spec-driven` + agentes; backup, restauração testada e (se na internet) autenticação e HTTPS viram critérios de aceite; `auditor-seguranca` só com exposição pela internet | reaproveitada |
| 8 | skill `implantacao` → `.specs/implantacao.md` (docker compose ou nuvem gratuita com limites conferidos na hora; publicar na nuvem exige confirmação) | nova; serve também para a fase 11 do fluxo 1 |
| 9 | checklist de revisão periódica em `uso-proprio/references/fases.md` | nova |

Orquestrador: skill `uso-proprio`. `/fluxo` marca o fluxo 2 como pronto. **Pendente:** teste real com uma ferramenta pessoal.

## Passo 10: fluxo 3, feature em projeto existente feito com IA

**Status:** construído em 2026-10-23.

Decisões do usuário: **Opus no pedido e no plano** (fases 1 e 3), reconhecimento no `leitor-codigo` (Haiku), resto em Sonnet; verificação com o `verificador` **e o `/code-review`** no diff; forma de integrar **perguntada a cada feature** (merge local, PR ou manter a branch).

| Fases | Peça | Origem |
|---|---|---|
| 1 Pedido | `tlc-spec-driven` (Specify) | reaproveitada |
| 2 Reconhecimento | skills `inventario` (projeto, uma vez, atualizado por diff) e `reconhecimento` (feature: onde entra, tabela reaproveitar / estender / criar, convenções, testes, riscos, escalonamento por arquitetura) | novas |
| 3 Plano | `tlc-spec-driven` (Design e Tasks), seguindo a tabela de reaproveitamento | reaproveitada |
| 4 Rede de proteção | skill `rede-de-protecao` (linha de base, falhas preexistentes, testes de caracterização em commit separado) | nova; serve aos fluxos de legado, refatoração e bug |
| 5 Implementação | `tlc-spec-driven` (Execute) em branch `feature/<nome>` | reaproveitada |
| 6 Verificação | `verificador` + `code-review`; `auditor-seguranca` se tocar login, permissões, pagamento ou dados pessoais | reaproveitada |
| 7 Integração | checagem final de testes, atualização do contexto do projeto, `finishing-a-development-branch`, `integracao.md` | reaproveitada |

**Pedido do usuário durante a construção:** em projeto feito por outra pessoa, sempre avaliar o que já existe para reaproveitar. Resolvido com o inventário do projeto e o passo obrigatório de reaproveitamento no reconhecimento (peça nova exige justificativa; biblioteca nova só se nenhuma instalada resolver).

## Passo 11: testes inegociáveis

**Status:** pedido do usuário em 2026-10-23 ("sempre temos que garantir os testes").

Seção "Testes (inegociável)" no `CLAUDE.md`, válida para todos os fluxos (exceto spike e aprendizado): toda mudança de comportamento com teste que falharia sem ela; testes nascem do critério de aceite; nunca apagar, pular ou enfraquecer teste (mudar teste existente exige motivo e aprovação); projeto sem testes começa criando a infraestrutura; **checagem final da suíte inteira, executada de verdade e com resultado mostrado, antes de integrar ou implantar**; CI obrigatório. A checagem final foi ligada em `feature` (fase 7), `implantacao` e `projeto-novo` (fase 10).

**Trava técnica (aprovada):** `.claude/scripts/trava-testes.py` + hook `PreToolUse` no Bash. `--rodar` executa a suíte de `.specs/projeto/testes.json` e registra o commit como verde (`.claude/.cache/suite-verde.json`). O hook bloqueia `git push` e `gh pr create` com suíte falhando (roda na hora se o commit não estiver verde) e `git merge <branch>` se o último commit da branch não estiver verde (no merge o hook roda antes, com a branch de destino checada, por isso o registro de commits verdes). Sem `testes.json`, bloqueia e manda rodar o `inventario`; projeto sem testes de propósito registra `dispensado` com motivo, só com aprovação. Testado em repositório descartável: 9 casos corretos; corrigida a codificação das mensagens de bloqueio. Ao entrar em vigor nesta sessão, bloqueou dois comandos que só mencionavam "git push" em texto; a regra passou a exigir que o comando esteja no início ou depois de `;`, `&&`, `|` ou `(`.

**Testes do próprio Rascunho (escolha do usuário: criar, não dispensar):** 26 testes `unittest` em `.claude/scripts/testes/` para `checar-tokens`, `verificar-atualizacoes` e `trava-testes`; `.specs/projeto/testes.json` aponta para eles. Primeira checagem final pela trava: verde.

## Passo 12: fluxo 4, feature em legado

**Status:** construído em 2026-10-23.

Decisões do usuário: **Opus em pedido, arqueologia e plano** (fases 1, 2-3 e 5); staging **perguntado a cada projeto**; a skill de liberação é **uma peça só**, usada também na fase 11 do projeto novo.

| Fases | Peça | Origem |
|---|---|---|
| 1 Pedido | `tlc-spec-driven` (Specify) | reaproveitada |
| 2-3 Arqueologia | `inventario` + `reconhecimento` + skill **`arqueologia`** (ambiente roda?, histórico do git, comportamento observado, conhecimento de pessoas, costuras e ponto único de integração, raio de impacto, staging e flag, saída de emergência) | nova por cima das existentes |
| 4 Rede de proteção | `rede-de-protecao`, caracterizando todo o raio de impacto | reaproveitada |
| 5 Plano | `tlc-spec-driven`, código novo ao lado do antigo | reaproveitada |
| 6-7 | Execute, `verificador`, `code-review`, `auditor-seguranca` condicional, fluxos vizinhos testados | reaproveitadas |
| 8 Liberação | checagem final, integração, skill **`liberacao`** (plano com flag ou gradual, staging, pausa antes de produção, monitoramento, critério de parada, reversão testada; `.specs/liberacao.md`) | nova; também é a fase 11 do fluxo 1 |
| 9 Registro | contexto do projeto com armadilhas e costuras, inventário e `integracao.md` | ampliado do fluxo 3 |

Orquestrador: skill `legado`. Fluxo 1 passou a ter a fase 11; resta a 12.

## Passo 13: fluxo 12, correção de bug

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `feature` e `legado`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/bugs/<slug>/`**: `relato.md` (fases 1-2), `reconhecimento.md`, `causa.md` (fases 3 a 6, com campos de estado `Reproduzido`, `Teste vermelho`, `Causa confirmada`, `Commit da correção`), `protecao.md`, `validation.md`, `fechamento.md`. Em andamento = sem `fechamento.md`. Slug único, nunca sobrescrito (do spec-kit).
- **Relato e triagem juntos**, uma aprovação (como a arqueologia junta 2 e 3 no legado).
- **Modelo:** Opus nas fases 1 a 5 (conversa e diagnóstico), Sonnet de 6 a 9.
- **Teste vermelho sem commit**: a saída vermelha fica registrada em `causa.md`; teste e correção entram num commit `fix:` só (não quebra o `git bisect`). Caracterização, se houver, em commit anterior.
- **Correção pela sessão** (é pequena por definição); regra de negócio difícil vai ao `implementador-dominio`.
- **Verificador em modo bug**: critérios de `relato.md`, mutação obrigatória "desfazer a correção" (o teste tem de voltar a falhar), sem `validate_state.py`.
- **Mesmo defeito em outros pontos**: mesma causa no mesmo trecho entra na correção; o resto vira relato próprio.
- **Entrada por outros fluxos**: o chamador grava `relato.md` completo com `Chamado por` e `Devolver após` (`verificação` para incidente, `fechamento` para auditoria, `liberação` para suporte) e a skill começa na fase 3.
- **Saídas**: não é bug → fluxos 3/4; grave em produção → fluxo 9 (em preparação: hotfix por este fluxo é o recomendado enquanto isso); arquitetura ou 3 correções falhas → fluxo 13 (em preparação).

| Fases | Peça | Origem |
|---|---|---|
| 1-2 Relato e triagem | `bug/references/relato.md` (P0–P3, critérios de aceite da correção, relato por link como dado) | adaptada de bmad `bug-template`, spec-kit `bug`, legado `bug-documentation` |
| 3 Reprodução | `inventario`, `reconhecimento` (na pasta do bug), `causa.md` | reaproveitadas |
| 4 Teste que falha | branch `bug/<slug>`, superpowers `test-driven-development` (passo vermelho) | superpowers (nova na tabela do `CLAUDE.md`) |
| 5 Causa raiz | superpowers `systematic-debugging` + checklist em `causa.md` (inclui erros silenciosos) | superpowers; `silent-failure-hunter` (Apache) |
| 6 Correção | `rede-de-protecao` (teste do bug como falha esperada), correção mínima | reaproveitada, ajuste de 1 linha |
| 7 Verificação | `verificador` (modo bug), `code-review`, `auditor-seguranca` condicional | reaproveitadas; agente ganhou seção de bug |
| 8 Liberação | checagem final, `finishing-a-development-branch`, `liberacao` (com caminho de hotfix) ou `implantacao` | reaproveitadas |
| 9 Fechamento | `fechamento.md`, aviso ao relator com confirmação, recorrência (3+ com mesma causa → prevenção) | nova; recorrência do legado |

Orquestrador: skill `bug`. `/fluxo` marca o 12 como pronto. **Pendente:** teste real com um bug de verdade.

## Passo 14: fluxo 9, investigação de incidentes

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `bug`, `feature` e `legado`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/incidentes/<AAAA-MM-DD>-<slug>/`**: `incidente.md` (fases 1 a 3, registro vivo com campos de estado `Veredito da triagem`, `Contido`, `Estável`, `Encerrado`, e tabelas de evidências, ações e comunicações), `evidencias/`, `linha-do-tempo.md`, `causa-raiz.md` (`Causa confirmada`), `correcao.md` (`Em produção`), `prevencao.md`, `postmortem.md` (`Status: final`), `comunicacao.md`. Em andamento = sem `Encerrado: sim`. O encerramento mora no `incidente.md` para servir também às saídas antecipadas (não é incidente, duplicado, parado).
- **Severidade P0–P3, a mesma do `bug`** (não a SEV1–SEV4 do wshobson): a triagem do incidente vira o `relato.md` do bug sem tradução. P3 não é incidente: vai para a skill `bug`.
- **Urgência nas fases 1 a 3:** sem pedido de troca de modelo (emergência não espera), perguntas curtas, registro enquanto age; aprovação de fase com rótulos da emergência (contido / outra medida / parar). **Cada ação em produção com confirmação específica** (o que, onde, como desfazer), separada da aprovação da fase. Fases 4, 5 e 7 em Opus; 6, 8 e 9 em Sonnet.
- **Evidências antes de mexer**, em minutos; se a cópia atrasar a contenção com dano grave em curso, pergunta-se. Evidência com dado pessoal ou segredo fica fora do git.
- **Código novo na restauração só pela skill `bug`** (hotfix): a regra de testes vale na emergência. Reverter, flag e reinício não precisam.
- **Caminho de segurança** (do desenho): isolar sem destruir, evidência forense, trocar credenciais, relógio da LGPD, só então restaurar; `auditor-seguranca` na causa raiz.
- **Correção definitiva (fase 6) pela skill `bug`**, com `relato.md` gravado pelo incidente (`Chamado por: incidente <id>`, `Devolver após: verificação`); o incidente faz checagem final, integração e `liberacao`. Comportamento novo vai a `feature`/`legado`; configuração com checagem automatizada; causa externa vai direto à prevenção. Vindo do `bug` ("grave em produção"), o incidente reusa a mesma pasta do bug.
- **Prevenção obrigatória** (ao menos uma ação de prevenção e uma de detecção, ou motivo), cada uma com responsável e prazo; alerta acionável com disparo testado (do `observability-setup` do legado). Runbook do projeto em `.specs/runbook.md`, criado ou atualizado quando o incidente mostrar a falta; consultado na triagem.
- **LGPD:** relógio iniciado na triagem (data e hora do conhecimento), porque o prazo de comunicação à ANPD é curto e não pode esperar a fase 9. Regra citada (LGPD art. 48, Resolução CD/ANPD nº 15/2024, 3 dias úteis) marcada `PREMISSA`, conferida pelo `pesquisador` na hora. A skill junta o material; a decisão é humana (controlador, encarregado, jurídico); operador avisa o cliente controlador. Incidente com LGPD em avaliação não se encerra.
- **Skill `bug` atualizada:** a saída "grave em produção" recomenda a skill `incidente`; hotfix direto só com o dano já contido.

| Fases | Peça | Origem |
|---|---|---|
| 1-3 Triagem, contenção, restauração | `incidente/references/resposta.md` (perguntas de triagem, P0–P3, classificação por sintoma, menu de medidas reversíveis, evidências, caminho de segurança, modelo de `incidente.md`); reversão pela `liberacao`; código novo pela `bug` | nova; adaptada do wshobson `incident-runbook-templates` (MIT) |
| 4 Linha do tempo | `references/analise.md` + `leitor-codigo` (git, deploys) | nova; técnica do bmad `codebase-historian` (MIT) |
| 5 Causa raiz | superpowers `systematic-debugging` + 5 porquês, gatilho × causa sistêmica, sem culpa; `pesquisador` (terceiros), `auditor-seguranca` (segurança) | reaproveitadas; wshobson `postmortem-writing` (MIT) |
| 6 Correção definitiva | skill `bug` (entra na fase 3, devolve após verificação), checagem final, `finishing-a-development-branch`, `liberacao`; `correcao.md` | reaproveitadas |
| 7 Prevenção | `references/postmortem.md` (prevenção, detecção, mitigação; runbook) | nova; wshobson + legado `observability-setup` |
| 8 Post-mortem | `references/postmortem.md` (sem culpa, completo ou curto) | adaptada do wshobson `postmortem-writing` (MIT) |
| 9 Comunicação | `references/comunicacao.md` (avisos durante e depois, LGPD/ANPD com avaliação humana) | nova; modelos de aviso do wshobson |

Orquestrador: skill `incidente`. `/fluxo` marca o 9 como pronto. **Pendente:** teste real (pode ser um simulado: derrubar uma aplicação de teste e percorrer as 9 fases) e revisão humana da seção de LGPD.

## Passo 15: fluxo 17, prova de conceito (spike)

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `bug`, `necessidade` e `viabilidade-tecnica`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/spikes/<slug>/`**: `spike.md` (fases 1-3, campos `Preparação aprovada`, `Início`, `Limite`, `Extensão`), `resultado.md` (fases 4-5, `Situação`), `registro.md` (fases 6-8, `Veredito`, `Confiança`, `Destino do código`). Em andamento = sem `Destino do código` preenchido. Saem de `.specs/produto/spikes/` (usado só pela viabilidade) para servir a qualquer fluxo.
- **Quatro aprovações para oito fases** (1-3, 4-5, 6-7, 8), como `necessidade` (1 a 3 num artefato) e `bug` (relato e triagem juntos): spike é curto e cada bloco produz um artefato só.
- **Modelo:** Opus em 1-3 (pergunta e critério) e 6-7 (veredito); Sonnet em 4-5 (experimento no `implementador`) e 8.
- **Prazo como decisão central:** relógio e número de tentativas (padrão 3, como as 3 correções falhas do `bug`), o que estourar primeiro; `Início` e `Limite` gravados ao despachar, conferidos pelo `implementador` com `date` e pela sessão a cada retomada. Estouro vira `resultado.md` com `prazo estourado` e segue para a conclusão. Extensão só por decisão do usuário, no máximo uma.
- **Critério congelado** na aprovação da preparação, com "deu certo", "deu errado", "inconclusivo" e "o resultado que provaria que não" (falsificação, do `the-fool`). Mudar o critério depois de ver o resultado invalida o spike.
- **Quem experimenta não dá o veredito:** o `implementador` devolve medições com o comando exato; a sessão reproduz a medição principal e compara com o critério (analogia com "quem escreve não verifica"). Confiança pela qualidade da evidência e explicações concorrentes.
- **Isolamento do código:** padrão `.specs/spikes/<slug>/codigo/`, fora do git (linha no `.gitignore` do projeto, com diff mostrado); quando precisa do código do projeto, worktree fora do repositório na branch `spike/<slug>`, nunca com merge, push ou PR (a trava de testes já bloqueia o merge). Os `.md` são versionados.
- **Descarte ou promoção:** descartar é o padrão (com confirmação do que será apagado). Promover = abrir o trabalho no fluxo que constrói, com `registro.md` como entrada e testes dos critérios de aceite; o código não é copiado e também é descartado. Trechos essenciais ficam como texto em `registro.md` ("não copiar: reescrever com testes"). Opção de manter fora do git até uma data.
- **Entrada por outros fluxos** (como o `bug`): o chamador grava `spike.md` com **Chamado por** e **Usar em**; a preparação completa o que falta numa confirmação (o prazo é sempre do usuário); a skill vai até a fase 8 e devolve veredito e confiança. Fluxo 25: um spike por finalista, critério e prazo idênticos. Fluxo 6: contrato no sandbox.
- **`viabilidade-tecnica` ajustada:** o caminho "spike" agora grava `spike.md` e aciona a skill `spike` (antes despachava o `implementador` direto); o modelo aponta para `.specs/spikes/<slug>/registro.md`. O **modo spike do `implementador`** passou a ter pasta padrão nova, controle de prazo por `date` e retorno com situação e comando da medição.
- `brainstorming` não é acionado (postura apenas, como dizia o levantamento): nada a registrar na tabela do `CLAUDE.md`.

| Fases | Peça | Origem |
|---|---|---|
| 1-3 Pergunta, critério e prazo | `spike/references/preparacao.md` (é spike? 4 motivos; pergunta sim/não ou número; critério falsificável; prazo em relógio e tentativas; modelo de `spike.md`, que é também o contrato de entrada); `pesquisador` quando a documentação responde | nova; bmad `spike-template` (MIT), legado `technical-spike-identification`, `the-fool` `evidence-audit` (CC-BY-4.0) |
| 4-5 Experimento e observação | agente `implementador` (modo spike) com o pedido de `references/experimento.md`; medição reproduzida pela sessão; `resultado.md` | reaproveitada, agente ajustado |
| 6-7 Conclusão e registro | `references/registro.md` (veredito, confiança, explicações concorrentes, riscos, trechos de referência), resposta levada ao **Usar em** | nova; `the-fool` e bmad |
| 8 Descarte ou promoção | `references/registro.md` (descartar, promover reescrevendo por `feature`/`legado`/`uso-proprio`/`projeto-novo`/chamador, ou manter até uma data) | nova |

Orquestrador: skill `spike`. `/fluxo` marca o 17 como pronto. **Pendente:** teste real com uma pergunta de verdade (ex.: limite de uma API gratuita) e, quando os fluxos 25 e 6 forem construídos, conferir o contrato de entrada.

## Passo 16: fluxo 25, escolha de tecnologia

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `spike`, `bug` e o `tlc-spec-driven`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/escolhas/<slug>/`**: `escolha.md` (fases 1-2 e estado: `Reversibilidade`, `Modo`, `Critérios aprovados`, `Decisão`, `Registro`, como o `incidente.md` concentra o estado) e `avaliacao.md` (fases 3 a 8: opções, eliminação, comparativo, `Finalistas`, `Teste prático`, riscos e saída, justificativa). Em andamento = sem `Registro`. Spikes em `.specs/spikes/<pergunta>-<finalista>/`, como a skill `spike` já previa.
- **Modo rigoroso ou enxuto pela reversibilidade** (do desenho: "reversibilidade pesa"; do tlc: só o difícil de reverter vira `AD-NNN`). Rigoroso: 3 a 5 opções, pesquisa em paralelo por opção, spike por finalista, ADR completo e `AD-NNN`. Enxuto: 2 a 3 opções, um pesquisador, sem spike, ADR leve, sem `AD-NNN`. A skill sugere; o usuário confirma. Na dúvida, rigoroso; dá para subir de modo no meio.
- **Blocos de aprovação** (como o `spike`): rigoroso 1-2, 3-5, 6, 7-8, 9; enxuto 1-2, 3-5, 7-9. Lista curta confirmada antes da pesquisa por opção (evita pesquisa paga à toa).
- **Modelo:** Opus em 1-5 e 7-8 (critérios, julgamento de evidência, decisão); Sonnet em 6 (a skill `spike` avisa por etapa) e 9 (registro). Enxuto pode seguir no modelo atual.
- **Critérios congelados** na aprovação das fases 1-2, antes de citar opções (favorita declarada fica anotada à parte); mudar exige motivo e aprovação, como o critério do spike.
- **Pesquisa no `pesquisador`**, que não pontua nem recomenda: a sessão dá as notas e o usuário escolhe. A sessão roda `date` e passa a data da consulta; toda evidência leva fonte e "consultado em" (o agente não tem relógio). Pedido com as 5 dimensões e os cuidados de frescor e de duas fontes do bmad.
- **Teste prático pela skill `spike`**: pergunta, critério e prazo combinados uma vez e copiados para cada `spike.md`; um spike de cada vez; prazo estourado de um finalista é dado da comparação. Sem ponto incerto relevante, dispensa com motivo.
- **Decisão do usuário** via `AskUserQuestion`, com a recomendação da sessão primeiro, fator decisivo nomeado e condição em que a escolha mudaria (do `build-vs-buy-analysis`). Empate: a mais simples e a mais reversível.
- **ADR:** pasta de ADR do projeto, se existir (convenção do projeto vence, como na `feature`); senão `.specs/decisoes/ADR-NNN-<slug>.md`. MADR adaptado em português (completo) ou frase "no contexto de..." (leve). Imutável: troca por ADR que substitui.
- **Compatível com o tlc sem duplicar:** o ADR é o registro completo; a entrada `AD-NNN` em `.specs/STATE.md` (formato do `memory.md` do tlc, só no rigoroso) é a restrição curta com o caminho do ADR. Chamada pelo Design do tlc, a entrada já existe e o `design.md` só a referencia. Substituição vale nos dois: ADR novo e `AD-NNN` novo com `superseded by`.
- **Entrada por outros fluxos** (como `bug` e `spike`): o chamador grava `escolha.md` com **Chamado por** e **Usar em**; as fases 1-2 viram uma confirmação (modo e critérios são do usuário); a skill vai até a fase 9 e devolve opção, ADR e `AD-NNN`. Chamadores: fluxo 1 (fase 7, stack), 6 (fornecedor), 30 (ferramenta).
- **Ajustes em peças existentes:** `projeto-novo` (fase 7 aciona a escolha para stack difícil de reverter), `viabilidade-tecnica` (a stack candidata fecha na fase 7 pela escolha), `spike/references/fases.md` (**Usar em** aponta para `avaliacao.md`).
- `the-jury` não entra (caro: 3 a 5 subagentes por decisão); só a ideia de pré-mortem nos riscos.

| Fases | Peça | Origem |
|---|---|---|
| 1-2 Decisão e critérios | `escolha-tecnologia/references/criterios.md` (decisão, reversibilidade e modo, eliminatórios, desejáveis com peso e requisito que motiva; modelo de `escolha.md`, que é também o contrato de entrada) | nova; legado `tech-stack-selection` |
| 3-5 Opções, eliminação, avaliação | agente `pesquisador` (panorama, depois um por opção em paralelo) com os pedidos de `references/avaliacao.md`; comparativo ponderado pela sessão | reaproveitada; bmad `deep-recon/types/technical.md` (MIT) |
| 6 Teste prático | skill `spike`, um por finalista, critério e prazo idênticos | reaproveitada |
| 7-8 Riscos, saída e decisão | `references/decisao.md` (dependência, custo de migrar, projeto morrer, plano B, pré-mortem; fator decisivo e condição de mudança) | nova; legado `build-vs-buy-analysis` |
| 9 Registro | `references/decisao.md` (ADR completo e leve, local, numeração, imutabilidade, `AD-NNN` do tlc) | adaptada do wshobson `architecture-decision-records` (MIT) e legado `adr-drafting` |

Orquestrador: skill `escolha-tecnologia`. `/fluxo` marca o 25 como pronto. **Pendente:** teste real com uma escolha de verdade (ex.: banco de um projeto do fluxo 1 na fase 7) e, quando os fluxos 6 e 30 forem construídos, conferir o contrato de entrada.

## Passo 17: fluxo 16, auditoria de segurança

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `bug`, `incidente` e `spike`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/seguranca/<AAAA-MM-DD>-<slug>/`**: `escopo.md` (fase 1, **Escopo aprovado**; também o contrato de entrada), `ameacas.md` (fases 2-3, **Ameaças aprovadas**), `achados.md` (fases 4 a 7, **Coleta**, **Teste ativo**, **Classificação aprovada**), `correcoes.md` (fase 8, **Críticos e altos fechados**), `relatorio.md` (fase 9, `Status: final` ou `parado`), `evidencias/` (saídas brutas, **fora do git**). Em andamento = sem `relatorio.md` final ou parado.
- **Aprovações:** 1, 2-3, 4-5, 6, 7, 8, 9. Ativos e ameaças juntos (como a arqueologia junta 2 e 3); varredura e revisão manual juntas (o mesmo agente coleta, sem decisão do usuário no meio). Escopo e classificação ficam sozinhos por serem decisões do usuário.
- **Modelo:** Opus em 1, 2-3 e 7 (autorização, modelo de ameaças, severidade); Sonnet em 4-5, 6, 8 e 9 (o `auditor-seguranca` roda em Opus de qualquer forma).
- **Escopo e autorização inegociáveis:** sistema que não é do usuário exige autorização por escrito (quem, quando, onde está o documento); terceiro só por cópia local do código publicado; sem autorização, `parado`. Teste ativo em local (padrão) ou staging autorizado; produção só com confirmação específica por teste. Lista fixa de proibições (negação de serviço, carga, força bruta, destrutivo, engenharia social, sistemas de terceiros, além da prova mínima). Invasão em curso ou dado vazado: pausa e skill `incidente`. Repositório público: pasta fora do git até fechar críticos e altos.
- **Modelo de ameaças pela sessão** (Opus, conversa com o usuário para confirmar premissas), com o resumo de segurança do repositório pelo `leitor-codigo`. Ameaças `TM-NNN`, STRIDE por elemento, prioridade por matriz 3 × 3, caminhos de foco que guiam a revisão manual.
- **Agente `auditor-seguranca` reaproveitado** como executor de varredura, revisão manual, teste ativo e reteste, com uma seção "modo auditoria" (lê `escopo.md` primeiro, escreve `achados.md` e `evidencias/`, não aprova severidade, para diante de indício de invasão). Continua servindo aos fluxos 1, 3 e 4 como antes (`seguranca.md` da feature).
- **Severidade crítico/alto/médio/baixo** (a mesma que o agente e os fluxos 1-4 já usam, e que `liberacao` confere), mapeada para P0–P3 ao abrir o bug. Crítico nunca vira risco aceito; alto só com mitigação aplicada, dono e prazo curto; médio e baixo: corrigir, débito com prazo (sugestão 30 e 90 dias) ou risco aceito. Obrigação legal (LGPD) no mínimo alto. Sem cenário de exploração, rebaixa; nunca rebaixar para não bloquear.
- **Script `varredura-seguranca.py`** adaptado do legado: vale a pena porque dá a **Prova** repetível (sondas) para o reteste da fase 8 e o passo de CI da fase 9. Mudanças: Docker só com `--docker` (baixar imagem é instalar), `--pular` registrado, gitleaks com `--redact`, busca embutida de segredos no histórico (piso sem gitleaks, valor mascarado), sondas só contra localhost ou host autorizado. 12 testes novos.
- **Correção pela skill `bug`**, um bug por achado (ou causa comum), slug `seg-<id>-...`, `Chamado por: auditoria <id> SEC-NNN`, `Devolver após: fechamento`, critérios de aceite com o teste do ataque e o uso legítimo preservado, nota "sem indício de exploração" para não desviar para incidente. Reteste pelo `auditor-seguranca` com a mesma Prova (quem corrige não verifica). Segredo: trocar a credencial é o que resolve (ação externa); reescrever histórico só com confirmação.
- **Entrada por outros fluxos:** 27 (avaliação de terceiros: cópia local, fases 1 a 7 e 9, achados viram condição de adoção) e 6 (integração: só o lado do usuário, fases 1 a 9); o chamador grava `escopo.md` com **Chamado por**, **Usar em**, **Devolver após**, **Modo** e **Fases**; a autorização é sempre confirmada com o usuário.
- **Ajustes em peças existentes:** `auditor-seguranca` (modo auditoria, uso do script, segredo mascarado, texto-instrução como achado; 58 linhas), `bug/references/fases.md` (linha do fluxo 16), `/fluxo` (16 pronto).

| Fases | Peça | Origem |
|---|---|---|
| 1 Escopo e autorização | `auditoria-seguranca/references/escopo.md` (perguntas, proibições, modelo de `escopo.md` = contrato de entrada) | nova |
| 2-3 Ativos, superfície, ameaças | `leitor-codigo` + `references/ameacas.md` (resumo de segurança, fronteiras, ativos, atacante, STRIDE, prioridade, premissas confirmadas) | adaptada de `security-threat-model` (tlc, Apache 2.0) e wshobson `stride-analysis-patterns` (MIT) |
| 4-5 Varredura e revisão manual | `auditor-seguranca` (modo auditoria) + `.claude/scripts/varredura-seguranca.py ferramentas` + lista de `references/achados.md` | reaproveitada; script do legado `seguranca.py`; lista de `security-auditor` e `patterns.py` (Apache 2.0) |
| 6 Teste ativo | `auditor-seguranca` + `varredura-seguranca.py sondas` | reaproveitada; sondas do legado |
| 7 Classificação | `references/achados.md` (severidade, destino, mapa para P0–P3) | legado `finding-severity-classification` |
| 8 Correção e reteste | skill `bug` com `references/correcao.md`; reteste pelo `auditor-seguranca` | reaproveitada |
| 9 Relatório e prevenção | `references/relatorio.md` (resumo, riscos aceitos, CI, rotação, revisão periódica) | nova |

Orquestrador: skill `auditoria-seguranca`. `/fluxo` marca o 16 como pronto. **Pendente:** teste real (ex.: uma aplicação de exemplo com uma falha de autorização plantada, percorrendo as 9 fases) e, quando os fluxos 27 e 6 forem construídos, conferir o contrato de entrada.

## Passo 18: fluxo 24, revisão de código

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `auditoria-seguranca`, `bug` e `feature`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/revisoes/<slug>/`**: `revisao.md` (fases 1-3: alvo com base e ponta revisada, pedido e critérios de aceite, tamanho, checagens; campos **Contexto aprovado** e **Checagens**; é também o contrato de entrada), `alegacoes.md` (descrição do PR e commits, sem análise), `achados.md` (fases 4-8, achados `REV-NNN`, **Análise**), `validation.md` (do `verificador`), `seguranca.md` (se despachado), `evidencias/` (fora do git), `retorno.md` (**Retorno entregue**), `decisao.md` (**Decisão**, rodadas). Em andamento = sem `decisao.md` com `aprovado`, `recusado`, `parado` ou `devolvido` (modo curto, ao chamador); `mudanças pedidas` espera o autor e volta como reteste. Atalho para o retorno curto (divisão pedida, checagem vermelha) marca as fases puladas como `dispensado`.
- **Aprovações:** 1-2, 3, 4-8, 9, 10. Contexto e tamanho juntos (a decisão de dividir sai do mesmo `git diff --stat`); checagens sozinhas porque vermelho é atalho para o retorno curto e rodar código de fora pede confirmação; as cinco lentes da análise juntas (os agentes rodam em paralelo, sem decisão do usuário no meio, como varredura e revisão manual na auditoria).
- **Modelo:** Opus em 1-2 (entender o pedido); Sonnet de 3 a 10 (verificação e registro; a decisão é do usuário, com regra clara: bloqueante aberto não recomenda aprovar).
- **Pedido antes do código; descrição do autor como alegação** (do `claims-check` do BMAD): a descrição do PR e os commits vão para `alegacoes.md` sem análise, e o agente só os lê depois de percorrer o código, para tentar falsificá-los.
- **Sem agente revisor novo.** `code-review` (skill da sessão, não editada) faz a caça a bugs da fase 4, sem `--comment` nem `--fix`. O **`verificador` ganhou um modo revisão** (casos limite, alegações, sensor de mutação, testes apagados, enfraquecidos ou que não contam): é verificação independente e já faz mutação numa cópia isolada, que é a melhor prova de "os testes falhariam se o código estivesse errado". `auditor-seguranca` condicional na fase 6 (agente aceita o caminho do relatório pelo pedido). Design e armadilhas de IA pela sessão, com `leitor-codigo` para achar duplicação e `pesquisador` para API de versão exata.
- **Teste enfraquecido, apagado, pulado ou que só repete a implementação é bloqueante** (regra inegociável do `CLAUDE.md`), aprovável só com motivo registrado e aceito pelo usuário.
- **Executar, não só ler:** checagens rodadas num worktree temporário fora do repositório (nunca trocando a branch do usuário; a suíte roda pelo comando de `testes.json` dentro do worktree, porque o `trava-testes.py` usa a pasta do projeto principal); cada critério de aceite exercitado. **Código de autor de fora da equipe só roda com confirmação específica**, depois de ler o diff atrás de script de instalação, rede ou escrita fora do projeto.
- **Retorno local por padrão**; comentar, aprovar ou pedir mudanças no GitHub são ações externas com confirmação específica e o texto exato mostrado.
- **Quem revisa não corrige:** o autor corrige; se é a IA do usuário, a correção volta ao fluxo de origem ou ao `implementador`, e o reteste revisa só o delta (`git diff <ponta anterior>..<nova>`, `range-diff` se o histórico foi reescrito), com a suíte inteira de novo. Três rodadas sem fechar os bloqueantes → escala.
- **Integrar não faz parte da revisão**; pedido pelo usuário depois de aprovar, segue checagem final e `finishing-a-development-branch`.
- **Entrada por outros fluxos** (como `auditoria-seguranca`): o chamador grava `revisao.md` com **Chamado por**, **Usar em**, **Devolver após**, **Modo** e **Fases**. Modo `curto` = fases 1-2 como confirmação, 3 dispensável, 4 a 8, devolve após `análise`; retorno e decisão ficam com o chamador. Fluxo 27: cópia local do terceiro, recorte de código revisado inteiro, sem a fase 6 (a auditoria é chamada à parte).
- **Fluxos 3 e 4 — aplicado:** a verificação troca o `code-review` direto pela `revisao-codigo` em modo curto (fases 4, 7 e 8; a 5 já é do `verificador` do fluxo), que continua acionando o `code-review` e acrescenta casos limite, armadilhas de IA e design. Aplicado como resposta recomendada (o usuário pediu para seguir as recomendadas); não contraria o passo 10, que só passa a ser executado por dentro da nova skill. Fluxo 12 mantém o `code-review` direto (correção pequena).

| Fases | Peça | Origem |
|---|---|---|
| 1-2 Contexto, tamanho e escopo | `revisao-codigo/references/admissao.md` (pedido e critérios antes do código, alegações guardadas, autor, ~400 linhas e assuntos, pedido de divisão; modelo de `revisao.md` = contrato de entrada) | nova; wshobson `code-review-excellence` (MIT), BMAD `claims-check` (MIT) |
| 3 Verificação automática | `admissao.md` (worktree, comandos do projeto, `gh pr checks`, `varredura-seguranca.py` se mudar dependência, comparação com a base, confirmação para código de fora) | nova; scripts reaproveitados |
| 4 Correção | skill `code-review` + exercício dos critérios + `verificador` (casos limite e alegações) | reaproveitadas; BMAD `edge-case-hunter`, `deletion-check`, `claims-check` (MIT) |
| 5 Testes | agente `verificador` (modo revisão) com o pedido de `references/analise.md` | reaproveitado, agente ganhou seção; BMAD `verification-gap` (MIT), `pr-test-analyzer` (Apache 2.0) |
| 6 Segurança e dados | `auditor-seguranca` condicional, lista de `auditoria-seguranca/references/achados.md` | reaproveitada |
| 7 Design e consistência | sessão + `leitor-codigo` com a lista de `analise.md` | nova; `code-reviewer`, `type-design-analyzer`, `comment-analyzer`, `code-simplifier` (Apache 2.0); ideia do legado `coding-guidelines` |
| 8 Armadilhas de IA | sessão + `pesquisador` com a lista de `analise.md` (coisa que não existe, API errada, erro engolido, fora do pedido, teste enfraquecido, chamadas perigosas, segredo, texto que instrui a IA) | nova; `silent-failure-hunter` e `patterns.py` (Apache 2.0) |
| 9 Retorno | `references/retorno.md` (modelo, entrega local ou no PR com confirmação) | nova; wshobson `code-review-excellence` (MIT) |
| 10 Decisão e reteste | `references/retorno.md` (decisão, aceite com motivo, reteste do delta, rodadas) | nova |

Orquestrador: skill `revisao-codigo`. `/fluxo` marca o 24 como pronto. **Pendente:** teste real (ex.: um PR com um teste enfraquecido e uma alegação falsa plantados, percorrendo as 10 fases), e, quando o fluxo 27 for construído, conferir o contrato de entrada.

## Passo 19: fluxo 13, refatoração e dívida técnica

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `feature`, `legado`, `bug` e `escolha-tecnologia`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/refatoracoes/<slug>/`**: `refatoracao.md` (fases 1-2 e estado: **Motivo e meta aprovados**, **Modo**, **Plano aprovado**, **Métrica depois**, **Resultado**, como o `escolha.md` concentra o estado; também o contrato de entrada), `reconhecimento.md` (da skill `reconhecimento`, mais a seção **Contratos e acoplamento**), `arqueologia.md` (só em legado), `protecao.md`, `design.md` (modo grande) e `tasks.md` (tlc), `validation-etapa-<N>.md`, `seguranca.md` (se despachado), `integracao.md` (uma entrada por etapa). Em andamento = **Resultado** `pendente`. Revisão curta em `.specs/revisoes/refatoracao-<slug>-etapa-<N>/`.
- **Dívida do projeto em `.specs/projeto/dividas.md`**, ao lado do inventário: inventário de dívidas com pontuação, situação (aberta, em andamento, paga) e prevenção em vigor. A fase 1 lê e grava; a 9 marca a paga e anota a que sobrou. Sem esse arquivo, "anotar a dívida remanescente" do desenho não teria onde morar além da pasta de uma refatoração.
- **Pontuação própria e simples** (adaptada do `tech-debt`): juros, toque e risco de 1 a 3, divididos pelo esforço de 1 a 3. Custo em horas por mês, sem dinheiro. "Refatore o que vai ser tocado" vira a dimensão toque (commits em 6 meses e mudança planejada).
- **Meta sem número não passa**: métrica medida antes, com comando ou contagem reproduzível, alvo e fora do escopo. Ferramenta de métrica não instalada não se instala sem confirmação.
- **Etapas como unidade de integração** (modo pequeno = uma etapa; grande = várias, cada uma com branch, verificação e integração próprias): resolve "PRs pequenos e frequentes" do desenho sem uma pasta por etapa. Etapa atual = primeira sem entrada em `integracao.md`; as fases 6 a 8 se repetem por etapa.
- **Modo pequeno ou grande** (como rigoroso ou enxuto na escolha de tecnologia): grande quando há muitos passos, várias partes, dados ou troca de framework, ou falta de testes possíveis no antigo; usa os padrões de estrangulamento do `legacy-migration-planner` (ramificar por abstração como padrão no mesmo deploy). Na dúvida, grande.
- **Rede antes do plano** (como no legado): a refatoração promete não mudar nada observável, então a caracterização cobre **todos os contratos** do mapeamento, não só o trecho dos passos. Sem rede verde, não começa; sem testes possíveis, saída de emergência (infraestrutura de testes como etapa 0, ou reescrita ao lado com execução paralela, ou parar).
- **Teste de caracterização quebrado = passo errado**: desfazer e refazer menor, nunca mudar o teste (regra do `CLAUDE.md`). Bug achado no caminho é anotado e vai para a skill `bug`, separado.
- **Modelo:** Opus em 1-2 e 5 (decisão e plano); Sonnet em 3, 4 e 6 a 9 (a `arqueologia` avisa Opus por conta própria).
- **Verificação:** `verificador` ganhou um **modo refatoração** (testes intactos, contratos iguais, sensor sobre o código refatorado, métrica e desempenho medidos de novo por quem não executou); depois, `revisao-codigo` em modo curto (fases 4, 7 e 8), como nos fluxos 3 e 4, com mudança de comportamento como bloqueante. `auditor-seguranca` condicional.
- **Integração:** checagem final por etapa; `liberacao` quando o trecho é crítico ou a troca é por flag (sequência sombra, canário, ampliar, limpeza; limpeza com confirmação específica).
- **Entrada por outros fluxos** (como `bug` e `spike`): `reconhecimento`/`feature`, `arqueologia`/`legado`, `bug` e `incidente` gravam `refatoracao.md` com **Chamado por**, **Usar em** e o motivo; as fases 1-2 viram uma confirmação; a skill vai até a fase 9 e devolve; o chamador refaz o próprio reconhecimento ou arqueologia, porque o código mudou.
- **Ajustes em peças existentes:** `reconhecimento`, `rede-de-protecao` e `arqueologia` (uma linha cada, para a pasta da refatoração); `verificador` (modo refatoração); `bug`, `feature`, `legado`, `incidente` e as próprias `reconhecimento` e `arqueologia` passam a apontar para a skill `refatoracao` em vez de "fluxo 13 (em preparação)"; `/fluxo` marca o 13 como pronto.
- `code-simplifier` e `writing-plans` só como ideia (não acionados): nada a registrar na tabela do `CLAUDE.md`.

| Fases | Peça | Origem |
|---|---|---|
| 1-2 Motivo, alvo e meta | `refatoracao/references/motivo.md` (dor com evidência, custo em horas por mês, toque pelo git, inventário e pontuação de dívida, métricas e como medir, modelo de `refatoracao.md` = contrato de entrada, modelo de `dividas.md`) | adaptada do wshobson `tech-debt` (MIT) |
| 3 Mapeamento | `inventario`, `reconhecimento`, `arqueologia` (legado) + `references/mapeamento.md` (quem depende, contratos observáveis, acoplamento por força, distância e volatilidade) | reaproveitadas; tlc `coupling-analysis` (MIT), BMAD `verification-gap` (MIT) |
| 4 Rede de proteção | `rede-de-protecao` cobrindo todos os contratos; golden master; linha de base de desempenho | reaproveitada, ajuste de 1 linha; `testing-safety-nets` do `legacy-migration-planner` (CC-BY-4.0) |
| 5 Plano em passos | `tlc-spec-driven` (Design no modo grande, Tasks) + `references/plano.md` (um tipo de mudança por passo, campos da tarefa, etapas, padrões de estrangulamento, execução paralela) | reaproveitada; tlc `legacy-migration-planner` (CC-BY-4.0) |
| 6 Execução | `tlc-spec-driven` (Execute) com `implementador`/`implementador-dominio`, ciclo mudar-rodar-commitar | reaproveitada |
| 7 Verificação | `verificador` (modo refatoração) com `references/verificacao.md`; `revisao-codigo` curta; `auditor-seguranca` condicional | reaproveitadas; agente ganhou seção |
| 8 Integração | checagem final, `finishing-a-development-branch`, `liberacao` se crítico; `references/registro.md` | reaproveitadas |
| 9 Registro | `references/registro.md` (meta comparada, contexto do projeto, inventário, `dividas.md`, prevenção) | nova; prevenção do `tech-debt` |

Orquestrador: skill `refatoracao`. `/fluxo` marca o 13 como pronto. **Pendente:** teste real (ex.: uma função grande com regra duplicada num projeto de exemplo, percorrendo as 9 fases no modo pequeno) e, num segundo teste, uma etapa do modo grande com ramificar por abstração.

## Passo 20: fluxo 5, performance e escala

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `refatoracao`, `spike` e `bug`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/performance/<slug>/`**: `performance.md` (fase 1 e estado: **Meta aprovada**, **Rodada**, **Causa confirmada**, **Plano aprovado**, **Rede de proteção**, **Meta atingida**, **Resultado**, como o `refatoracao.md`; também o contrato de entrada), `medicoes.md` (linha de base, cada mudança medida, produção depois), `carga/` (roteiro de medição versionado, sem segredo, base da guarda no CI), `diagnostico.md` (uma seção por rodada), `evidencias/` (saídas brutas; fora do git se tiverem dado de produção), `opcoes.md`, `tasks.md` (tlc), `reconhecimento.md`, `protecao.md`, `validation-rodada-<N>.md`, `seguranca.md` (se houver), `guarda.md`, `integracao.md`. Em andamento = **Resultado** `pendente`. Revisão curta em `.specs/revisoes/performance-<slug>-rodada-<N>/`.
- **Rodadas** no lugar das etapas da refatoração: o desenho manda "meta não atingida → volta ao diagnóstico". As fases 3 a 7 se repetem; os campos de rodada voltam a `pendente`; três rodadas sem a meta escalam ao usuário (saída arquitetural, meta parcial ou rever a meta), como as 3 correções falhas do `bug`.
- **Meta sem número não passa** (como na refatoração): métrica em percentil, alvo, cenário reproduzível, ambiente e prazo, mais **guardas** (o que não pode piorar: erro, memória, custo). Alvos de referência do wshobson só como ponto de partida.
- **Ferramenta já instalada ou script mínimo** na linguagem do projeto; instalar é decisão do usuário (como as métricas da refatoração). Tabela de ferramentas por necessidade, não por stack fixa.
- **Segurança da carga:** carga, `EXPLAIN ANALYZE` e perfil em produção, ou carga que passa por terceiro, exigem confirmação específica (pode ser negação de serviço, custo ou bloqueio); padrão local ou staging com dublês, como o teste ativo da auditoria.
- **Ganho confirmado = faixas sem sobreposição** entre as repetições antes e depois, guardas sem piora. Não confirmado é revertido com `git revert` (fica no histórico, que também é aprendizado). Quem mudou não mede o próprio ganho: a sessão mede na fase 6 (como no `spike`, em que quem experimenta não dá o veredito) e o `verificador` repete na fase 7.
- **Uma tarefa por vez** no Execute do tlc, sem lotes paralelos (duas mudanças juntas invalidam a medição).
- **Otimizar não muda resultado:** opção que muda algo observável (cache com dado velho, paginação, resposta antes do fim) é decisão do usuário na fase 4 e ganha critério de aceite e teste. Rede de proteção pelas skills `reconhecimento` e `rede-de-protecao` depois do plano (como na `feature`), porque o trecho tocado só se conhece com a opção escolhida.
- **Opção incerta → skill `spike`; trocar componente ou infraestrutura → skill `escolha-tecnologia`**, ambas com **Chamado por** `performance <slug>` e **Usar em** `opcoes.md`. Escalar por último.
- **Guarda (fase 8) automatizada no CI**, preferindo proxy determinístico (contagem de consultas, tamanho do pacote, memória) a tempo de resposta, que oscila em CI; carga curta e Lighthouse CI em job próprio, contra a aplicação subida no job. **A guarda precisa falhar sem a otimização**, provado em cópia isolada com os commits `perf:` revertidos: é o teste que "falharia sem a mudança" da regra de testes. SLO, alerta por taxa de queima e painel quando houver produção (do `slo-implementation`). Integração na mesma fase (checagem final, forma de integrar, `liberacao` com produção), para a guarda entrar junto com o ganho.
- **Web à parte** (`web.md`, lido só quando o alvo é página): LCP, INP (no lugar do FID) e CLS no p75, Lighthouse e LHCI com `upload` local (o armazenamento público temporário é ação externa); `budget.json` do Lighthouse tratado como descontinuado (`PREMISSA`, conferir na versão).
- **Modelo:** Opus em 1, 3 e 4 (meta, diagnóstico, escolha); Sonnet em 2 e 5 a 9.
- **Entrada por outros fluxos:** `refatoracao` (meta de velocidade; antes dizia "em preparação"), `incidente` (prevenção de lentidão contida) e `bug` (defeito que é só lentidão) gravam `performance.md` com **Chamado por**, **Usar em** e **Sintoma**; a fase 1 vira uma confirmação.
- **Registro:** oportunidades restantes em `.specs/projeto/dividas.md` (tipo `desempenho`), reaproveitando o modelo da refatoração; **limite atual** medido (carga em degraus até o p95 disparar) quando a meta é de capacidade.
- **Ajustes em peças existentes:** `verificador` (seção de refatoração vira "refatoração ou performance", sem crescer), `rede-de-protecao` e `reconhecimento` (uma linha cada, para a pasta de performance), `refatoracao` (saída "meta de velocidade" aciona a skill), `bug` (saída "só lentidão"), `incidente/references/postmortem.md` (prevenção de lentidão), `/fluxo` (5 pronto).
- `chrome-devtools` só como ideia (servidor MCP de DevTools quando já configurado): nada a instalar.

| Fases | Peça | Origem |
|---|---|---|
| 1 Meta | `performance/references/meta.md` (sintoma, lentidão ou escala, métricas típicas com alvos de referência, cenário, ambiente, guardas, prazo; modelo de `performance.md` = contrato de entrada) | nova; alvos do wshobson `performance-optimization` (MIT) |
| 2 Linha de base | `references/medicao.md` (segurança da carga, ferramenta instalada ou script mínimo, taxa de chegada, aquecimento, repetições, percentis, ruído, ganho confirmado; modelo de `medicoes.md`); `references/web.md` | nova; wshobson `performance-optimization` (MIT), tlc `perf-lighthouse` e `core-web-vitals` (MIT) |
| 3 Diagnóstico | `leitor-codigo` + `references/diagnostico.md` (caminho quente, roteiro de perfil por recurso, degraus de carga, fração do tempo e ganho máximo, causa confirmada, saída arquitetural) | reaproveitada; roteiro do wshobson (MIT) |
| 4 Opções | `references/opcoes.md` (categorias, ganho, esforço, risco, mudança de comportamento, reversível); skills `spike` e `escolha-tecnologia`; `tlc-spec-driven` (Tasks) | nova; categorias do wshobson (MIT) |
| 5 Rede de proteção | `inventario`, `reconhecimento`, `rede-de-protecao` na pasta do trabalho | reaproveitadas, ajuste de 1 linha |
| 6 Otimização | `tlc-spec-driven` (Execute), uma tarefa por vez, com `implementador`/`implementador-dominio`; medir, manter ou reverter | reaproveitada |
| 7 Verificação | `verificador` (modo performance) com `references/verificacao.md`; `revisao-codigo` curta; `auditor-seguranca` condicional | reaproveitadas; agente com seção compartilhada |
| 8 Guarda e integração | `references/guarda.md` (checagem no CI provada contra a versão sem a otimização, SLO e alerta, `guarda.md`, integração, `liberacao`) | nova; wshobson `slo-implementation` (MIT), `perf-lighthouse` (MIT) |
| 9 Registro | `references/registro.md` (gargalo, correção, números, limite atual, contexto, `dividas.md`) | nova |

Orquestrador: skill `performance`. `/fluxo` marca o 5 como pronto. **Pendente:** teste real (ex.: uma API de exemplo com consulta N+1 e sem índice, base com 100 mil registros, percorrendo as 9 fases com autocannon ou k6 locais) e, num segundo teste, uma página web com Lighthouse CI.

## Passo 21: fluxo 14, documentar projeto existente

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `performance`, `refatoracao`, `auditoria-seguranca` e `feature`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/documentacao/<slug>/`** (uma pasta por trabalho, como os outros fluxos, para permitir revisões depois): `documentacao.md` (fase 1 e estado: tabela **Fases** com `pendente`, `feita (<data>)` ou `dispensada — <motivo>`, tabela **Documentos** com destino e situação, **Achados fora do escopo**, **Manutenção**, **Resultado**; também o contrato de entrada), `levantamento.md`, `execucao.md`, `arquitetura.md`, `comportamento.md`, `convencoes.md`, `riscos.md`, `contexto.md`, `validacao.md` (uma seção por rodada), `evidencias/` (fora do git). Fase atual = primeira `pendente`; em andamento = **Resultado** `pendente`.
- **Dois níveis de fonte:** o artefato de trabalho tem a fonte completa (`arquivo:linha` ou comando com resultado e data); o documento do projeto cita caminho (linha muda a cada commit) e só traz comandos executados. O não verificado fica marcado **no próprio documento**, para o leitor ver: `Não verificado` (lido, não executado), `Premissa` (veio de pessoa ou documento antigo), `[A ESCLARECER]`.
- **Documentação no lugar que o projeto já usa** (README, `docs/`, `CLAUDE.md`/`AGENTS.md`), decidido na fase 1; sem convenção, README + `docs/` + `CLAUDE.md`. Escrita na branch `docs/<slug>`, criada na fase 3, commit `docs:` por fase aprovada. Cada fase de 3 a 8 escreve o seu pedaço (o usuário aprova o texto real), em vez de juntar tudo no fim.
- **Público define as fases:** tabela público × documentos × fases dispensadas (você, novo dev, IA, cliente, auditor); inventário e execução nunca são dispensados. Profundidade **enxuta** (README que roda, arquitetura, contexto para IA) como recomendada.
- **Reaproveitamento sem duplicar:** fase 2 = skill `inventario` + levantamento só do que ele não cobre (estrutura, versões, pontos de entrada, scripts, CI, ambientes, nomes de variáveis, documentos existentes com estado atual/desatualizado/contraditório, trabalhos anteriores dos fluxos). Fases 3 e 5 = método das seções 1 e 3 da `arqueologia`, para o projeto inteiro (a `arqueologia` não é acionada: costuras e raio de impacto não servem aqui). Fase 6 = perguntas de padrões do `reconhecimento` com as inconsistências no centro (qual seguir: o mais recente e mais seguido; empate, pergunta). Fase 7 = levantamento com `git log`, `leitor-codigo` e `varredura-seguranca.py ferramentas`; dívidas em `.specs/projeto/dividas.md` (modelo da `refatoracao`); `auditoria-seguranca` oferecida como trabalho separado, sem contrato de chamada.
- **Execução num worktree limpo** (fase 3): sem `node_modules`, `.env` e caches, que escondem passos faltantes. Segredo só num `.env` local do worktree, posto pelo usuário; instalar fora do worktree é decisão do usuário; nunca produção.
- **Arquitetura (fase 4):** C4 do wshobson como referência de níveis, contexto e contêiner bastam; contêiner tirado dos arquivos de deploy. Mermaid `flowchart` (renderiza em qualquer lugar; a sintaxe C4 do Mermaid ficou como `Premissa`, experimental). Cada caixa e seta com evidência; **um segundo `leitor-codigo` confere o diagrama** (quem desenha não confere). Opus nesta fase.
- **Contexto para IA (fase 8) é o modelo único do contexto do projeto:** seções do BMAD traduzidas (orientação, regras, onde fica cada coisa, rodar e verificar, convenções que fogem do padrão, armadilhas, documentação) com a linha de verificação (data e commit). `feature`, `legado`, `refatoracao` e `performance` passam a apontar para esse modelo e dizem em que seção vai cada coisa (comando novo, padrão novo, costura, armadilha). Avaliação com a rubrica do `claude-md-improver` antes de mudar; destino de cada instrução existente (manter, reescrever, mover, automatizar, apagar) com os quatro motivos do BMAD para apagar, generalizado em `escrita.md` para qualquer documento existente. Sem marcadores de bloco gerenciado.
- **Validação (fase 9) pelo agente `verificador`**, novo modo documentação: é o agente de verificação independente, só escreve o relatório e não corrige; o `implementador` faz commits e segue spec, papel errado. O pedido passa só a documentação e o worktree limpo do commit da doc, sem resumo da sessão; o agente registra a falha **antes** de improvisar e confere uma amostra de afirmações. Alternativas oferecidas: sessão nova do usuário ou uma pessoa, no mesmo formato. Rodadas até passar; três sem passar, escala.
- **Manutenção:** linha "atualize na mesma mudança" no contexto do projeto; `feature` e `legado` passam a corrigir `docs/` e README que a mudança torna falsos; checagem de links e dos comandos do "Como rodar" no CI como proposta; revisão periódica por um novo trabalho em modo `revisão` (parte do commit anterior e do `git diff`).
- **Testes:** a documentação não muda comportamento, mas a checagem final e a trava valem para o merge; projeto sem testes pergunta (criar a infraestrutura antes, recomendado; dispensa com aprovação; manter a branch).
- **Modelo:** Opus em 1 e 4; Sonnet no resto.
- **Entrada por outros fluxos:** avaliação de terceiros (27) e quem precisar de documentação grava `documentacao.md` com **Chamado por**, **Usar em** e **Fases**; a fase 1 vira confirmação.
- **Ajustes em peças existentes:** `verificador` (modo documentação), `feature` e `legado` (modelo de contexto e docs na mesma mudança), `refatoracao/references/registro.md` e `performance/references/registro.md` (modelo de contexto), `arqueologia` (parte de `execucao.md` se existir), `reconhecimento` (oferece `documentar` e usa seus artefatos), `/fluxo` (14 pronto).

| Fases | Peça | Origem |
|---|---|---|
| 1 Objetivo e público | `documentar/references/objetivo.md` (perguntas, público × documentos × fases, modelo de `documentacao.md` = contrato de entrada) | nova |
| 2 Inventário | skill `inventario` + `references/levantamento.md` com `leitor-codigo` | reaproveitada; ideia do BMAD `codebase.template.md` (MIT) |
| 3 Execução | `references/execucao.md` (worktree limpo, seguir o escrito, tropeços, "Como rodar") | método da `arqueologia` §1 |
| 4 Arquitetura | `references/arquitetura.md` (níveis, pedido ao `leitor-codigo`, Mermaid, conferência por segundo leitor) | adaptada do wshobson `c4-architecture` (MIT) |
| 5 Comportamento | `references/comportamento.md` (3 a 7 fluxos, rodar, provocar erros, estranho como é) | método da `arqueologia` §3 |
| 6 Convenções | `references/convencoes.md` com `leitor-codigo` | perguntas do `reconhecimento` |
| 7 Riscos e dívidas | `references/riscos.md` (`git log`, `varredura-seguranca.py`, `dividas.md`) | reaproveitadas; `auditoria-seguranca` oferecida |
| 8 Contexto para IA | `references/contexto-ia.md` (arquivo, avaliação, o que entra e não entra, modelo de seções, destinos) | adaptada do `claude-md-improver` (Apache 2.0) e do BMAD `bmad-project-context` (MIT) |
| 9 Validação e manutenção | `references/validacao.md` (pedido ao `verificador`, classificação, rodadas, manutenção, integração) | nova; agente ganhou seção |
| 3 a 8 | `references/escrita.md` (fonte, marcas, porquê, curto, sem segredo, destino do que existe) | nova; motivos para apagar do BMAD (MIT); ideia do `docs-writer` (MIT) |

Orquestrador: skill `documentar`. `/fluxo` marca o 14 como pronto. **Pendente:** teste real (ex.: um projeto pequeno de exemplo com README desatualizado e um passo de instalação faltando, percorrendo as 9 fases com público "novo dev + IA" e conferindo se o `verificador` acha o passo faltante na fase 9).

## Passo 22: fluxo 27, avaliação de projeto de terceiros

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `documentar`, `auditoria-seguranca`, `revisao-codigo` e `escolha-tecnologia`, pendentes de revisão do usuário.

Decisões por analogia:

- **Fluxo-composição:** a skill define objetivo, critérios de decisão, legal e propriedade, dependências e infraestrutura, sustentabilidade, custo total e relatório; qualidade é a `revisao-codigo` (modo curto, recorte do código inteiro na cópia), segurança é a `auditoria-seguranca` (fases 1 a 7 e 9, sem corrigir), comparação com alternativas é a `escolha-tecnologia`, inventário é a skill `inventario`. Os contratos de entrada ficam num só arquivo (`composicao.md`), como cada skill chamada pede.
- **Artefatos em `.specs/avaliacoes/<slug>/`**: `avaliacao.md` (fase 1 e estado: motivo, uso pretendido, critérios congelados, tabela **Fases** com `pendente`/`feita`/`dispensada`, **Resultado**; também o contrato de entrada), `acesso.md`, `alegacoes.md` (material do vendedor sem análise, como na revisão), `legal.md`, `inventario.md`, `execucao.md`, `qualidade.md`, `seguranca.md`, `dependencias.md`, `saude.md`, `decisao.md`, `relatorio.md`, `achados.md` (consolidado), `evidencias/` fora do git. Fase atual = primeira `pendente` (como na `documentar`, porque o motivo dispensa fases). Em andamento = **Resultado** `pendente`. Revisão em `.specs/revisoes/terceiro-<slug>/`, auditoria em `.specs/seguranca/<data>-terceiro-<slug>/`.
- **Critérios de decisão antes de olhar o candidato**, no formato da `escolha-tecnologia` (eliminatórios e desejáveis com peso), para a fase 9 passá-los adiante sem reescrever. Impressão de demonstração anotada à parte, como a "favorita declarada".
- **Motivo × fases** (comprar, herdar, adotar como dependência, contratar quem fez, contribuir), como público × fases na `documentar`; profundidade completa ou enxuta. **Legal nunca é dispensada.**
- **Achados consolidados** `AV-NNN` com **efeito na decisão** (`impeditivo`, `condição`, `custo`, `nota`), custo de corrigir (estimativa ou não quantificável) e quem resolve (vendedor, nós, ninguém): é o que transforma achados de várias fases em decisão e argumento de negociação. Os das skills chamadas entram com o ID delas.
- **Saída "direto à decisão"** quando um eliminatório falha (licença, titularidade, não roda): não gastar as fases seguintes, com a opção de seguir para ter argumento.
- **Cópia fora do projeto do usuário**, clone sem submódulos, nada executado na fase 2; **nunca abrir sessão do Claude Code dentro da cópia** (o `.claude/settings.json` e os ganchos do terceiro rodariam); `CLAUDE.md`, `AGENTS.md` e afins do terceiro são dado e instrução escondida é achado.
- **Executar só em ambiente isolado** (contêiner recomendado, com só a cópia montada, sem variáveis do usuário, rede cortada depois de instalar; VM ou área descartável; ou não executar), com confirmação específica e leitura prévia dos scripts de instalação. O mesmo ambiente serve à revisão (checagens) e à auditoria (teste ativo). Credenciais só de teste.
- **Legal como material próprio**, com aviso de que não é parecer jurídico: licença do projeto, matriz uso pretendido × família de licença (permissiva, copyleft fraco, GPL, AGPL, código disponível, não comercial), dependências (ferramentas que leem sem instalar na fase 3; as que precisam das dependências instaladas na fase 4, no ambiente isolado; sem ferramenta, `pesquisador` nas diretas), código copiado, componentes pagos, titularidade e cessão (Lei 9.609/1998, a confirmar com advogado), marcas, LGPD (com o checklist do legado `risk-and-compliance-check`) e obrigações. Seção "Para o advogado".
- **Script `propriedade-git.py`** adaptado do `security-ownership-map` (Apache 2.0), só com a biblioteca padrão: fator ônibus do projeto e em 12 meses, arquivos de um autor, atividade mensal em 24 meses, código sensível sem dono e órfão, donos ocultos; JSON com e-mails em `evidencias/`, Markdown só com nomes. 15 testes novos. Vale a pena porque o cálculo à mão é longo e a fase 8 precisa de número reproduzível.
- **Pessoas por papel** no relatório; e-mails do git são dado pessoal (fora do git). Avalia-se código e histórico, não a vida de quem escreveu.
- **Vulnerabilidade em projeto aberto**: aviso privado aos mantenedores (`SECURITY.md`), ação externa com texto aprovado; nunca issue pública.
- **Decisão** com custo total em faixa por horizonte (preço, corrigir, rodar, manter, obrigações, sair), comparação com construir só o que leva ao bom resultado, fator decisivo e "mudaria se" (do legado `build-vs-buy-analysis`); adotar, adotar com condições, renegociar ou recusar; com `impeditivo` aberto, adotar não é a recomendada. Negociar, assinar e pagar são do usuário.
- **`documentar` depois da decisão**, não na fase 4: documentar antes de decidir é desperdício, e a skill grava no repositório do projeto. A fase 4 usa o método de `documentar/references/execucao.md` (o mesmo da seção 1 da `arqueologia`).
- **Modelo:** Opus em 1, 3 e 9 (critérios, legal, decisão); Sonnet no resto (as skills chamadas avisam o delas).
- **Aprovações:** uma por fase; nas 5 e 6, as das skills chamadas e depois a da avaliação sobre o resumo.
- **Ajustes em peças existentes:** `inventario` (chamado pela avaliação: raiz na cópia, saída na pasta da avaliação, sem `testes.json`, que é do projeto do usuário e alimenta a trava), `revisao-codigo/references/fases.md` e `auditoria-seguranca/references/fases.md` (linha do 27: ambiente isolado e contrato), `escolha-tecnologia` (27 entre os chamadores), `documentar` (chamada depois de adotar), `/fluxo` (27 pronto). Contratos das skills chamadas conferidos: `revisao.md` com **Devolver após** `análise` e `escopo.md` com **Devolver após** `relatório` batem com o que elas esperam.

| Fases | Peça | Origem |
|---|---|---|
| 1 Objetivo | `avaliar-terceiros/references/objetivo.md` (perguntas, critérios, motivo × fases, modelo de `avaliacao.md` = contrato de entrada) | nova; forma dos critérios da `escolha-tecnologia` |
| 2 Acesso e escopo | `references/acesso.md` (material, cópia fora do projeto, instruções do terceiro como dado, `alegacoes.md`, **Não visto**) | nova; `alegacoes.md` da `revisao-codigo` |
| 3 Legal e propriedade | `references/legal.md` (licenças, dependências, titularidade, marcas, LGPD, obrigações, para o advogado) | nova; LGPD do legado `risk-and-compliance-check` |
| 4 Execução | `references/execucao.md` (leitura prévia, ambiente isolado, inventário, prometido × observado) + skill `inventario` | método da `documentar` e da `arqueologia` §1; reaproveitada com ajuste |
| 5 Qualidade | skill `revisao-codigo` (curto) com `references/composicao.md` | reaproveitada |
| 6 Segurança | skill `auditoria-seguranca` (1 a 7 e 9) com `references/composicao.md` | reaproveitada |
| 7 Dependências e infraestrutura | `references/dependencias.md` + `pesquisador` | nova |
| 8 Saúde e sustentabilidade | `references/saude.md` + `.claude/scripts/propriedade-git.py` + `pesquisador` | adaptada do `security-ownership-map` (Apache 2.0) e do BMAD `technical.md` dimensão 5 (MIT) |
| 9 Custo total e decisão | `references/decisao.md`; skill `escolha-tecnologia` se houver alternativas | adaptada do legado `build-vs-buy-analysis`; reaproveitada |
| 10 Relatório | `references/relatorio.md`; `documentar` como próximo passo | nova |

Orquestrador: skill `avaliar-terceiros`. `/fluxo` marca o 27 como pronto. **Pendente:** teste real (ex.: um repositório aberto pequeno com uma dependência AGPL e um mantenedor único, avaliado para uso em SaaS fechado, conferindo se a fase 3 dispara a saída "direto à decisão"; e, num segundo teste, a execução em contêiner com uma alegação do README refutada).

## Passo 23: fluxo 6, integração com terceiros

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `avaliar-terceiros`, `feature`, `legado` e `documentar`, pendentes de revisão do usuário.

Decisões por analogia:

- **Por cima da `feature` (ou `legado`), sem repetir as fases delas.** Integrar é uma feature (comportamento novo, com spec, reconhecimento, plano, rede, execução, verificação e integração da branch), diferente de refatoração e performance, que têm natureza própria (não mudar comportamento; medir em rodadas) e por isso chamam as peças direto. Repetir aqui duplicaria cinco fases e a bifurcação projeto IA × legado. A skill faz as fases 1 a 4 (antes do código) e 9 (depois), e as 5 a 8 andam por dentro da skill escolhida, com um mapa de fases e os acréscimos num só arquivo (`composicao.md`), como os contratos da `avaliar-terceiros`. `feature` e `legado` ganharam uma linha "chamada por outro fluxo": `spec.md` com **Chamado por** `integração <slug>` segue os acréscimos e devolve ao chamador ao gravar `integracao.md`.
- **Artefatos em `.specs/integracoes/<slug>/`**: `terceiro.md` (fase 1 e estado: **Fornecedor**, **Rota de saída**, **Feature**, tabela **Fases** com `pendente`/`feita`/`dispensada`, **Voltas à escolha**, **Resultado**, como `avaliacao.md` e `documentacao.md`), `contrato.md` (3), `seguranca-legal.md` (4), `verificacao.md` (7), `monitoramento.md` (9), `evidencias/` (respostas brutas do sandbox, fora do git). A construção fica em `.specs/features/integracao-<slug>/` (artefatos da `feature`/`legado`), a escolha em `.specs/escolhas/fornecedor-<slug>/`, o spike em `.specs/spikes/<slug>-contrato/`, a auditoria em `.specs/seguranca/<data>-integracao-<slug>/`. O nome `integracao.md` ficou fora de propósito: já é o artefato de fim de feature. Em andamento = **Resultado** `pendente`.
- **Fase 2 pela `escolha-tecnologia`**, com reversibilidade sugerida (fácil quando o adaptador isola e o fornecedor não guarda dado nosso; difícil com dados ou estado pouco exportáveis, como cartões salvos e assinaturas, ou fidelidade) e critérios sugeridos (custo no volume, limites, SLA e histórico de status, termos, documentação e SDK, política de versões, rota de saída). Critérios e modo continuam do usuário. Fornecedor imposto: fase dispensada, mas custo, limites, SLA, termos e rota de saída são levantados pelo `pesquisador` mesmo assim.
- **Fase 3 em duas camadas**: documentação atual pelo `pesquisador` (pedido com 11 itens, fonte e data), depois **um spike** com a pergunta "o sandbox bate com a documentação nos itens críticos C-01 a C-NN?" (respeita "uma pergunta por spike" sem abrir um spike por item); pergunta numérica que pese (limite real, latência) ganha spike próprio. Cada item `documentado`, `confirmado no sandbox`, `diverge` ou `não testável`. Amostras reais sanitizadas viram base dos testes de contrato na fase 6.
- **Fase 4 vem antes do desenho**, porque o que não pode sair muda o desenho (minimização, checkout hospedado). LGPD adaptada do `gdpr-data-handling` (MIT) e do `compliance-validation` do legado; tabela de fatos legais toda `PREMISSA` (arts. 5, 7, 11, 14, 18, 19, 33, 37, 38, 39, 42 e 48; Resoluções CD/ANPD nº 15/2024 e nº 19/2024; PCI DSS) até o `pesquisador` conferir. Lacuna de obrigação legal não vira débito; base legal e papéis são do controlador. Fornecedor pode ser **controlador independente** (antifraude, pagamento), o que muda contrato e aviso de privacidade. "Não é parecer jurídico" no topo, como na `avaliar-terceiros`.
- **Desenho (fase 5) com 16 seções** obrigatórias ou `não se aplica — motivo` (adaptador no vocabulário do domínio, tempo limite, nova tentativa só em transitório e idempotente, disjuntor, limite do nosso lado, idempotência, fila e caixa de saída, webhooks, reconciliação, degradação, desligamento por flag, validação da resposta, configuração, observabilidade sem dado pessoal, teto de custo, SDK ou HTTP) e 11 **critérios de falha em EARS** como ponto de partida da spec. Ferramenta concreta é a que o reconhecimento achar; peça nova só se nenhuma instalada resolver.
- **Testes (fase 6)**: a suíte padrão (`testes.json`, a que a trava roda) **nunca chama a rede**; simulador no nível HTTP alimentado pelas amostras reais (para não divergir do real); testes de contrato contra as amostras e contra o esquema publicado; um teste por falha (tempo esgotado, lentidão, 5xx, 429 com `Retry-After`, erro definitivo, corpo malformado, campo ausente e novo, 401, disjuntor, idempotência, fila de mortos, flag, teto de custo, webhooks forjados, repetidos e fora de ordem); relógio controlado. Testes de sandbox separados, marcados, só com confirmação e chave de sandbox; no CI só com aprovação para guardar a chave.
- **Auditoria restrita na fase 7, fases 1 a 7, Devolver após `classificação`** (o contrato antigo da `auditoria-seguranca` dizia 1 a 9 com correção pela skill `bug`): o código ainda está na branch da feature, e a `bug` abriria branch a partir da principal, onde ele não existe. Crítico e alto viram tarefa da feature, com o teste do ataque; reteste pelo `auditor-seguranca` com a mesma Prova, registrado em `verificacao.md`. A auditoria restrita substitui o `auditor-seguranca` avulso da verificação da `feature`. Para a auditoria não ficar "em andamento" para sempre, a skill passou a gravar `relatorio.md` curto (`Status: final — devolvido a <chamador> após <fase>`) quando devolve antes da fase 9.
- **Verificação própria (fase 7)** além do PASS da feature: ponta a ponta no sandbox (ação externa), segredos e logs lidos com o nível de produção, limite de taxa contra o pico, custo mensal com fonte e teto testado.
- **Liberação (fase 8) pela `liberacao`** com itens próprios: chaves de produção e webhook cadastrados pelo usuário (nunca passam pela conversa), flag começando desligada, reversão = desligar e ver a degradação, alcance mínimo (sem sandbox: menor operação real, com confirmação), critério de parada de terceiro. No `legado`, a fase 8 dele já chama a `liberacao`. Uso próprio: `implantacao`.
- **Monitoramento (fase 9)**: tabela de sinais (erro por tipo, latência, disjuntor, fila, webhooks, reconciliação, custo e cota) com alerta acionável e **disparo testado** (como na prevenção da skill `incidente`); versão fixada e fim de suporte; canal de avisos com dono; revisão periódica pelo `pesquisador`; checagem de contrato agendada opcional; rotação com data; entrada no `.specs/runbook.md`. Mudança anunciada abre integração nova `<slug>-<versão>` começando no contrato.
- **Saída de emergência** (do desenho): contrato diverge muito, limite ou custo inviável, SLA incompatível com a criticidade ou risco legal alto → volta à fase 2, registrada em **Voltas à escolha**; ADR novo substitui o anterior.
- **Projeto novo sem código** (fluxo 1): fases 1 a 4 aqui, entregues ao Design do tlc; 5 a 9 ficam no fluxo 1.
- **Modelo:** Opus em 1, 2, 4 e 5; Sonnet em 3 e 6 a 9 (as skills chamadas avisam o delas).
- **Aprovações:** uma por fase; nas fases com skill chamada, as dela e depois a da integração sobre os itens próprios (como na `avaliar-terceiros`).
- **Ajustes em peças existentes:** `feature` e `legado` (linha de chamada por outro fluxo), `auditoria-seguranca` (contrato do fluxo 6 e `relatorio.md` curto ao devolver antes da 9), `escolha-tecnologia/references/fases.md` e `spike/references/fases.md` (**Usar em** apontando para `terceiro.md` e `contrato.md`), `/fluxo` (6 pronto). Contratos conferidos: `escolha.md` com **Chamado por** `integração <slug>` e `spike.md` com **Chamado por** `integração <fornecedor>` batem com os modelos delas; o de `escopo.md` mudou como descrito.
- `mcp-builder` não entra (trata de servidor MCP, não de integrar fornecedor); `pci-compliance` só como ideia na linha de cartão.

| Fases | Peça | Origem |
|---|---|---|
| 1 Necessidade | `integracao-terceiros/references/necessidade.md` (perguntas, integrar é o caminho?, modelo de `terceiro.md`) | nova |
| 2 Escolha do serviço | skill `escolha-tecnologia` com o contrato de `references/composicao.md` | reaproveitada |
| 3 Contrato | `pesquisador` + skill `spike` com `references/contrato.md` (pedido, sandbox, saída, modelo) | reaproveitadas; legado `api-contract-design` |
| 4 Segurança e legal | `references/seguranca-legal.md` (fatos legais `PREMISSA`, dados, LGPD, segredos, entrada externa) + `pesquisador` | adaptada do wshobson `gdpr-data-handling` (MIT) e legado `compliance-validation`; ideia do `pci-compliance` (MIT) |
| 5 Desenho | skill `feature` ou `legado` (Specify, reconhecimento ou arqueologia, Design e Tasks) + `references/desenho.md` | reaproveitadas, ajuste de 1 linha; legado `api-integration` |
| 6 Implementação | a mesma skill (rede de proteção, Execute) + testes de `references/desenho.md` | reaproveitadas |
| 7 Verificação | a mesma skill (`verificador`, `revisao-codigo` curta) + skill `auditoria-seguranca` restrita + `references/verificacao.md` | reaproveitadas; auditoria com contrato ajustado |
| 8 Liberação | integração da branch pela mesma skill + skill `liberacao` com `references/monitoramento.md` | reaproveitadas |
| 9 Monitoramento | `references/monitoramento.md` (sinais, alertas testados, mudanças do fornecedor, rotação, runbook) | nova; alerta testado como na skill `incidente` |

Orquestrador: skill `integracao-terceiros`. `/fluxo` marca o 6 como pronto. **Pendente:** teste real (ex.: envio de e-mail transacional por um fornecedor com sandbox num projeto de exemplo, percorrendo as 9 fases pela `feature`, com um tempo esgotado e um webhook forjado nos testes; e, num segundo teste, um pagamento com cartão em checkout hospedado, conferindo a fase 4 e a liberação com valor mínimo) e revisão humana de `seguranca-legal.md` (fatos legais conferidos pelo `pesquisador`).

## Passo 24: fluxo 30, automação de processo

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `integracao-terceiros`, `uso-proprio` (`necessidade`), `feature`, `legado` e `escolha-tecnologia`, pendentes de revisão do usuário.

Decisões por analogia:

- **Fases 1 a 3 numa conversa, um artefato e uma aprovação**, como a `necessidade` do uso próprio (são curtas e uma depende da outra). A fase 1 exige **uma execução real anotada** (descrição de memória fica `PREMISSA`); a fase 2 tem **conta de retorno escrita** (horas economizadas por mês, horas para construir, manutenção, meses para empatar, horizonte, erros evitados, risco) e quatro vereditos: `automatizar`, `automatizar parte`, `não automatizar`, `padronizar primeiro`. Com os dois últimos, a aprovação vem antes da fase 3 e o **Resultado** já fica gravado.
- **Artefatos em `.specs/automacoes/<slug>/`**: `processo.md` (fases 1 a 3 e estado: **Dono**, **Ferramenta**, **Onde mora**, **Como se testa**, **Construção**, tabela **Fases** com `pendente`/`feita`/`dispensada`, **Resultado**, como `terceiro.md`), `desenho.md` (5), `execucao.md` (7), `operacao.md` (8 e 9), `evidencias/` (saídas com dado real, fora do git). Em andamento = **Resultado** `pendente`. Construção em projeto existente em `.specs/features/automacao-<slug>/`; escolha em `.specs/escolhas/automacao-<slug>/`.
- **Escada de ferramentas** (fase 4) do mais simples ao mais caro: recurso nativo, agendador do sistema, script curto, serviço pronto, código no projeto, agente de IA; cada degrau descartado com motivo. **IA só com motivo escrito** e travas obrigatórias (saída validada por regra, aprovação antes do irreversível, teto de custo, limite de iterações, testes com respostas ruins). `escolha-tecnologia` só com alternativas reais, modo enxuto sugerido; o contrato de entrada bate com o modelo de `criterios.md` (**Chamado por** `automação <slug>`).
- **Onde mora** decidido na fase 4, com recomendação pelo caso: no projeto existente (mexe em dados e regras dele), num **repositório de automações do usuário** (script avulso e hook pessoal; uma pasta por automação, suíte e CI comuns), num repositório próprio, ou no serviço pronto (configuração exportada para o repositório). Pasta solta sem git não é opção. Se a sessão começou em outro repositório, a pasta de `.specs/automacoes/<slug>/` é copiada para o destino e o original fica **Resultado** `movida para <caminho>`.
- **Desenho seguro com 17 seções** obrigatórias ou `não se aplica — motivo` (gatilho e execução única, ações e reversibilidade, permissões mínimas, segredos, **simulação obrigatória e padrão**, idempotência, falha parcial e retomada, **teto de ação em massa** e de custo, aprovação humana, exceções, registro, relatório, alerta de falha e de "não rodou", pausa, validação da entrada, dados e LGPD, dependências externas) e **11 critérios EARS `AUT-NN`** como ponto de partida da spec. Simulação é o padrão: agir exige ordem explícita.
- **Implementação (fase 6) em quatro caminhos**: projeto existente pela `feature` ou `legado` (como a integração, por cima delas, com os acréscimos em `composicao.md`; a automação entra **inerte** na branch principal: simulação por padrão e sem agendamento; no `legado`, a fase 8 dele não roda, porque ligar é a fase 8 daqui); script avulso ou hook pelo `tlc-spec-driven` no repositório da automação, com `verificador` e checagem final; serviço pronto sem código por **casos de teste executados e registrados** (configuração pura não é código do projeto; pedaço de código embutido é código e tem teste). A suíte nunca age em dado real; amostras reais sanitizadas.
- **Execução assistida (fase 7)** em sombra (simulação ao lado do manual, que continua valendo) ou com aprovação antes de agir, ou os dois em sequência; **critério de confiança escrito antes** (com irreversível, no mínimo 3 rodadas); divergência classificada por causa (automação → teste e correção; processo → `processo.md` e `desenho.md`; manual → ganho anotado). Ler dado real e agir com aprovação são ação externa, confirmadas no início. Três rodadas sem confiança: escala.
- **Operação (fase 8)**: `implantacao` para ferramenta pessoal, `liberacao` para produção com usuários (simulação no ambiente real, aprovação, depois sozinha; alcance pequeno); agendador local ou do CI só com registro. **Ligar o agendamento é ação com confirmação específica.** Alerta de falha **e de "não rodou"** (verificação de fora da automação), ambos com **disparo testado** (como na `incidente` e na `integracao-terceiros`); relatório a cada execução, inclusive sem nada a fazer; pausa testada; dono e substituto; entrada no runbook em produção.
- **Manutenção (fase 9)**: documentação no lugar de **Onde mora** (o que faz, como simular, **como pausar e como desligar de vez**, dono), gatilhos de revisão, revisão periódica com decisão manter / ajustar / aposentar (aposentar = desligar e revogar a credencial).
- **Automação do Claude Code** (`claude-code.md`): tabela de peças (hook, skill/comando, subagente, `claude -p`, `loop`/`schedule`) como ponto de partida a conferir na documentação atual; a skill `update-config` escreve a configuração, esta skill decide o quê e por quê; `settings.json` com confirmação e diff; na `.claude` do Rascunho, só texto proposto. Regra de hook adaptada do `writing-rules` do `hookify` (Apache 2.0), com **aviso antes de bloqueio** como a simulação da peça e desativar sem apagar como a pausa; script de hook é código com teste (como `trava-testes.py`). Laço de agente com limite de iterações e conclusão verificável (ideia do `ralph-loop`). O plugin `hookify` não é instalado.
- **Saídas**: `padronizar primeiro`, retorno negativo (oferecer só o passo mais caro), é integração de produto (`integracao-terceiros`), dano em produção agora (pausa e `incidente`); alerta real vira `bug` ou `incidente`.
- **Modelo:** Opus de 1 a 5 (conversa, conta, escolha e desenho); Sonnet de 6 a 9.
- **Aprovações:** uma para 1-3, depois uma por fase; nas fases 4 (com escolha), 6 e 8, as das skills chamadas e depois a da automação sobre os itens próprios.
- **Ajustes em peças existentes:** `feature` e `legado` (linha de chamada por `automação <slug>`; o `legado` para depois da integração da branch), `escolha-tecnologia/references/fases.md` (linha do 30 com o **Usar em** real), `/fluxo` (30 pronto). `dispatching-parallel-agents` não entra (fases sequenciais).

| Fases | Peça | Origem |
|---|---|---|
| 1-3 Processo, retorno e escopo | `automacao/references/processo.md` (perguntas, execução anotada, conta de retorno, vereditos, escopo, modelo de `processo.md`) | nova |
| 4 Ferramenta | `references/ferramenta.md` (escada, IA com travas, onde mora, como se testa) + skill `escolha-tecnologia` enxuta com `references/composicao.md`; `references/claude-code.md` para peças do Claude Code | reaproveitada; `claude-code.md` adaptada do `hookify writing-rules` (Apache 2.0), ideias do `ralph-loop` e do `claude-automation-recommender` |
| 5 Desenho seguro | `references/desenho.md` (17 seções, `AUT-01` a `AUT-11`, testes, modelo) | nova; dependências externas e LGPD apontam para `integracao-terceiros` |
| 6 Implementação | skill `feature` ou `legado` com `composicao.md`; `tlc-spec-driven` + `verificador` no repositório da automação; casos de teste do serviço pronto | reaproveitadas, ajuste de 1 linha |
| 7 Execução assistida | `references/execucao.md` (modo, critério de confiança, rodadas, divergências, modelo) | nova |
| 8 Operação | `references/operacao.md` + skill `implantacao` ou `liberacao` | reaproveitadas; alerta testado como na `incidente` |
| 9 Manutenção | `references/operacao.md` (documentação, gatilhos, revisão periódica) | nova; modelo de contexto da `documentar` |

Orquestrador: skill `automacao`. `/fluxo` marca o 30 como pronto. **Pendente:** teste real (ex.: um relatório semanal montado à mão a partir de uma planilha, automatizado por script Python no Agendador de Tarefas do Windows, percorrendo as 9 fases com a conta de retorno, a simulação, duas rodadas em sombra e o alerta de "não rodou" testado; e, num segundo teste, um hook do Claude Code em modo aviso por uma semana antes de bloquear).

**Decisão do usuário (2026-10-23), fluxo 30:** automação feita só por configuração num serviço pronto, sem código, prova o comportamento com casos de teste executados e registrados com evidência, mais a execução assistida; código embutido no serviço continua com teste automatizado. Registrada como exceção na seção de testes do `CLAUDE.md`.

## Passo 25: fluxo 7, redesign de interface

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `refatoracao`, `performance`, `mockup-visual` e `integracao-terceiros`, pendentes de revisão do usuário.

Decisões por analogia:

- **Peças chamadas direto, sem passar pela `feature`.** Pelo próprio critério do passo 23: integrar e automatizar são features (comportamento novo); redesign tem natureza própria, como a refatoração — **comportamento constante** (regras de negócio não mudam) e mudança em **etapas tela a tela** —, e por isso chama `inventario`, `reconhecimento`, `rede-de-protecao`, `tlc-spec-driven`, `verificador`, `revisao-codigo` e `liberacao` direto, com etapas como a `refatoracao` (`validation-etapa-<N>.md`, uma entrada de `integracao.md` por etapa). Passar pela `feature` exigiria uma spec EARS de "comportamento novo" que não existe e repetiria o reconhecimento.
- **Artefatos em `.specs/redesign/<slug>/`**: `redesign.md` (fase 1 e estado: motivo, meta com linha de base, o que não muda, escopo, **Mockup aprovado**, **Flag**, **Liberação**, **Comparação visual**, tabelas **Fases** e **Etapas**, **Resultado**), `inventario-telas.md`, `reconhecimento.md` (e `arqueologia.md` em legado), `capturas/antes/` e `capturas/telas.json`, `pesquisa.md` (`P-NN`), `mockup/` (estrutura da `mockup-visual`), `sistema.md`, `acessibilidade.md` (requisitos, linha de base e auditoria por etapa), `migracao.md`, `tasks.md`, `protecao.md`, `validation-etapa-<N>.md`, `seguranca.md` (se houver), `integracao.md`, `medicao.md`, `evidencias/` fora do git. Revisão em `.specs/revisoes/redesign-<slug>-etapa-<N>/`. Fase atual: primeira `pendente` das 1 a 7; depois, a situação da etapa atual (`planejada` → 8, `construída` → 9, `integrada` → 10 se a liberação for por etapa).
- **Compatível com `.specs/mockup/`**: durante o redesign, `.specs/mockup/` (fluxo 1) continua sendo a referência da interface **atual** e não é tocado; o mockup novo mora em `.specs/redesign/<slug>/mockup/`, com a mesma estrutura. Com **manter** na fase 10, o anterior vai para `mockup-anterior/` e o novo é promovido a `.specs/mockup/` (`git mv`), para as features seguintes e a etapa 3 da `mockup-visual` usarem o atual sem saber do redesign.
- **`mockup-visual` estendida com um modo redesign** (ajuste mínimo, comportamento atual mantido): pasta do redesign, etapa 1 partindo das capturas e dos `P-NN` com a tela de hoje na galeria, etapa 2 em duas aprovações (2a guia = fase 5; 2b **todas as telas** do escopo × estados × PC e celular, navegáveis, com `telas.json` = fase 6) e etapa 3 com `comparar-visual.mjs`. Uma skill nova repetiria direções, guia, publicação e checklist; o modo fica em `mockup-visual/references/redesign.md` e o `SKILL.md` dela ganhou uma seção de 7 linhas e a `description` ajustada. Muitas telas: a sessão desenha as do fluxo principal, o `implementador` replica as demais em lotes com uma tela modelo, conferidas pelo checklist.
- **`comparar-visual.mjs` adaptado para `.claude/scripts/`**, em Node: roda no projeto da interface, que é onde o Playwright está (o legado já resolvia o Playwright pelo `--pacote`); portar para Python exigiria o Playwright de Python no projeto. Acréscimos: `--so-app` (capturas do estado atual na fase 2), `--listar` (confere o mapa sem navegador), bloco `flag` (consulta, cookie ou `localStorage`) para ligar a interface nova, `--flag desligada`, `limite` por tela, `--navegador` (Firefox e WebKit para a verificação), saída padrão em `<pasta do telas.json>/comparacao/<data>/`. **Testes**: as funções puras são exportadas e o `main` só roda quando o arquivo é executado; 15 testes Python (`test_comparar_visual.py`) chamam o `node` para importar o módulo e para a linha de comando sem Playwright (`--listar`, erros de uso, mapa inválido, Playwright ausente). Precisa do `node` no PATH: sem ele, um teste **falha** (não pula). A captura e a diferença no navegador não têm teste automatizado aqui (exigiria o Chromium na suíte); foram conferidas à mão com o Playwright 1.64 já em cache na máquina, numa página de exemplo servida localmente: flag por cookie e por consulta (0,00%), `--flag desligada` acusando `DIVERGE` acima do limite da tela, `--so-app`, servidor do `--iniciar` derrubado no fim e navegador não instalado saindo com código 2 (corrigido: antes deixava o servidor de pé).
- **Comparação pixel a pixel volta, só no redesign.** O passo 5 tirou essa comparação do fluxo 1 por ser pesada; aqui o desenho exige "diferença visual dentro do limite" e são todas as telas, então ela é o meio (automático quando o projeto tem Playwright; instalar é decisão do usuário, perguntada na fase 7, com prints lado a lado como alternativa). Limite por tela calibrado com o usuário na primeira tela (`PREMISSA`: 2%). Roda localmente por etapa; no CI só com imagem fixa e decisão do usuário (fonte e sistema mudam o desenho do texto).
- **`checar-tokens.py` aceita vários caminhos e arquivos**: enquanto a interface antiga (cheia de valores soltos) convive com a nova, só o código novo é checado; na etapa de remoção, a interface inteira. Dois testes novos.
- **Coexistência e testes**: flag por tela ou rota (recomendada), tema por classe raiz (só reskin) ou aplicação separada (último caso); desligada é o padrão em produção até a fase 10; opção "voltar ao visual antigo" recomendada. A rede de proteção caracteriza cada tela **pela interface**, com cada teste rodando **com a flag desligada e ligada** e as mesmas asserções: é a prova de que a regra não mudou. Seletores por papel, rótulo e texto; testes existentes que dependem de classe CSS são listados com proposta e aprovação na fase 7 (nunca alterados sem ela); a mudança de teste da etapa de remoção (deixar de rodar na posição desligada) também é aprovada na fase 7.
- **Etapas**: 1 fundação (tokens, componentes, flag, testes, comparação e tokens configurados), 2 a N telas ou fluxos curtos (não misturar antigo e novo no meio de uma tarefa), R remoção só depois de **manter**. Ordem recomendada: uma tela de risco baixo primeiro, depois os `P-NN` de maior prioridade.
- **Acessibilidade como requisito**: WCAG 2.2 AA como padrão declarado (exigência legal, como LBI e eMAG, fica `PREMISSA` até o `pesquisador`); checklist pelos quatro princípios com os critérios da 2.2 (alvo de 24 px, foco não encoberto, ajuda consistente, entrada redundante, autenticação acessível); severidade crítica (bloqueia guia, tela e integração), séria (bloqueia a liberação salvo aceite com prazo), moderada (tarefa). Automática (`@axe-core/playwright` como teste da suíte recomendado) mais manual obrigatória (teclado, leitor de tela, zoom, 320 px, movimento).
- **Pesquisa com saída de emergência**: problemas `P-NN` com tipo (aparência, organização, navegação, fluxo, regra, desempenho, acessibilidade); se os prioritários são de fluxo ou regra, o redesign para e oferece `feature` (**Resultado** `virou feature`); navegação pode entrar no escopo se nenhuma regra mudar; desempenho vai para `performance`. Teste rápido com 5 pessoas, conduzido pelo usuário, com as mesmas tarefas repetidas na verificação e na medição.
- **Linha de base na fase 1**, medida antes de qualquer mudança (pelo menos uma métrica medida; sem medida, vira observação); guardas de desempenho da página e conversão fora do foco. Painel de uso, gravação ou A/B novos são mudança no produto (LGPD; fornecedor externo pela `integracao-terceiros`).
- **Liberação** pela `liberacao` com itens próprios: alcance interno → voluntários → porcentagem → todos; A/B só com amostra para a métrica no prazo, sorteio por usuário, amostra e duração decididas antes; comunicação na própria interface e ao suporte; reversão = desligar a flag, testada. **Decisão** manter / ajustar / reverter; reverter pergunta se o código novo fica inerte ou sai.
- **Verificador em modo redesign** (uma frase acrescentada à seção de refatoração e performance), com o pedido em `redesign/references/verificacao.md`: testes intactos, suíte nas duas posições, regras iguais, antiga intacta, sensor na tela nova, tokens, comparação visual subindo o app localmente, acessibilidade automática, escopo. Revisão curta com critérios próprios; `auditor-seguranca` quando a etapa toca dados pessoais (formulários costumam tocar).
- **Modelo:** Opus em 1, 3, 4, 5, 6 e 7 (conversa, pesquisa, desenho e plano); Sonnet em 2, 8, 9 e 10.
- **Ajustes em peças existentes:** `mockup-visual` (modo redesign), `checar-tokens.py` (vários caminhos), `verificador`, `reconhecimento` e `rede-de-protecao` (uma frase cada, para a pasta do redesign), `/fluxo` (7 pronto). `webapp-testing` (Apache 2.0) e `frontend-design` só como inspiração.

| Fases | Peça | Origem |
|---|---|---|
| 1 Motivo e meta | `redesign/references/motivo.md` (perguntas, métricas por problema, guardas, modelo de `redesign.md`) | nova |
| 2 Inventário | skills `inventario`, `reconhecimento` (e `arqueologia`) na pasta + `references/inventario-telas.md` + `comparar-visual.mjs --so-app` + `checar-tokens.py` como contagem | reaproveitadas, ajuste de 1 frase; script adaptado do legado |
| 3 Pesquisa | `references/pesquisa.md` (fontes, roteiro do teste com usuários, `P-NN`, saída de emergência) + `pesquisador` | nova |
| 4 Direções | skill `mockup-visual` etapa 1, modo redesign | reaproveitada, estendida |
| 5 Sistema de design | `mockup-visual` etapa 2a + `references/sistema.md` + `references/acessibilidade.md` | estendida; legado `design-system-consistency-check` e `accessibility-review`; wshobson `wcag-audit-patterns` (MIT) e tlc `web-accessibility` (MIT) |
| 6 Mockup completo | `mockup-visual` etapa 2b (todas as telas, estados, navegável, `telas.json`) | estendida |
| 7 Plano de migração | `references/migracao.md` + `tlc-spec-driven` (Tasks) + skill `rede-de-protecao` | nova; reaproveitadas, ajuste de 1 frase |
| 8 Implementação | `tlc-spec-driven` (Execute) + `references/construcao.md` + `checar-tokens.py` + `comparar-visual.mjs` | reaproveitada; scripts estendido e adaptado |
| 9 Verificação | `verificador` (modo redesign) + `references/verificacao.md` + `revisao-codigo` curta + `auditor-seguranca` condicional + integração da etapa | reaproveitadas; agente com uma frase |
| 10 Liberação e medição | skill `liberacao` + `references/liberacao-medicao.md` (A/B, medição, decisão, remoção, promoção do mockup) | reaproveitada; nova |

Orquestrador: skill `redesign`. `/fluxo` marca o 7 como pronto. **Pendente:** teste real (ex.: um app web de exemplo com 4 telas — lista, detalhe, formulário com validação, painel —, Playwright instalado, percorrendo as 10 fases com a flag por rota, os testes de comportamento nas duas posições, a comparação visual calibrada na primeira tela e uma violação crítica de acessibilidade plantada para a fase 9 achar; é também o primeiro uso do `comparar-visual.mjs` com navegador).

## Passo 26: fluxo 8, projeto de aprendizado

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `spike`, `necessidade` e `redesign`, pendentes de revisão do usuário.

Decisões por analogia:

- **Artefatos em `.specs/aprendizado/<slug>/`**: `plano.md` (fases 1 a 4: objetivos `O-1` a `O-3` com **Como vou provar**, **Prazo**, **Extensão**, ponto de partida, fontes com data e versão, veículo, fatias, **Fora do objetivo**, **Onde mora o código**, **Objetivos aprovados**, **Plano aprovado**), `diario.md` (fase 5: tabela de fatias com situação, degrau máximo, **Código mostrado** e se explicou; uma seção por fatia), `verificacao.md` (fase 6, **Resultado**), `notas.md` (fases 7-8, **Destino**, **Revisitar em**). Em andamento = `notas.md` sem **Destino**. Os `.md` ficam no repositório da sessão; o **código do veículo nunca** fica no repositório de um produto (padrão: pasta de estudos própria, com git próprio opcional). Diferente do spike, o código não vai para `.specs/` porque é do usuário e pode ser arquivado para consulta.
- **Cinco aprovações para oito fases** (1-2, 3-4, 5, 6, 7-8), como os blocos do spike: objetivo e ponto de partida são uma conversa só; fontes e veículo dependem um do outro (o projeto de referência inspira o veículo). Na fase 5, cada fatia fecha com uma pergunta de próximo passo (próxima, reforçar, verificação, parar) e a aprovação da fase vem com a última fatia.
- **Tutora, não autora**: na fase 5 a sessão não usa Edit nem Write nos arquivos do veículo; lê, roda para conferir, pergunta, aponta arquivo e linha, sugere quebrar de propósito e pede explicação com as próprias palavras. **Escada de ajuda** em 5 degraus (pergunta, onde olhar, conceito em palavras, pseudocódigo ou contexto análogo, exemplo mínimo), um por vez e só depois de uma tentativa. **Código só em três casos**, todos registrados na coluna **Código mostrado**: exemplo mínimo no degrau 5 (análogo, não a solução), pedido explícito do usuário (atendido sem sermão, seguido de explicação do trecho) e **andaime** listado na fase 4 como fora do objetivo (ideia do `learning-output-style`, ao contrário dele: a lógica é sempre do usuário). Fatias com código mostrado ou degrau 4-5 são as preferidas para refazer na verificação.
- **Uma pergunta por vez e pare depois dela** (do `learning-opportunities` e da postura do `brainstorming`, que não é acionado). Resposta errada recebe correção direta. **Conflito com a regra de perguntas do `CLAUDE.md` resolvido assim**: o exercício passa pela caixa de `AskUserQuestion`, mas com palpites plausíveis em ordem qualquer, **sem "(Recomendado)"** (marcar a recomendada entregaria a resposta); pedidos de explicação oferecem ações (explicar agora, quero uma dica, ainda não sei). Proposta de exceção de uma linha para o `CLAUDE.md`.
- **Ciclo da fatia** (fase 5): recordação da fatia anterior sem consulta (espaçamento), apresentar com onde ler na fonte, o usuário tenta primeiro, ajuda pela escada, revisão do que ele escreveu, quebrar de propósito com previsão, explicar com as próprias palavras, registrar. Fecha quando **funciona e foi explicada**. Testes como objetivo: a fatia começa pelo teste que o usuário escreve.
- **Objetivos verificáveis**: verbo observável e **Como vou provar** sem consulta, decididos na fase 1; é contra eles que a fase 6 avalia. Maior risco de não entender vai cedo na ordem das fatias.
- **Fontes** (fase 3) pelo `pesquisador`: documentação oficial, um tutorial ou curso, um projeto de referência (último commit e licença), com data da consulta e versão; no máximo 4 fontes no total, cada uma ligada a um objetivo.
- **Verificação** (fase 6) em três partes, **sem ensinar durante a avaliação**: refazer sem consulta (padrão: a fatia com mais ajuda), explicação como se ensinasse (escrita pelo usuário), perguntas por objetivo (por quê, e se, transferência, análise de erro). Escala atingido / parcial / não atingido com evidência; parcial volta à fase 5 com uma fatia de reforço (o **Resultado** volta a `pendente`) ou vira lacuna.
- **Prazo** como no spike: data fixa, conferida a cada retomada; vencido ou objetivo atingido antes → verificação com o que há (recomendado), fatias restantes `cortada`; no máximo uma extensão.
- **Decisão final** (fase 8): arquivar (código na pasta, para consulta), aprofundar (estudo `<slug>-2` a partir das lacunas), **aproveitar como base** (regra de promoção do spike: abrir `uso-proprio`, `projeto-novo` ou `feature` com `notas.md` como entrada, reescrita com testes, código de estudo não copiado) ou descartar (com confirmação do que será apagado). Recomendada pelo resultado da verificação.
- **Exceção à regra de testes** só enquanto o código é de estudo (já prevista no `CLAUDE.md`). Publicar o veículo é ação externa no repositório dele.
- **Modelo:** Opus em 1-4 (objetivos e escopo) e 6 (avaliação); **Sonnet na 5**, a conversa mais longa, sobre tecnologia documentada, com Opus sugerido só para uma fatia em que a explicação não assenta depois de duas tentativas ou de conceito profundo; Sonnet em 7-8.
- **Ajustes em peças existentes:** só `/fluxo` (8 pronto, atalho `aprendizado`). Nenhum agente novo: o `pesquisador` serve como está; quem avalia é a sessão (subagente não pode perguntar ao usuário).

| Fases | Peça | Origem |
|---|---|---|
| 1-2 Objetivo e ponto de partida | `aprendizado/references/plano.md` (perguntas, objetivos com prova, prazo, maior risco, modelo de `plano.md`) | nova; postura do `brainstorming` |
| 3-4 Fontes e veículo | agente `pesquisador` com o pedido de `plano.md` + conversa (2 ou 3 veículos, fatias, fora do objetivo, onde mora o código) | reaproveitada; nova |
| 5 Construção guiada | `references/tutoria.md` (pergunte e pare, ciclo da fatia, escada de ajuda, quando mostrar código, exercícios, modelo de `diario.md`) | adaptada do tlc `learning-opportunities` (CC-BY-4.0 no frontmatter, repositório MIT); `learning-output-style` (Apache 2.0) só referência |
| 6 Verificação | `references/verificacao.md` (refazer sem consulta, ensinar, perguntas por objetivo, escala, modelo) | nova; tipos de pergunta do `learning-opportunities` |
| 7-8 Registro e decisão final | `references/registro.md` (notas nas palavras do usuário, revisitar em, destino, modelo de `notas.md`) | nova; promoção como no `spike` |

Orquestrador: skill `aprendizado`. `/fluxo` marca o 8 como pronto. Bloom e learn-faster-kit (`.awesome`) ficaram só como ponteiros. **Pendente:** teste real (ex.: aprender FastAPI com autenticação por token em uma semana, veículo "lista de leituras pessoal" em 4 fatias, conferindo que a sessão não edita o veículo, que um pedido explícito de código fica registrado e que a fase 6 não dá respostas).

## Passo 27: fluxo 10, sugestão de melhoria vinda de terceiros

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `inventario`, `liberacao`, `bug`, `automacao` e `integracao-terceiros`, pendentes de revisão do usuário.

Decisões por analogia:

- **Peça comum nova: skill `demandas`** (registro único), genérica como `inventario` e `liberacao`, para os fluxos 10, 11 e 32, que começam todos por "registrar num lugar único" e "verificar se já existe". Skill, e não só formato de arquivo, porque há comportamento repetido nos três (procurar duplicados pelo problema, juntar como evidência, mudar situação com histórico, avisar o autor com confirmação, encaminhar no formato de cada destino, conferir se o trabalho ligado terminou) que divergiria se cada fluxo o reescrevesse. Ela não avalia nem decide: é do fluxo dono, como o `inventario` não planeja. Sem `fases.md` e sem aprovação própria (a aprovação é da fase do chamador).
- **Artefatos em `.specs/demandas/`**: `registro.md` (índice e painel, uma linha por demanda, com o **Objetivo do produto** no topo, usado na avaliação de valor) e uma pasta por demanda `DEM-NNN-<slug>/` com `demanda.md` (comum: tipo, fluxo dono, situação, canal, fonte, autor, interessados, **Originada de**, **Ligação**, **Revisitar em**, palavras literais, histórico, comunicações), o arquivo do fluxo dono (`sugestao.md`; reservados `solicitacao.md` e `suporte.md`) e `encaminhamento.md`. Os três fluxos usam a mesma pasta, em vez de `.specs/sugestoes/`, `.specs/solicitacoes/` e `.specs/suporte/`: um caso de suporte que traz uma ideia gera uma sugestão ligada a ele, e a busca de duplicados olha um lugar só.
- **IDs estáveis**: `DEM-NNN` sequencial, nunca reaproveitado, independente do título; colisão entre branches renumera a mais nova com registro no histórico. Pessoas: `PES-NNN` (`AUT-` já é dos critérios da automação e `P-NN` dos problemas do redesign).
- **Tipos** (como a demanda entrou): `sugestão` (sem poder de decidir), `solicitação` (quem decide e cobra), `suporte` (problema, dúvida, reclamação). O que ela **vira** (bug, feature, redesign...) é o destino do encaminhamento, em **Ligação**. Tipo trocado na triagem vira linha no histórico.
- **Situações** comuns: `recebida`, `em análise`, `aguardando autor`, `em observação`, `planejada`, `encaminhada`, `entregue`, `fechada — <desfecho>` (resolvida, recusada, duplicada de, já atendida, sem resposta do autor, desistência, parada). Espera exige **Revisitar em** (data ou gatilho). Em andamento = não começa com `fechada`. "Não resolveu" depois da entrega vira demanda nova com **Originada de**, para não reescrever o histórico.
- **Dados pessoais mínimos (LGPD)**: no repositório só `PES-NNN` e o papel; nome e contato **sempre** em `.specs/demandas/contatos.md`, fora do git (com `.specs/demandas/*/evidencias/`, linhas garantidas no `.gitignore` na primeira demanda, como o `codigo/` do spike). Sempre fora, e não só em repositório público: a visibilidade muda e o histórico do git é permanente. Contato guardado só enquanto houver demanda aberta da pessoa ou consentimento para novo contato; ao fechar a última, oferecer apagar. Ferramenta de suporte ou CRM: **Contato em** aponta para ela. Palavras do autor literais, com dado de terceiros e segredos trocados por `[removido: <tipo>]`. Base legal e prazos `PREMISSA`; não é parecer jurídico.
- **Duplicados pelo problema, não pela solução**, em três camadas (registro, trabalhos em `.specs/`, produto pelo `inventario` e `leitor-codigo`), com grau (mesmo problema, parecido, só o tema). Juntar é decisão do usuário; o autor da duplicada vira **Interessado** da original e recebe os avisos dela. Interessados são a evidência de "várias pessoas com a mesma dor".
- **Aviso ao autor** sempre redigido, mostrado e enviado só com confirmação: **eu envio** (Recomendado quando o canal é do usuário), **por um conector disponível** (dizendo para quem e por onde) ou **não avisar agora** com motivo. Modelos de recebimento, perguntas (uma mensagem só, até 4 perguntas), decisão (uma linha por decisão, inclusive recusa com motivo honesto), entrega (com "resolveu?") e fechamento. Nunca expõe outros autores, detalhe interno ou prazo não combinado.
- **Encaminhamento no formato que cada destino já aceita**, com mapa pelo problema: `bug` (`relato.md` com **Chamado por** `demanda DEM-NNN`, **Devolver após** `fechamento` e **sem** a triagem, que é do bug), `performance`, `documentar` (**Chamado por** `fluxo N <pasta>`), `feature` e `legado` (Specify partindo de `encaminhamento.md`, **Origem** no `spec.md`), `redesign`, `integracao-terceiros` e `automacao` (fase 1 deles parte de `encaminhamento.md`, **Origem** no artefato principal), segurança (`bug` P0/P1 ou `incidente`), produto novo (`projeto-novo` noutro repositório ou recusa por coerência), pedido com autoridade (fluxo 11). `encaminhamento.md` sem dado pessoal: problema, critérios de aceite Dado/Quando/Então (ponto de partida; o destino reescreve em EARS), "como saber se resolveu", fora de escopo, evidência, riscos, menor versão. A conferência de ligações usa o artefato de fim de cada destino (`integracao.md`, `fechamento.md`, **Resultado**, `Encerrado: sim`).
- **Fase 1 com a `demandas`**, que já faz a busca rápida de duplicata ao registrar (para não perguntar ao autor o que outra demanda já respondeu); a verificação completa fica na fase 3, depois de o problema estar claro, na ordem do desenho.
- **Fase 2 pergunta ao autor por mensagem**, porque a sessão não fala com ele: o usuário responde o que sabe; o resto vai numa mensagem com confirmação e situação `aguardando autor` (padrão sugerido de espera: 14 dias, `PREMISSA`). Sem resposta: seguir com confiança baixa ou fechar.
- **Fase 3 com vereditos** nova, duplicada, parecida (não juntar, avaliar junto), já atendida (com `arquivo:linha`, tela ou documentação; sem certeza é nova), já em andamento (liga ao trabalho existente), mal-entendido, é bug, é suporte, é solicitação. Segurança ou vazamento relatado sai já para a fase 8, antes da 2.
- **Fases 4 a 6 adaptadas**: RICE do `product-roadmap-prioritization` (legado) com a conta à vista, escalas de impacto e confiança, item sem objetivo do produto questionado, dizer o que sai ou atrasa; eixos do `commercial-impact-triage` (legado) aplicados ao `plano-comercial.md` do fluxo 1 (mesmas 7 seções), com "na dúvida, marque" e revisão do plano como decisão do usuário (skill `plano-comercial`); riscos de produto (demanda, adoção medida por um evento, confiança, retorno) e "menor versão que resolve" do `before-you-build` (wshobson, MIT); pré-mortem e inversão do `methods.csv` do bmad (MIT, inspiração); 2 ou 3 perguntas sobre o ponto mais incerto da conta antes da decisão, ideia do `discernment-nudge` (Apache 2.0, não acionado). Confiança acima de 50% exige mais de uma fonte: insistência de uma pessoa é alcance 1. Valor baixo pode dispensar a fase 5.
- **Decisão da fase 6 com quatro saídas**: fazer agora, planejar (sem data inventada; situação `planejada`, fase 8 quando chegar a vez), observação (gatilho e data de revisita; fases 4 a 6 voltam a `pendente` com a evidência nova), recusar. Sempre do usuário, com a recomendada primeiro.
- **Fase 7 antes da 8**, na ordem do desenho; com "fazer agora" a 8 vem em seguida. Interessados recebem o mesmo aviso, com confirmação única para o lote.
- **Fase 9 só com entrega disponível para o autor** (integrado não é liberado: conferir `liberacao.md` ou `implantacao.md`); pergunta "resolveu?"; aprendizado de uma linha comparando o estimado com o uso medido; contato oferecido para apagar.
- **Estado em `sugestao.md`** (tabela **Fases** e **Decisão**, como `terceiro.md` e `processo.md`), com exceções pela situação de `demanda.md` (aguardando autor, observação, planejada, encaminhada). Dispensas por veredito numa tabela em `fases.md`.
- **Modelo:** Opus em 2, 4, 5, 6 e 8 (conversa, juízo de valor, decisão, critérios de aceite); Sonnet em 1, 3, 7 e 9 (registro, busca, mensagem, fechamento).
- **Aprovações:** uma por fase; as operações da `demandas` não pedem aprovação própria.
- **Ajustes em peças existentes:** `feature` e `legado` (parágrafo "vinda de uma demanda": Specify a partir de `encaminhamento.md`, **Origem** no `spec.md`, aviso de fechamento ao gravar `integracao.md`), `bug` (parágrafo "vindo de uma demanda": relato sem triagem começa na fase 1-2, aviso ao relator pelo fluxo dono) e `bug/references/relato.md` (valor `demanda <DEM-NNN>` em **Chamado por**), `/fluxo` (10 pronto; `demandas` como peça que ajuda nos 11 e 32). `redesign`, `integracao-terceiros`, `automacao`, `performance` e `documentar` não mudam: recebem a entrada pelo formato que já têm, e a conferência de ligações da `demandas` acha o fim.

| Fases | Peça | Origem |
|---|---|---|
| 1 Recebimento | skill **`demandas`** (registrar, busca rápida, aviso de recebimento) + modelo de `sugestao.md` em `sugestao/references/fases.md` | nova (peça comum dos fluxos 10, 11 e 32) |
| 2 Entendimento do problema | `sugestao/references/entendimento.md` (perguntas, problema sem a solução) + `demandas` (perguntas ao autor) | nova |
| 3 Verificação | `demandas` (procurar, juntar) + `inventario` + `leitor-codigo` + vereditos de `entendimento.md` | nova; reaproveitadas |
| 4 Valor | `references/avaliacao.md` (RICE parte de valor, evidência, alinhamento, riscos de produto, eixos comerciais) | adaptada do legado `product-roadmap-prioritization` e `commercial-impact-triage`; wshobson `before-you-build` (MIT) |
| 5 Custo e risco | `references/avaliacao.md` (esforço, riscos, manutenção, coerência, pré-mortem, menor versão) + `leitor-codigo` | nova; pré-mortem do bmad `methods.csv` (inspiração); `before-you-build` |
| 6 Priorização | `references/avaliacao.md` (RICE, comparação com o registro e o trabalho aberto, perguntas sobre a conta, quatro decisões) | legado `product-roadmap-prioritization`; ideia do `discernment-nudge` |
| 7 Resposta ao autor | `demandas` (avisar, `references/mensagens.md`) | nova |
| 8 Encaminhamento | `demandas` (encaminhar, `references/encaminhamento.md`) + skill de destino | nova; reaproveitadas, ajuste de 1 parágrafo em `feature`, `legado` e `bug` |
| 9 Fechamento do ciclo | `sugestao/references/fases.md` (Fechamento) + `demandas` (conferir ligações, avisar, contato) | nova |

Orquestrador: skill `sugestao`. `/fluxo` marca o 10 como pronto. **Pendente:** teste real (ex.: num projeto de exemplo com `inventario.md`, três sugestões de uma vez — "botão de exportar para Excel" de dois clientes com palavras diferentes, que a fase 3 junta pelo problema; "modo escuro", que vai para observação com gatilho; "tem como ver o pedido de outro cliente?", que é falha de segurança e sai já para o `bug` —, percorrendo as 9 fases na primeira até o encaminhamento à `feature` e o fechamento depois da integração, conferindo que nenhum nome ou contato entra no git e que nenhuma mensagem sai sem confirmação). Os fluxos 11 e 32, ao serem construídos, usam a `demandas` e acrescentam só o arquivo próprio (`solicitacao.md`, `suporte.md`) e, se precisarem, modelos de mensagem novos.

## Passo 28: fluxo 11, solicitação de feature sob demanda

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `sugestao`, `demandas`, `feature` e `legado`, pendentes de revisão do usuário.

Decisões por analogia:

- **Irmã da `sugestao`**: mesma forma (orquestrador com 9 fases, tabela **Fases** em `solicitacao.md`, fase descoberta pela primeira não feita, com exceções pela situação de `demanda.md`; saídas; dispensas por veredito em `fases.md`) e mesma base (skill `demandas` nas fases 1, 3, 6, 7 e 9). Nenhuma pasta nova em `.specs/`: o arquivo `solicitacao.md`, já reservado, fica em `.specs/demandas/DEM-NNN-<slug>/`. Nenhum agente novo.
- **Diferença central: quem pede decide e cobra.** Por isso, **confirmação por escrito** do solicitante em três pontos (critérios na fase 2, acordo na 5, aceite na 8), com frase exata de resposta ("confirmo", "aceito"), resposta registrada (data, canal, trecho) e silêncio, conversa ou "ok, mas..." não valendo. Sem ela a fase não fecha; construir sem confirmação não é opção. Exceção: o próprio usuário é o solicitante (registrado), e a resposta dele na `AskUserQuestion` vale como escrita.
- **Data pedida não é prazo**: a fase 1 registra a data pedida e o motivo (evento, contrato, regulação); nenhuma data sai antes do acordo. Também registra **quem dá o aceite** (pode ser outra pessoa).
- **Fronteira entre esclarecimento e spec** (para não fazer o Specify duas vezes): a fase 2 produz, com o solicitante, objetivo, quem usa, hoje, indispensável × desejável, estados da jornada, casos de exceção, regras de negócio e critérios `CA-NN` em Dado/Quando/Então na linguagem dele, sem tecnologia. O Specify da `feature`/`legado` (fase 1 deles) parte de `encaminhamento.md`, traduz cada `CA-NN` em EARS citando a origem e pergunta só o técnico (dimensões implícitas, histórias, rastreabilidade, `validate_spec.py`); dúvida que mudaria um `CA-NN`, o escopo ou o prazo volta à solicitação como renegociação. ID `CA-NN` escolhido por estar livre (`AUT-`, `P-`, `O-`, `AV-`, `C-` já em uso).
- **Triagem depois do esclarecimento**, na ordem do desenho (a busca rápida da `demandas` na fase 1 já pega o óbvio): feature nova, ajuste, é bug, já existe, já em andamento, duplicada/parecida (juntar só se os `CA-NN` cabem), outro fluxo; checagens curtas de conflito, regra de negócio, dados (LGPD `PREMISSA`), segurança e custo (eixos comerciais da `sugestao` quando há plano). Segurança ou vazamento relatado sai já, antes da fase 2.
- **Estimativa** (fase 4) do `effort-estimation` (legado, citado): por parte com a complexidade que justifica, faixa P/M/G/GG e confiança, capacidade conhecida ou "não informada", risco de prazo nomeado, incerteza que impede estimar vira `spike`; inclui testes, proteção, verificação e liberação. **Opções** (2 ou 3, nunca de enfeite): mínima agora e completa depois, parcial por menos, completa, cada uma com os `CA-NN` cobertos; "mais barato que construir" uma vez antes (do `tlc-prd`). Opções vão ao solicitante, que escolhe.
- **Acordo** (fase 5) com versões: escopo (`CA-NN`), adiado (cada item vira demanda nova `planejada` com **Originada de**), prazo com confiança e condição, 2 a 4 **marcos** ligados a fases do destino, forma do aceite, o que conta como desvio. Comparação com o trabalho em andamento e "o que sai ou atrasa" (como na `sugestao`); conflito entre solicitantes é decisão do usuário, nunca da sessão. Renegociação gera versão nova confirmada por escrito.
- **Execução** (fase 6) pela operação **Encaminhar** da `demandas`, com os `CA-NN` em `encaminhamento.md`; feita quando o artefato de fim do destino existe e cada `CA-NN` liga a um critério com PASS em `validation.md`.
- **Acompanhamento** (fase 7) corre junto com a 6 (`em andamento` as duas): atualização em cada marco; **desvio avisado na hora**, com 2 opções (cortar desejável e manter data, ou manter escopo com nova data); pedido novo no meio vira demanda nova. `feature` e `legado` lembram o marco ao fechar a fase ligada a ele.
- **Aceite** (fase 8) **antes de liberar para todos** (staging, local ou produção com flag só para o solicitante), roteiro de um passo por `CA-NN` com dados de exemplo. Critério não atendido → `bug` (o `CA-NN` como esperado); **ajuste pequeno** (não muda `CA-NN` nem prazo, cabe em P) → `feature` `<slug>-ajuste-N`; mudança de escopo → nova `DEM-NNN`.
- **Entrega** (fase 9): `liberacao` ou `implantacao` (o `legado` já libera na fase 8 dele, depois do aceite), contexto e documentação de uso conferidos, comunicado com o adiado e seus IDs, aprendizado estimado × real, `fechada — resolvida`, contato oferecido para apagar.
- **Mensagens próprias** em `solicitacao/references/mensagens.md` (entendimento, opções, acordo, atualização, desvio, aceite), complementando as da `demandas`, com as mesmas regras de envio com confirmação.
- **Modelo:** por analogia com a `sugestao`, Opus nas fases de conversa e juízo (2 esclarecimento, 4 estimativa e opções, 5 negociação); Sonnet em 1, 3 (busca em Haiku), 7, 8 e 9; na 6 vale o modelo de cada fase do destino.
- **Ajustes em peças existentes:** `/fluxo` (11 pronto); `feature` e `legado` (parágrafo "vinda de uma demanda": `CA-NN` já confirmados, Specify só técnico, volta à solicitação se mudar o combinado, lembrete de marco; no `legado`, liberação para todos espera o aceite); `sugestao` (saída "é solicitação" aponta a skill); `demandas` (tabela de tipos, campo **Fluxo** do modelo, linha do fluxo 11 no mapa de destinos, mudança de escopo na solicitação, modelos de mensagem do fluxo dono).

| Fases | Peça | Origem |
|---|---|---|
| 1 Recebimento | skill `demandas` (registrar, busca rápida, aviso) + modelo de `solicitacao.md` em `solicitacao/references/fases.md` | reaproveitada; nova |
| 2 Esclarecimento | `solicitacao/references/esclarecimento.md` (situação do pedido, rodadas, tipos dor/ausência/construção, jornada, exceções, regras de negócio, `CA-NN`, fronteira com o Specify, confirmação por escrito) + mensagem de entendimento | adaptada do tlc `tlc-prd` (CC-BY-4.0) e do bmad `ticket-template` (MIT); legado `requirement-elicitation`; ideia da extensão `grill` do spec-kit (MIT, só README) |
| 3 Triagem | `demandas` (procurar) + `inventario` + `leitor-codigo` + classificação e checagens de `esclarecimento.md` | reaproveitadas; nova |
| 4 Estimativa e opções | `solicitacao/references/acordo.md` (por parte, faixa, confiança, capacidade, spike, opções) + `leitor-codigo` + `spike` | legado `effort-estimation`; "mais barato que construir" do `tlc-prd` |
| 5 Negociação e prioridade | `acordo.md` (comparação, o que atrasa, acordo com versões, marcos, adiado como demanda nova) | nova; "o que sai ou atrasa" como na `sugestao` |
| 6 Execução | `demandas` (encaminhar) + `feature`/`legado`/`bug`/demais | reaproveitadas, ajuste de 1 parágrafo em `feature` e `legado` |
| 7 Acompanhamento | `solicitacao/references/acompanhamento.md` + mensagens de atualização e desvio | nova |
| 8 Aceite | `acompanhamento.md` (demonstração por `CA-NN`, ajuste × bug × escopo) + `bug`/`feature` | nova |
| 9 Entrega e fechamento | `acompanhamento.md` + `liberacao`/`implantacao` + `demandas` (avisar, fechar, contato) | reaproveitadas |

Orquestrador: skill `solicitacao`. `/fluxo` marca o 11 como pronto. **Pendente:** teste real (ex.: num projeto de exemplo com `inventario.md`, o gestor pede "relatório de vendas por vendedor até o dia 30, para a reunião de metas": data pedida registrada sem promessa; esclarecimento com 4 `CA-NN` e um desejável (exportar); confirmação por escrito simulada; triagem acha uma consulta parecida existente; opções mínima × completa; acordo com 3 marcos e o exportar adiado como DEM nova; `feature` com o Specify traduzindo os `CA-NN` sem repetir perguntas; um desvio no reconhecimento avisado antes do marco; aceite com um ajuste de rótulo e um pedido novo virando DEM; conferindo que nenhum nome ou contato entra no git e nenhuma mensagem sai sem confirmação).

## Passo 29: fluxo 32, suporte ao cliente

**Status:** construído em 2026-10-23 por subagente, seguindo `ROTEIRO-CONSTRUCAO.md`; decisões tomadas por analogia com `sugestao`, `solicitacao`, `demandas`, `bug` e `incidente`, pendentes de revisão do usuário. Último dos 21 fluxos: `/fluxo` tem todos **Pronto**.

Decisões por analogia:

- **Irmã da `sugestao` e da `solicitacao`**: mesma forma (orquestrador com 9 fases, tabela **Fases** em `suporte.md`, fase descoberta pela primeira não feita nem dispensada, com exceções pela situação de `demanda.md`; saídas; dispensas por veredito em `fases.md`) e mesma base (skill `demandas` nas fases 1, 3, 5, 6, 7 e 9). O arquivo `suporte.md`, já reservado, fica em `.specs/demandas/DEM-NNN-<slug>/`. Nenhum agente novo.
- **Base de conhecimento em `.specs/demandas/base-conhecimento.md`**, e não em `.specs/suporte/`: a contagem de casos repetidos vem do registro de demandas, a busca de duplicados da `demandas` passa a olhar também a base, e não se cria pasta nova. Entradas `BC-NNN` (ID livre) no formato pergunta em uma frase e resposta em uma ou duas, com fonte oficial e incerto marcado (do `internal-comms`), **Tag**, **Contagem**, **Casos**, **Vale para** e **Revisada em**; tabela **Problemas conhecidos** (bugs abertos com contorno); **Combinados** do projeto no topo (prazo da próxima notícia por prioridade, espera por resposta, janela de repetição, alçadas por papel e canal, sem nomes). Entrada que deixou de valer não se apaga.
- **Tags de causa raiz com vocabulário fixo** (`clareza`, `documentacao`, `defeito`, `conta`, `cobranca`, `terceiro`, `desempenho`, `falta-funcao`, `expectativa`, `seguranca`), cada uma com o sinal para o produto, para a contagem funcionar. **3 ou mais casos com a mesma causa e tema** numa janela de 90 dias (`PREMISSA`), como a recorrência da skill `bug` e o `bug-documentation` do legado, viram sugestão interna (autor `equipe`, **Originada de**, os casos como evidência) na skill `sugestao`, ou os autores entram como **Interessados** de uma sugestão existente (que sai de observação): assim "pedidos recorrentes viram prioridade".
- **Tipos** do desenho (dúvida de uso, bug, pedido de feature, cobrança, conta, segurança); reclamação é tom, não tipo. **Prioridade P0–P3 pela escala da skill `bug`**, vista por quem usa, justificada por impacto e contorno, nunca pela insistência. Primeira resposta diz o prazo da **próxima notícia**, nunca o da solução.
- **Verificação rápida** em quatro camadas (base, casos anteriores pela `demandas`, bugs abertos e runbook, incidentes abertos), com **falha em andamento** detectada por incidente aberto ou 3 casos iguais em poucas horas (`PREMISSA`) ou liberação recente na função: o caso liga ao incidente em vez de diagnosticar a pessoa.
- **Acesso mínimo e registrado**: reproduzir com dados de exemplo primeiro; conta real só se preciso, em modo leitura, pelo meio previsto do projeto, com confirmação antes de cada acesso e linha na tabela **Acessos** (`A-N`, o quê sem o dado visto, onde, por quê, como, quem autorizou). Escrita na conta é ação externa com valor anterior e como desfazer; correção em massa ou por script é mudança de comportamento (skill `bug` ou `feature`, com teste). Nunca pedir senha, código de verificação ou dado de cartão.
- **Bug pelo contrato do fluxo 32 que a skill `bug` já tinha**: `relato.md` **com** a triagem (o suporte reproduziu com a pessoa), **Chamado por** `suporte DEM-NNN`, **Devolver após** `liberação`; a `bug` começa na reprodução e devolve com `fechamento.md` curto deixando o aviso ao suporte. Não o contrato "vinda de demanda" (sem triagem, devolver após fechamento), que fica para sugestão e solicitação. A pessoa recebe contorno e expectativa honesta, sem data inventada; mais casos do mesmo bug viram **Interessados**.
- **Incidente**: caso ligado sai de espera com `Estável: sim` no `incidente.md` (a pessoa não espera o post-mortem); os casos ficam em **Casos de suporte** do incidente e são avisados pela skill `suporte`. **Segurança** em três saídas: exploração ou vazamento agora → `incidente`; defeito localizado → `bug` P0/P1; suspeita ampla → `auditoria-seguranca`. Sempre antes do diagnóstico e sem detalhe da falha à pessoa.
- **Comunicação** com regras próprias em `suporte/references/mensagens.md` (o mais importante primeiro, sem culpar ninguém, admitir o erro nosso com desculpa curta, incerteza dita, posição oficial passada a quem decide, uma mensagem de perguntas só) e modelos de solução, contorno, falha conhecida, escalonamento, lembrete, decisão negativa, mais os da `demandas`. Toda mensagem enviada só com confirmação.
- **Confirmação** fecha só com "resolveu" ou prazo vencido: espera de 3 dias úteis com um único lembrete (`PREMISSA`, ajustável nos combinados); não resolveu volta ao diagnóstico sem repetir perguntas; na terceira volta, oferecer escalar. Caso reaberto depois de fechado é demanda nova com **Originada de**.
- **Escalonamento acionável de qualquer fase** (2, 4, 5): a fase 8 começa `pendente` e só entra na conta da fase atual quando `em andamento`; sem uso, `dispensada — não precisou`. **Pacote de passagem** adaptado do `on-call-handoff-patterns` (situação agora, o que sabemos, o que já foi feito, o que precisa ser decidido, quem é quem, retorno), sem dado pessoal no git e com **Retorno esperado em**. Cobrança, contrato, legal, pedido do titular (LGPD) e acesso de terceiro à conta vão a quem decide; a sessão não promete valor nem interpreta a lei.
- **Modelo:** Opus nas fases 2, 4, 5 e 8 (triagem, diagnóstico, decisão de resolução, passagem); Sonnet em 1, 3, 6, 7 e 9. Em P0, nenhuma troca de modelo é pedida e a aprovação é curta (como nas fases 1 a 3 do `incidente`).
- **Ajustes em peças existentes:** `/fluxo` (32 pronto, atalho `atendimento`); `demandas` (tabela de tipos e campo **Fluxo** apontando a skill, `base-conhecimento.md` em "Onde fica" e na camada do registro do **Procurar**, nota do contrato do suporte com o `bug` e do `Estável: sim` do incidente em `encaminhamento.md`, modelos do fluxo dono em `mensagens.md`); `bug` (frase: do suporte o relato chega com triagem; `relato.md` com `suporte <DEM-NNN>`); `incidente` (entrada "vindo do suporte", campos **Origem do relato** `demanda DEM-NNN` e **Casos de suporte**, aviso pela skill `suporte` em `comunicacao.md`); `sugestao` (saída "é suporte" passa à skill `suporte` quando a pessoa tem um problema).

| Fases | Peça | Origem |
|---|---|---|
| 1 Recebimento | skill `demandas` (registrar, busca rápida, aviso) + modelo de `suporte.md` em `suporte/references/fases.md` + mensagem "recebimento" | reaproveitada; nova |
| 2 Classificação | `suporte/references/atendimento.md` (tipos, P0–P3 da skill `bug`, combinados) | nova; escala do `bug` |
| 3 Verificação rápida | `atendimento.md` + `base-conhecimento.md` + `demandas` (procurar) + `.specs/bugs/` e `.specs/incidentes/` | nova; reaproveitadas |
| 4 Diagnóstico | `atendimento.md` (reprodução, acesso mínimo com tabela **Acessos**, perguntas uma vez) + `leitor-codigo` | nova |
| 5 Resolução | `atendimento.md` + `demandas` (encaminhar) + skill `bug` (contrato do fluxo 32) | nova; relato com o rigor do legado `bug-documentation` |
| 6 Comunicação | `suporte/references/mensagens.md` + `demandas` (avisar) | nova; princípios do `internal-comms` (Apache 2.0) |
| 7 Confirmação | laço "pessoa não responde" em `fases.md` + mensagens de lembrete e fechamento | nova |
| 8 Escalonamento | `suporte/references/escalonamento.md` (alçadas, pacote de passagem) | adaptada do wshobson `on-call-handoff-patterns` (MIT) |
| 9 Aprendizado | `suporte/references/base-conhecimento.md` (tags, contagem, base, sugestão interna) + `sugestao` + `demandas` | nova; limiar de 3 do legado `bug-documentation`; formato pergunta e resposta do `internal-comms` |

Orquestrador: skill `suporte`. `/fluxo` marca o 32 como pronto; nenhuma skill diz mais "em preparação" sobre outro fluxo. **Pendente:** teste real (ex.: num projeto de exemplo com `inventario.md`, três casos — "não acho onde muda a senha" (dúvida de uso, vira `BC-001`; dois casos depois com a mesma tag `clareza` geram a sugestão interna no terceiro); "fui cobrado duas vezes" (cobrança, acesso de leitura registrado, escalonamento com pacote de passagem e retorno); "o relatório sai em branco desde ontem" (bug reproduzido, relato com triagem à skill `bug`, contorno à pessoa, devolução após a liberação e confirmação) —, conferindo que nenhum nome, contato ou dado da conta entra no git e que nenhuma mensagem sai sem confirmação). O "Estado ao fim da rodada" abaixo ainda descreve a primeira rodada (4 de 21) e precisa ser atualizado pela sessão principal.

---

## Passo 30: limpeza do projeto

**Status:** feito em 2026-10-23, a pedido do usuário ("remover tudo que não está sendo utilizado; manter `.claude_legado`").

| Removido | Motivo |
|---|---|
| 9 clones de referência (`.tlc`, `.superpowers`, `.speckit`, `.bmad`, `.openspec`, `.wshobson`, `.anthropic-skills`, `.anthropic-plugins`, `.awesome`), ~165 MB fora do git | Nenhum fluxo os lê; serviram para o levantamento e a adaptação. O código adaptado é conferido no GitHub (`adaptado` no `fontes.json`) e cada `ATRIBUICAO.md` guarda origem e commit. Saíram as 9 entradas `referencia` do `fontes.json`, as linhas do `.gitignore` e a menção no `CLAUDE.md`. O tipo `referencia` continua suportado pelo `verificar-atualizacoes.py`, se um clone voltar. |
| `.rascunho/teste-1-cuidados/` | Arquivo do teste 1, só citado como histórico; fica no histórico do git. |
| `__pycache__` de `.claude/scripts` | Gerado. |

Mantidos: `.claude`, `.claude_legado`, `.agents` (lock do `tlc-spec-driven`), `.specs` (`testes.json`) e, em `.rascunho`, `DECISOES.md`, `DESENHO-FLUXO-1.md`, `FLUXO-*.md` (citados pelas skills), `ROTEIRO-CONSTRUCAO.md` e `REAPROVEITAMENTO.md` (citado em atribuições). Os caminhos de clone citados no `REAPROVEITAMENTO.md` e nas atribuições ficam como registro histórico.

---

## Passo 31: instalador dos fluxos

**Status:** construído em 2026-10-23. Pergunta do usuário: começar um projeto numa pasta vazia já com os fluxos. Escolha do usuário: instalador agora; plugin depois dos testes reais (a reforma do plugin muda `CLAUDE.md`, rules, caminhos de scripts e permissões).

`.claude/scripts/instalar.py <pasta>`: cria a pasta, faz `git init` se não for repositório, copia a `.claude` sem `.cache`, `__pycache__` e `settings.local.json`, completa o `.gitignore` e grava `.claude/.instalacao.json` (origem, commit, data, hash de cada arquivo). Não cria `.specs`. `--atualizar` substitui só o que o projeto não mudou, lista conflitos (`--forcar` sobrescreve), apaga o que saiu dos fluxos se não foi mudado e nunca toca arquivo criado pelo projeto; `--simular` mostra antes. Avisa se faltar `git`, `node` ou o plugin superpowers na conta. 22 testes, com injeção de falha conferida (3 mutações pegas). O `contexto-ia.md` passou a excluir `.claude/CLAUDE.md` da busca de contexto do projeto.

---

## Passo 32: mockup oferecido sempre que houver tela

**Status:** feito em 2026-10-24. Falta sentida pelo usuário ao criar um módulo de uso pessoal: não havia mockup para ver a tela. Só o fluxo 1 fazia mockup como fase; o fluxo 2 dizia "só se o usuário pedir" (ninguém oferecia) e os fluxos 3 e 4 não tinham. Escolha do usuário: **oferecer sempre que houver tela**, com "fazer o mockup" recomendado.

| Onde | Mudança |
|---|---|
| `reconhecimento` | Campos **Telas** e **Mockup** (`não se aplica`, `pendente`, `aprovado`, `dispensado — motivo`). |
| `feature` | Fase 2b Mockup (antes do plano) quando **Mockup** `pendente`; plano segue o mockup; comparação na verificação; promoção na integração. |
| `legado` | Fase 3b Mockup (antes da rede de proteção), mesma lógica; promoção no registro. |
| `uso-proprio` | Fase 4 pergunta depois do Specify; decisão em `necessidade.md` (**Mockup**); comparação na fase 7. |
| `mockup-visual` | **Modo módulo** (`references/modulo.md`): pasta `.specs/features/<feature>/mockup/`, sem direções quando o projeto já tem guia (token novo proposto à parte), guia mínimo que reproduz a aparência atual quando não tem, todas as telas do módulo com estados numa aprovação, promoção para `.specs/mockup/` na integração. |

Teste estrutural novo em `test_skills.py` (feature, legado e uso-proprio citam a `mockup-visual`; reconhecimento tem **Mockup**; modo módulo existe), escrito antes da mudança e visto falhando.

---

## Passo 33: marcos de troca de sessão

**Status:** feito em 2026-10-24. Motivo: num projeto real (POC de cuidado com medicação), a sessão principal chegou a 397,8 mil tokens de contexto durante a construção, com um lote por agente de 16 a 28 minutos. Escolha do usuário: instituir marcos e trocar de sessão.

- **Regra no `CLAUDE.md`** (vale para todos os fluxos, sem editar as 21 skills): nos marcos (próxima fase pede outro modelo; antes da construção; a cada 2 ou 3 lotes; antes da verificação e da integração ou liberação; conversa com 3 fases ou mais), a pergunta de fim de fase oferece **seguir numa sessão nova (Recomendado)**.
- **Procedimento** em `.claude/skills/fluxo/references/marcos.md`: conferir que as decisões estão em artefato, gravar `## Retomada` no `.specs/STATE.md` (fluxo, item, fase aprovada e data, próxima fase e modelo, lote da construção, o que foi combinado e não está em artefato) e orientar `/clear` e `/fluxo`.
- **`/fluxo`** lê `## Retomada` antes do menu e oferece retomar; se a retomada e os arquivos discordarem, valem os arquivos.
- **Memória da conversa eliminada:** `feature` e `legado` davam o plano por aprovado com "aprovação nesta sessão"; agora o `reconhecimento.md` tem **Plano aprovado em**. Teste estrutural impede a volta dessa dependência.

A sessão não mede o próprio contexto nem abre outra sessão: ela recomenda; o `/clear` é do usuário.

---

## Passo 34: trava de modelo

**Status:** feito em 2026-10-24. Pedido do usuário: não seguir no modelo errado quando o aviso de `/model` passa despercebido. Escolha: regra (não hook), nos dois sentidos.

Regra no `CLAUDE.md` (seção Modelos): ao entrar numa fase ou retomá-la, a sessão compara o próprio modelo (nome nas instruções de sistema) com o que a fase pede; diferente, pergunta **antes de qualquer trabalho da fase**: trocar (recomendado; a sessão para até `/model`) ou seguir assim. Opus pedido e Sonnet em uso: perde qualidade; Sonnet pedido e Opus em uso: só custa mais. Seguir assim vale para a fase e fica em `.specs/STATE.md`, seção `## Modelo`. O `/fluxo` e o procedimento de marcos aplicam a trava na retomada. Subagentes têm modelo fixo.

Não é hook: até onde se sabe, o hook não recebe o modelo da sessão de forma confiável, e teria de deduzir a fase pelos arquivos (não conferido na documentação). Teste estrutural garante que a regra continue no `CLAUDE.md`, no `/fluxo` e nos marcos.

---

## Passo 35: instalação local (repositório corporativo)

**Status:** feito em 2026-10-24. Pergunta do usuário: usar os fluxos num projeto corporativo sem nunca subir para o git de lá, num repositório que já tem a própria `.claude`. Escolha: modo local no instalador.

Conferido na documentação do Claude Code (2026-10-24): ganchos e `permissions.allow` do `settings.local.json` se somam aos do `settings.json` do projeto; `CLAUDE.local.md` na raiz é carregado junto do `CLAUDE.md`; o Claude Code só ignora o `settings.local.json` sozinho quando é ele que o cria. Não coberto pela documentação: skills ignoradas pelo git carregarem normalmente (esperado, pois a leitura é da pasta; confirmar no primeiro uso).

`instalar.py <repo> --local`: exige repositório git; recusa a instalação inteira em conflito de nome, sem escrever nada; não copia os nossos `CLAUDE.md` e `settings.json`: as regras vão para um bloco marcado no `CLAUDE.local.md` (com regras próprias do modo local: não versionar, não mexer no `.gitignore`, evitar `git clean -X`, contexto do projeto anotado no `CLAUDE.local.md` e não no `CLAUDE.md` do time), e ganchos e permissões são somados ao `settings.local.json` (o que foi somado fica no manifesto e sai na atualização seguinte); cada arquivo instalado, a `.specs/`, o `CLAUDE.local.md` e o `settings.local.json` entram num bloco do `.git/info/exclude`. `--atualizar` segue o modo do manifesto. 10 testes novos (inclui `git status` limpo depois de instalar, atualizar e criar `.specs`), com 4 defeitos injetados pegos; teste de fumaça num repositório que imita o corporativo.

Cuidados para o usuário: `git clean -fdX` apaga os fluxos e os artefatos; conferir a política de uso de IA da empresa.

---

## Estado ao fim da rodada (2026-10-23)

**Fluxos prontos (21 de 21):** os 4 da rodada anterior e, nesta rodada (passos 13 a 29, construídos em sequência por um agente por fluxo, revisados e commitados um a um): 12 Bug, 9 Incidente, 17 Spike, 25 Escolha de tecnologia, 16 Auditoria de segurança, 24 Revisão de código, 13 Refatoração, 5 Performance, 14 Documentar, 27 Avaliar terceiros, 6 Integração, 30 Automação, 7 Redesign, 8 Aprendizado, 10 Sugestão (com a peça comum `demandas`), 11 Solicitação, 32 Suporte. Material de terceiros escolhido em `.rascunho/REAPROVEITAMENTO.md` e adaptado com registro em `fontes.json`; roteiro de construção em `.rascunho/ROTEIRO-CONSTRUCAO.md`.

**Testado de verdade:** fluxo 1 nas fases 1 a 6 (teste 1). Os 17 fluxos novos foram percorridos só no papel. Scripts com 74 testes automatizados (inclui o teste estrutural das skills, `varredura-seguranca.py`, `propriedade-git.py` e `comparar-visual.mjs`, que exige `node` no PATH).

**Próximas rodadas:**

1. Teste real dos fluxos, começando pelos de base: bug, revisão de código, spike e escolha de tecnologia. Cada passo 13 a 29 descreve o teste sugerido.
2. Conferir as `PREMISSA` legais (LGPD/ANPD em incidente, integração e avaliação de terceiros) com uma pessoa antes de uso real.
3. Fase 12 do fluxo 1 (operação e aprendizado).
4. Confirmar o hook de atualizações numa sessão aberta do zero.
5. Atualizar o superpowers para 7.x (via `/plugin`).
6. Empacotar como plugin quando estável (rules viram skill ou hook).
7. Antes de qualquer push deste repositório: olhar o commit `d273d66` (senhas de teste e URL de postgres no histórico, achadas pela varredura) e rodar `python .claude/scripts/trava-testes.py --rodar`.

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

### Status de progresso (tarefas concluídas)

- **Pedido:** ter, entre fases e entre sessões, algo como "Faltam 45 de 180 tarefas: 75% concluído".
- **Decisão:** script `progresso.py` (só lê) + skill `/progresso`. Conta os títulos `### T<n>:` de todos os `tasks.md` em `.specs/`; tarefa concluída = todas as caixas `Done when` marcadas (sem caixas, `**Status**` concluído; caixa aberta vence o status). Duas linhas: item atual (argumento, `## Retomada` ou o único item em aberto) e projeto todo.
- **Onde aparece:** resumo de fim de fase (regra no `CLAUDE.md`), `/progresso` sob demanda, campo **Progresso** da `## Retomada` e repetição pelo `/fluxo` ao retomar. Antes de haver tarefas, mostra só a fase do fluxo, sem percentual.
- **Por quê:** o `tlc-spec-driven` não fixa o formato da marca de concluída; as caixas `Done when` são o que ele já exige marcar no mesmo commit da tarefa. Não se edita o pacote.
- **Limites aceitos:** só conta o que já está em `tasks.md` (o total cresce quando se planeja feature nova); todas as tarefas pesam igual.
- **Conta correta:** concluídas ÷ total. O exemplo do pedido ("faltam 45 de 180: 25%") invertia o percentual; 45 faltantes de 180 são 75% concluído.

### Roadmap por unidade (progresso de projetos que não detalham tudo em tasks.md)

- **Motivo:** o primeiro uso do `/progresso` em três projetos reais mostrou o limite do `tasks.md`: o ControleEmCasa conduz o trabalho por 18 etapas grandes (`.md/PLANO.md`) e mostrou "Sem tarefas ainda"; o Gestão da Pelada mostrou 96% de uma feature entre 8. O `tasks.md` só cobre o já detalhado.
- **Decisão:** `.specs/projeto/roadmap.md`, tabela com uma linha por etapa ou feature e coluna **Situação** de vocabulário fixo (`Concluída`, `Em andamento`, `Não começada`). O `progresso.py` mostra a linha **Plano** (e **Em andamento**) antes das linhas de tarefas. Quem aprova a unidade troca a Situação no mesmo commit.
- **Por quê assim:** converter etapas grandes em `tasks.md` daria tarefas sem critério de pronto; um vocabulário fixo evita adivinhar a situação de texto livre. Sem roadmap, nada muda.
- **Também corrigido no mesmo uso:** campo **Item** da Retomada com texto depois do caminho; saída em UTF-8 em pipe no Windows; resposta da skill em formato único, sem análise própria.

### Roteiro acima da feature e vocabulário único

- **Motivo:** o `/progresso` em três projetos reais mostrou três quebras diferentes do mesmo tipo de trabalho: 8 features (Gestão da Pelada), 18 etapas em `PLANO.md` fora dos fluxos (Controle em Casa) e uma feature de 170 tarefas em 20 Phases (Evolução Segura). O processo só definia o nível da feature (`tlc-spec-driven`); faltava quem quebra o produto em features, em que ordem e de que tamanho.
- **Decisão:** skill `roteiro`, fase **6b** (fluxo 1) e **3b** (fluxo 2), que quebra o escopo em features fatiadas na vertical e grava `.specs/projeto/roadmap.md` mais um `AD-NNN` no `STATE.md`. Pula sozinha quando o escopo cabe em uma feature. Nos fluxos 3 e 4 entra antes do Specify se o pedido for grande demais. Só a próxima feature recebe spec, design e tarefas.
- **Numeração:** "6b" e "3b" em vez de renumerar as fases, para não mexer em `Retomada`, tabelas, hooks e artefatos já gravados nos projetos.
- **Vocabulário (`CLAUDE.md`):** roteiro, feature, fase do fluxo, Phase (termo do tlc, mantido) e tarefa. "Etapa" não é termo novo: projetos que a usam mantêm o rótulo na coluna do roadmap.
- **Limite:** 80 tarefas por feature. É aviso do `progresso.py` (não bloqueio) e fica fora dos validadores do pacote `tlc-spec-driven`, que não se edita. Referências: fundação do Pelada 49, conta-e-acesso 44, Evolução Segura 170.
- **Fora desta decisão:** o `/progresso` ler os `tasks.md` da branch ou do worktree em que a construção está (hoje lê só a pasta em que roda).

### Tamanho da tarefa em vez de limite de quantidade (substitui o limite de 80 tarefas)

- **Decisão do usuário:** não limitar quantas tarefas uma feature tem; limitar o **tamanho de cada tarefa**, buscando sempre a menor possível, com meta de **até 2 horas de trabalho humano**.
- **Aplicação:** seção `## Tarefas` do `CLAUDE.md` (vale para todo `tasks.md` e prevalece sobre o tamanho sugerido pelo tlc). Toda tarefa leva `**Estimativa**: <N>h` (ou `<N> min`) logo depois de **What**; acima de 2h, divide-se a tarefa. As skills `feature`, `legado`, `projeto-novo` e `uso-proprio` repetem a regra na linha em que o `tasks.md` é criado.
- **Verificação:** o `progresso.py` avisa tarefa acima de 2h (`LIMITE_HORAS`) e, só em `tasks.md` que já usa o campo, tarefa sem estimativa. `tasks.md` antigo, sem nenhuma estimativa, fica quieto. O aviso não bloqueia. O validador do pacote tlc segue intacto e aceita o campo extra.
- **Efeito no roteiro:** a skill `roteiro` deixa de dimensionar feature por contagem de tarefas. P, M e G viram tamanho relativo (soma das estimativas); o critério para dividir uma feature é ela não se validar e liberar como uma unidade.
- **Testes substituídos:** os testes do aviso por contagem (`TestAvisoDeFeatureGrande`) foram escritos na mesma sessão e trocados pelos de estimativa (`TestEstimativa`) por decisão do usuário; nenhum teste foi enfraquecido para passar.
- **Medida antes da decisão** (validador do tlc nos três projetos): 0 erros; Phases com mediana de 3 a 9 tarefas; nenhuma tarefa de código sem teste. O número de tarefas (49, 44 e 170) não era o problema; o tamanho de cada tarefa ainda não era medido em nenhum deles.
- O limite de 80 do registro anterior ("Roteiro acima da feature") fica sem efeito.

### Execução por lote com relato por tarefa, visibilidade e revisão por risco

- **Motivo:** a sensação de fluxo longo, sem visibilidade e mais lento. Lido o `implement.md` e o `sub-agents.md` do tlc contra o `EXECUTION-FLOW.md` do legado: não há troca de contexto dentro da tarefa (o mesmo agente escreve o teste, implementa, roda o gate e se revisa); o custo está na cerimônia por tarefa (premissas, plano, duas tabelas de adequação com `arquivo:linha`), na ausência de paralelismo e no número de tarefas, que a regra de até 2h multiplicou. Hipótese, não medida.
- **Histórico:** uma primeira versão (um trabalhador por tarefa, execução inline permitida) foi implementada e desfeita a pedido do usuário no mesmo dia; esta é a versão refeita com duas mudanças dele.
- **Decisões do usuário (S6, lotes paralelos, descartada por ora):**
  1. **Sem execução inline: sempre por subagente, um lote por vez** (seção `## Execução` do `CLAUDE.md`, com precedência sobre o `sub-agents.md` do tlc). Some a oferta de subagentes e a pergunta sobre isso (o que era o S5). Feature pequena é um lote só; a skill do fluxo pode restringir mais (performance: uma tarefa por vez).
  2. **A execução continua por lote, e o agente relata o V2 de cada tarefa:** depois de cada commit o trabalhador roda `progresso.py --tarefa` e devolve uma linha por tarefa. Limite aceito: o subagente só devolve texto ao terminar, então o usuário lê as linhas no fim do lote; ao vivo, só com `/progresso` em outro terminal. A sessão principal acrescenta o V2 do lote (`--lote`). O trabalhador é o `implementador-dominio` se o lote tiver alguma tarefa de risco alto (ou sem o campo), senão o `implementador`.
  3. **V1 e V3** no `/progresso`: Produto, Feature atual, Phase atual, Tarefa atual (primeira pendente com dependências prontas), Última tarefa, Ritmo e previsão. A previsão multiplica as horas estimadas pendentes pelo fator real ÷ estimado das últimas 10 tarefas medidas (as estimativas são de trabalho humano, o tempo real é do agente: o fator calibra a diferença). A linha **Projeto** só aparece com mais de um `tasks.md`. O tempo vem do `git log` do `tasks.md` (intervalo entre conclusões consecutivas; acima de 90 min é pausa e fica "não medido"): dentro de um lote é preciso; na primeira tarefa do lote inclui o que a sessão principal fez desde a anterior.
  3b. **Rótulos:** `Plano` virou `Produto` e `Item atual` virou `Feature atual`, para casar com o vocabulário do `CLAUDE.md`.
  4. **S3, lote por horas:** Phases inteiras somando até 14h de Estimativa (7 tarefas de 2h, a capacidade que o tlc calibrou; sem estimativa a tarefa conta 1h; cauda de até 2 tarefas se junta ao lote anterior).
  5. **S4, hook `commit-msg`:** o `instalar.py` grava o hook que roda o `check_commit.py` **só nos commits do Claude Code** (variável `CLAUDECODE=1`, que o Claude Code define nos comandos que executa); commit manual, `Merge`, `Revert`, `fixup!` e `squash!` passam. Nunca sobrescreve hook do projeto nem mexe com `core.hooksPath` em uso. Procura `python3`, `python` e `py` e ignora o que não roda (o atalho da Microsoft Store), para nunca bloquear commit por falta de Python.
  6. **S1 e S2, revisão por risco:** novo campo `**Risco**: alto|baixo` (ausente = alto) depois de Estimativa. O gate roda sempre. Risco baixo: uma linha por critério (`critério → arquivo:linha`). Risco alto: uma linha por critério e caso limite com a asserção, mais `Órfãos:`. Baixo que toque autenticação, SQL, entrada externa, CI, dependência, segredo ou log vira alto. As linhas ficam no trabalho do trabalhador (o retorno só traz o que reprovou) e o `verificador` continua conferindo todas as tarefas por inteiro no fim da feature. Isto **substitui o passo 6.4 do `implement.md`** (um "hard gate" do tlc) por precedência do `CLAUDE.md`, como já foi feito com o tamanho da tarefa; a regra de Testes inegociável não muda.
- **Testes alterados por esta decisão (4 testes de `test_progresso.py`, motivo: rótulos e formato do V3 aprovados pelo usuário):** `test_item_atual_vem_da_retomada...` (`Item atual (` virou `Feature atual (`), `test_plano_aparece_antes_das_tarefas` (`Plano:` virou `Produto:` e a linha `Projeto:` some quando repete a feature), `test_so_roadmap_sem_tarefas...` (`Plano:` virou `Produto:`) e `TestMain.test_saida_em_texto` (`Projeto:` virou `Feature atual (...)`). Nenhum teste foi apagado, pulado ou enfraquecido; o arquivo passou de 55 para 89 testes e o de instalação de 32 para 43.
- **Também corrigido no caminho:** com todas as tarefas concluídas e sem Retomada, o `progresso.py` não identificava a feature; agora usa o único `tasks.md`.
- **Medida real antes de fechar (somente leitura):** EvolucaoSegura_LJS, 188 de 199 tarefas, ritmo medido de 7,1 tarefas/h; a última tarefa levou 4 min para 2h estimadas (cerca de 3%, uma tarefa só). Indica que o tempo de agente e a estimativa humana estão em escalas diferentes e que a calibração por fator é necessária. A leitura do histórico custa cerca de 2 s.
- **Fora desta decisão:** S6 (lotes paralelos), o `/progresso` ler o `tasks.md` do worktree em que a construção está, e amostragem das estimativas pelo verificador.

### Custo: medição, modelo pelo domínio e plano pronto (branch `melhoria-custo`)

- **Motivo:** comparação com o processo do time no épico TDV-249 (Thunders): mesmo plano de partida, começo no mesmo horário. O Rascunho consumiu 84% do limite semanal em dois dias. Medido com o `custo.py` nas transcrições de 30/10 a 02/11: o agente `implementador-dominio` (Opus) respondeu por ~411 M dos ~666 M de tokens de cache lido (62%) e 1,48 M dos 3,44 M de saída (43%). Das 121 tarefas, 103 eram `**Risco**: alto` e por isso iam ao Opus. Os mesmos lotes ficaram com ~200 mil tokens de contexto médio por chamada; o `implementador` (Sonnet) teve ~59 mil.
- **M1, `custo.py`:** script novo, só leitura, que soma tokens das transcrições (`~/.claude/projects/<pasta>/**/*.jsonl`) por modelo, agente (lido do `.meta.json` do subagente), dia, branch ou sessão, com filtro de período e de branch e tabela de preços opcional. Não conhece preços. Serve para comparar dois fluxos na mesma tarefa.
- **M2, `**Domínio**: sim|não`:** campo novo da tarefa, depois de `**Risco**` (ausente = não). Passa a escolher o trabalhador: `implementador-dominio` (Opus) só em lote com tarefa de domínio; senão `implementador` (Sonnet). `**Risco**` continua definindo só a profundidade da revisão. A regra de promoção de risco (log, SQL, entrada externa…) não muda; ela deixa de levar ao Opus.
- **M3, plano pronto:** seção `## Plano pronto` do `CLAUDE.md`. Com `plano.md` externo na pasta do épico, `reconhecimento.md` e `arqueologia.md` viram conferência do delta (até ~30 linhas cada, com `Base: plano pronto ...`). Histórico e raio de impacto do que o plano não cita, costuras novas, ambiente e **rede de proteção** continuam obrigatórios. No épico TDV-249 a mesma investigação foi refeita 4 vezes (~160 linhas por feature).
- **Testes:** `test_custo.py` (7 testes) e dois testes novos em `test_skills.py`. Nenhum teste existente foi alterado. Suíte: 223 testes verdes.
- **Lote de 14h para 6h (aprovado pelo usuário em 2026-11-02):** `LOTE_HORAS = 6.0` no `progresso.py` e `CLAUDE.md` (3 tarefas de 2h; uma Phase maior que isso fica inteira). Motivo: o contexto médio por chamada do `implementador-dominio` foi ~200 mil tokens, contra ~59 mil do `implementador`, e cada chamada relê o contexto inteiro; lote menor mantém o contexto pequeno. Hipótese, ainda não isolada: os dois grupos diferem em mais de um fator. Medir no teste dos dois fluxos (cache lido por chamada).
- **Testes existentes alterados por esta decisão (3 de `test_progresso.py`, `TestLotes`, e a asserção `**14h**` de `test_skills.py`):** `test_junta_phases_inteiras_ate_a_capacidade`, `test_sem_estimativa_cada_tarefa_conta_1h` e `test_sem_phases_cada_tarefa_e_uma_unidade` trocaram os números da capacidade (14h para 6h) com a mesma regra testada; nenhum foi apagado, pulado ou enfraquecido. Os outros 3 testes de lote seguem iguais.
- **Fora desta decisão:** verificação proporcional e conferência cruzada no verificador (M4 a M6 da análise), para uma segunda rodada.

### Tempo: modo enxuto, prova de tela e verificação proporcional (branch `melhoria-tempo`)

- **Motivo:** teste A/B da feature 5 do TDV-249 (Thunders, 2026-11-02, mesmo ponto de partida): o processo do time terminou em 22 min e o Rascunho em 2h02. Perfil medido do Rascunho: planejamento 21 min, back 3, front 65, troca de sessão 8, verificação 24. Achados que explicam a diferença: (1) spec, reconhecimento e tarefas foram reescritos do zero sobre critérios e `plano.md` já prontos; (2) o trabalhador não tem a ferramenta Skill e remontou à mão o ambiente de E2E (login, sessão, config do Playwright), cerca de 40 min; (3) o verificador repetiu dois `ng build` (~11 min) que o trabalhador já tinha rodado, e as mutações custavam só 3 a 5 min; (4) a decisão do reconhecimento ("estender `span.small-title`", "ao lado do código") não chegou ao trabalhador, que usou um elemento de bloco, e o E2E só conferia o texto; (5) quatro perguntas de modelo, 17 perguntas no total, e uma troca de sessão para uma feature de 4 tarefas.
- **Decisões do usuário (2026-11-02):**
  1. **Modo enxuto, em qualquer fluxo com entrada pronta** (`plano.md` ou critérios escritos): um agente (`planejador`) confere a entrada no HEAD e grava só o `tasks.md` (Delta até 10 linhas, Critérios por ID, Linha de base, T0 de caracterização); sem `spec.md`, `reconhecimento.md`, `arqueologia.md`, `design.md` nem `protecao.md` separados; uma aprovação, que já despacha o primeiro lote. O `validate_tasks.py` exige só quatro seções, então as de conferência do modelo do tlc saem sem tocar o pacote.
  2. **Modelo pela entrada:** planejamento em Opus sem plano nem critérios, com ambiguidade, contrato novo, evento, migração ou dinheiro; com entrada pronta, Sonnet, com a sessão em Sonnet e o `planejador` como subagente de modelo fixo (sem troca manual de `/model`). Sem entrada pronta, a trava de modelo pergunta uma vez por item, e não por fase. Execução sempre Sonnet; Opus só em lote com tarefa `**Domínio**: sim`.
  3. **Prova de tela:** o teste de tela roda **uma vez ao fim do lote** que toca interface, só o spec novo e só no front principal; o ambiente é preparado pela sessão principal antes de despachar; **teto de 2 tentativas de 5 min**, em segundo plano; passou disso, relata `E2E não executado: <motivo>`. Critério com palavra de posição ou aparência exige asserção espacial ou visual.
  4. **Vizinhança e decisão literal:** o trabalhador acha 1 ou 2 usos vizinhos do mesmo padrão e registra `Molde:` no commit; decisão nomeada em **Reuses** ("estender X") vale literalmente e o verificador a confere.
  5. **Verificação proporcional:** gate reaproveitado pela árvore do commit (`git rev-parse HEAD^{tree}`); até 3 mutações (todas só com risco alto em dinheiro, contrato, migração, autorização ou dado pessoal); `validation.md` compacto (~40 linhas); `revisao-codigo` e `code-review` só com tarefa de risco alto (em legado, sempre).
  6. **Marcos de troca de sessão** no modo enxuto: só a cada 3 lotes.
- **O que mudou:** `CLAUDE.md` (seções Modo enxuto e Verificação proporcional; Execução, Aprovação, Marcos e Modelos ajustadas), agente novo `planejador`, agentes `implementador`, `implementador-dominio` e `verificador`, skills `feature` e `legado`. O pacote `tlc-spec-driven` não foi tocado.
- **Testes:** cinco novos em `test_skills.py` (inclui o `tasks.md` enxuto passando no `validate_tasks.py` real). Nenhum teste existente foi alterado. Suíte: 228 verdes.
- **Estimativa, não medida:** repetir a feature 5 deve cair de 121 para cerca de 28 a 40 min; o piso depende do ambiente de E2E de pé e de não haver worktree frio. Valida-se com um terceiro braço, em worktree novo e sem os artefatos anteriores, e em outra feature.
- **Fora desta decisão:** `bug`, `refatoracao`, `performance` e `redesign` só adotam o modo enxuto depois de conferir os artefatos de entrada de cada um; as particularidades de ambiente de E2E de um projeto ficam no contexto do projeto (no Thunders, `CLAUDE.local.md`), não nos fluxos genéricos; levar a mudança para as instalações é com `instalar.py --atualizar` e a confirmação do usuário.

### Tempo: fluxos de construção herdam a Execução e a revisão por risco (direto na `main`)

- **Motivo:** a medição que gerou a decisão anterior (22 min sem as skills contra 2h02 com elas) pede simplificar, principalmente a execução. Os fluxos `bug`, `refatoracao`, `performance`, `redesign` e `integracao-terceiros` ainda mandavam fazer o que o `CLAUDE.md` já não pede mais.
- **O que mudou (só remove cerimônia ou aponta para o `CLAUDE.md`, sem regra nova):** `bug` deixa de corrigir na sessão e usa um lote de uma tarefa por subagente; `refatoracao`, `performance`, `redesign` e `integracao-terceiros` só acionam a `revisao-codigo` curta com tarefa de `**Risco**: alto`; o sensor dos três primeiros tem teto de 3 mutações; os de construção apontam para a seção Execução do `CLAUDE.md`; o `redesign` ganha a prova de tela (E2E uma vez ao fim do lote, teto 2×5 min).
- **Fora desta decisão:** modo enxuto em `bug` e `refatoracao`, que seguem pendentes de conferir os artefatos de entrada de cada um (ver decisão anterior).
- **Testes:** um novo em `test_skills.py`; nenhum existente alterado.

### Execução v2: sessão única, ciclo pela criticidade do lote e reuso resolvido no planejamento (branch `ajuste/execucao-v2`)

- **Motivo:** teste de velocidade da feature `fundacao` do TarefasDaCasa (T1 a T39, 2026-11-03), quatro execuções do mesmo plano. Tempo ativo até a T39: `livre` (sem fluxo) ~15 min, `rascunho` original (subagente por lote) ~85 min até a T36, `rascunho3` (sessão única, teste primeiro) ~51 min até a T35, `rascunho4` (leve e pesado, banco de pé) ~57 min até a T35 e ~85 min até a T39. Verificação independente: `rascunho` PASS (1 médio), `rascunho4` PASS (0 altos, 2 médios, 6 baixos), `livre` FAIL (2 altos, 5 médios; as mutações `set_config` e `comBanco` sobreviveram). O ganho de qualidade veio dos testes de comportamento de transação, RLS e conexão (~1.650 linhas de teste a mais), não do gate completo, das mutações e das linhas de revisão a cada lote, para os quais não há contraprova.
- **Ressalva de método:** a lista fixa de mutações M1 a M10 estava no prompt da `rascunho4`, então o "10 de 10 mortas" não é independente. Por isso a verificação v2 deriva as mutações dos riscos e não as entrega a quem constrói.
- **Decisões do usuário (2026-11-03):**
  1. **Sessão única, teste primeiro**; o `implementador-dominio` (Opus, modelo fixo) só no lote com tarefa de `**Domínio**: sim`. Resolve os lotes de Domínio que rodaram em Sonnet por falta de `/model`.
  2. **Criticidade do lote** (`**Criticidade**: crítica|comum` na tarefa; ausente = crítica): o lote comum escreve testes e código em paralelo, sem vermelho, com `typecheck` e teste do pacote; o crítico vê o teste falhar e roda os pacotes tocados com banco. O `progresso.py --lote` mostra a criticidade e o script fecha o lote ao mudar de criticidade quando ele já tem 2h.
  3. **Gate completo (lint, format, checagens, suíte) no marco e ao fim**, não a cada lote; **sem mutação no lote**; **verificador no marco (a cada 6 lotes) e no fim**, com mutações derivadas por ele.
  4. **Reuso de origem externa é do planejamento:** `reuso.md` (origem, destino, adaptação, `FUN-NN`, tarefa) e linha do mapa em Reuses; a execução só abre a origem quando o mapa diz código adaptado.
  5. **Pré-voo de ambiente** (`preparar-ambiente.py`): gerenciador de pacotes, Docker, porta do banco e `dedupePeers`, uma vez antes do primeiro lote. **Serviços de apoio de pé** através dos lotes e das trocas de sessão.
  6. **Autorização antecipada de mudança de teste** em `## Autorizações` do `STATE.md`; **marcos a cada 6 lotes**, inclusive no modo enxuto.
  7. **Verificação:** checa que o comando do `testes.json` cobre todos os pacotes, que cada commit de código fecha verde (amostragem) e que IDs de `FUN-NN` de teste copiado batem com a spec.
- **O que mudou:** `CLAUDE.md` (Execução reescrita; Tarefas, Reuso de origem externa, Modo enxuto, Verificação proporcional, Marcos, Testes e Modelos ajustadas), `progresso.py` (criticidade e Domínio por lote), `preparar-ambiente.py` (novo), agentes `implementador-dominio` (reescrito), `implementador` (spike e tarefa solta), `verificador` e `planejador`, skills `feature`, `projeto-novo`, `uso-proprio`, `refatoracao`, `performance`, `bug`, `redesign`, `progresso` (referência `medicao.md`) e `fluxo/references/marcos.md`.
- **Testes:** 7 novos em `test_progresso.py`, 20 em `test_preparar_ambiente.py` e um em `test_skills.py`. **Testes existentes alterados (aprovado pelo usuário ao pedir esta atualização):** em `test_skills.py`, `test_execucao_por_lote_com_v2_por_tarefa` (renomeado para `test_execucao_na_sessao_com_ciclo_pela_criticidade`), `test_modelo_do_trabalhador_vem_do_dominio_nao_do_risco`, `test_modo_enxuto_com_entrada_pronta`, `test_prova_de_tela_vizinhanca_e_gate_registrado` e `test_verificacao_proporcional_ao_risco`: guardavam o texto do modelo antigo (subagente por lote, marcos a cada 3 lotes, mutações fixas), que esta decisão substitui; cada um passou a guardar o texto novo equivalente. Suíte: 266 verdes.
- **Estimativa, não medida:** a meta é 35 a 40 min ativos para T1 a T39 com verificador PASS; 25 min não é realista sem cortar teste de comportamento. Valida-se com uma `rascunho5` do mesmo plano, com o `reuso.md` já feito no planejamento, a lista de mutações escondida de quem constrói e o retrabalho medido em coluna própria. Se não bater, o fluxo não segue para os outros projetos.
- **Fora desta decisão:** `medir-lotes.py` (mede só subagente) e o `validate_tasks.py` do tlc (pacote, não se edita): a regra "origem sem linha no mapa reprova" é conferida pelo `planejador` e na aprovação, não pelo validador.

### Execução v3: ajustes depois do teste de 6 lotes (livre2 contra rascunho2, branch `ajuste/execucao-v3`)

- **Motivo:** teste de velocidade e qualidade de T1 a T25 da `fundacao` do TarefasDaCasa (2026-11-03), com revisão independente de PR e as mesmas dez mutações para os dois braços, que nenhum construtor recebeu. `livre2`: 24,7 min, 109,8 mil tokens de saída (só Sonnet); revisão aprovar com ressalvas, 0 críticos, 2 altos, 11 médios. `rascunho2`: 47,6 min (~33 sem o verificador do marco), 176,5 mil tokens de saída (62,7 mil em Opus, 35,6 mil no verificador); aprovar com ressalvas, 0 críticos, 2 altos, 13 médios. Nos lotes comuns a `rascunho2` foi mais rápida (8 min contra 15,5); nos críticos, mais lenta (20,5 contra 9,1). O ganho de qualidade nos lotes de Domínio em Opus não apareceu.
- **Decisões do usuário (2026-11-03):**
  1. **Verificador do marco em segundo plano** (até 3 mutações), sem bloquear a retomada; campo **Verificador do marco** na `## Retomada`. As 10 mutações ficam para o fim da feature.
  2. **Matriz política × comando** no ciclo crítico: teste por comando (SELECT, INSERT, UPDATE, DELETE, incluindo sem `WHERE`) em que a policy aberta ou sem `WITH CHECK` morra.
  3. **Pré-voo**: confere o Node contra `engines` (aviso) e se o comando do `testes.json` roda todos os scripts `test:*` e pacotes.
  4. **Higiene de teste de banco**: limpar no `finally`, sem depender do estado do cluster, sem banco órfão.
  5. **Conferência spec × design** antes do `tasks.md`: cada divergência vira AD no `STATE.md` e a tarefa a cita; sem AD nem `SPEC_DEVIATION` é lacuna.
  6. **Execução sempre em Sonnet, planejamento sempre em Opus** (o `planejador` passa a Opus). O agente `implementador-dominio` foi removido: `**Domínio**` obriga a listar casos limite e estados antes de codar e a perguntar na lacuna da spec, e não escolhe mais o modelo. Substitui a decisão de Opus por subagente para lote de Domínio da "Execução v2". Isso também elimina o fallback improvisado, porque o tipo `implementador-dominio` não estava disponível na sessão.
- **O que mudou:** `CLAUDE.md` (Execução, Verificação proporcional, Modelos, Tarefas, seção nova Conferência spec × design), agentes `planejador` (Opus), `verificador`, `implementador` e remoção do `implementador-dominio`, `preparar-ambiente.py` (Node e suíte), `progresso.py` (marca `Domínio` sem `Opus`), `marcos.md` e as skills `bug`, `feature`, `performance`, `projeto-novo`, `redesign`, `refatoracao`, `revisao-codigo`, `uso-proprio` e `progresso`.
- **Testes:** 9 novos em `test_preparar_ambiente.py`. **Testes existentes alterados (aprovado pelo usuário ao pedir estes ajustes):** em `test_skills.py`, `test_execucao_na_sessao_com_ciclo_pela_criticidade`, `test_modelo_do_trabalhador_vem_do_dominio_nao_do_risco` (renomeado para `test_execucao_sempre_em_sonnet_e_planejamento_em_opus`), `test_modo_enxuto_com_entrada_pronta` e `test_prova_de_tela_vizinhanca_e_gate_registrado`, que guardavam o agente Opus de Domínio e o planejador em Sonnet; em `test_progresso.py`, a asserção da marca `(crítico, Domínio: Opus)`. Suíte: 276 verdes.
- **Fora desta decisão:** `reuso.md` com coluna de defeito herdado da origem (achado do código copiado do Pelada), junção do commit de fechamento ao último commit do grupo e medição automática por etapa, para uma próxima rodada. Os `ATRIBUICAO.md` de `performance`, `redesign`, `refatoracao` e `revisao-codigo` ainda citam o agente removido: são listas de crédito de origem, não instruções. A atualização dos outros projetos (`instalar.py --atualizar`) fica para quando o usuário pedir.

### Execução v4: executor por marco, verificação com achados e correções por severidade (branch `ajuste/executor-lotes`)

- **Motivo:** o usuário viu como mais viável tirar a escrita dos lotes da sessão principal (conversa cara e longa) e separar quem constrói de quem revisa e de quem corrige. No projeto Livre o Claude executa o projeto sem chamar subagente nem skill; esse é o estilo do executor.
- **Decisões do usuário (2026-11-03):**
  1. **Executor por marco:** a sessão principal despacha um agente `executor` (Sonnet) a cada 6 lotes; ele roda os lotes seguidos sozinho, sem subagentes, sem skills e sem falar com o usuário. Lacuna de spec ou decisão: para e devolve "Perguntas para o usuário"; a sessão pergunta e o redispara.
  2. **Verificador a cada marco** em modo revisão (código e qualidade da execução), com `achados.md` classificando cada achado como crítico ou não crítico.
  3. **Um executor por achado, um de cada vez** (sem paralelo): críticos em **Opus** (a sessão passa `model: opus`), não críticos em Sonnet, críticos primeiro. Depois, nova verificação sobre o diff das correções; no máximo 2 rodadas, depois pergunta ao usuário.
  4. **Fim do projeto:** verificador robusto (feature inteira, até 10 mutações) e, se houver achado, o mesmo ciclo de correção.
- **Substitui:** "sessão única" e "verificador do marco em segundo plano" (v2 e v3). Mantém: execução dos lotes em Sonnet, planejamento em Opus, `**Domínio**` sem escolher modelo.
- **O que mudou:** `CLAUDE.md` (Execução, Verificação proporcional, Modelos), agentes `executor` (novo) e `verificador` (modo revisão de marco e `achados.md`), `marcos.md` e `test_skills.py`.
- **Em aberto:** custo e tempo do ciclo completo não foram medidos; o teste de velocidade contra o `livre2` mostra se o ciclo de achados compensa. As skills de fluxo ainda dizem "a sessão implementa" onde não foram revisadas.

### Execução v5: fluxos terminam no planejamento; /preparar, /executar, /validar e /finalizar (branch `ajuste/execucao-v5`)

- **Motivo:** a v4 (executor por marco, achados e corretores em Opus) deixava a sessão principal só orquestrando e trazia um ciclo longo dentro do fluxo. O usuário preferiu separar o planejamento do que vem depois, executar na sessão principal "no estilo Livre" e validar por feature, com retrabalho em lote próprio.
- **Decisões do usuário (2026-11-03):**
  1. **Todo fluxo termina no planejamento** (`tasks.md` com tarefas e lotes). A única mensagem final é "O plano está disponível para execução." Bug e incidente também: analisam, geram as tarefas de correção e esperam o `/executar`. No fluxo 1, a fase 8 (Preparação) vira só a quebra em tarefas e lotes, em Opus; as fases 9 a 12 saem do fluxo.
  2. **`/preparar`**: infraestrutura guiada, em dois níveis em `.specs/preparacao.md`. Nível 1 síncrono (repositório e remoto, ambiente local com banco, esqueleto, CI, `testes.json`, pré-voo, hook), necessário para o `/executar` (que **recusa e lista o que falta**); Nível 2 assíncrono (staging, produção, segredos, backup, observabilidade, deploy), até o fim da execução. `/preparar` e `/executar` podem rodar em paralelo.
  3. **`/executar`**: na sessão principal, **sem skills e sem subagentes**, uma worktree por feature, um commit de fechamento por lote, **sem PR por lote**. Ao fechar o lote, o `contexto.py` mede o contexto da sessão; **acima de 300k** para e pede `/clear`.
  4. **`/validar`**: por feature, na mesma branch e worktree: `verificador` (inclui o que se chama de QA automatizado, cobertura só por critério), `revisao-codigo` e `auditor-seguranca`. Gera `validation.md` e, se achar problema, um **lote de retrabalho separado** (Phase `Retrabalho R<n>` no `tasks.md`). O usuário usa a mesma sessão para re-executar e validar de novo, até não sobrar retrabalho.
  5. **`/finalizar`**: depois que tudo estiver validado e integrado: E2E geral do projeto (jornadas definidas no planejamento), lançamento (fase 11) e operação e aprendizado (fase 12).
- **Assumido por mim, sem pergunta explícita (conferir):** (a) a integração da feature à branch de origem é do `/validar`, com PASS, e pergunta merge local ou PR; push, PR e merge exigem confirmação específica; (b) a branch pai fica no topo do `tasks.md` (`**Branch pai**`); (c) o `/preparar` roda em Sonnet; (d) a aprovação "seguir / ajustar / parar" da última fase de planejamento foi removida, e o `/executar` é a aprovação; (e) a verificação robusta final deixou de existir como etapa própria: cada `/validar` usa até 10 mutações, e o `/finalizar` roda o E2E geral e, se o projeto for à internet, oferece a auditoria de segurança do conjunto; (f) o item do `/executar` pode ser feature, bug, refatoração, performance, redesign ou automação (qualquer pasta de `.specs/` com `tasks.md`).
- **Substitui:** a v4 inteira (agente `executor`, ciclo do marco, `achados.md`, correções em Opus) e a regra de "gate completo no marco".
- **O que mudou:** `CLAUDE.md` (nova seção Fim do planejamento e comandos de execução; Execução, Verificação proporcional, Aprovação, Marcos, Modelos), skills novas `preparar`, `executar`, `validar` e `finalizar`, agente `executor` removido, `verificador` (achados do `/validar`), `planejador` (Branch pai), `progresso.py` (lote `Retrabalho` próprio), scripts novos `contexto.py` e `preparacao.py`, skills dos fluxos (terminam no plano), `marcos.md` e `/fluxo`.
- **Em aberto:** o `medir-lotes.py` não mede por lote dentro de uma sessão (só o `contexto.py` ao fechar cada lote); o `implement.md` do `tlc-spec-driven` (pacote, não editável) continua mandando oferecer subagentes e executar inline, e só a precedência do `CLAUDE.md` o contém; não foi testada uma execução de ponta a ponta dos quatro comandos.

### Otimização do fluxo, passo 1: medir a v5 por comando (sem branch ainda)

- **Motivo:** análise de 2026-11-04 mostrou que a v5 nunca rodou de ponta a ponta e que o `medir-lotes.py` só mede subagentes, que o `/executar` não usa mais. Sem linha de base, qualquer otimização (disparador automático, `pre-validar.py`, aprovações automáticas, modo enxuto em bug e refatoração) é palpite. Decisão do usuário: começar pela medição, em **projeto de teste novo** (descartável, feature de 6 a 10 tarefas).
- **O que mudou:** script novo `medir-fluxo.py` (só leitura) e `test_medir_fluxo.py` (18 testes). Corta a sessão principal em segmentos pelo `<command-name>/x</command-name>` e mostra por segmento tempo ativo, espera, saída, cache lido, contexto máximo, perguntas, subagentes, skills e Bash. Espera = resposta de `AskUserQuestion`, pausa antes de nova fala do usuário e qualquer pausa acima de 10 min entre registros.
- **Armadilhas achadas ao testar em transcrição real:** (1) o Claude Code grava um bloco por linha com o mesmo `message.id`, então o uso conta uma vez por resposta (valor final de saída) e os blocos de ferramenta contam em toda linha; o `custo.py` conta só a primeira linha e pode subestimar a saída. (2) Sessão esquecida aberta entrava como tempo ativo (850 e 1091 min). (3) Registro fora de ordem gerava espera negativa.
- **Limites conhecidos:** permissão aprovada em menos de 10 min conta como ativo; o consumo dos subagentes não entra (usar `custo.py --por agente`).
- **Testes:** 18 novos; nenhum existente alterado. Suíte: 319 verdes.
- **Próximo:** criar o projeto de teste, rodar `/fluxo`, `/preparar`, `/executar` e `/validar` de ponta a ponta e registrar a linha de base com este script. Depois, na ordem sugerida: permissões do `/executar`, `pre-validar.py`, disparador automático.

### Otimização do fluxo, passo 2: linha de base da v5 (ControleFinanceiroTeste, 2026-11-04)

- **Como foi medido:** uso próprio (fluxo 2), pedido de uma frase ("controle financeiro simples: só conta, entrada e saída"), sem critérios escritos, projeto descartável em `C:\Leandro\Projetos\ControleFinanceiroTeste`. `medir-fluxo.py` na sessão principal e `custo.py --por agente,modelo` nos subagentes.
- **Resultado:** 12 tarefas originais + 7 de retrabalho (R1 com T13 a T16, R2 com T17 a T19), PASS na 3ª rodada do `/validar`, integrado à `main`. Relógio de 18:06 a ~20:30 (~2h24, com ~50 min parados entre o `/executar` do R2 e o `/validar` da rodada 3); tempo ativo da sessão principal 68,7 min, espera 16,9 min. 14 perguntas. 194 chamadas na principal, 327 mil tokens de saída e 39 M de cache lido no total (Opus: 92,5 mil na principal + 35,1 mil no `auditor-seguranca`).
- **Ativo por comando:** planejamento (`/fluxo`, `/model`, `/clear`) ~21,5 min; `/preparar` 4,8; `/executar` 12,2 (as 12 tarefas originais, ~1 min por tarefa) + 7,4 (retrabalho); `/validar` 8,7 + 8,8 + 5,3 = **22,8 min, mais que a construção inteira**. Validação mais retrabalho = ~30 min, 44% do ativo.
- **Achados:** (1) o retrabalho vem de A-01/A-02 (critério sem prova), A-03/A-04 (CSRF, Host e cabeçalhos, que só viraram AD-005 no R1) e, no R2, de A-05/A-06/A-07: mutantes que sobreviveram em código escrito no próprio R1 e rastreabilidade de teste, ou seja, consertar o conserto; (2) o `/preparar` herdou 232 mil tokens de contexto do planejamento (3,9 M de cache lido em 18 chamadas) e o primeiro `/executar` foi recusado com o Nível 1 incompleto, como projetado; (3) o contexto cresceu 221 mil, 273 mil e 300 mil ao longo das três rodadas do `/validar`, na mesma sessão; (4) o ritual `/fluxo`, `/model`, `/clear`, `/fluxo` consumiu ~4,5 min antes do planejamento de fato.
- **Limites da medição:** uma feature, um projeto; o tempo dos subagentes do `/validar` aparece dentro do ativo do comando (a principal espera por eles); `general-purpose` apareceu com 10 chamadas sem eu ter identificado quem o chamou.
- **Próximo:** requisitos de segurança padrão no planejamento de app web (para não nascerem no retrabalho), sessão nova entre planejamento e `/preparar` e entre rodadas do `/validar`, e o disparador automático.

### Otimização do fluxo, passo 3: regras contra retrabalho e sensor do verificador mais barato (2026-11-04)

- **Motivo:** a linha de base (passo 2) mostrou `/validar` com 22,8 min contra 12,2 min da construção, e retrabalho em cascata (R1 de segurança e de prova de critério; R2 consertando o R1). Decisão do usuário: testar a hipótese de que regras antes do código reduzem retrabalho, repetindo a feature. Usar skills ou agentes no `/executar` foi descartado: os achados vieram de requisito ausente no plano (A-03, A-04, A-07) e de testes que cobriram só o ramo comum (A-01, A-02, A-05, A-06), não de falta de skill; o histórico (livre 15 min contra 51 a 85 min com fluxo) aponta que o ganho de qualidade vem dos testes de comportamento.
- **Regras novas no `CLAUDE.md`:** (1) seção **Segurança padrão de app web** (planejamento): escuta em 127.0.0.1, recusa de método que muda estado por `Sec-Fetch-Site` e `Origin`, `Host` esperado, cabeçalhos com `Referrer-Policy: same-origin`, saída escapada, tudo no primeiro lote do servidor, crítico; (2) **Guarda, um teste por ramo** no ciclo crítico (cada método HTTP e cada variante de entrada, falhando sem a guarda); (3) **Critério de erro tem teste de erro** (gatilho de falha, em qualquer lote).
- **Sensor do verificador mais barato** (medido: ~10 de 18 min do verificador foram comando): mutante roda só o teste do arquivo mutado, o e2e roda uma vez para os mutantes que só ele prova, a cópia isolada liga `node_modules` por junção e nunca por `cp -r`, e o `typecheck` por amostragem é de no máximo 3 commits (antes o verificador fez 9). Regras iguais no `CLAUDE.md` e no `agents/verificador.md`.
- **Testes:** 2 novos em `test_skills.py`; nenhum existente alterado. Suíte: 321 verdes.
- **Instalado** no projeto de teste com `instalar.py --atualizar` (3 arquivos, sem conflito).
- **Estimativa, não medida:** o retrabalho de segurança deve sumir da feature repetida e o `/validar` deve cair; a repetição diz se é verdade. Comparar com a linha de base do passo 2: ativo por comando, número de achados por rodada, rodadas até PASS, tempo do verificador.
- **Em aberto:** sessão nova entre planejamento e `/preparar` e entre rodadas do `/validar`, disparador automático e pré-checagem por script (A-07) seguem sem implementar.

## Passo 36: `/rascunho` no projeto do zero (2026-11-04)

- **Decisão:** nos fluxos 1 e 2 a construção ganha uma primeira passada, `/rascunho`, que escreve teste e código sem rodar nada; depois `/executar` roda e leva ao verde; depois `/validar`. Marca no `tasks.md`: `**Passada**: rascunho` no topo e `**Status**: rascunhada` por tarefa (em aberto na contagem; `progresso.py --lote --rascunho` acha o próximo lote não rascunhado).
- **Motivo:** escrever sem parar no ciclo rodar-e-corrigir é mais rápido e mantém o contexto pequeno; o `/executar` corrige com a suíte à frente.
- **Worktrees:** uma por feature, sempre em `.worktree/<slug>` (ignorada pelo git), mantidas até o `/executar`; limpeza única ao fim. O `/rascunho` integra cada feature à Branch pai (merge local, com confirmação) e sugere a feature seguinte.
- **Trava:** `trava-testes.py --rascunho` registra o commit como rascunho e libera só o merge na Branch pai; push e PR seguem exigindo suíte verde (aprovado pelo usuário). Modelo do `/rascunho`: Opus.

## Passo 37: `/rascunho` mais rápido, direto na Branch pai (2026-11-04)

- **Decisão (usuário):** o `/rascunho` roda **direto na Branch pai** (`main`), sem worktree e sem merge; **um commit local por tarefa finalizada** (com `**Status**: rascunhada` no mesmo commit, sem commit de fechamento de lote); `contexto.py --comando rascunho` **a cada 5 lotes**; mínimo de verificações (só confere `**Passada**: rascunho`). O `/executar` cria a worktree a partir da Branch pai e herda os commits por tarefa.
- **Substitui parcialmente o passo 36:** a worktree por feature no rascunho e o merge local ao fim saem; `trava-testes.py --rascunho` fica sem uso pelo `/rascunho` (mantido, com testes). Risco aceito: a `main` passa a ter código sem teste rodado até o `/executar`.
- **Lacuna de Domínio:** o `/rascunho` não para; deixa `[LACUNA] <o quê>` no código e `Lacunas:` na tarefa, segue pela interpretação mais conservadora; o `/executar` procura as marcas e pergunta (`AskUserQuestion`) antes de levar a tarefa ao verde. "Cada commit fecha verde" não vale no rascunho; vale só que nada importe arquivo de tarefa posterior.
- **Correção da trava:** `settings.json` ganha o mesmo hook `trava-testes.py` com `matcher: PowerShell` (antes só `Bash`: `git push`, `gh pr create` e `git merge` pelo PowerShell passavam). O script já lia `tool_input.command`; `instalar.py` soma grupos de hook genericamente, então o novo matcher segue no `--atualizar` e no `--local`. Teste em `test_trava_testes.py`.

## Passo 38: menos chamadas de shell e saída mais curta na execução (2026-11-04)

- **Motivo:** um lote crítico do `/executar` chamava o shell de ~15 a 20 vezes (estimativa pelas regras, não medida), e a saída inteira dos testes enchia o contexto até os 300k.
- **`fechar-lote.py` (novo):** uma chamada roda o gate (`--gate` filtrado pelos pacotes tocados, ou o `testes.json`), grava as tarefas concluídas e `Gate: <comando> @ <árvore> = verde` no `tasks.md`, faz o commit de fechamento e imprime 3 linhas (gate, `progresso.py --lote`, `contexto.py`). Gate vermelho não escreve nada. Substitui 5 a 6 chamadas. O `/rascunho` não o usa (sem gate nem commit de fechamento).
- **Regras no `CLAUDE.md` e nas skills:** typecheck, `git add` e `git commit` do grupo numa chamada com `&&`; reporter mínimo nos testes (o `/preparar` grava o comando assim); `Read`, `Glob` e `Grep` no lugar de `cat`, `ls`, `grep` e `git show`.
- **Descartado:** restringir o hook `trava-testes.py`. A saída dele não entra no contexto quando passa e o script já sai logo depois de ler o comando; o custo é só a partida do Python, e o matcher não filtra por conteúdo do comando.

## Passo 39: `/executar` leva cada tarefa rascunhada por um ciclo próprio (2026-11-06)

- **Decisão (usuário):** depois do `/rascunho` funcionar bem, o `/executar` sobre lote rascunhado passa a seguir, **tarefa a tarefa**: (1) confere se atende os requisitos, (2) code review próprio sobre o diff, (3) roda os testes da tarefa, (4) corrige tudo até o verde, (5) fecha a tarefa com commit e vai à próxima.
- **Mantido:** sem skills e sem subagentes (o review é feito pela própria sessão); a marca `concluída` e o `Gate:` continuam no commit de fechamento do lote (`fechar-lote.py`), pois a marca exige o gate real. Lote não rascunhado segue o ciclo comum/crítico da seção Execução.
- **`/validar` (mesmo passo):** como o `/executar` já confere e revisa cada tarefa, o `/validar` roda a suíte completa e abre como retrabalho (Phase `Retrabalho R<n>`) tudo o que entender ser falha ou lacuna da feature inteira.
