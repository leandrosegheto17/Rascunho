# Guia do fluxo de feature em projeto legado, de ponta a ponta

Este guia mostra o fluxo 4 (skill `legado`) funcionando, com um exemplo inventado do começo ao fim. O desenho está em [FLUXO-FEATURE-LEGADO.md](FLUXO-FEATURE-LEGADO.md); a divisão entre planejamento e execução está em "Execução v5" no [DECISOES.md](DECISOES.md). O formato é o mesmo do [GUIA-USO-PROPRIO.md](GUIA-USO-PROPRIO.md).

**Quando usar:** acrescentar uma funcionalidade a um sistema **antigo**, pouco testado, escrito por gente que já saiu. Para projeto recente feito com IA e com testes, use o fluxo 3 (`feature`). Para limpar código sem mudar comportamento, `refatoracao`. Para defeito, `bug`.

**Princípio:** mexer sem entender tudo e sem quebrar o que funciona há anos. O código novo entra **ao lado** do antigo, por **um único ponto de integração**.

**Exemplo (fictício):** a **Loja Régis**, um sistema de pedidos em PHP de 2011, sem testes, com um servidor de produção. A feature: **enviar o comprovante do pedido por e-mail** quando o pedido é finalizado.

## Planejamento e execução são separados

O `/fluxo` (skill `legado`) **só planeja** e termina no `tasks.md` com a frase **"O plano está disponível para execução."** O resto é de comandos que você chama:

```
/fluxo legado ── Opus ── pedido → arqueologia → (mockup) → plano → rede de proteção planejada
      │                                                         ──► "O plano está disponível para execução."
      ├── /preparar   ── infraestrutura (em paralelo ao /executar)
      ├── /executar   ── worktree da feature, sem skills nem subagentes, suíte inteira a cada lote
      ├── /validar    ── verificador + revisão de código (sempre) + segurança; retrabalho; com PASS integra
      └── /finalizar  ── E2E geral, liberação cuidadosa, operação
```

## O que muda em relação à feature em projeto com IA

| | Feature (fluxo 3) | Legado (fluxo 4) |
|---|---|---|
| Entendimento do código | Reconhecimento | **Arqueologia**: como funciona de fato, histórico do git, ambiente, quem sabe |
| Antes de mudar | Rede de proteção do trecho tocado | Rede de proteção de **todo o raio de impacto** (tarefa T0) |
| Onde o código entra | Onde o padrão do projeto indica | **Ao lado** do antigo, por uma costura única |
| Gate de cada lote | Suíte inteira só ao fim da feature | **Suíte inteira ao fim de cada lote** |
| Revisão de código | Se há tarefa de risco alto | **Sempre**, no diff |
| Liberação | Normal | **Cuidadosa**: flag, staging, reversão testada |
| Saída de emergência | Não existe | Se o impacto é alto demais, o fluxo para e pergunta |

---

## Parte 1: o fluxo (`/fluxo`, tudo em Opus)

Digite `/fluxo` e escolha feature em legado, ou `/fluxo 4`. A skill lista `.specs/features/`: pastas sem `integracao.md` são features em andamento. A fase vem dos arquivos, então o mesmo comando começa e retoma.

**Entrada pronta (modo enxuto):** com um `plano.md` ou critérios já escritos, a IA oferece o **modo enxuto (Recomendado)**: um agente confere a entrada no código atual e grava só o `tasks.md`, e termina com a frase final, sem aprovação ao fim. Em legado ele mantém costura, raio de impacto e ambiente no Delta, e a T0 caracteriza todo o raio de impacto. Ambiente que não roda ou impacto alto: modo completo.

### Fase 1: Pedido

O `tlc-spec-driven` escreve a spec, com requisitos em EARS:

```
FUN-01  QUANDO um pedido passar para "finalizado", O SISTEMA DEVE enviar ao cliente um comprovante.
FUN-02  SE o cliente não tiver e-mail, ENTÃO O SISTEMA DEVE finalizar o pedido e registrar em log.
FUN-03  SE o envio falhar, ENTÃO O SISTEMA NÃO DEVE impedir nem desfazer a finalização do pedido.
```

