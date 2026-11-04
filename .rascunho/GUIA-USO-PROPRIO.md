# Guia do fluxo de uso próprio, de ponta a ponta

Este guia mostra o fluxo 2 funcionando, fase por fase, com um exemplo inventado do começo ao fim. O desenho do fluxo está em [FLUXO-USO-PROPRIO.md](FLUXO-USO-PROPRIO.md); as regras que a IA segue estão em `.claude/skills/uso-proprio/` e no `.claude/CLAUDE.md`.

**Quando usar:** ferramenta pessoal, só você usa, roda no seu computador (Docker) ou numa nuvem gratuita, custo zero. Para produto que será vendido, use o fluxo 1 (`projeto-novo`). Para mexer num projeto que já existe, use o fluxo 3 (`feature`).

**Exemplo usado neste guia (fictício):** o **Assina**, um app para acompanhar as assinaturas que você paga (streaming, nuvem, academia), com valor, data de cobrança e aviso antes de renovar.

## Visão geral

```
/fluxo → "Aplicação para uso próprio"
   │
   ▼
1-3 Necessidade ── Opus ── necessidade.md ──► construir / adaptar algo pronto / desistir
   ▼
4   Desenho enxuto ── Opus ── spec.md (+ mockup, se tem tela)
   ▼
5-6 Preparação e construção ── Sonnet ── tasks.md → executor (6 lotes por marco)
   │                                        └─ a cada marco: gate → verificador → correções
   ▼
7   Validação ── Sonnet ── validation.md (+ seguranca.md se na internet)
   ▼
8   Implantação ── Sonnet ── implantacao.md, script único, backup
   ▼
9   Uso e manutenção ── revisão a cada 1 a 3 meses: manter / evoluir / aposentar
```

Em **toda** fase: a IA resume o que fez e pergunta, numa caixa de opções, **seguir / ajustar / parar**. Nada avança sem o seu "seguir". Parar é um resultado válido e fica registrado.

Em **todo** ponto em que a IA precisa de uma decisão sua, a pergunta aparece como caixa clicável (nunca como texto solto). Se você não souber responder, escolha **Ainda não sei**: o ponto vira `[A ESCLARECER]` no documento e você resolve depois.

## Como começar

Digite `/fluxo` e escolha **uso próprio**, ou vá direto com `/fluxo 2`. A skill olha a pasta `.specs/` para descobrir em que fase o trabalho está, então o mesmo comando serve para **começar** e para **retomar** depois de dias ou numa sessão nova.

A primeira linha da resposta sempre situa você:

> **Fase 1 de 9, Necessidade.** Esta fase rende melhor em Opus: use `/model opus`.

Se a sessão estiver no modelo errado, a IA pergunta antes de trabalhar (trava de modelo). Fases 1 a 4 pedem **Opus**; da 5 em diante, **Sonnet**.

---

## Fases 1 a 3: Necessidade (Opus)

**Pergunta:** vale o meu tempo construir isso, e cabe na minha infraestrutura com custo zero?

**O que acontece:** uma conversa curta. A IA entende a dor, manda o agente `pesquisador` procurar algo pronto (gratuito, de preferência auto-hospedável) e propõe escopo, onde roda, stack, dados e backup. Termina com **um** arquivo e **uma** aprovação.

**Exemplo:**

> Você: quero um app para controlar minhas assinaturas e me avisar antes de renovar.

A IA pergunta o que muda o rumo (no máximo 3 perguntas):

```
Onde você quer usar?          ○ Só no meu PC (Docker)  ○ Também no celular  ○ Ainda não sei
Quantas assinaturas hoje?     ○ Até 10  ○ 10 a 30  ○ Ainda não sei
Aviso por onde?               ○ E-mail  ○ Notificação do navegador  ○ Só uma lista na tela
```

O `pesquisador` volta com alternativas, por exemplo um app open source de finanças pessoais que já tem "contas recorrentes". A IA mostra o que cada uma cobre e o que não cobre.

**Resultado:** `.specs/produto/necessidade.md`, com:

