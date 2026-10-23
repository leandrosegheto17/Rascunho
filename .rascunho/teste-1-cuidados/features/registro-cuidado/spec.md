# Registro de cuidado Specification

## Problem Statement

Famílias que dividem o cuidado de um idoso ou dependente, com ou sem cuidador contratado, não têm um registro único do que foi feito: se o remédio foi dado, se a pessoa comeu e tomou banho, o que ocorreu no turno. A informação se espalha em conversas, papéis e memória. O MVP entrega um registro compartilhado, em português, no celular, para validar se grupos reais o usam e pagariam por ele.

## Goals

- [ ] Um membro registra remédio, banho, refeição ou ocorrência em até 3 toques a partir da tela inicial.
- [ ] Todo membro vê o registro de outro membro em até 5 segundos, com conexão ativa.
- [ ] Um novo membro entra no grupo e faz o primeiro registro em até 3 minutos, sem instalar o app.
- [ ] Nenhum dado de um grupo é acessível por quem não pertence a ele.
- [ ] Famílias ativas após 30 dias, registros por dia por grupo e membros ativos por grupo são medidos desde o primeiro dia.

## Out of Scope

| Feature | Reason |
| ------- | ------ |
| Alertas e lembretes de remédio | Aproxima o app de software como dispositivo médico (RDC 657/2022) e exige notificações push |
| Plano de medicação com horários e controle de estoque | Mesma razão; fora da menor solução |
| Escala de turnos e agenda de consultas | Fora da Opção B |
| Várias pessoas cuidadas por grupo | Decisão do usuário: uma pessoa por grupo |
| Permissões diferentes para o cuidador contratado | Decisão do usuário: só administrador e membro |
| Editar ou apagar um registro | Decisão do usuário: só anular com motivo |
| Relatórios para médico ou agência | Fora da Opção B |
| App nativo e lojas de apps | O MVP é PWA |
| Cobrança, plano gratuito com limites | A assinatura vem depois do MVP; a disposição a pagar é medida por lista de espera |
| Termo de consentimento assinado | Depende do parecer do advogado |
| Uso direto pela pessoa cuidada | O público são os familiares e o cuidador |
| Funções clínicas (diagnóstico, sinais vitais, orientação de dose) | Evita enquadramento como dispositivo médico |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --------------------- | -------------- | --------- | ---------- |
| Como se entra no app | Código de 6 dígitos por e-mail, válido por 10 minutos, com até 5 tentativas | Funciona no PWA instalado e no Safari, sem depender de link; barato (viabilidade técnica) | y |
| Como se registra remédio | Lista da pessoa cadastrada pelo administrador, mais opção "outro" em texto livre | Registro em um toque sem travar quando surge remédio novo | y |
| Correção de registro | Anular com motivo de até 140 caracteres; sem editar nem apagar | Preserva a confiança no histórico e simplifica a sincronização com fila local | y |
| Papéis | Administrador e membro; "cuidador" é rótulo sem permissão própria | Menor regra de acesso que permite revogar quem sai | y |
| Pessoas por grupo | Uma | Consentimento claro por grupo; menos telas | y |
| Hora do registro | Hora atual, ajustável para até 24 horas atrás, nunca futura; guarda também a hora do lançamento | Quem anota depois não perde o horário real; limita a retroatividade | y |
| Consentimento | O administrador declara ser a pessoa ou o responsável e aceita os termos ao criar o grupo; cada convidado aceita o aviso ao entrar; aceites gravados com data | Única base legal realista é o consentimento (pesquisa); validade jurídica depende do advogado | y |
| Exclusão | O administrador exclui o grupo; dados ocultos e apagados em 30 dias, incluindo fotos | Atende ao direito de eliminação sem apagar por clique errado | y |
| Tamanho do grupo | No máximo 20 membros ativos por grupo | Cobre famílias grandes com cuidadores; protege o limite de conexões em tempo real | n |
| Convite | Link com token de uso único, válido por 7 dias, revogável; só entra após aprovação do administrador | Link pode ser reencaminhado pelo WhatsApp (pesquisa de viabilidade) | n |
| Sessão | Permanece 30 dias sem uso; ao expirar, novo código | Equilibra conveniência com o risco de aparelho perdido; o iPhone pode descartar a sessão antes | n |
| Ocorrência | Texto de 1 a 500 caracteres e no máximo 1 foto | Registro curto; limita armazenamento | n |
| Foto | Compressão no aparelho para até 1 MB e lado maior de 1.600 px, metadados removidos | Evita upload pesado e vaza menos dado (viabilidade técnica) | n |
| Linha do tempo | Mostra o dia atual; "dias anteriores" carrega um dia por vez; filtro por tipo | Leitura rápida no celular | n |
| Atualização da linha do tempo | Em até 5 segundos com conexão ativa, por assinatura em tempo real ou consulta periódica | O mecanismo é decisão do desenho; o contrato é o prazo | n |
| Fuso horário | Horário de Brasília (America/Sao_Paulo) para todos | Mercado inicial é o Brasil | n |
| Idioma | Português do Brasil | Mercado inicial | n |
| Cuidador contratado sem e-mail | Fora do MVP; o cuidador precisa de e-mail para entrar | Login por e-mail; WhatsApp custa mais e não está confirmado | n |
| Hospedagem | Dados em São Paulo | Evita transferência internacional (LGPD) | n |
| Notificações | Nenhuma no MVP | Sem push; alertas ficaram fora do escopo | y |

