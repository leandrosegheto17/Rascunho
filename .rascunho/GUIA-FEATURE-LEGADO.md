# Guia do fluxo de feature em projeto legado, de ponta a ponta

Este guia mostra o fluxo 4 (skill `legado`) funcionando fase por fase, com um exemplo inventado do começo ao fim. O desenho do fluxo está em [FLUXO-FEATURE-LEGADO.md](FLUXO-FEATURE-LEGADO.md); as regras que a IA segue estão em `.claude/skills/legado/` e no `.claude/CLAUDE.md`. O formato é o mesmo do [GUIA-USO-PROPRIO.md](GUIA-USO-PROPRIO.md).

**Quando usar:** acrescentar uma funcionalidade a um sistema **antigo**, pouco testado, escrito por gente que já saiu, sem IA no histórico. Para um projeto recente feito com IA e com testes, use o fluxo 3 (`feature`). Para limpar ou reorganizar código sem mudar comportamento, use `refatoracao`. Para corrigir defeito, `bug`.

**Princípio:** mexer sem entender tudo e sem quebrar o que funciona há anos. O código novo entra **ao lado** do antigo, por **um único ponto de integração**; o antigo muda o mínimo.

**Exemplo usado neste guia (fictício):** a **Loja Régis**, um sistema de pedidos em PHP de 2011, sem testes, com um único servidor de produção. A feature: **enviar o comprovante do pedido por e-mail ao cliente** quando o pedido é finalizado.

## O que muda em relação à feature em projeto com IA

| | Feature (fluxo 3) | Legado (fluxo 4) |
|---|---|---|
| Entendimento do código | Reconhecimento: onde a mudança entra | **Arqueologia**: como funciona de fato, histórico do git, ambiente, quem sabe |
| Antes de mudar | Rede de proteção do trecho tocado | Rede de proteção de **todo o raio de impacto** |
| Onde o código entra | Onde o padrão do projeto indica | **Ao lado** do antigo, por uma costura única |
| Gate de cada lote | Suíte inteira só no marco | **Suíte inteira ao fim de cada lote** |
| Revisão de código | Só se há tarefa de risco alto | **Sempre**, no diff |
| Liberação | Normal | **Cuidadosa**: flag, staging, reversão testada |
| Saída de emergência | Não existe | Se o impacto é alto demais, o fluxo para e pergunta |

## Visão geral

```
/fluxo → "Feature em projeto legado"
   │
   ▼
1   Pedido ──────────── Opus ── spec.md
2-3 Arqueologia ─────── Opus ── inventario.md, reconhecimento.md, arqueologia.md
3b  Mockup (se tem tela) ─────── mockup do módulo
4   Rede de proteção ── Sonnet ── protecao.md + commit de caracterização
5   Plano ───────────── Opus ── design.md, tasks.md
6   Implementação ───── Sonnet ── executor (6 lotes por marco) + ciclo de achados
7   Verificação ─────── Sonnet ── validation.md (PASS) + revisão do diff
8   Liberação ───────── Sonnet ── .specs/liberacao.md
9   Registro ────────── Sonnet ── contexto do projeto, inventario.md, integracao.md
```

Em **toda** fase a IA resume o que fez e pergunta, numa caixa de opções, **seguir / ajustar / parar**. Nada avança sem o seu "seguir". Em **todo** ponto de decisão a pergunta aparece como caixa clicável, e **Ainda não sei** registra o ponto como `[A ESCLARECER]`.

## Como começar

Digite `/fluxo` e escolha feature em legado, ou use `/fluxo 4`. A skill lista `.specs/features/`: as pastas sem `integracao.md` são features em andamento. Se não houver nenhuma, é feature nova; se houver, a IA pergunta qual retomar. A fase é descoberta pelos arquivos, então o mesmo comando **começa** e **retoma** (inclusive numa sessão nova).

A primeira linha situa você:

> **Feature comprovante-por-email (legado), fase 1 de 9, Pedido.** Esta fase rende melhor em Opus: use `/model opus`.