| Seção | Exemplo no Assina |
|---|---|
| Necessidade e alternativas | "Planilha hoje; o app X cobre 80% mas não avisa por e-mail" |
| Escopo pessoal | Cadastrar, listar, total do mês, aviso 3 dias antes. Fora: gráficos, multiusuário |
| Onde roda | Local com Docker; sem nuvem |
| Dados e backup | SQLite num volume; backup diário em outra pasta; perder custa pouco, mas quero restaurar |
| Exposição | Só rede local (sem login, sem HTTPS) |
| **Veredito** | **construir** (motivo: o aviso por e-mail que nada pronto faz) |

**Decisão do veredito:**

- **construir:** segue para a fase 4.
- **adaptar algo pronto:** o fluxo **encerra**, mostra qual solução e oferece ajudar a configurá-la. É um bom resultado: você economizou semanas.
- **desistir:** encerra com o motivo registrado.

Se o escopo for grande demais para uma feature, a skill `roteiro` quebra em features ordenadas (fase 3b). Ferramenta pessoal quase nunca precisa; ela pula e diz o motivo.

---

## Fase 4: Desenho enxuto (Opus)

**Pergunta:** qual a estrutura mais simples que serve?

**O que acontece:** o `tlc-spec-driven` escreve a **spec** a partir da `necessidade.md` e deixa o próprio tlc dimensionar a profundidade (ferramenta pessoal costuma ser pequena ou média). Backup, **restauração testada** e, se houver internet, **login e HTTPS** entram como critérios de aceite, não como lembretes.

**Resultado:** `.specs/features/assina/spec.md`, com requisitos no formato EARS e IDs rastreáveis. Exemplo de trecho:

```
FUN-03  QUANDO faltarem 3 dias ou menos para a cobrança de uma assinatura,
        O SISTEMA DEVE enviar um e-mail de aviso uma única vez por ciclo.
FUN-07  QUANDO o usuário executar o script de restauração com um arquivo de
        backup, O SISTEMA DEVE recuperar todas as assinaturas exatamente
        como estavam no momento do backup.
```

**Mockup (se tem tela):** depois da spec, a IA pergunta:

```
O Assina tem tela. Fazer o mockup?
  ● Fazer o mockup (Recomendado)   2 a 3 telas-chave e um guia de estilo em .specs/mockup/
  ○ Dispensar                      Vai direto para as tarefas
```

Se fizer, a skill `mockup-visual` propõe 2 ou 3 direções visuais, você escolhe e aprova o guia e as telas. O resultado é registrado em `necessidade.md` na linha **Mockup**: `aprovado`, `dispensado — <motivo>` ou `não se aplica`.

---

## Fases 5 e 6: Preparação e construção (Sonnet)

Aqui o fluxo mudou na v4: **a sessão principal não escreve o código dos lotes.** Ela orquestra; quem constrói é o agente `executor`.

### Preparação: o `tasks.md`

O tlc quebra a spec em **tarefas pequenas** (`T1`, `T2`...). Cada uma tem, por regra do projeto:

| Campo | Para que serve | Exemplo |
|---|---|---|
| Estimativa | Até 2h de trabalho humano; acima disso, divide | `1h` |
| Risco | alto/baixo: define a profundidade da revisão | `baixo` |
| Domínio | sim só para regra difícil ou ambígua | `não` |
| Criticidade | crítica/comum: define o ciclo do lote | `comum` |

As primeiras tarefas de um uso próprio são sempre as mesmas: **ambiente reproduzível (Docker)**, **esqueleto que roda ponta a ponta** e **script de backup e de restauração**. Só depois vêm as funcionalidades.

As tarefas são agrupadas em **lotes** (até 6h somadas). O comando `python .claude/scripts/progresso.py --lote` mostra o lote atual e a criticidade dele. Projeto pequeno como o Assina cabe em 1 ou 2 lotes.

Antes do primeiro lote roda o **pré-voo** (`preparar-ambiente.py`): confere Docker, porta livre, gerenciador de pacotes e se o comando de teste do projeto de fato roda tudo. Ele imprime o comando que corrige cada problema.

### Construção: o ciclo do marco

Um **marco** são 6 lotes (ou o que sobrar, nos projetos pequenos). O que acontece em cada um:

```
1. executor (Sonnet) ──► executa os lotes seguidos, sozinho
        │               teste primeiro, commit por grupo, Gate: registrado
        │               lacuna de spec? PARA e devolve "Perguntas para o usuário"
        ▼
2. sessão principal ──► gate completo (lint, formato, suíte inteira)
        ▼
3. verificador ───────► revisa código e qualidade da execução → achados.md
        │               cada achado: crítico ou não crítico
        ▼
4. corretores ────────► um executor por achado, UM DE CADA VEZ
        │               críticos: Opus (primeiro)   não críticos: Sonnet
        ▼
5. verificador ───────► olha só o diff das correções: fecha ou reabre
        │               repete até zerar (máx. 2 rodadas; depois pergunta a você)
        ▼
   marco fechado
```

**Exemplo de `achados.md` no Assina:**

| ID | Gravidade | Onde | Achado | Situação |
|---|---|---|---|---|
| A-01 | crítico | `backup.py:22` | O backup copia o arquivo SQLite enquanto o app grava; pode sair corrompido | corrigido, fechado |
| A-02 | não crítico | `lista.ts:40` | Formatação de data duplicada em duas telas | corrigido, fechado |

O A-01 foi para um executor **Opus** e o A-02 para um **Sonnet**. Você não precisa fazer nada, a menos que a IA pergunte.

### Quando o executor para e pergunta

Imagine que a spec não diz o que fazer com uma assinatura anual cobrada em 29 de fevereiro. O executor **não inventa a regra**. Ele para e devolve a pergunta; a sessão principal abre uma caixa para você:

```
Assinatura anual com cobrança em 29/02: em ano não bissexto, cobra em...
  ○ 28/02 (Recomendado)   Mantém o aviso antes do vencimento real
  ○ 01/03                 Segue o que a maioria dos serviços faz
  ○ Ainda não sei         Fica como [A ESCLARECER] e o lote não avança nessa tarefa
```

Você responde, a sessão dispara o executor de novo e ele continua de onde parou.

### Trocar de sessão (marcos)

Em projetos longos, a conversa fica cara. Ao fechar um marco, a IA oferece **seguir numa sessão nova (Recomendado)**: grava a seção `## Retomada` do `.specs/STATE.md` (lote, serviços no ar, estado dos achados), e você faz `/clear` e `/fluxo`. A sessão nova retoma só pelos arquivos. Você não perde nada, porque toda aprovação está gravada.

### Regras de teste que valem aqui

- Toda mudança de comportamento tem **teste automatizado** que falharia sem ela.
- Os testes nascem dos **critérios de aceite**, nunca do código já escrito.
- Ninguém apaga, pula ou enfraquece teste para fazê-lo passar.

---

## Fase 7: Validação (Sonnet)

**Pergunta:** funciona, é seguro e os dados estão a salvo?

**O que acontece:** um `verificador` independente (nunca o mesmo agente que construiu) faz a verificação **robusta** da feature inteira: rastreia cada critério até a asserção que o prova (`arquivo:linha`), injeta falhas pequenas numa cópia isolada para ver se os testes pegam (até 10 mutações) e, no caso do uso próprio, **restaura o backup a partir de uma cópia limpa**.

Se houver achado, entra o mesmo ciclo de correção do marco.

**Resultado:** `.specs/features/assina/validation.md`, curto (~40 linhas):

```
Validação: assina — PASS
Critérios: 14/14 com asserção localizada
Gate: 62 testes passaram, 0 falharam
Sensor: 6 mutações, 6 mortas
Restauração: backup de ontem restaurado numa cópia limpa, 23 assinaturas conferidas
```

**Segurança:** se o app **ficar exposto na internet**, o `auditor-seguranca` (Opus) roda depois do PASS e gera `seguranca.md`. Sem achado crítico ou alto, segue. O Assina fica só na rede local, então essa etapa é dispensada e o motivo fica registrado.

**Falhou a restauração?** Volta para a construção. **Não implanta.**

---

## Fase 8: Implantação (Sonnet)

**Pergunta:** como colocar no ar com um comando, sem perder dados e com volta fácil?