**Open questions:** none - all resolved or logged above (required before the spec is confirmed).

Pontos jurídicos e de plataforma continuam sendo risco do MVP, não pré-requisito: validade do consentimento por idoso sem discernimento e sem curatela, papel da plataforma na LGPD, e comportamento do PWA no iPhone (sessão após 7 dias, link de convite). Ver `decisao.md` e `viabilidade-tecnica.md`.

---

## User Stories

### P1: Entrar no app e criar o grupo ⭐ MVP

**User Story**: Como familiar que organiza o cuidado, quero entrar com meu e-mail e criar o grupo da pessoa cuidada, para começar a registrar com a família.

**Why P1**: Sem conta e grupo nada mais existe; o consentimento nasce aqui.

**Acceptance Criteria** (each line is one EARS pattern):

1. WHEN uma pessoa informa um e-mail válido THEN the system SHALL enviar um código de 6 dígitos para esse e-mail, válido por 10 minutos.  <!-- event-driven -->
2. WHEN a pessoa informa o código correto dentro da validade THEN the system SHALL iniciar uma sessão que dura 30 dias sem uso.  <!-- event-driven -->
3. IF a pessoa erra o código 5 vezes seguidas THEN the system SHALL invalidar o código e bloquear novos envios para esse e-mail por 15 minutos.  <!-- unwanted-behavior -->
4. IF o código informado expirou ou já foi usado THEN the system SHALL recusar o código e oferecer o envio de um novo.  <!-- unwanted-behavior -->
5. IF o e-mail informado não tem formato válido THEN the system SHALL mostrar a mensagem "Informe um e-mail válido" sem enviar código.  <!-- unwanted-behavior -->
6. WHEN uma pessoa autenticada cria um grupo informando o nome da pessoa cuidada e marcando a declaração de que é a pessoa ou seu responsável THEN the system SHALL criar o grupo, torná-la administradora e gravar o aceite com data e hora.  <!-- event-driven -->
7. IF a pessoa tenta criar o grupo sem marcar a declaração THEN the system SHALL impedir a criação e explicar que a declaração é obrigatória.  <!-- unwanted-behavior -->

**Independent Test**: Pedir o código por e-mail, entrar, criar um grupo com a declaração marcada e ver a tela do grupo vazia.

---

### P1: Convidar familiares e cuidador ⭐ MVP

**User Story**: Como administrador, quero convidar familiares e o cuidador por link e aprovar quem entra, para que só pessoas certas vejam o cuidado.