O FUN-03 é típico de legado: o pedido funciona há anos e a feature nova **não pode** derrubá-lo.

### Fases 2 e 3: Arqueologia

Inventário, reconhecimento e `arqueologia.md`, em sete passos:

| Passo | No exemplo |
|---|---|
| Ambiente: o projeto roda? | PHP 5.6, MySQL 5.5, um `.sql` de carga que não está no README. **Roda, depois de 40 min.** |
| Histórico do git | `finalizar_pedido.php` mudou 14 vezes em 2 anos, 6 correções: **ponto quente** |
| Comportamento observado | O total é recalculado no fim com arredondamento diferente da tela |
| Conhecimento de pessoas | "O Carlos conhecia, mas saiu; só a Dona Marta usa" |
| Costuras e raio de impacto | Costura: o gancho `depois_de_finalizar()`, hoje vazio. Raio: relatório diário e transportadora |
| Ambientes | Só produção, sem flag: entra no plano criar uma flag por configuração |
| Saída de emergência | Não foi o caso |

Se o impacto for alto demais, o fluxo para e pergunta: **refatorar antes**, **serviço novo ao lado**, **reduzir o escopo** ou **seguir com o risco registrado**. Se o ambiente não roda, fazê-lo rodar vira a **primeira tarefa**.

### Fase 3b: Mockup (só se mudar telas)

A IA pergunta se faz o mockup do módulo. Sem guia de estilo no projeto, o guia mínimo **reproduz a aparência atual**. No exemplo o comprovante é um e-mail, então a fase é pulada.

### Fase 4: Plano

`tlc-spec-driven` (Design e Tasks) com as exigências do legado: código novo **ao lado** do antigo pelo ponto único, mudança mínima no arquivo antigo (uma linha chamando o código novo), **feature flag** e plano de volta. Refatoração não entra.

### Fase 5: Rede de proteção planejada (só planeja)

Pelo método da skill `rede-de-protecao`, mas **sem escrever teste agora**: a IA roda a suíte uma vez para a `## Linha de base` (na Loja Régis não há suíte: a primeira tarefa cria a infraestrutura mínima) e planeja a **T0**, que caracteriza o comportamento atual de **todo o raio de impacto** (o que o sistema *faz hoje*, incluindo o estranho).

Exemplo do `tasks.md`:

```
**Branch pai**: main
T0  Caracterizar finalizar_pedido, relatório diário e transportadora      2h  risco alto  crítica
T1  Flag COMPROVANTE_EMAIL_ATIVO (desligada por padrão)                   1h  risco baixo comum
T2  Montar o corpo do comprovante a partir do pedido                      2h  risco alto  crítica  FUN-01
T3  Enviar o e-mail sem nunca lançar exceção para quem chamou             2h  risco alto  crítica  FUN-02, FUN-03
T4  Chamar T3 em depois_de_finalizar() atrás da flag                      1h  risco alto  crítica  FUN-01
```

Pronto o `tasks.md`, a IA diz só **"O plano está disponível para execução."**

---

## Parte 2: os comandos

### `/preparar`

Infraestrutura em dois níveis (`.specs/preparacao.md`). No legado, o Nível 1 inclui fazer o ambiente **rodar** e um CI que roda a caracterização. O Nível 2 traz staging, flag em produção, backup e reversão testada. Pode rodar em paralelo ao `/executar`.

### `/executar`

Recusa começar com o Nível 1 incompleto. Cria a worktree `feature/<slug>` a partir da Branch pai e executa **na sessão principal, sem skills nem subagentes**.

- A **T0 vem primeiro**: escreve os testes de caracterização e confirma que passam (a rede de proteção).
- **Suíte inteira ao fim de cada lote**, e os testes de caracterização continuam verdes. Se um deles quebrar, a feature mudou comportamento existente: a IA para e pergunta se ajusta a feature ou aceita a mudança (registrada). **Teste de caracterização nunca é apagado para a feature passar.**
- Um commit de fechamento por lote, **sem PR**. Ao fechar cada lote, `contexto.py` mede o contexto: acima de 300k, para e pede `/clear`.
- Lacuna da spec (ex.: e-mail com formato inválido conta como "sem e-mail"?) vira caixa de pergunta: tratar como sem e-mail, tentar enviar mesmo assim ou ainda não sei.

