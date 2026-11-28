---
name: executar
description: Executa o tasks.md de uma feature na sessão principal, sem skills e sem subagentes, em uma worktree própria da feature — lê os lotes e as tarefas, escreve testes a partir dos critérios, implementa e fecha cada lote com um commit, medindo o contexto ao fim de cada lote (acima de 300k, para e pede /clear). Sem PR por lote; a integração é do /validar. Use quando o fluxo disser que o plano está disponível, ou para executar o lote de retrabalho gerado pelo /validar. Recusa começar se o Nível 1 do /preparar estiver incompleto. Não planeja, não valida e não faz push.
model: sonnet
effort: medium
---

# /executar

Você **só executa**. Nada de skills, nada de subagentes: não use a ferramenta `Skill`, não use `Agent`, nem `leitor-codigo`. Você tem o `tasks.md`, o código e a seção **Execução** do `CLAUDE.md`. Esta sessão é a que escreve o código; quem verifica depois é o `/validar`.

Roda em **Sonnet** (trava de modelo do `CLAUDE.md`).

## 1. Qual feature

Liste os `tasks.md` com tarefa em aberto em `.specs/` (`features/`, `bugs/`, `refatoracoes/`, `performance/`, `redesign/`, `automacoes/`, `cobertura/` e `e2e/`; `python .claude/scripts/progresso.py` ajuda). A pasta que tem o `tasks.md` é o "item"; no texto abaixo, "feature" vale para qualquer item. Respeite o argumento recebido, se houver. Mais de uma: pergunte qual (via `AskUserQuestion`), a mais antiga primeiro como recomendada. Nenhuma: diga que não há plano a executar e que o `/fluxo` faz o planejamento.

## 2. Condições para começar

1. `python .claude/scripts/preparacao.py --nivel1`. Saída diferente de 0: **recuse**, mostre os itens que faltam e diga para rodar `/preparar`. Não escreva nada.
2. A feature depende de outra que ainda não está integrada (campo **Branch pai** no topo do `tasks.md`)? Diga e confirme a branch pai.
3. `python .claude/scripts/preparar-ambiente.py` uma vez antes do primeiro lote do projeto; corrija o que ele apontar.
4. Leia `.specs/projeto/regras-execucao.md` (comandos, armadilhas, testes que já falham). Sem o arquivo, crie-o pelo modelo de `.claude/skills/preparar/references/regras-execucao.md` com o que descobrir.

## 3. Worktree da feature

- `git worktree list`. Se a feature já tem worktree, entre nela e retome.
- Senão: **Branch pai** = a do topo do `tasks.md` (`**Branch pai**: <nome>`) ou a branch atual (padrão `main`). Crie na pasta `.worktree/` da raiz (confira que `.worktree/` está no `.gitignore`):
  `git worktree add .worktree/<slug> -b feature/<slug> <pai>`
- **Depois do `/rascunho`** (`**Passada**: rascunho` no topo): o `/rascunho` commitou direto na Branch pai (uma tarefa por commit); crie a worktree normalmente, a partir dela, e os commits do rascunho já vêm junto. Veja a seção 4.
- **Ajuste** (Phase `Ajuste J<n>`, do `/ajustar`) em item já integrado, sem worktree viva: crie `.worktree/<slug>-j<n>` com a branch `feature/<slug>-j<n>` a partir da Branch pai. Com a worktree viva, siga nela.
- Trabalhe nela até o fim. Registre a Branch pai no topo do `tasks.md` se faltar. A trava de testes e o hook de commit valem na worktree.

## 4. Os lotes

`python .claude/scripts/progresso.py --lote` diz o lote atual e a criticidade. Para cada lote, na ordem:

1. Siga o **ciclo do lote comum** ou o **do lote crítico** da seção Execução do `CLAUDE.md`: testes a partir dos critérios, vermelho no crítico, código, gate do lote.
2. **Vizinhança antes de editar** (`Molde: <arquivo:linha>` no commit); a decisão nomeada na tarefa vale literalmente (Reuses).
3. Tarefa de `**Domínio**: sim`: antes de codar, liste os casos limite e os estados. Lacuna da spec: grave `**Bloqueio**` na tarefa e siga com a que não depende dela (seção Execução, **Bloquear e seguir**).
4. **Commit por grupo de tarefas**, em português, citando `Tn` e `FUN-NN`, cada um fechando verde. Encadeie `typecheck && git add && git commit` numa chamada só.
5. **Fechamento do lote, uma chamada:** `python .claude/scripts/fechar-lote.py` (com `--gate "<comando filtrado pelos pacotes tocados>"` e `--rodape "<atribuição>"`). Roda o gate, grava status e `Gate:` no `tasks.md`, faz o commit de fechamento e imprime três linhas: gate, `progresso.py --lote` e `contexto.py`. Gate vermelho: nada é escrito; corrija e rode de novo.
6. **Contexto:** a terceira linha do passo 5. Saída 3 (acima de 300k): **pare**, diga só "Contexto acima do limite: rode /clear e depois /executar" e não comece o lote seguinte. O estado está no `tasks.md` e no git.

Item em **etapas** (refatoração e redesign em modo grande): uma etapa por vez, na ordem do `refatoracao.md` ou do `redesign.md`, cada uma com o gate que a skill do fluxo manda (a seção "Para o /executar e o /validar" dela vale).