**Why P1**: Um registro compartilhado só vale com mais de uma pessoa; o convite é o ponto frágil de segurança.

**Acceptance Criteria**:

1. WHEN o administrador gera um convite THEN the system SHALL criar um link com token de uso único, válido por 7 dias.  <!-- event-driven -->
2. WHEN uma pessoa abre um link de convite válido THEN the system SHALL pedir login por código e mostrar o aviso de consentimento antes de pedir o aceite.  <!-- event-driven -->
3. WHEN a pessoa aceita o aviso THEN the system SHALL registrar o pedido de entrada como pendente e invalidar o link.  <!-- event-driven -->
4. WHEN o administrador aprova um pedido pendente THEN the system SHALL tornar a pessoa membro, com o rótulo de "familiar" ou "cuidador" escolhido por ela.  <!-- event-driven -->
5. IF o link está expirado, já usado ou revogado THEN the system SHALL mostrar "Convite inválido" e não revelar o nome do grupo.  <!-- unwanted-behavior -->
6. WHEN o administrador revoga um convite pendente THEN the system SHALL invalidar o link imediatamente.  <!-- event-driven -->
7. WHEN o administrador remove um membro THEN the system SHALL encerrar as sessões dele no grupo e bloquear o acesso a todos os dados do grupo em até 5 segundos.  <!-- event-driven -->
8. IF o grupo já tem 20 membros ativos THEN the system SHALL recusar novas aprovações e informar o limite.  <!-- unwanted-behavior -->

**Independent Test**: Gerar um convite, abrir em outro aparelho, aceitar o aviso, aprovar, e ver o novo membro acessar o grupo; remover o membro e ver o acesso cair.

---

### P1: Registrar remédio, banho, refeição e ocorrência ⭐ MVP

**User Story**: Como membro do grupo, quero registrar o que fiz em poucos toques, para que os outros saibam o que já foi feito.

**Why P1**: É o valor central do produto; o critério de usabilidade é "poucos toques".

**Acceptance Criteria**:

1. WHEN o administrador cadastra um remédio com nome e dose em texto THEN the system SHALL incluí-lo na lista de remédios do grupo.  <!-- event-driven -->
2. WHEN um membro toca num remédio da lista e confirma THEN the system SHALL gravar o registro com o remédio, o autor e a hora atual.  <!-- event-driven -->
3. WHEN um membro escolhe "outro remédio" e informa um nome de 1 a 80 caracteres THEN the system SHALL gravar o registro com esse nome em texto livre.  <!-- event-driven -->
4. WHEN um membro registra banho THEN the system SHALL gravar o registro com o autor e a hora, sem exigir outro campo.  <!-- event-driven -->
5. WHEN um membro registra refeição escolhendo café da manhã, almoço, lanche, jantar ou ceia, e opcionalmente "comeu tudo", "comeu pouco" ou "recusou" THEN the system SHALL gravar o registro com essas escolhas.  <!-- event-driven -->
6. WHEN um membro registra uma ocorrência com texto de 1 a 500 caracteres THEN the system SHALL gravar o registro com o texto, o autor e a hora.  <!-- event-driven -->
7. WHEN um membro escolhe uma hora diferente da atual dentro das últimas 24 horas THEN the system SHALL gravar o registro com essa hora e guardar também o instante do lançamento.  <!-- event-driven -->
8. IF a hora escolhida é futura ou anterior a 24 horas THEN the system SHALL recusar a hora e mostrar o intervalo permitido.  <!-- unwanted-behavior -->
9. IF o texto da ocorrência está vazio ou passa de 500 caracteres THEN the system SHALL recusar o registro e indicar o limite.  <!-- unwanted-behavior -->
10. IF o membro toca duas vezes no mesmo botão de confirmação em até 10 segundos com os mesmos dados THEN the system SHALL gravar um único registro.  <!-- unwanted-behavior -->
11. The system SHALL permitir que o membro conclua um registro de remédio, banho ou refeição em no máximo 3 toques a partir da tela inicial.  <!-- ubiquitous -->

