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