**Lote rascunhado** (`**Passada**: rascunho`, tarefas com `**Status**: rascunhada`): o teste e o código já existem, escritos sem rodar. Cada tarefa traz `**Testes**:` (arquivo › nome do teste, com o `FUN-NN`) e `**Código**:`; tarefa rascunhada sem `**Testes**:` volta à lista de pendências e você a localiza em `git log --grep "T<n>"`. Lote normal ainda não rascunhado num item com a passada: **recuse** e mande rodar `/rascunho` (lotes de retrabalho e de ajuste não passam por ele e seguem o ciclo normal). Serviços de apoio (banco, Docker) sobem agora, pela primeira vez.

Em vez de escrever, **leve cada tarefa do lote, uma por vez e na ordem, por este ciclo** (só passa à próxima quando a atual fecha):

1. **Requisitos:** leia a tarefa (**What**, **Done when**, critérios `FUN-NN`, ADs citadas, Reuses) e confira, lendo o `git show`/diff do commit dela com `Read`/`Grep`, se código e teste atendem **cada** requisito. Requisito sem teste, teste que não prova o critério ou desvio sem `SPEC_DEVIATION`: anote como correção.
2. **Code review** (você mesmo, sobre o diff da tarefa, sem skill nem agente): correção e casos limite, guarda sem teste por ramo, segurança (entrada externa, SQL, autorização, log, segredo), molde da vizinhança seguido, duplicação e código morto. Em tarefa de `**Risco**: alto` seja minucioso; em risco baixo, uma passada curta. Anote os achados como correção.
3. **Testes da tarefa:** rode só os arquivos de `**Testes**:` (reporter mínimo). No lote crítico, confirme que os de comportamento falham ou passam **pelo motivo certo**.
4. **Correções:** aplique tudo o que os passos 1 a 3 acharam (código primeiro; teste só muda se o erro for dele, com o motivo no commit, nunca enfraquecido) e rode de novo até o **verde**. `[LACUNA]` (`git grep -n "\[LACUNA\]"` e a linha `Lacunas:` da tarefa): leve ao verde pela interpretação que está no código, grave `**Bloqueio**` com a pergunta e não a conclua; a resposta vem ao fim, e então ajuste código e teste e retire a marca e o bloqueio. Falha inesperada: causa raiz antes de mexer.
5. **Fechar a tarefa:** `typecheck && git add && git commit` numa chamada, citando `Tn` e `FUN-NN` (resumo curto do que o review corrigiu, se corrigiu algo). Ela **só é marcada concluída** no commit de fechamento do lote (`fechar-lote.py`), porque a marca exige o `Gate:` real; até lá segue `rascunhada` e não conta como pronta. Vá para a próxima tarefa.

Tarefa com `**Bloqueio**` é pulada neste ciclo, assim como a que depende dela. Ao fim das tarefas do lote, rode o gate do lote pelo passo 5 da lista acima (`fechar-lote.py`: grava `Gate:` e troca `rascunhada` por `concluída` em todas) e o contexto (passo 6).

Lote de **retrabalho** (Phase `Retrabalho R<n>`, gerada pelo `/validar`) é executado como qualquer outro, depois dos normais; cada tarefa cita o achado `A-NN` que corrige. O de **ajuste** (Phase `Ajuste J<n>`) também; a tarefa de reverter tira o código e o teste do critério removido, com o motivo no commit. Tarefa `cancelada` é ignorada.

Dúvida ou 2 tentativas sem verde: `**Bloqueio**` na tarefa e siga (seção Execução, **Bloquear e seguir**; os casos de parada na hora estão lá). Teste que falha de forma inesperada: ache a causa raiz antes de mudar qualquer coisa. Lição nova sobre o projeto (comando, armadilha, teste que já falhava): acrescente com a data em `.specs/projeto/regras-execucao.md`.

## 5. Fim da feature

**Antes, os bloqueios:** havendo tarefa com `**Bloqueio**`, pergunte tudo em lotes de até 4 perguntas (`AskUserQuestion`), cada uma dizendo a tarefa e o que ela trava. Grave a resposta na tarefa, apague a linha do bloqueio e execute o que destravou (patch salvo em `bloqueios/` serve de ponto de partida). Sem resposta: diga o que ficou bloqueado e que a feature **não** está pronta para o `/validar`.

Com todas as tarefas concluídas: rode o **gate completo** (lint, format, checagens do CI e a suíte inteira) e corrija o que falhar. Depois diga apenas: **"Feature <nome> pronta para validar: rode /validar."** com a linha final do `progresso.py`.

## Regras

- **Nunca** enfraqueça, pule ou apague um teste para fazê-lo passar; mudar teste existente exige o motivo no commit e a aprovação da regra de Testes.
- Nada de "já que estou aqui": só o escopo das tarefas.
- Divergiu da spec ou do desenho? `SPEC_DEVIATION: <o quê>` no código e no commit; siga as ADs do `STATE.md`.
- **Sem push, sem PR, sem merge, sem deploy.** A integração é do `/validar`, com confirmação específica.
- Tarefa de interface: só `tokens.css` e os componentes do guia; prova de tela conforme a seção Execução.
- **Poucas chamadas, saída curta:** use `Read`, `Glob` e `Grep` (não `cat`, `ls`, `grep`, `git show`), testes com reporter mínimo e comandos encadeados com `&&`.
- Tudo em português.
