# Guia do fluxo de uso próprio, de ponta a ponta

Este guia mostra o fluxo 2 funcionando, com um exemplo inventado do começo ao fim. O desenho do fluxo está em [FLUXO-USO-PROPRIO.md](FLUXO-USO-PROPRIO.md); a decisão que define a divisão entre planejamento e execução está em "Execução v5" no [DECISOES.md](DECISOES.md).

**Quando usar:** ferramenta pessoal, só você usa, roda no seu computador (Docker) ou numa nuvem gratuita, custo zero. Para produto que será vendido, use o fluxo 1 (`projeto-novo`). Para mexer num projeto que já existe, use o fluxo 3 (`feature`).

**Exemplo (fictício):** o **Assina**, um app para acompanhar as assinaturas que você paga (streaming, nuvem, academia), com valor, data de cobrança e aviso antes de renovar.

## A ideia central

O `/fluxo` **só planeja**. Ele termina no `tasks.md` com tarefas e lotes e diz uma única frase: **"O plano está disponível para execução."** Tudo o que vem depois é chamado por você, com quatro comandos:

```
/fluxo uso-proprio ── Opus ── necessidade → desenho → tarefas e lotes ──► "O plano está disponível para execução."
        │
        ├── /preparar  ── infraestrutura, guiada com você (Nível 1 síncrono + Nível 2 assíncrono)
        │        (pode rodar em paralelo ao /executar)
        ├── /executar  ── executa o tasks.md na worktree da feature, sem skills nem subagentes
        ├── /validar   ── verificador + revisão + segurança; lote de retrabalho; com PASS integra
        └── /finalizar ── E2E geral, implantação, operação e aprendizado
```

Em toda fase de planejamento a IA resume o que fez e pergunta, numa caixa de opções, **seguir / ajustar / parar**. **Ainda não sei** registra o ponto como `[A ESCLARECER]`. A **última** fase do planejamento (tarefas e lotes) não pergunta: o seu `/executar` é a aprovação.

---

## Parte 1: o fluxo (`/fluxo`, tudo em Opus)

Digite `/fluxo` e escolha uso próprio, ou use `/fluxo 2`. A skill descobre a fase pelos arquivos de `.specs/`, então o mesmo comando começa e retoma. Ela avisa para usar `/model opus`.

### Fases 1 a 3: Necessidade

**Pergunta:** vale o meu tempo construir isso, e cabe na minha infraestrutura com custo zero?

Uma conversa curta. A IA entende a dor, manda o `pesquisador` procurar algo pronto e propõe escopo, onde roda, dados e backup. Termina com **um** arquivo, `.specs/produto/necessidade.md`, e uma aprovação.

```
Onde você quer usar?          ○ Só no meu PC (Docker)  ○ Também no celular  ○ Ainda não sei
Aviso por onde?               ○ E-mail  ○ Notificação do navegador  ○ Só uma lista na tela
```

| Seção do `necessidade.md` | Exemplo no Assina |
|---|---|
| Necessidade e alternativas | Planilha hoje; o app X cobre 80% mas não avisa por e-mail |
| Escopo pessoal | Cadastrar, listar, total do mês, aviso 3 dias antes. Fora: gráficos, multiusuário |
| Onde roda | Local com Docker |
| Dados e backup | SQLite num volume; backup diário em outra pasta; quero restaurar |
| Exposição | Só rede local |
| **Veredito** | **construir** (o aviso por e-mail que nada pronto faz) |

Com **adaptar algo pronto** ou **desistir**, o fluxo **encerra**. É um bom resultado: você economizou semanas.

### Fase 4: Desenho enxuto

O `tlc-spec-driven` escreve a **spec** com requisitos em EARS e IDs rastreáveis. Backup, **restauração testada** e (se na internet) login e HTTPS entram como **critérios de aceite**:

```
FUN-03  QUANDO faltarem 3 dias ou menos para a cobrança, O SISTEMA DEVE enviar um e-mail
        de aviso uma única vez por ciclo.
FUN-07  QUANDO o usuário executar o script de restauração com um backup, O SISTEMA DEVE
        recuperar todas as assinaturas exatamente como estavam.
```

Se a ferramenta tem tela, a IA pergunta se faz o **mockup** (recomendado: 2 a 3 telas-chave e um guia de estilo em `.specs/mockup/`).

### Fase 5: Quebra em tarefas e lotes

Só o `tasks.md`, ainda em Opus. Cada tarefa é pequena, com os campos exigidos:

| Campo | Para que serve | Exemplo |
|---|---|---|
| Estimativa | Até 2h de trabalho humano | `1h` |
| Risco | alto/baixo: profundidade da revisão | `baixo` |
| Domínio | sim só para regra difícil ou ambígua | `não` |
| Criticidade | crítica/comum: ciclo do lote | `comum` |

O topo leva `**Branch pai**: main` (onde o `/validar` integra). A fase grava também `.specs/projeto/jornadas.md`: as jornadas ponta a ponta do E2E geral (ex.: "cadastrar assinatura → receber o aviso → restaurar o backup").

Infraestrutura (Docker, esqueleto, CI, backup) **não vira tarefa aqui**: é do `/preparar`. Pronto o plano, a IA diz só **"O plano está disponível para execução."**

---

## Parte 2: os comandos

### `/preparar` (Sonnet): a infraestrutura, junto com você

