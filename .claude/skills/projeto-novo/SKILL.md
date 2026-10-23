---
name: projeto-novo
description: Orquestra o fluxo de projeto novo (construir um software para vender), da ideia à validação — descobre em que fase o projeto está pelos artefatos em .specs/, avisa a troca de modelo, aciona a skill certa (descoberta, viabilidade-tecnica, plano-comercial, decisao, tlc-spec-driven) e pede aprovação ao fim de cada fase. Use quando o usuário quiser começar ou retomar um projeto novo, ou via /fluxo. Não use para feature em projeto existente, bug ou outros fluxos.
---

# Projeto novo (fluxo 1)

Você é o **orquestrador**: decide a fase, aciona a peça certa e controla as aprovações. O trabalho de cada fase está nas skills e agentes que você aciona. As 12 fases, suas perguntas e critérios de passagem estão em [references/fases.md](references/fases.md); leia-o na primeira vez que acionar esta skill na sessão.

## 1. Descobrir onde estamos

Liste `.specs/produto/` e `.specs/features/`. A **primeira linha que se aplica** define a fase:

| Situação dos arquivos | Fase atual |
|---|---|
| `.specs/` não existe ou `produto/` vazio | 1 Ideia |
| `ideia.md`, sem `problema.md` | 2 Discovery |
| `problema.md`, sem `solucao.md` | 3 Solução e valor |
| `solucao.md`, sem `viabilidade-tecnica.md` | 4 Viabilidade técnica |
| `viabilidade-tecnica.md`, sem `decisao.md` | 5 Plano comercial (opcional) ou Decisão |
| `decisao.md` com veredito `matar` | Encerrado: mostre o motivo e pare |
| `decisao.md` com veredito `esclarecer` | Volte à fase indicada em "Voltar para" |
| `decisao.md` com `seguir`, sem `features/*/spec.md` | 6 MVP |
| `spec.md`, sem `design.md` e sem `tasks.md` | 7 Desenho (o tlc pode pular, se a feature for simples) |
| `design.md` ou spec simples, sem `tasks.md` | 8 Preparação |
| `tasks.md` com tarefas em aberto | 9 Construção |
| todas as tarefas concluídas, sem `validation.md` com PASS | 10 Validação |
| `validation.md` com PASS, sem `seguranca.md` | 10 Validação: auditoria de segurança |
| `seguranca.md` sem achado crítico ou alto em aberto | 11 Lançamento |

Para retomar uma construção interrompida, o `tlc-spec-driven` reconcilia `.specs/STATE.md` com o git; deixe que ele faça isso.

## 2. Situar o usuário

Uma linha: "**Fase N de 12, <nome>.** Anterior: <fase>, aprovada." Se a fase pede outro modelo, avise:

- fases 1 a 7: "Esta fase rende melhor em Opus: use `/model opus`."
- fases 8 a 12: "Esta fase pode seguir em Sonnet: use `/model sonnet`."

## 3. Acionar a peça da fase

| Fase | Acione | Observações |
|---|---|---|
| 1, 2, 3 | skill `descoberta` | Ela retoma da etapa que falta e para a cada etapa. |
| 4 | skill `viabilidade-tecnica` | |
| 5 | pergunte: "Quer fazer o plano comercial agora? (opcional)" → sim: skill `plano-comercial`; não: siga para a decisão | |
| Decisão | skill `decisao` | Com `seguir`, ela prepara a entrada do MVP. |
| 6 | skill `tlc-spec-driven`, fase **Specify** | Entrada: seção "Se seguir: entrada do MVP" de `decisao.md`. Projeto novo costuma ser de tamanho Complex. |
| 7 | `tlc-spec-driven`, fase **Design** | Se houver interface, use a skill `frontend-design` para o mockup das telas principais. Use `leitor-codigo` se já houver código. |
| 8 | `tlc-spec-driven`, fase **Tasks** | Peça que as **primeiras tarefas** sejam: repositório e estrutura, ambiente local reproduzível, esqueleto que roda ponta a ponta e CI com os testes. |
| 9 | `tlc-spec-driven`, fase **Execute** | Trabalhadores: `implementador` (lote mecânico) ou `implementador-dominio` (lote de domínio). Isole com `using-git-worktrees`. |
| 10 | verificador do `tlc-spec-driven` (agente `verificador`) | Com PASS, despache o `auditor-seguranca` sobre a feature. Achado crítico ou alto vira tarefa de correção e volta à fase 9. Ao final, `finishing-a-development-branch`. |
| 11, 12 | **ainda sem peça** | Diga que estas fases ainda não foram construídas e ofereça conduzi-las manualmente seguindo `references/fases.md`. |

## 4. Fechar a fase

Quando a peça terminar, apresente:

- o que foi produzido (caminho do arquivo) e 3 a 5 linhas com o essencial;
- o critério de passagem da fase (de `references/fases.md`) e se foi atendido;
- as opções **seguir / ajustar / parar**, e qual é a próxima fase.

Não avance sem aprovação explícita. Ajuste fica na mesma fase. Voltar a uma fase anterior só se a decisão dela mudar.

Antes de declarar uma fase concluída, aplique `verification-before-completion`: o que a fase promete precisa estar no arquivo, não só na conversa.

## Regras

- Ações externas (push, deploy, publicar, banco de produção) exigem confirmação específica, mesmo com a fase aprovada.
- Parar é um resultado válido: registre o motivo no artefato da fase.
- Tudo em português.