Fases 1, 2-3, 3b e 5 pedem **Opus**; as demais, **Sonnet**. Se a sessão estiver no modelo errado, a IA pergunta antes de trabalhar.

**Entrada pronta (modo enxuto):** se você já tem um `plano.md` ou critérios de aceite escritos, a IA oferece o **modo enxuto (Recomendado)**: um agente confere a entrada no código atual e grava só o `tasks.md`, com uma única aprovação. Em legado ele mantém o que a arqueologia tem de obrigatório (costura, raio de impacto, ambiente) e a tarefa T0 caracteriza todo o raio de impacto. Ambiente que não roda ou impacto alto: modo completo.

---

## Fase 1: Pedido (Opus)

**Pergunta:** o que a feature faz e como saberei que está pronta?

**O que acontece:** o `tlc-spec-driven` (fase Specify) conversa com você e escreve a spec. Se o pedido for grande demais para uma feature (vários fluxos de valor que não se liberam juntos), a skill `roteiro` quebra antes.

**Resultado:** `.specs/features/comprovante-por-email/spec.md`, com requisitos em EARS e IDs rastreáveis:

```
FUN-01  QUANDO um pedido passar para o status "finalizado", O SISTEMA DEVE enviar
        ao e-mail do cliente um comprovante com número, itens e total.
FUN-02  SE o cliente não tiver e-mail cadastrado, ENTÃO O SISTEMA DEVE finalizar
        o pedido normalmente e registrar a omissão em log, sem erro para o usuário.
FUN-03  SE o envio falhar, ENTÃO O SISTEMA NÃO DEVE impedir nem desfazer a
        finalização do pedido.
```

**Critério de passagem:** critérios testáveis e `validate_spec.py` sem erro. O FUN-03 é típico de legado: o pedido já funciona há anos, a feature nova **não pode** derrubá-lo.

---

## Fases 2 e 3: Arqueologia (Opus)

**Pergunta:** como essa parte funciona de verdade, e por onde posso entrar sem mexer no que funciona?

**O que acontece, em ordem:**

1. **Inventário** (`inventario.md`): o que o projeto já tem pronto (telas, regras, tabelas, bibliotecas).
2. **Reconhecimento** (`reconhecimento.md`): módulos e arquivos afetados, padrões em uso, testes existentes (aqui, nenhum).
3. **Arqueologia** (`arqueologia.md`), em sete passos:

| Passo | O que a IA faz | No exemplo |
|---|---|---|
| Ambiente | Tenta instalar e rodar, registra versões e passos manuais | PHP 5.6, MySQL 5.5, um `.sql` de carga inicial que não está no README. **Roda: sim, depois de 40 min.** |
| Histórico | `git log` do trecho: quem mexeu, quando, correções de bug | `finalizar_pedido.php` mudou 14 vezes em 2 anos, 6 delas correções: **ponto quente** |
| Comportamento observado | Executa o fluxo e anota o estranho | Total do pedido é recalculado no fim com arredondamento diferente da tela |
| Conhecimento de pessoas | Pergunta a você, em caixa de opções | "Quem conhece o fechamento de pedido?" → "O Carlos, que saiu; só a Dona Marta usa" |
| Costuras e raio de impacto | Escolhe um **ponto único de integração** e lista quem depende do trecho | Costura: o gancho `depois_de_finalizar()` que já existe e hoje está vazio. Raio: relatório diário de vendas, integração com a transportadora |
| Ambientes | Pergunta se há staging e feature flag | "Só produção; sem flag" → entra no plano criar uma flag simples por configuração |
| Saída de emergência | Só se o impacto for alto demais | Não foi o caso |

**Se o impacto for alto demais**, o fluxo para e pergunta:

```
O raio de impacto é grande e não há costura limpa. Como seguir?
  ○ Refatorar antes (skill refatoracao)   Cria a costura, depois refaz a arqueologia
  ○ Serviço novo ao lado do legado        Estrangula aos poucos, sem tocar no antigo
  ○ Reduzir o escopo                      Entrega só a parte que cabe numa costura
  ○ Seguir com o risco registrado         Sem rede completa; fica no arqueologia.md
```

**Se o ambiente não roda:** fazê-lo rodar vira a **primeira tarefa**. Sem isso não existe fase 4.

**Critério de passagem:** ambiente roda (ou há tarefa para fazê-lo rodar), comportamento e histórico registrados, ponto único de integração escolhido, impacto aceito ou escalado.

---

## Fase 3b: Mockup (só se a feature cria ou muda telas)

A Loja Régis não muda telas nesta feature (o comprovante é um e-mail), então a fase é pulada. Quando há tela, a IA pergunta:

```
A feature muda telas. Fazer o mockup?
  ● Fazer o mockup (Recomendado)   Só as telas do módulo, em .specs/features/<feature>/mockup/
  ○ Dispensar                      Registra o motivo no reconhecimento.md
```

Sem guia de estilo no projeto, o guia mínimo **reproduz a aparência atual** do legado, para a tela nova não destoar.

---

## Fase 4: Rede de proteção (Sonnet)

**Pergunta:** como saberei se quebrei algo?

**O que acontece:** a IA cria a branch `feature/comprovante-por-email` e roda a skill `rede-de-protecao`:

1. Roda a suíte atual como **linha de base** e separa as falhas que já existiam. (Na Loja Régis não há suíte: o primeiro passo é criar a infraestrutura mínima de testes e um teste que roda.)
2. Escreve **testes de caracterização**: eles não dizem o que o sistema *deveria* fazer, e sim o que ele **faz hoje**, incluindo o estranho. Cobrem **todo o raio de impacto**, não só o trecho alterado.

**Resultado:** `protecao.md` e um commit separado `test: caracterização de finalizar_pedido`. Exemplo do que é caracterizado:

- finalizar um pedido de 3 itens grava o total `R$ 107,35` (com o arredondamento estranho);
- o relatório diário soma esse pedido na data da finalização, não da criação;
- a integração com a transportadora recebe o payload no formato atual.

**Critério de passagem:** o comportamento do raio de impacto está caracterizado e **verde**.

> **Regra inegociável:** teste de caracterização nunca é apagado nem enfraquecido para a feature passar. Se um deles quebra, a feature **mudou um comportamento existente** e isso exige decisão sua.

---

## Fase 5: Plano (Opus)

**Pergunta:** qual o menor desvio possível?

**O que acontece:** o tlc faz **Design** e **Tasks**, com as exigências do legado:

- código novo **ao lado** do antigo, entrando pelo ponto único (o gancho `depois_de_finalizar()`);
- mudança mínima no arquivo antigo (uma linha chamando o código novo);
- **feature flag** quando possível, e **plano de volta**;
- **refatoração não entra** (é outro fluxo).

**Resultado:** `design.md` e `tasks.md`. Cada tarefa tem Estimativa (até 2h), Risco, Domínio e Criticidade. Exemplo:

```
T1  Flag COMPROVANTE_EMAIL_ATIVO em config (desligada por padrão)        1h  risco baixo  comum
T2  Montar o corpo do comprovante a partir do pedido                     2h  risco alto   crítica   FUN-01
T3  Enviar o e-mail sem nunca lançar exceção para quem chamou            2h  risco alto   crítica   FUN-02, FUN-03
T4  Chamar T3 no gancho depois_de_finalizar() atrás da flag              1h  risco alto   crítica   FUN-01
```

Aprovado o plano, a IA grava a data em **Plano aprovado em** no `reconhecimento.md`.

---

## Fase 6: Implementação (Sonnet)

**Pergunta:** a feature funciona sem alterar o que existe?

A sessão principal **não escreve o código dos lotes**. Ela orquestra; quem constrói é o agente `executor`.