Grava `.specs/preparacao.md` com dois níveis, um item por vez, `[x]` só com evidência:

| Nível 1, síncrono (**necessário antes do `/executar`**) | Nível 2, assíncrono (fecha até o fim da execução) |
|---|---|
| Repositório e remoto | Staging e produção, ou o destino do Docker |
| Ambiente local que sobe com um comando | Segredos dos ambientes (nunca no repositório) |
| Esqueleto ponta a ponta | Backup agendado e **restauração testada** |
| Comando de teste (`testes.json`) | Observabilidade |
| CI com uma execução verde | Pipeline de deploy, com reversão testada |
| Pré-voo e hook de commit | |

Tudo o que cria recurso fora da máquina, custa dinheiro ou publica pede a sua confirmação específica. O `/preparar` **não publica** a aplicação.

### `/executar` (Sonnet): só execução

- **Condição:** `preparacao.py --nivel1` completo. Faltando algo, ele **recusa e lista** o que falta, sem escrever nada.
- **Como roda:** na sessão principal, **sem skills e sem subagentes**, numa **worktree da feature** (`git worktree add ../assina-<slug> -b feature/<slug>`).
- **Por lote:** testes a partir dos critérios (e vermelho no lote crítico), código, gate, **um commit por grupo de tarefas** e um **commit de fechamento** com o `Gate:`. Sem PR por lote.
- **Contexto:** ao fechar cada lote, `contexto.py` mede o contexto. **Acima de 300k**, ele para e pede `/clear` e `/executar`; o estado está no `tasks.md` e no git.
- **Lacuna da spec:** pergunta direto a você, por caixa. Exemplo: assinatura anual cobrada em 29/02 em ano não bissexto → 28/02, 01/03 ou ainda não sei.
- **Fim:** gate completo (lint, formato, suíte inteira) e a frase **"Feature assina pronta para validar: rode /validar."**

### `/validar`: uma feature por vez, na mesma branch

Roda em paralelo o `verificador` (cada critério até `arquivo:linha`, cobertura por critério, mutações, QA automatizado pela suíte e pelos testes de tela), a `revisao-codigo` e, se o app tocar segurança ou internet, o `auditor-seguranca`. Resultado em `validation.md`:

```
Validação: assina — FAIL (rodada 1)
Critérios: 13/14   Gate: 62 passaram   Sensor: 6 mutações, 5 mortas
Achados: A-01 (crítica) backup.py:22 copia o SQLite enquanto o app grava; pode corromper
```

- **Com achado:** o `/validar` acrescenta ao `tasks.md` a Phase **`Retrabalho R1`** (uma tarefa por achado, cada uma começando pelo teste que reproduz). É um **lote separado** dos normais. Você roda `/executar` (ele executa o R1) e `/validar` de novo, **na mesma sessão** se quiser, até não sobrar retrabalho. Na 3ª rodada a IA pergunta se segue.
- **Com PASS:** roda a suíte registrada (`trava-testes.py --rodar`) e pergunta como integrar à Branch pai: **merge local** ou **PR**. Push, PR e merge exigem a sua confirmação específica. Grava o `integracao.md` e oferece remover a worktree.

### `/finalizar` (Sonnet): o projeto inteiro

- **Condições:** todo item validado e integrado, e `preparacao.py --nivel2` completo. Senão ele recusa e lista.
- **E2E geral:** roda as jornadas do `jornadas.md` no staging (ou local). Falha vira retrabalho, como no `/validar`.
- **Implantação:** a skill `implantacao` (script único, teste de fumaça, backup rodado). Publicar na nuvem pede confirmação específica.
- **Operação e aprendizado:** grava `.specs/operacao.md` com a data da primeira revisão.

### Revisão periódica (a cada 1 a 3 meses)

- [ ] Ainda uso? Se não, aposentar.
- [ ] O backup rodou? Restaurar um recente numa cópia limpa.
- [ ] Há atualização de segurança nas dependências?
- [ ] Decisão: **manter, evoluir ou aposentar**. Evoluir volta ao `/fluxo` como feature.

---

## Onde ficam os artefatos

```
.specs/
├── produto/necessidade.md            fases 1-3
├── features/assina/
│   ├── spec.md  tasks.md             fases 4-5 (tasks.md: Branch pai, status, Gate:, Retrabalho R<n>)
│   ├── validation.md                 /validar
│   └── integracao.md                 /validar com PASS
├── projeto/jornadas.md  testes.json  fase 5 e /preparar
├── preparacao.md                     /preparar (Nível 1 e 2)
├── e2e-geral.md  operacao.md         /finalizar
└── STATE.md                          decisões (AD-NNN), modelo, ## Retomada
```

## Dúvidas comuns

| Situação | O que fazer |
|---|---|
| Voltei depois de uma semana | `/fluxo` (planejamento) ou o comando da etapa; todos leem `.specs/` |
| O `/executar` recusou começar | Falta item do Nível 1: rode `/preparar` |
| O contexto passou de 300k | `/clear` e `/executar`; ele retoma pelo `tasks.md` |
| Não sei responder uma pergunta | **Ainda não sei**; vira `[A ESCLARECER]` |
| Já existe algo pronto que serve | Veredito **adaptar algo pronto**; o fluxo encerra |
| Quero evoluir a ferramenta depois | `/fluxo feature` |
