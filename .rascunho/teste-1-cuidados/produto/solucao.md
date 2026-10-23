# Solução: Registro compartilhado de cuidados entre familiares

- **Data**: 2026-10-23
- **Opção recomendada**: B — Registro compartilhado em PWA, validado com poucas famílias

## Opções

### Opção A — Usar algo pronto (WhatsApp + modelo de mensagem, ou app gratuito existente)
- **Esboço**: a família continua no grupo de WhatsApp, mas adota um formato fixo de mensagem ("Remédio: X às 8h", "Banho: feito") e, se quiser, um app gratuito de registro compartilhado (como os que a pesquisa lista). Nada novo é construído; o ganho vem da disciplina e do formato.
- **Investimento aceitável**: pequeno (dias, só para testar o formato com famílias reais).
- **Ganhos e perdas**: ganha zero custo e nenhum risco de LGPD para nós. Perde a busca e a visão por dia, o filtro por tipo e a garantia de que a informação não se afoga na conversa. Serve também como teste da hipótese de dor: se o formato no WhatsApp já resolve, o produto não se justifica.
- **Armadilhas**: sem produto próprio não há o que vender; só vale como aprendizado.

### Opção B — Registro compartilhado em PWA (a menor coisa que funcionaria como produto)
- **Esboço**: uma pessoa cria o "círculo de cuidado" para quem recebe o cuidado e convida familiares (e, se houver, o cuidador) por link. Uma tela inicial com quatro botões grandes — remédio, banho, refeição, ocorrência — registra a ação com quem fez e a hora, em poucos toques. Uma linha do tempo única do dia mostra tudo para todos. Ocorrência aceita texto curto e, talvez, foto. Funciona no navegador do celular, instalável na Tela de Início, sem loja de aplicativos. Sem alertas, sem escala, sem agenda.
- **Investimento aceitável**: médio (semanas).
- **Ganhos e perdas**: ganha o que a hipótese central pede (visão única do cuidado, rápida para quem é pouco técnico), custo baixo de distribuição e iteração rápida. Perde alertas de horário de remédio, que as famílias podem esperar, e a presença nas lojas de apps. Risco: retenção baixa, concorrência do WhatsApp e dos apps gratuitos.
- **Armadilhas**: o cadastro e a permissão de cada participante, a privacidade e o consentimento (dado de saúde sensível na LGPD), e a tentação de acrescentar lembretes, escala e consultas antes de validar o uso.

### Opção C — App completo de coordenação de cuidados (registro, plano de medicação com alertas, escala, agenda e relatórios)
- **Esboço**: além do registro, o app guarda o plano de remédios com horários e avisa quem precisa dar, controla quem cobre cada turno, a agenda de consultas e gera relatório para o médico ou para a agência. Pode ter versão para agências de cuidadores.
- **Investimento aceitável**: grande (meses).
- **Ganhos e perdas**: ganha diferenciação frente a apps simples e um argumento de preço mais forte, inclusive para agências. Perde velocidade e prova: constrói muito antes de saber se a família usa o registro básico, e entra em território clínico (alerta de medicação errado tem consequência real).
- **Armadilhas**: notificações no PWA do iPhone exigem instalação e iOS 16.4+, o que empurra para app nativo; responsabilidade sobre doses e horários; escopo que cresce sem fim.

## Recomendação

Recomendo a **Opção B**, precedida de um teste barato da **Opção A**: antes de construir, pedir a 5 a 10 famílias que usem o formato fixo no WhatsApp por uma ou duas semanas e observar onde dói. Isso fecha a lacuna mais forte da pesquisa (a dor está sem evidência direta) pelo menor custo, e o que for aprendido define o que o registro precisa ter.

A B liga-se aos objetivos do problema (visão única, poucos toques, serve com e sem cuidador) e permite medir as métricas de sucesso (retenção em 30 dias, registros por dia, familiares ativos por grupo). A C é prematura: soma a maior parte do risco antes de existir uma prova de uso. Se o teste da A mostrar que o formato no WhatsApp resolve, a recomendação passa a ser **não construir**.

## Fora do escopo da opção recomendada

- Alertas e lembretes de remédio.
- Escala de turnos, agenda de consultas, contratação de cuidadores.
- Plano de medicação com horários e controle de estoque.
- Relatórios para médicos ou agências.
- App nativo nas lojas.
- Funções clínicas (diagnóstico, sinais vitais).
- Uso direto pela pessoa cuidada.

## Premissas a validar

- A dor existe: famílias perdem informação hoje e isso incomoda o bastante para trocar de ferramenta (teste da Opção A com 5 a 10 famílias).
- Pessoas pouco técnicas registram uma ação em poucos toques no celular.
- Existe disposição a pagar no Brasil; a assinatura de família é o modelo mais provável, mas não confirmado. Concorrentes gratuitos pressionam o preço.
- O consentimento do titular ou responsável legal pode ser tratado no cadastro e é aceito pelas famílias (validação jurídica antes de lançar).
- Retenção em 30 dias acima do benchmark de apps de saúde (3–8%).
- Um PWA basta no mercado-alvo, já que a v1 não precisa de notificações.