**Antes do primeiro lote:** o pré-voo (`preparar-ambiente.py`) confere ferramentas, porta do banco e se o comando de teste roda tudo.

**Ciclo do marco (6 lotes; no Loja Régis, 1 marco):**

```
1. executor (Sonnet) ──► lotes seguidos, teste primeiro, commit por grupo
        │               SUÍTE INTEIRA ao fim de CADA lote (exceção do legado)
        │               lacuna de spec? PARA e devolve "Perguntas para o usuário"
        ▼
2. sessão principal ──► gate completo (lint, formato, suíte)
        ▼
3. verificador ───────► revisa código e qualidade → achados.md (crítico / não crítico)
        ▼
4. corretores ────────► um por achado, um de cada vez: críticos em Opus, demais em Sonnet
        ▼
5. verificador ───────► olha só o diff das correções; repete até zerar (máx. 2 rodadas)
```

**Exemplo de achado no legado:**

| ID | Gravidade | Onde | Achado |
|---|---|---|---|
| A-01 | crítico | `comprovante.php:31` | O envio de e-mail roda dentro da transação do pedido; se o servidor SMTP demorar, o pedido fica travado (FUN-03) |
| A-02 | não crítico | `comprovante.php:55` | Texto do e-mail com acentuação em duas codificações |

**Quando o executor para:** o FUN-02 não diz se um cliente com e-mail inválido (não vazio) conta como "sem e-mail". O executor não inventa:

```
E-mail com formato inválido no cadastro do cliente. O que fazer?
  ○ Tratar como sem e-mail (Recomendado)   Registra em log e finaliza o pedido
  ○ Tentar enviar mesmo assim              O servidor pode rejeitar e gerar ruído
  ○ Ainda não sei                          Fica [A ESCLARECER]; o lote não avança nessa tarefa
```

**Critério de passagem:** gates verdes e **caracterização intacta**. Se um teste de caracterização quebrar, a IA para e pergunta: ajustar a feature ou aceitar a mudança de comportamento (registrada).

Em projetos longos, ao fechar um marco a IA oferece **seguir numa sessão nova (Recomendado)**: grava a `## Retomada` do `.specs/STATE.md` e você faz `/clear` e `/fluxo`.

---

## Fase 7: Verificação (Sonnet)

**Pergunta:** funciona e não houve regressão?

**O que acontece, nesta ordem:**

1. **Verificador robusto** (feature inteira, até 10 mutações): rastreia cada critério até a asserção (`arquivo:linha`), injeta falhas numa cópia isolada e confere os testes de caracterização. Resultado: `validation.md`.
2. Com **PASS**, a **`revisao-codigo` em modo curto** revisa o diff. Em legado ela roda **sempre**, não só com risco alto.
3. **`auditor-seguranca`** só se a feature tocar login, permissões, pagamento ou dados pessoais (o e-mail do cliente é dado pessoal; no exemplo a auditoria entra para checar injeção de cabeçalho no envio).
4. **Teste manual dos fluxos vizinhos** listados no raio de impacto: gerar o relatório diário e conferir a transportadora.

**Resultado:**

```
Validação: comprovante-por-email — PASS
Critérios: 3/3 com asserção localizada
Gate: 41 testes (28 de caracterização), 0 falhas
Sensor: 5 mutações, 5 mortas
Fluxos vizinhos: relatório diário e transportadora conferidos manualmente
```

---

## Fase 8: Liberação cuidadosa (Sonnet)

**Pergunta:** como coloco no ar com reversão fácil?

1. **Checagem final de testes:** com tudo commitado, `python .claude/scripts/trava-testes.py --rodar`. Suíte vermelha, não libera. Um hook também bloqueia `git push`, `gh pr create` e `git merge` sem a suíte verde registrada.
2. **Integração da branch:** a IA pergunta por caixa se será merge local ou PR. Push, PR e deploy exigem **confirmação específica**.
3. **Skill `liberacao`:** plano conforme a arqueologia (staging e flag). Na Loja Régis, sem staging:
   - subir com a flag **desligada**;
   - ligar em horário calmo, acompanhar o log do primeiro pedido;
   - **pausa obrigatória** antes de produção, para você confirmar;
   - reversão testada: desligar a flag, ou voltar ao commit anterior com o comando registrado.

