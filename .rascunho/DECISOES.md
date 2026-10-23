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

Teste encerrado por escolha do usuário. A sessão de teste chegou a gerar a spec do MVP (fase 6, `tlc-spec-driven`): `spec.md` com 9 histórias e 61 critérios EARS, títulos de seção em inglês (exigidos pelo validador) e conteúdo em português; `validate_spec.py` passou sem erros nem avisos. Artefatos arquivados em `.rascunho/teste-1-cuidados/`. Branch `novo-fluxo-claude` juntada na `main` local (sem push).

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

---

## Estado ao fim da rodada (2026-10-23)

**Fluxos prontos (4 de 21):** 1 Projeto novo (fases 1 a 11), 2 Uso próprio, 3 Feature em projeto IA, 4 Feature em legado. `/fluxo` com menu em dois cliques e atalhos.

**Testado de verdade:** fluxo 1 nas fases 1 a 6 (teste 1, arquivado em `.rascunho/teste-1-cuidados/`); scripts com 26 testes automatizados; trava de testes em uso nesta sessão.

**Próximas rodadas:**

1. Testar de ponta a ponta a construção, a verificação e a liberação (fluxos 1 a partir da fase 7, 3 e 4) num projeto real.
2. Próximo fluxo sugerido: 12 Correção de bug; depois 24 Revisão de código.
3. Fase 12 do fluxo 1 (operação e aprendizado).
4. Confirmar o hook de atualizações numa sessão aberta do zero.
5. Atualizar o superpowers para 7.x (via `/plugin`).
6. Empacotar como plugin quando estável (rules viram skill ou hook).
7. Antes de qualquer push deste repositório: `python .claude/scripts/trava-testes.py --rodar` (a trava exige o commit verde).

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
