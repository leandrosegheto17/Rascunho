# Plano: ajuste pós-teste, execução sem parar, qualidade e produção

- **Data**: 2026-11-27 · **Situação**: passos 41 a 44 construídos na branch `feature/melhorias-ajuste-execucao`, ainda não usados em projeto real nem integrados à `main`
- **Origem**: comparação com um processo de equipe e com a camada pessoal feita sobre ele. As ideias são reescritas aqui, sem copiar arquivo, texto ou nome de terceiros.
- **Escolha do usuário**: os quatro pacotes.

## Regras da construção

- Toda mudança de regra ou de script ganha teste (`test_skills.py`, `test_progresso.py`, `test_fechar_lote.py`) escrito antes, e a suíte inteira roda ao fim de cada passo.
- O `CLAUDE.md` (239 linhas, sempre carregado) recebe só a regra curta; o detalhe vai para `references/`.
- `tlc-spec-driven` não é editado. Skill com até 150 linhas.
- Cada passo vira uma entrada em `DECISOES.md` e um commit.

## Ordem

| Passo | Pacote | Por que nesta posição | Estimativa |
|---|---|---|---|
| 41 | Regras de qualidade | Só texto; melhora o próximo planejamento | 3h |
| 42 | Executar sem parar | Introduz o status `bloqueada` nos scripts | 7h |
| 43 | Ajuste e teste manual | Usa o mesmo tratamento de status e de lote | 9h |
| 44 | Diagnóstico em produção | Independente | 3h |

## Passo 41: regras de qualidade

| T | O que | Onde | Estimativa |
|---|---|---|---|
| 1 | **Exemplos com valores**: cada regra de tarefa `Domínio: sim` tem ao menos um exemplo Dado/Quando/Então com números e o caso limite; o planejamento **refaz as contas**, cruza regras e tabelas e pergunta o que divergir, sem ajustar a fonte para a conta fechar | `CLAUDE.md` (junto de Conferência spec × design), `planejador.md` | 1h |
| 2 | **Casos por risco**: valores limite (zero, um, máximo, arredondamento, soma 100%); datas (véspera, primeiro, último, dia seguinte, sobreposição, buraco); migração com dado antigo, duas vezes e revertida; evento repetido ou fora de ordem; flag ligada e desligada. Caso que exige decisão de negócio vira pergunta | `CLAUDE.md` (ciclo crítico), `verificador.md` | 1h |
| 3 | **Cenário mais frágil** obrigatório, mesmo com PASS | `verificador.md`, `validar/references/relatorio.md`, `revisao-codigo/references/retorno.md` | 30 min |
| 4 | **Arquivos críticos**: os 3 mais alterados no git (fora gerados, travas e configuração); tarefa que os toca é `Risco: alto` | `inventario/SKILL.md` | 30 min |

## Passo 42: executar sem parar

| T | O que | Onde | Estimativa |
|---|---|---|---|
| 1 | **Fechar pendências no fim do planejamento**: listar o que pararia a execução (`[A ESCLARECER]`, regra de domínio sem resultado, tarefa sem teste, gate ou molde, serviço de apoio sem como subir, teste existente que vai mudar); perguntar em lotes de 4; gravar respostas e autorizações em `STATE.md`. Vem antes da mensagem final | `CLAUDE.md` (Fim do planejamento), `planejador.md` | 1h30 |
| 2 | **Campo `**Bloqueio**`** (no lugar de um status novo, para não sobrescrever `rascunhada`): conta como aberta; a bloqueada e quem depende dela são puladas | `progresso.py` | 2h |
| 3 | `fechar-lote.py` não marca como concluída a tarefa bloqueada | `fechar-lote.py` | 1h |
| 4 | **Regra nova de parada**: dúvida ou 2 tentativas sem verde marcam `bloqueada — <pergunta>`, a sessão segue com o que não depende e pergunta tudo ao fim. Dúvida achada no meio do código usa o `[LACUNA]` que já existe. Continuam parando na hora: contexto, segurança e ação externa | `CLAUDE.md` (Execução), `executar/SKILL.md` | 1h |
| 5 | **Regras de execução do projeto** em `.specs/projeto/regras-execucao.md` (comandos, serviços, armadilhas, testes que já falham, lições com data; até ~60 linhas): criado pelo `/preparar`, lido por `/rascunho`, `/executar` e `/validar`, atualizado pelo `/executar` | skills citadas, `artefatos.md` | 1h30 |