**Independent Test**: Cadastrar dois remédios, registrar um remédio, um banho, uma refeição e uma ocorrência, e conferir autor e hora de cada um.

---

### P1: Ver a linha do tempo do grupo ⭐ MVP

**User Story**: Como membro, quero ver tudo o que aconteceu hoje, de todos, numa só lista, para saber o que já foi feito antes de agir.

**Why P1**: É a metade "compartilhado" do valor; sem ela não há como saber se o remédio já foi dado.

**Acceptance Criteria**:

1. WHEN um membro abre o grupo THEN the system SHALL mostrar os registros do dia atual, do mais recente para o mais antigo, com tipo, autor, hora e, para remédio, o nome e a dose.  <!-- event-driven -->
2. WHEN outro membro grava um registro THEN the system SHALL exibi-lo na linha do tempo dos demais membros com conexão ativa em até 5 segundos.  <!-- event-driven -->
3. WHEN o membro escolhe um filtro por tipo THEN the system SHALL mostrar somente registros desse tipo.  <!-- event-driven -->
4. WHEN o membro pede dias anteriores THEN the system SHALL carregar um dia por vez, a partir do dia anterior ao último exibido.  <!-- event-driven -->
5. WHILE o dia atual não tem registros the system SHALL mostrar uma mensagem de vazio com o botão para o primeiro registro.  <!-- state-driven -->
6. IF a consulta da linha do tempo falha THEN the system SHALL mostrar "Não foi possível atualizar" com o botão "Tentar de novo" e manter os registros já exibidos.  <!-- unwanted-behavior -->
7. The system SHALL ordenar os registros pela hora do registro e, em empate, pelo instante do lançamento.  <!-- ubiquitous -->

**Independent Test**: Com dois aparelhos no mesmo grupo, registrar num e ver aparecer no outro em até 5 segundos; trocar o filtro e voltar ao dia anterior.

---

### P2: Anular um registro

**User Story**: Como autor ou administrador, quero anular um registro errado com um motivo, para corrigir o histórico sem apagá-lo.

**Why P2**: Erros de toque vão acontecer; não bloqueia o valor central, mas a confiança depende disso.

**Acceptance Criteria**:

1. WHEN o autor do registro ou o administrador anula um registro informando um motivo de 1 a 140 caracteres THEN the system SHALL marcar o registro como anulado, com quem anulou, quando e o motivo.  <!-- event-driven -->
2. WHILE um registro está anulado the system SHALL exibi-lo riscado na linha do tempo, com o motivo visível.  <!-- state-driven -->
3. IF um membro que não é o autor nem administrador tenta anular um registro THEN the system SHALL recusar a ação.  <!-- unwanted-behavior -->
4. IF um registro já está anulado THEN the system SHALL impedir nova anulação e manter o motivo original.  <!-- unwanted-behavior -->
5. The system SHALL NOT permitir editar nem apagar um registro depois de gravado.  <!-- ubiquitous -->

**Independent Test**: Registrar um remédio por engano, anulá-lo com motivo e ver o registro riscado para os demais membros.

---

### P2: Anexar foto à ocorrência

**User Story**: Como membro, quero anexar uma foto a uma ocorrência (por exemplo, uma marca na pele), para mostrar à família sem descrever.

**Why P2**: Ajuda o valor, mas aumenta o risco de dado sensível; fica opcional.

**Acceptance Criteria**:

1. WHEN o membro anexa uma foto a uma ocorrência THEN the system SHALL reduzir a imagem no aparelho para até 1 MB, com lado maior de 1.600 px, e remover os metadados antes do envio.  <!-- event-driven -->
2. WHERE a ocorrência tem foto the system SHALL exibi-la apenas para membros do grupo, por endereço assinado que expira em até 15 minutos.  <!-- optional-feature -->
3. IF o membro tenta anexar mais de uma foto à mesma ocorrência THEN the system SHALL recusar a segunda e informar o limite de uma.  <!-- unwanted-behavior -->
4. IF o envio da foto falha THEN the system SHALL manter o texto da ocorrência na fila e oferecer reenviar a foto.  <!-- unwanted-behavior -->

