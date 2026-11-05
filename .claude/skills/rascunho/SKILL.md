---
name: rascunho
description: Primeira passada de construção de um projeto do zero (fluxos 1 e 2, tasks.md com "Passada - rascunho") — na sessão principal, sem skills e sem subagentes, escreve os testes a partir dos critérios e o código de cada lote na worktree da feature, commita, e não roda nada (nem testes, nem typecheck, nem lint, nem build). Marca as tarefas como rascunhadas; quem roda, corrige e leva ao verde é o /executar. Use quando o fluxo disser que o plano está disponível e o tasks.md pedir a passada de rascunho. Não executa, não valida e não faz push.
model: opus
effort: medium
---

# /rascunho

Você **só escreve**. Teste e código de cada lote, na ordem do `tasks.md`, **sem executar nada**: nenhum teste, `typecheck`, lint, build, servidor, banco ou instalação de dependência. Nada de skills, nada de subagentes. O que roda e fica verde é do `/executar`; o que é verificado de ponta a ponta é do `/validar`. Roda em **Opus** (trava de modelo do `CLAUDE.md`): como o código nasce sem a suíte à frente, o raciocínio fica por conta de quem escreve. O `/executar` seguinte volta a **Sonnet**.

Motivo: escrever tudo de uma vez, sem parar para o ciclo de rodar e corrigir, é mais rápido e mantém o contexto pequeno; o `/executar` depois corrige com a suíte à frente.

## 1. Qual feature e condições

1. Liste os `tasks.md` de `.specs/` com tarefa em aberto (`python .claude/scripts/progresso.py`). Respeite o argumento. Mais de uma: pergunte qual via `AskUserQuestion`.
2. O `tasks.md` precisa ter `**Passada**: rascunho` no topo. Sem a linha, **recuse**: o item não é projeto do zero; diga para rodar `/executar`.
3. `python .claude/scripts/preparacao.py --nivel1`. Saída diferente de 0: **recuse** e mande rodar `/preparar` (o esqueleto e a worktree dependem do Nível 1; isto só confere o arquivo, não roda o ambiente).
4. **Uma worktree por feature**, em `.worktree/<slug>` (confira que `.worktree/` está no `.gitignore`): `git worktree list`; senão `git worktree add .worktree/<slug> -b feature/<slug> <pai>`, com a **Branch pai** do topo do `tasks.md` (padrão `main`). Para a feature 2 em diante, a Branch pai já traz o rascunho integrado das anteriores. Não rode `preparar-ambiente.py`: ele executa coisas, e isso é do `/executar`.

## 2. Os lotes

`python .claude/scripts/progresso.py --lote --rascunho` diz o **primeiro lote ainda não rascunhado** e a criticidade (sai com 1 e "Todos os lotes já foram rascunhados" quando acabou). Para cada lote, na ordem do Execution Plan e só com as dependências escritas:

1. **Vizinhança antes de editar** e **Reuses** valem como no `/executar`: siga o molde (`Molde: <arquivo:linha>` no commit) e a decisão nomeada na tarefa, literalmente.
2. **Testes primeiro, a partir dos critérios de aceite** (nunca do código), conforme a Test Coverage Matrix. No lote **crítico**, escreva também o que o erro deixaria passar em silêncio: matriz política × comando, um teste por ramo de cada guarda, teste de erro com gatilho de falha, higiene de teste de banco, cada critério de tarefa de `**Risco**: alto` com teste cujo nome cita o `FUN-NN` (seção Execução do `CLAUDE.md`). Depois o código. Todos os arquivos do lote em chamadas paralelas.
3. Tarefa de `**Domínio**: sim`: antes de codar, liste os casos limite e os estados; lacuna da spec: **pare e pergunte** via `AskUserQuestion`.
4. **Sem rodar nada.** Releia o que escreveu contra o critério e a tarefa (imports, nomes, assinaturas entre arquivos) em vez de executar; o que a execução apontar é do `/executar`.
5. **Commit por grupo de tarefas**, em português, citando `Tn` e `FUN-NN`, corpo com `Molde:`. Nenhum commit afirma que algo passa. Depois, **um commit de fechamento do lote** que grava `**Status**: rascunhada` em cada tarefa do lote (caixas `- [ ]` ficam abertas) e, sob o lote, a linha `Rascunho: <comando de gate previsto> @ <árvore> = não executado`, com a árvore de `git rev-parse HEAD^{tree}`; sem `amend`.
6. Mostre a linha de `progresso.py --lote` do lote (ela diz "rascunhado").
7. **Contexto:** `python .claude/scripts/contexto.py`. Saída 1 (acima de 300k): **pare**, diga só "Contexto acima do limite: rode /clear e depois /rascunho". O estado está no `tasks.md` e no git.

Lote de **retrabalho** não passa por aqui: vai direto ao `/executar`.

## 3. Fim

Com todos os lotes da feature rascunhados (não rode o gate completo):

1. **Integre à Branch pai** (merge local, `--no-ff`), só depois de `python .claude/scripts/trava-testes.py --rascunho` na worktree, que registra o commit como rascunho (o merge é liberado; push e PR continuam exigindo suíte verde). Pergunte antes via `AskUserQuestion` (**merge local (Recomendado)** / **deixar para depois**): merge exige confirmação específica. **A worktree e a branch `feature/<slug>` ficam**: o `/executar` as retoma.
2. Mostre a linha final do `progresso.py` e consulte o roteiro (`.specs/projeto/roadmap.md`): se há **feature seguinte** com `tasks.md` de `**Passada**: rascunho` ainda não rascunhado, pergunte via `AskUserQuestion` **rascunhar a feature <nome> agora (Recomendado)** / **parar**; aceitando, repita desde a seção 1 (se o contexto estiver acima do limite, peça `/clear` e `/rascunho`). Feature do roteiro sem `tasks.md` ainda precisa do planejamento (`/fluxo`): diga.
3. Sem feature seguinte: diga apenas **"Projeto rascunhado: rode /executar."** (o `/executar` vai de feature em feature nas worktrees de `.worktree/`).

## Regras

- **Nada executa.** Nem para "só conferir". Dúvida de sintaxe se resolve lendo o código e a documentação.
- Nunca pule, comente ou enfraqueça um teste para "caber": ele é a prova do critério, e vai ser rodado pelo `/executar`.
- Nada de "já que estou aqui": só o escopo das tarefas. Divergiu da spec ou do desenho: `SPEC_DEVIATION: <o quê>` no código e no commit.
- **Sem push, sem PR, sem merge, sem deploy.**
- Tarefa de interface: só `tokens.css` e os componentes do guia; a prova de tela é do `/executar`.
- Tudo em português.