## Passo 43: ajuste pós-teste e roteiro manual

### Comando `/ajustar`

Entrada: o item e o que se viu no teste. Classifica cada ponto:

| Retorno | Caminho |
|---|---|
| Não é isso que eu queria | Revisa o critério na spec (revisão N+1) |
| Faltou um caso | Acrescenta o critério ou o exemplo |
| Está certo, mas quebra | Skill `bug` |
| A decisão técnica é ruim | AD nova que substitui a anterior |

Efeito nas tarefas: nunca renumerar nem apagar. Tarefa aberta afetada é editada; tarefa concluída fica e ganha uma **nova** na Phase `Ajuste J<n>` (lote próprio); critério removido marca a tarefa aberta como `cancelada` e cria a de reverter o código já feito. O `validation.md` anterior é renomeado para o histórico, o que obriga novo `/validar`. Mudar teste existente segue a regra de Testes. Termina com a mensagem de plano disponível.

| T | O que | Estimativa |
|---|---|---|
| 1 | `progresso.py`: `cancelada` sai da contagem; Phase `Ajuste` é lote próprio | 2h |
| 2 | Skill `ajustar` e referência do formato; entrada no `/fluxo` e no `CLAUDE.md` | 2h |
| 3 | `/executar` (branch `feature/<slug>-j<n>`) e `/validar` reconhecem o ajuste | 1h |

### Roteiro manual

| T | O que | Estimativa |
|---|---|---|
| 4 | No planejamento, critério que a suíte e o teste de tela não provam recebe `Prova: manual`; acima de 30% do total, aviso para rever | 1h |
| 5 | `/validar` grava `roteiro-manual.md` (pré-condições, passos, esperado, como verificar, resultado em branco) e lista o pendente | 2h |
| 6 | `/finalizar` exige resultado ou dispensa registrada; reprovado vai para o `/ajustar` | 1h |

## Passo 44: diagnóstico em produção

| T | O que | Onde | Estimativa |
|---|---|---|---|
| 1 | **Consulta a banco de produção**: só leitura; hipótese, motivo, consulta mínima sem `SELECT *`, risco e aprovação **a cada execução** (nunca na lista de permissões); resultado resumido, sem dado pessoal; dizer se confirmou ou refutou | `bug/references/producao.md` (novo) | 1h |
| 2 | **Logs**: antes de concluir por ausência, confirmar serviço, janela e se aquele nível é coletado | mesma referência | 30 min |
| 3 | **Consulta alterada pela correção**: medir a antiga e a nova no pior caso; apontar para `performance/references/medicao.md` | mesma referência | 30 min |
| 4 | Ligar `bug`, `suporte` e `incidente` à referência; aviso ao relator sem termo técnico e sem prazo não combinado | skills citadas | 1h |

## Fora do plano

Subagente e confirmação por tarefa; artefatos de equipe (cards, mapa de serviços, divisão entre devs); vídeo de demonstração e manual de usuário (podem entrar depois, com produto à venda).

## Riscos

- **Seguir com tarefa bloqueada** pode gerar retrabalho se a dependência não estiver declarada em `Depends on`. Mitigação: o planejamento confere as dependências; a resposta da pergunta é aplicada antes do `/validar`.
- **Mais texto no `CLAUDE.md`** aumenta o contexto de toda sessão. Mitigação: detalhe em `references/`.
- **Nenhum ganho de tempo está medido.** Comparar a próxima feature com a linha de base anterior.