**Independent Test**: Anexar uma foto de 8 MB, ver o envio de no máximo 1 MB e abrir a foto em outro membro; tentar abrir o endereço da foto fora do grupo e ser recusado.

---

### P2: Registrar com conexão ruim

**User Story**: Como membro em casa com wifi fraco, quero que o registro não se perca, para anotar mesmo sem conexão.

**Why P2**: Perda de registro destrói a confiança; o iPhone não tem sincronização em segundo plano.

**Acceptance Criteria**:

1. IF o aparelho está sem conexão quando o membro confirma um registro THEN the system SHALL guardar o registro numa fila local, marcado como "não enviado".  <!-- unwanted-behavior -->
2. WHEN o app é aberto ou a conexão volta com registros na fila THEN the system SHALL enviá-los em ordem e removê-los da fila a cada confirmação do servidor.  <!-- event-driven -->
3. WHILE há registros na fila the system SHALL mostrar o aviso "N registros não enviados" e o botão "Enviar agora".  <!-- state-driven -->
4. IF o mesmo registro da fila é enviado mais de uma vez THEN the system SHALL gravar uma única ocorrência dele, identificada pelo código gerado no aparelho.  <!-- unwanted-behavior -->
5. IF a sessão expirou antes do envio THEN the system SHALL manter a fila e retomar o envio depois do novo login.  <!-- unwanted-behavior -->

**Independent Test**: Registrar com o aparelho em modo avião, reabrir com rede e ver o registro aparecer uma única vez na linha do tempo dos demais.

---

### P2: Excluir o grupo e sair

**User Story**: Como administrador, quero excluir o grupo e seus dados, e como membro quero sair, para controlar o dado de saúde da pessoa cuidada.

**Why P2**: Exigência de eliminação da LGPD; não bloqueia o uso inicial.

**Acceptance Criteria**:

1. WHEN o administrador confirma a exclusão do grupo digitando o nome da pessoa cuidada THEN the system SHALL ocultar o grupo para todos os membros e agendar o apagamento definitivo para 30 dias depois.  <!-- event-driven -->
2. WHEN passam 30 dias da exclusão THEN the system SHALL apagar definitivamente os registros, as fotos, os convites e os aceites do grupo.  <!-- event-driven -->
3. WHEN o administrador cancela a exclusão dentro de 30 dias THEN the system SHALL restaurar o grupo com todos os dados.  <!-- event-driven -->
4. WHEN um membro sai do grupo THEN the system SHALL encerrar o acesso dele e manter os registros que ele fez no grupo.  <!-- event-driven -->
5. IF o único administrador tenta sair sem indicar outro administrador THEN the system SHALL recusar a saída e pedir a indicação.  <!-- unwanted-behavior -->

**Independent Test**: Excluir um grupo, ver que some para todos, restaurá-lo no mesmo dia e confirmar que os dados voltam.

---

### P3: Medir uso do produto

**User Story**: Como dono do produto, quero acompanhar o uso desde o primeiro dia, para decidir se o MVP deu certo.

**Why P3**: As métricas de sucesso nascem no MVP, mas o app funciona sem elas.

**Acceptance Criteria**:

1. The system SHALL contar, por grupo e por dia, os registros criados e os membros que registraram, sem armazenar o conteúdo dos registros nessas contagens.  <!-- ubiquitous -->
2. WHEN o dono do produto consulta o painel de uso THEN the system SHALL mostrar os grupos ativos após 30 dias, os registros por dia por grupo e os membros ativos por grupo.  <!-- event-driven -->

---

## Edge Cases

