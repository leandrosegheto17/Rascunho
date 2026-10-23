# Decisão: Registro compartilhado de cuidados entre familiares

- **Data**: 2026-10-23
- **Veredito**: seguir (por decisão do usuário, contra o parecer de "esclarecer" abaixo)
- **Artefatos lidos**: ideia.md, pesquisa.md, problema.md, solucao.md, viabilidade-tecnica.md, plano-comercial.md

## Notas

| Critério | Nota | Justificativa |
|---|---|---|
| Validade do problema | adequado | O cuidado familiar de idosos é real e cresce (5,1 milhões de cuidadores familiares em 2019; 32,1 milhões de pessoas com 60+ no Censo 2022). Que a perda de informação entre familiares seja uma dor forte continua sendo PREMISSA. |
| Força das evidências | fraco | Demografia e lei são sólidas, mas a dor, a disposição a pagar e os concorrentes brasileiros não têm evidência direta. A confiança geral da pesquisa é média-baixa, com buscas baseadas em resumos. Nenhuma família foi ouvida. |
| Valor contra não fazer nada | desconhecido | O custo de não fazer nada não foi quantificado (sem dado de erro de medicação ou de conflito familiar no Brasil), e o substituto, o WhatsApp, custa zero. |
| Opção de solução | adequado | A Opção B é pequena, bem delimitada e cabe no investimento aceitável (semanas). A própria recomendação manda testar a Opção A antes de construir, e esse teste não foi feito. |
| Viabilidade técnica | adequado | Viável com riscos: nada precisa ser inventado, custo de cerca de R$ 150 a R$ 415 por mês no teto. Riscos abertos: base legal do consentimento (exige advogado) e experiência no iPhone (exige aparelho real). |
| Viabilidade comercial | fraco | "Fecha se" houver cerca de 43 grupos pagantes ativos, mas só com o seu tempo valorado a R$ 0 (com R$ 100/hora seriam cerca de 233). Chance estimada de 15% (julgamento). Concorrentes gratuitos fortes e disposição a pagar sem evidência. |
| Riscos | adequado | Os riscos estão identificados, com mitigação para quase todos. Os dois mais graves (consentimento por idoso sem discernimento e adoção contra o WhatsApp) dependem de validação externa. |

## Veredito e motivo

**Esclarecer.** O problema é real em escala, a solução é pequena e tecnicamente viável, mas a regra do fluxo não permite "seguir" com a força das evidências em `fraco` e o plano comercial em `fraco`. Falta a prova que mais importa: que famílias sentem a dor o bastante para trocar o WhatsApp e pagar. O projeto é barato de testar, e o teste cabe em semanas e custa quase nada. Isso é diferente de uma ideia a matar: nenhuma evidência contradiz o problema, só falta evidência a favor.

## Decisão do usuário (2026-10-23)

O parecer das notas era **esclarecer**: força das evidências e viabilidade comercial em `fraco`, o que, pela regra do fluxo, impede um "seguir" automático. Apresentadas as opções (esclarecer primeiro, seguir mesmo assim, matar), o usuário escolheu **seguir mesmo assim**. A decisão é dele e está registrada aqui. Consequências aceitas:

- A dor, a disposição a pagar e a base legal do consentimento seguem como PREMISSA e viram **riscos do MVP**, não pré-requisitos.
- A validação (entrevistas, teste do formato no WhatsApp, advogado, spike no iPhone) passa a correr em paralelo à construção, e o lançamento amplo fica condicionado ao advogado.
- Se a validação mostrar que a dor não existe ou ninguém paga, o projeto pode ser encerrado depois de construído; o custo do MVP é de semanas.

## Entrada do MVP

- **Problema**: famílias que dividem o cuidado de um idoso ou dependente (com ou sem cuidador contratado) não têm um registro único do que foi feito.
- **Solução escolhida**: Opção B — registro compartilhado em PWA, em português, para o celular.
- **Entra**:
  - Grupo ("círculo de cuidado") para uma pessoa cuidada, com convite por link, aprovação do administrador e consentimento no aceite.
  - Login que funcione sem instalar o PWA (e-mail por link ou código).
  - Quatro registros em poucos toques: remédio, banho, refeição e ocorrência, com quem fez e a hora.
  - Linha do tempo única do grupo, atualizada quase em tempo real, filtrável por tipo.
  - Ocorrência com texto curto e foto opcional.
  - Fila local para registrar com conexão ruim, com reenvio ao reabrir.
- **Fica de fora**: alertas e lembretes, plano de medicação com horários, escala de turnos, agenda de consultas, relatórios, app nativo nas lojas, funções clínicas, uso direto pela pessoa cuidada, cobrança (a assinatura pode vir depois do MVP).
- **Métricas de sucesso**: famílias ativas após 30 dias (benchmark de apps de saúde 3% a 8%); registros por dia por grupo; familiares ativos por grupo; tempo para registrar uma ação; disposição a pagar medida por lista de espera ou pré-venda.
- **Restrições e riscos técnicos**:
  - Dado de saúde sensível (LGPD): consentimento específico, hospedagem em São Paulo, isolamento por grupo no banco com testes, foto privada.
  - Sem alertas nem orientação clínica, para ficar fora da RDC 657/2022.
  - iPhone: o link de convite abre no Safari, sessão do PWA incerta, sem Background Sync.
  - Stack candidata (a decidir no desenho): PWA com Supabase em São Paulo, custo de cerca de R$ 150 a R$ 415 por mês no teto.
- **Perguntas em aberto**:
  - Consentimento por idoso sem discernimento e sem curatela; papel da plataforma na LGPD (advogado).
  - Quantas pessoas cuidadas por grupo (uma ou várias).
  - Limites do plano gratuito e momento de cobrar.
  - Login por e-mail é usável para o público 50+, ou WhatsApp/Google?

## Pausa do fluxo (2026-10-23)

Na fase 6 (definição do MVP), com `context.md` e um rascunho de `spec.md` gravados em `.specs/features/registro-cuidado/` e **sem** `validate_spec.py` rodado, o usuário pediu para pausar o fluxo todo. Nada foi construído nem commitado. Para retomar: rodar `validate_spec.py` sobre o rascunho, ajustar o que ele apontar e pedir a aprovação da spec. A spec está marcada como rascunho, não aprovada.

## Parecer original das notas: esclarecer

- **O que falta**:
  - [A ESCLARECER: A dor existe? Entrevistar de 5 a 10 famílias que dividem o cuidado de um idoso e ver como registram hoje.]
  - [A ESCLARECER: O formato fixo no WhatsApp (Opção A) resolve? Rodar o teste por uma ou duas semanas e anotar o que falha.]
  - [A ESCLARECER: Famílias pagariam? Medir interesse com lista de espera e preço (R$ 19,90/mês) ou pré-venda.]
  - [A ESCLARECER: Consulta a advogado sobre consentimento por idoso sem discernimento e sem curatela, e papel da plataforma na LGPD.]
  - [A ESCLARECER: Spike em iPhone real: login após mais de 7 dias, link de convite aberto no WhatsApp e foto pela câmera.]
- **Voltar para**: descoberta (discovery), para trazer evidência de usuários reais ao `pesquisa.md` e ao `problema.md`. Em seguida, atualizar o plano comercial com preço e conversão medidos.
- **Critério para voltar à decisão**: a dor confirmada em entrevistas ou no teste (por exemplo, a maioria das famílias entrevistadas relata perda de informação e o formato no WhatsApp não basta) e algum sinal de pagamento. Se o formato no WhatsApp resolver ou ninguém demonstrar interesse em pagar, o veredito passa a ser **matar**.