### `/validar`

Na mesma branch e worktree, em paralelo: `verificador` (critérios, mutações, suíte e caracterização), `revisao-codigo` (**sempre** em legado) e `auditor-seguranca` (o e-mail do cliente é dado pessoal). Mais o **teste manual dos fluxos vizinhos** (relatório diário e transportadora), que é seu.

- **Com achado:** vira a Phase `Retrabalho R1` no `tasks.md`, lote próprio. Exemplo: "A-01 (crítica): o envio roda dentro da transação do pedido; se o SMTP demorar, o pedido trava (FUN-03)". Você roda `/executar` e `/validar` de novo, até não sobrar retrabalho.
- **Com PASS:** `trava-testes.py --rodar`, e a pergunta de como integrar (**merge local** ou **PR**). Push, PR e merge pedem confirmação específica. Registra o contexto do projeto: como rodar o ambiente (os 40 minutos viram 3 comandos), as costuras e as **armadilhas** (ex.: "o total é recalculado com `round()` no fim; a caracterização trava esse valor").

### `/finalizar`

Com tudo validado e integrado e o Nível 2 completo: E2E geral e **liberação cuidadosa** pela skill `liberacao`: sobe com a flag **desligada**, liga em horário calmo, acompanha o primeiro pedido, **pausa obrigatória antes de produção** e reversão testada (desligar a flag ou voltar o commit). Fecha com `.specs/operacao.md`.

---

## Laços comuns

| Situação | O que acontece |
|---|---|
| Ambiente não roda | A primeira tarefa é fazê-lo rodar; sem isso não há rede de proteção |
| Impacto alto demais | Refatorar antes, serviço novo ao lado, reduzir escopo ou seguir com risco registrado |
| Teste de caracterização quebrou | Decisão sua: ajustar a feature ou aceitar a mudança, registrando |
| Monitoramento acusou problema na liberação | Reverte e gera retrabalho para o `/executar` |
| Algo quebrou depois, em produção | `bug`; se há dano em curso, `incidente` |

## Quando o pedido vem de outro fluxo

- **De uma demanda** (sugestão, solicitação, suporte): a spec parte de `.specs/demandas/DEM-NNN-<slug>/encaminhamento.md` e leva no topo **Origem: demanda DEM-NNN**. Ao integrar, o `/validar` avisa que a demanda pode ir ao fechamento. Em solicitação, a liberação para todos espera o aceite.
- **De uma integração com terceiro** ou **de uma automação**: segue estas fases com acréscimos próprios.

## Onde ficam os artefatos

```
.specs/
├── projeto/inventario.md                   fases 2-3 e registro
├── features/comprovante-por-email/
│   ├── spec.md  reconhecimento.md          fases 1-2
│   ├── arqueologia.md                      fases 2-3
│   ├── design.md  tasks.md                 fases 4-5 (Branch pai, T0, Linha de base, Retrabalho R<n>)
│   ├── validation.md                       /validar
│   └── integracao.md                       /validar com PASS (encerra a feature)
├── preparacao.md                           /preparar
├── liberacao.md  e2e-geral.md  operacao.md /finalizar
└── STATE.md                                decisões (AD-NNN), modelo, ## Retomada
```

## Dúvidas comuns

| Situação | O que fazer |
|---|---|
| Ninguém sabe como o trecho funciona | **Ainda não sei**; vira `[A ESCLARECER]` e risco na arqueologia |
| O `/executar` recusou começar | Falta item do Nível 1: rode `/preparar` |
| O contexto passou de 300k | `/clear` e `/executar`; retoma pelo `tasks.md` e pelo `Gate:` |
| Quero só limpar o código antes | É `refatoracao`, não este fluxo |
| O projeto é recente e tem testes | Use o fluxo 3 (`feature`) |
