---
name: feature
description: Orquestra o fluxo de feature em projeto existente feito com IA — pedido (spec), reconhecimento do código, plano, rede de proteção, implementação em branch isolada, verificação (verificador + /code-review) e integração — descobrindo a fase pelos artefatos em .specs/features/<feature>/ e pedindo aprovação a cada fase. Use quando o usuário quiser adicionar uma funcionalidade a um projeto que já existe, ou via /fluxo. Não use para projeto do zero (projeto-novo, uso-proprio) nem para código legado sem testes (fluxo de legado).
---

# Feature em projeto existente (fluxo 3)

Você é o **orquestrador**. As 7 fases e seus critérios estão em [references/fases.md](references/fases.md); leia-o na primeira vez que acionar esta skill na sessão.

Princípio: **entender o que já existe e não quebrar nada.** A feature segue as convenções do projeto, mesmo que haja jeito melhor; melhorar o resto é outra tarefa.

## 1. Qual feature

Liste `.specs/features/`. Features **em andamento** são as que não têm `integracao.md`.

- Nenhuma em andamento: é uma feature nova; siga para a fase 1.
- Uma ou mais: pergunte via `AskUserQuestion` qual retomar, com a opção **Feature nova**.

## 2. Descobrir a fase da feature

A **primeira linha que se aplica** define a fase:

| Situação em `.specs/features/<feature>/` | Fase atual |
|---|---|
| sem `spec.md` | 1 Pedido |
| `spec.md`, sem `reconhecimento.md` | 2 Reconhecimento |
| `reconhecimento.md`, sem `protecao.md`, e sem plano aprovado (`tasks.md`, `design.md` ou aprovação nesta sessão) | 3 Plano |
| plano aprovado, sem `protecao.md` | 4 Rede de proteção |
| `protecao.md`, com tarefas em aberto ou sem `validation.md` | 5 Implementação |
| todas as tarefas concluídas, sem `validation.md` com PASS | 6 Verificação |
| `validation.md` com PASS, sem `integracao.md` | 6 Verificação (revisão do diff e segurança) e 7 Integração |

## 3. Situar o usuário

Uma linha: "**Feature <nome>, fase N de 7, <fase>.**" Avise a troca de modelo:

- fases 1 e 3: "Esta fase rende melhor em Opus: use `/model opus`."
- demais: "Esta fase pode seguir em Sonnet: use `/model sonnet`."

## 4. Acionar a peça da fase

| Fase | Acione | Observações |
|---|---|---|
| 1 Pedido | `tlc-spec-driven`, fase **Specify** | Critérios de aceite testáveis e o que fica de fora. Deixe o tlc dimensionar (Small, Medium, Large). |
| 2 Reconhecimento | skill `inventario` (cria ou atualiza `.specs/projeto/inventario.md`), depois skill `reconhecimento` | O reconhecimento decide, para cada necessidade, reaproveitar / estender / criar. Se ele escalar (mudança grande de arquitetura), siga a decisão do usuário. |
| 3 Plano | `tlc-spec-driven`, fases **Design** e **Tasks** (ele pula o que não precisa) | Passe o `reconhecimento.md`: o plano segue a tabela de reaproveitamento, o modelo a seguir e as convenções. Peça nova fora da tabela precisa de justificativa. Toda tarefa tem teste. |
| 4 Rede de proteção | crie a branch `feature/<nome>` (ou worktree, com `using-git-worktrees`); depois a skill `rede-de-protecao` | |
| 5 Implementação | `tlc-spec-driven`, fase **Execute**, na branch | Lotes com `implementador` ou `implementador-dominio`. A suíte inteira roda no fim de cada lote: nenhuma falha nova além das preexistentes de `protecao.md`. |
| 6 Verificação | verificador do `tlc-spec-driven` (agente `verificador`); com PASS, a skill `code-review` sobre o diff da branch | Se a feature toca login, permissões, pagamento ou dados pessoais, despache também o `auditor-seguranca`. Achado bloqueante vira tarefa e volta à fase 5. |
| 7 Integração | veja abaixo | |

### Integração (fase 7)

0. **Checagem final de testes:** na branch, rode a suíte inteira e compare com a linha de base de `protecao.md`. Falha nova bloqueia a integração e volta à fase 5. Mostre o resultado ao usuário.
1. **Contexto do projeto:** atualize o arquivo de instruções do projeto (`CLAUDE.md` ou equivalente) com o que esta feature ensinou: novo padrão, comando novo, armadilha. Se não existia contexto, crie um mínimo (como rodar, testar, estrutura, convenções) a partir do `reconhecimento.md`. Mostre o diff ao usuário.
2. **Forma de integrar:** pergunte via `AskUserQuestion`: **merge local** na branch principal, **PR no GitHub** (push e abertura do PR são ações externas, com confirmação) ou **manter a branch**. Use `finishing-a-development-branch` para executar.
3. Grave `.specs/features/<feature>/integracao.md`: data, forma (merge, PR com link, branch mantida), commit final, resultado da suíte na checagem final, contexto atualizado (sim/não).

## 5. Fechar a fase

Apresente o que foi produzido (caminho e 3 a 5 linhas) e o critério de passagem, e pergunte via `AskUserQuestion`: **seguir / ajustar / parar**. Antes de declarar uma fase concluída, aplique `verification-before-completion`.

## Regras

- A feature segue as convenções do projeto. Refatoração vira outra tarefa (fluxo 13), nunca entra junto.
- Diff pequeno e branch isolada.
- Push, PR, deploy e alterações em banco de produção exigem confirmação específica.
- Tudo em português.
