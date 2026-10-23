# Reaproveitamento de terceiros nos fluxos restantes

Levantamento de 2026-10-23 nas pastas de referência (`.tlc`, `.speckit`, `.bmad`, `.openspec`, `.wshobson`, `.awesome`, `.anthropic-skills`, `.anthropic-plugins`, `.superpowers`, `.claude_legado`), feito por 5 leitores em paralelo. Cada fluxo, ao ser construído, **lê o arquivo de origem inteiro** antes de usar.

## Política

- **Adaptar, não instalar.** O conteúdo útil (checklist, modelo, roteiro) é traduzido e enxugado para `references/` da skill nossa. Instalar plugin ou skill de pacote cria dependência e é decisão do usuário (`/atualizacoes`).
- **Registro:** todo trecho adaptado de terceiro ganha entrada `adaptado` em `.claude/fontes.json` e atribuição em `references/ATRIBUICAO.md`. Material do `.claude_legado` é do usuário: só citar a origem.
- **Licenças:** MIT (tlc, speckit, bmad, openspec, wshobson, superpowers) e Apache 2.0 (anthropic-skills, plugins oficiais, `security-threat-model`, `security-ownership-map`): adaptar com aviso. CC-BY-4.0 (`the-fool`, `the-jury`, `codenavi`, `pr-review`): adaptar com atribuição. **Fora:** `.awesome` (CC BY-NC-ND, só ponteiro), `claude-security` (proprietário), skills `docx/pdf/pptx/xlsx` (proprietárias), itens sem licença declarada (`coding-guidelines` do legado, `create-technical-design-doc`, conectores externos) só como inspiração.
- **Fora por enviar código a serviço externo:** `security-guidance` (hook) e `claude-security`. O `patterns.py` do `security-guidance` pode virar checklist (Apache 2.0).
- **Superpowers:** `test-driven-development` entra no fluxo de bug (teste que falha primeiro); `brainstorming` serve de postura no aprendizado e no spike, sem ser acionado. Registrar na tabela do `CLAUDE.md` quando o fluxo for construído.

## Por fluxo (ordem de construção)

| # | Fluxo | Usar | Inspiração |
|---|---|---|---|
| 12 | Bug | `.bmad/skills/bmad-agent-po/assets/bug-template.md` (P0–P3, reprodução, teste que falha); `.claude_legado/skills/bug-documentation`; superpowers `systematic-debugging` + `test-driven-development` | `.speckit/extensions/bug`; `pr-review-toolkit/agents/silent-failure-hunter.md`; `webapp-testing` para reproduzir em UI |
| 9 | Incidente | `.wshobson/plugins/incident-response/skills/postmortem-writing` (sem culpa, 5 porquês) e `incident-runbook-templates`; skill `bug` para a correção | `.bmad/.../codebase-historian.md` (linha do tempo); `.claude_legado/skills/observability-setup` |
| 17 | Spike | `.bmad/skills/bmad-agent-po/assets/spike-template.md`; agente `implementador` em modo spike | `.claude_legado/skills/the-fool` (critério de sucesso); `technical-spike-identification` |
| 25 | Escolha de tecnologia | `.claude_legado/skills/adr-drafting` (MADR) e `tech-stack-selection`; `.wshobson/.../architecture-decision-records`; `.bmad/skills/bmad-deep-recon/types/technical.md` (5 dimensões) | `build-vs-buy-analysis`; `the-jury` (caro) |
| 16 | Auditoria de segurança | `security-threat-model` (Apache, `.tlc` ou legado); `.wshobson/.../stride-analysis-patterns`; `.claude_legado/scripts/seguranca.py`; `finding-severity-classification`; agente `auditor-seguranca` | `code-modernization/agents/security-auditor.md`; `security-guidance/hooks/patterns.py` |
| 24 | Revisão de código | `.bmad/skills/bmad-code-review/references/claims-check.md` e `review-prompts/edge-case-hunter.md`; agentes do `pr-review-toolkit` (Apache); skill `code-review` | `wshobson code-review-excellence`; `patterns.py` (armadilhas de IA); `coding-guidelines` (sem licença: só ideia) |
| 13 | Refatoração | `.wshobson/plugins/code-refactoring/commands/tech-debt.md` (pontuação de dívida); `coupling-analysis` e `legacy-migration-planner` do `.tlc` (MIT); `rede-de-protecao`, `reconhecimento` | `code-simplifier`; `bmad verification-gap.md`; superpowers `writing-plans` |
| 5 | Performance | `.wshobson/plugins/application-performance/commands/performance-optimization.md`; `perf-lighthouse` e `core-web-vitals` (`.tlc`, só web) | `slo-implementation`; `chrome-devtools` |
| 14 | Documentar | `claude-md-management/skills/claude-md-improver` (Apache); `.bmad/skills/bmad-project-context` e `bmad-deep-recon/assets/codebase.template.md`; C4 do `.wshobson`; `inventario` | `docs-writer`; `codenavi` |
| 27 | Avaliar terceiros | `build-vs-buy-analysis`, `security-ownership-map` (bus factor), `risk-and-compliance-check` do legado; fluxos 16, 24 e 14 | `bmad technical.md` dimensão 5 (saúde do ecossistema) |
| 6 | Integração | `api-integration`, `api-contract-design`, `compliance-validation` (LGPD) do legado; `wshobson gdpr-data-handling` adaptado para LGPD; fluxo 25 para escolher fornecedor; `liberacao` | `pci-compliance`; `mcp-builder` |
| 30 | Automação | fluxo 25 para a ferramenta; `hookify/skills/writing-rules` | `ralph-loop`; `dispatching-parallel-agents`; `claude-automation-recommender` |
| 7 | Redesign | `mockup-visual`; `.claude_legado/scripts/comparar-visual.mjs`; `accessibility-review` e `design-system-consistency-check` do legado; `wcag-audit-patterns` | `frontend-design`; `webapp-testing` |
| 8 | Aprendizado | `.tlc/.../learning-opportunities` | `learning-output-style`; postura do `brainstorming`; Bloom e learn-faster-kit (`.awesome`, só ponteiro) |
| 10 | Sugestão | `commercial-impact-triage` e `product-roadmap-prioritization` (RICE) do legado; `wshobson before-you-build` | `bmad methods.csv` (pré-mortem); `discernment-nudge` |
| 11 | Solicitação | `requirement-elicitation` e `effort-estimation` do legado; `bmad ticket-template`; skills `feature`/`legado` e `tlc-spec-driven` | `tlc-prd`; extensão `grill` do speckit |
| 32 | Suporte | `bug-documentation` (triagem); fluxos 12, 9 e 10 | `internal-comms`; `on-call-handoff-patterns` |

## Nada encontrado (material próprio)

Spike além do modelo, suporte ao cliente, due diligence de licença (fluxo 27) e LGPD específica: escrever do zero ou com o `pesquisador`.