**Resultado:** entrada em `.specs/liberacao.md`. Se o monitoramento acusar problema, reverte e corrige na fase 6.

---

## Fase 9: Registro (Sonnet)

**Pergunta:** o próximo a mexer aqui vai sofrer menos?

1. **Contexto do projeto** (`CLAUDE.md` ou equivalente; cria um mínimo se não houver): como rodar o ambiente (os 40 minutos viram 3 comandos), as costuras usadas e as **armadilhas** descobertas. Também corrige o que a feature tornou falso no README ou em `docs/`.
2. **`inventario.md`** com as peças novas.
3. **`integracao.md`**: data, forma de integração, commit, resultado da suíte, link para a liberação.

Exemplo de armadilha registrada: *"`finalizar_pedido.php` recalcula o total com `round()` no fim, diferente da tela; os testes de caracterização travam esse valor. Não 'corrija' sem decisão."*

Com `integracao.md` gravado, a feature é considerada encerrada e some da lista de "em andamento".

---

## Laços comuns

| Situação | O que acontece |
|---|---|
| Ambiente não roda | A primeira tarefa é fazê-lo rodar; sem isso não há fase 4 |
| Impacto alto demais | Refatorar antes, serviço novo ao lado, reduzir escopo ou seguir com risco registrado |
| Teste de caracterização quebrou | A feature mudou comportamento existente: decisão sua (ajustar ou aceitar, registrando) |
| Monitoramento acusou problema na liberação | Reverte e corrige na fase 6 |
| Algo quebrou depois, em produção | `bug`; se há dano em curso, `incidente` |

## Quando o pedido vem de outro fluxo

- **De uma demanda** (sugestão, solicitação, suporte): o Specify parte de `.specs/demandas/DEM-NNN-<slug>/encaminhamento.md` e a spec leva no topo **Origem: demanda DEM-NNN**. Ao fechar, a IA avisa que a demanda pode ir ao fechamento com o autor. Em solicitação, a liberação para todos espera o aceite (demonstração com flag ligada só para quem pediu).
- **De uma integração com terceiro** ou **de uma automação**: segue estas fases com acréscimos próprios; a automação para depois da integração da branch.

## Para acompanhar o progresso

`/progresso` mostra onde você está (ex.: "Faltam 6 de 12 tarefas: 50% concluído"). O resumo de cada fase já traz essas linhas.

## Onde ficam os artefatos

```
.specs/
├── projeto/inventario.md                   fases 2 e 9
├── features/comprovante-por-email/
│   ├── spec.md                             fase 1
│   ├── reconhecimento.md                   fase 2 (Mockup, Plano aprovado em)
│   ├── arqueologia.md                      fases 2-3
│   ├── protecao.md                         fase 4
│   ├── design.md  tasks.md                 fase 5 (status e Gate: por lote)
│   ├── achados.md                          fases 6 e 7
│   ├── validation.md                       fase 7
│   └── integracao.md                       fase 9 (encerra a feature)
├── liberacao.md                            fase 8
└── STATE.md                                decisões (AD-NNN), modelo, ## Retomada
```

## Dúvidas comuns

| Situação | O que fazer |
|---|---|
| Voltei depois de uma semana | `/fluxo`. Ele lê `.specs/` e diz em que fase está |
| A IA está no modelo errado | Escolha **Vou trocar** e digite `/model opus` ou `/model sonnet` |
| Ninguém sabe como o trecho funciona | Responda **Ainda não sei**; vira `[A ESCLARECER]` e risco registrado na arqueologia |
| Quero só limpar o código antes | Isso é `refatoracao`, não este fluxo |
| O projeto é recente e tem testes | Use o fluxo 3 (`feature`) |