- IF dois membros registram o mesmo remédio no mesmo minuto THEN the system SHALL gravar os dois registros e exibi-los lado a lado, sem fundi-los.
- IF o serviço de e-mail não entrega o código THEN the system SHALL permitir pedir novo código após 60 segundos e mostrar o motivo do atraso.
- WHEN um membro removido tenta abrir o grupo THEN the system SHALL mostrar "Você não faz parte deste grupo" sem revelar dados do grupo.
- IF um usuário tenta acessar o grupo de outra pessoa trocando o identificador na requisição THEN the system SHALL recusar o acesso e não revelar se o grupo existe.
- IF o aparelho tem o relógio adiantado em mais de 5 minutos THEN the system SHALL usar a hora do servidor como referência para recusar horas futuras.
- WHEN o iOS descarta a sessão do PWA THEN the system SHALL pedir novo código sem perder a fila local.
- IF o administrador cadastra um remédio com nome repetido THEN the system SHALL avisar e pedir confirmação antes de duplicar.

---

## Cobertura das dimensões implícitas

| Dimensão | Resolução |
| -------- | --------- |
| Validação de entrada e limites | Limites de e-mail, texto, motivo, hora e foto nas histórias P1 e P2 |
| Falha e falha parcial | Falha de consulta, de envio de foto, de e-mail e de conexão (fila local) |
| Idempotência, repetição e duplicidade | Duplo toque, reenvio da fila com código do aparelho |
| Limites de autenticação e taxa | Código com 5 tentativas e bloqueio de 15 minutos; convite de uso único; isolamento por grupo |
| Concorrência e ordem | Ordenação por hora do registro e instante do lançamento; registros simultâneos não se fundem |
| Ciclo de vida e expiração dos dados | Código 10 minutos, convite 7 dias, sessão 30 dias, foto assinada 15 minutos, exclusão em 30 dias |
| Observabilidade | Contagens de uso sem conteúdo (P3); registros de erro sem dado de saúde, a definir no desenho |
| Falha de dependência externa | E-mail não entregue; serviço de armazenamento de foto indisponível |
| Integridade de transição de estado | Registro ativo para anulado (sem volta); convite pendente para usado, expirado ou revogado; grupo ativo para em exclusão e de volta |

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| -------------- | ----- | ----- | ------ |
| ACE-01 | P1: Entrar no app e criar o grupo (envio do código) | Design | Pending |
| ACE-02 | P1: Entrar no app e criar o grupo (sessão) | Design | Pending |
| ACE-03 | P1: Entrar no app e criar o grupo (bloqueio por tentativas) | Design | Pending |
| ACE-04 | P1: Entrar no app e criar o grupo (código inválido) | Design | Pending |
| ACE-05 | P1: Entrar no app e criar o grupo (e-mail inválido) | Design | Pending |
| GRP-01 | P1: Entrar no app e criar o grupo (criar grupo e aceite) | Design | Pending |
| GRP-02 | P1: Entrar no app e criar o grupo (declaração obrigatória) | Design | Pending |
| CON-01 | P1: Convidar familiares e cuidador (gerar convite) | Design | Pending |
| CON-02 | P1: Convidar familiares e cuidador (abrir convite e aviso) | Design | Pending |
| CON-03 | P1: Convidar familiares e cuidador (pedido pendente) | Design | Pending |
| CON-04 | P1: Convidar familiares e cuidador (aprovação) | Design | Pending |
| CON-05 | P1: Convidar familiares e cuidador (convite inválido) | Design | Pending |
| CON-06 | P1: Convidar familiares e cuidador (revogar convite) | Design | Pending |
| CON-07 | P1: Convidar familiares e cuidador (remover membro) | Design | Pending |
| CON-08 | P1: Convidar familiares e cuidador (limite de membros) | Design | Pending |
| REG-01 | P1: Registrar (cadastrar remédio) | Design | Pending |
| REG-02 | P1: Registrar (remédio da lista) | Design | Pending |
| REG-03 | P1: Registrar (outro remédio) | Design | Pending |
| REG-04 | P1: Registrar (banho) | Design | Pending |
| REG-05 | P1: Registrar (refeição) | Design | Pending |
| REG-06 | P1: Registrar (ocorrência) | Design | Pending |
| REG-07 | P1: Registrar (hora ajustada) | Design | Pending |
| REG-08 | P1: Registrar (hora inválida) | Design | Pending |
| REG-09 | P1: Registrar (texto da ocorrência inválido) | Design | Pending |
| REG-10 | P1: Registrar (duplo toque) | Design | Pending |
| REG-11 | P1: Registrar (até 3 toques) | Design | Pending |
| LIN-01 | P1: Ver a linha do tempo (dia atual) | Design | Pending |
| LIN-02 | P1: Ver a linha do tempo (atualização em 5 s) | Design | Pending |
| LIN-03 | P1: Ver a linha do tempo (filtro) | Design | Pending |
| LIN-04 | P1: Ver a linha do tempo (dias anteriores) | Design | Pending |
| LIN-05 | P1: Ver a linha do tempo (vazio) | Design | Pending |
| LIN-06 | P1: Ver a linha do tempo (falha de consulta) | Design | Pending |
| LIN-07 | P1: Ver a linha do tempo (ordem) | Design | Pending |
| ANU-01 | P2: Anular um registro (anular) | - | Pending |
| ANU-02 | P2: Anular um registro (exibição) | - | Pending |
| ANU-03 | P2: Anular um registro (permissão) | - | Pending |
| ANU-04 | P2: Anular um registro (já anulado) | - | Pending |
| ANU-05 | P2: Anular um registro (sem editar nem apagar) | - | Pending |
| FOT-01 | P2: Foto (compressão) | - | Pending |
| FOT-02 | P2: Foto (acesso restrito) | - | Pending |
| FOT-03 | P2: Foto (uma por ocorrência) | - | Pending |
| FOT-04 | P2: Foto (falha de envio) | - | Pending |
| OFF-01 | P2: Conexão ruim (fila local) | - | Pending |
| OFF-02 | P2: Conexão ruim (reenvio em ordem) | - | Pending |
| OFF-03 | P2: Conexão ruim (aviso) | - | Pending |
| OFF-04 | P2: Conexão ruim (sem duplicar) | - | Pending |
| OFF-05 | P2: Conexão ruim (sessão expirada) | - | Pending |
| EXC-01 | P2: Excluir o grupo e sair (exclusão) | - | Pending |
| EXC-02 | P2: Excluir o grupo e sair (apagamento em 30 dias) | - | Pending |
| EXC-03 | P2: Excluir o grupo e sair (restaurar) | - | Pending |
| EXC-04 | P2: Excluir o grupo e sair (sair do grupo) | - | Pending |
| EXC-05 | P2: Excluir o grupo e sair (último administrador) | - | Pending |
| MET-01 | P3: Medir uso (contagens) | - | Pending |
| MET-02 | P3: Medir uso (painel) | - | Pending |

**ID format:** `[CATEGORY]-[NUMBER]` (ex.: `ACE-01`, `REG-03`, `LIN-02`)

**Status values:** Pending → In Design → In Tasks → Implementing → Verified

**Coverage:** 54 total, 0 mapped to tasks, 54 unmapped ⚠️

---

## Success Criteria

How we know the feature is successful:

- [ ] Um membro novo entra no grupo e faz o primeiro registro em até 3 minutos, sem instalar o app.
- [ ] Um registro aparece nos demais aparelhos em até 5 segundos.
- [ ] Nenhum teste de autorização consegue ler dado de um grupo a que o usuário não pertence.
- [ ] Pelo menos 5 famílias reais usam o app por 30 dias e a retenção em 30 dias é medida (benchmark de apps de saúde: 3% a 8%).
- [ ] Pelo menos 1 em cada 5 grupos ativos demonstra disposição a pagar na lista de espera com preço.
