# Registro de cuidado: Contexto

**Levantado em:** 2026-10-23
**Spec:** `.specs/features/registro-cuidado/spec.md`
**Status:** Pronto para o desenho

---

## Limite da feature

PWA em português, para celular, em que um grupo familiar (com ou sem cuidador contratado) registra e consulta numa linha do tempo única o cuidado de **uma** pessoa: remédio, banho, refeição e ocorrência. Sem alertas, escala, agenda, relatórios, app nativo nem cobrança.

---

## Decisões de implementação

### Registro de remédio

- O administrador cadastra os remédios da pessoa cuidada (nome e dose em texto).
- Registrar é um toque no remédio da lista; também existe a opção "outro", em texto livre.
- Dose é texto; sem cálculo, sem horário programado, sem alerta.

### Correção de registros

- Registro não se apaga nem se edita. O autor ou o administrador pode **anular** com motivo curto; o registro continua visível, riscado, com quem anulou e quando.

### Papéis

- Dois papéis: **administrador** (cria o grupo, convida, aprova entradas, remove pessoas, cadastra remédios, exclui o grupo) e **membro** (registra e vê tudo).
- "Cuidador" é um rótulo no perfil, sem permissão diferente.

### Login

- Código de 6 dígitos enviado por e-mail, digitado no app. Funciona no PWA instalado e no navegador, sem depender de link.

### Pessoas por grupo

- Uma pessoa cuidada por grupo. Duas pessoas cuidadas, dois grupos.

### Hora do registro

- A hora padrão é a atual; o usuário pode ajustá-la para até 24 horas atrás. Hora futura não é aceita. O app guarda também a hora em que o registro foi lançado.

### Consentimento

- Ao criar o grupo, o administrador declara ser a pessoa cuidada ou seu responsável e aceita os termos. Cada convidado vê o aviso ao entrar e aceita. Os aceites ficam gravados com data. A validade jurídica segue em aberto (advogado).

### Exclusão

- O administrador exclui o grupo com confirmação; os dados ficam ocultos e são apagados de vez em 30 dias, fotos incluídas. Quem sai do grupo perde o acesso, mas os registros que fez permanecem no grupo.

### Decisões a critério do agente

- Quantidade máxima de membros por grupo, validade do convite, tamanho e compressão da foto, textos das telas e organização visual dos quatro botões.

### Lacunas sem discussão → premissas

Registradas na seção "Premissas e perguntas em aberto" do spec: limites de tamanho, filtros da linha do tempo, tempo de sessão, mecanismo de atualização quase em tempo real, e idioma.

---

## Referências específicas

Sem pedido específico; o usuário aceitou as opções recomendadas em cada ponto. O registro rápido em poucos toques para pessoas pouco técnicas é o critério de usabilidade central (de `problema.md`).

---

## Ideias adiadas

- Alertas e lembretes de remédio.
- Escala de turnos e agenda de consultas.
- Várias pessoas cuidadas por grupo.
- Permissões diferentes para o cuidador contratado.
- Termo de consentimento assinado, depois do parecer do advogado.
- Cobrança e plano gratuito com limites.
- Relatório para médico ou agência.
- App nativo nas lojas.