**Antes de tudo:** a checagem final de testes. Com tudo commitado, roda `python .claude/scripts/trava-testes.py --rodar`. Suíte vermelha, não implanta. Um hook também bloqueia `git push`, `gh pr create` e `git merge` quando o commit não tem a suíte verde registrada.

**O que acontece (destino "local com Docker", como no Assina):**

- `docker-compose.yml` com reinício automático e volume nomeado para os dados;
- variáveis num `.env` fora do git;
- tarefa agendada de backup diário;
- **script único** de implantação (`scripts/implantar.ps1`, no seu Windows) e comando de volta à versão anterior.

**Nuvem gratuita?** A IA pede ao `pesquisador` os **limites atuais** do serviço (nunca de memória) e **pede confirmação específica** antes de publicar, dizendo o serviço e o que será enviado. Publicar é ação externa.

**Teste de fumaça:** abrir o app, cadastrar uma assinatura, reiniciar o container e conferir que o dado persiste; rodar o backup uma vez e ver o arquivo gerado.

**Resultado:** `.specs/implantacao.md` com comandos, endereço, backup e como voltar.

---

## Fase 9: Uso e manutenção

Daqui em diante é uso real. A ferramenta pessoal morre por **abandono**, não por falta de clientes, então a IA sugere uma **revisão a cada 1 a 3 meses** (ou quando você voltar ao projeto):

- [ ] Ainda uso? Se não usei no último período, considerar aposentar.
- [ ] O backup rodou? Restaurar um recente numa cópia limpa.
- [ ] Há atualização de segurança nas dependências?
- [ ] (Nuvem) Os limites do plano gratuito mudaram?
- [ ] Continua só na rede local ou passou a ter acesso pela internet?
- [ ] **Decisão:** manter, evoluir ou aposentar.

- **Evoluir:** vira uma **feature** pelo fluxo 3 (`/fluxo feature`) ou volta à fase 4 se for mudança grande. Exemplo: "quero ver gráfico de gasto por mês".
- **Aposentar:** exportar os dados em formato aberto, parar e remover o serviço, registrar em `implantacao.md` onde ficou a exportação.
- **Algo quebrou:** é um bug, fluxo `bug` (`/fluxo bug`). Se um defeito em produção causa dano em curso, é `incidente`.

---

## Para acompanhar o progresso

- `/progresso` mostra a qualquer momento onde você está (ex.: "Faltam 8 de 20 tarefas: 60% concluído").
- Ao fim de cada fase o resumo já traz essas linhas.

## Onde ficam os artefatos

```
.specs/
├── produto/necessidade.md          fases 1-3
├── features/assina/
│   ├── spec.md                     fase 4
│   ├── tasks.md                    fase 5 (status e Gate: por lote)
│   ├── achados.md                  fase 6 (marcos) e 7
│   └── validation.md               fase 7
├── mockup/                         fase 4 (se tem tela)
├── seguranca.md                    fase 7 (se exposto à internet)
├── implantacao.md                  fases 8-9
└── STATE.md                        decisões (AD-NNN), modelo escolhido, ## Retomada
```

## Dúvidas comuns

| Situação | O que fazer |
|---|---|
| Voltei ao projeto depois de uma semana | `/fluxo`. Ele lê `.specs/` e diz em que fase está |
| A IA está no modelo errado para a fase | Ela pergunta; escolha **Vou trocar** e digite `/model opus` ou `/model sonnet` |
| Não sei responder uma pergunta | Escolha **Ainda não sei**; vira `[A ESCLARECER]` |
| Quero parar no meio | Escolha **parar**; o motivo fica registrado e dá para retomar depois |
| Já existe algo pronto que serve | Veredito **adaptar algo pronto**; o fluxo encerra e ajuda a configurar |
| O executor devolveu uma pergunta | A sessão abre a caixa de opções; sua resposta destrava o próximo disparo |
| Quero mostrar o projeto a mais gente | Isso muda o escopo (login, privacidade, suporte) e aproxima do fluxo 1; veja "Em aberto" em [FLUXO-USO-PROPRIO.md](FLUXO-USO-PROPRIO.md) |
