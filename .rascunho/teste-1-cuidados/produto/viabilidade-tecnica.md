# Viabilidade técnica: Registro compartilhado de cuidados entre familiares

- **Data**: 2026-10-23
- **Opção avaliada**: Opção B — Registro compartilhado em PWA, validado com poucas famílias
- **Veredito**: viável com riscos

## Incertezas e como foram resolvidas

| # | Incerteza | Dimensão | Caminho | Resultado | Evidência |
|---|---|---|---|---|---|
| 1 | Qual base legal e quem consente por um idoso sem discernimento | dados | pesquisa | Consentimento do titular ou responsável legal é a única base realista. Sem curatela, o consentimento de familiar ou cuidador é zona cinzenta, sem fonte. Exige advogado | LGPD art. 11, I e II (resumos de terceiros) |
| 2 | Papel da plataforma na LGPD (controladora, operadora) | dados | pesquisa | Uso doméstico fica fora da LGPD (art. 4º, I), mas a plataforma tem fim econômico e define finalidade e meios. Enquadramento sem fonte; exige advogado | guia ANPD de agentes de tratamento (resumo) |
| 3 | Hospedagem fora do Brasil | dados | pesquisa | Exige as cláusulas-padrão da ANPD (Res. 19/2024). Hospedar em São Paulo evita a questão | Res. CD/ANPD 19/2024 (comentário jurídico) |
| 4 | O app cai na regra de software como dispositivo médico | dados | pesquisa | Um diário sem alertas nem recomendação tende a ficar fora da RDC 657/2022. Lembretes ou alertas podem trazê-lo para dentro | RDC 657/2022 (só resumos, baixa-média) |
| 5 | Plataforma e ferramentas existem prontas | funcionalidade central | pesquisa | Sim. Supabase (Postgres, auth, realtime e storage, região São Paulo) cobre o essencial; não é preciso inventar nada | supabase.com/pricing e /docs/guides/platform/regions |
| 6 | Link de convite e login no iPhone | plataforma | pesquisa | O link provavelmente abre no Safari e não no PWA instalado, que tem cookies e armazenamento separados. Há relato de logout após 7 dias. Fluxo precisa funcionar sem instalar o app. Resolução definitiva só em aparelho | WebKit Bugzilla 237350; fórum Apple 710157 |
| 7 | Registro sem conexão boa | plataforma | pesquisa | Background Sync não existe no Safari. Alternativa: fila local com reenvio ao abrir o app e botão "reenviar". Registros só de inclusão, com ID gerado no cliente, evitam conflito | caniuse.com/background-sync |
| 8 | Tempo real da linha do tempo | volume | pesquisa | Supabase Realtime: gratuito 200 conexões e 2 mi mensagens/mês; Pro 500 e 5 mi. Estimativa de ~2,4 mi mensagens/mês no teto, o que exige o plano Pro | supabase.com/docs/guides/realtime/limits |
| 9 | Meio de login para público 50+ | plataforma | pesquisa | E-mail por link é o mais barato (cerca de R$ 9 por 10 mil envios); SMS é caro (cerca de R$ 3.300); WhatsApp fica no meio, com preço não confirmado. Usabilidade para 50+ sem evidência | aws.amazon.com/ses/pricing; twilio.com/en-us/sms/pricing/br |
| 10 | Foto pela câmera e compressão no iPhone | plataforma | risco aceito | Entrada de arquivo com câmera é documentada, mas varia por navegador; compressão no cliente é rotina. Verificar no teste em aparelho, sem spike próprio | MDN (atributo capture) |
| 11 | Volume e desempenho | volume | risco aceito | Teto de cerca de 20 mil eventos por dia e 7 GB de banco no ano; carga baixa para qualquer das opções | cálculo próprio (PREMISSA) |
| 12 | PWA e as lojas depois | plataforma | risco aceito | Android pode ser empacotado em TWA sem reescrever; iOS exigiria casca nativa (Capacitor), não pesquisada. Fora da v1 | developer.chrome.com (TWA) |

## Dados e LGPD

- **Dados guardados**: identificação da pessoa cuidada (nome, talvez idade), participantes do grupo (nome, contato de login), eventos de remédio (nome, dose, horário), banho, refeição, ocorrência em texto e, opcionalmente, foto.
- **Dado pessoal ou sensível**: sim. Remédio, ocorrências e foto de pessoa idosa são dado de saúde (art. 11); o texto livre da ocorrência pode revelar mais. Há também dado do cuidador contratado no mesmo grupo.
- **Cuidados exigidos**:
  - Consentimento específico e destacado, do titular ou do responsável legal, antes do primeiro registro.
  - Hospedar em São Paulo para evitar transferência internacional; se houver fora, usar cláusulas-padrão da ANPD.
  - Controle de acesso por grupo, criptografia em trânsito e em repouso, e foto em armazenamento privado.
  - Política de retenção e exclusão (a definir com advogado), canal com o titular, plano de resposta a incidente (3 dias úteis, na leitura da pesquisa).
  - Manter o produto sem alertas, sugestões de dose ou orientação clínica, para ficar fora da RDC 657/2022; cuidar da comunicação do produto.
  - Registrar operações e avaliar RIPD conforme a escala.

## Segurança

- **Autorização por grupo:** todo dado só pode ser lido por quem pertence ao grupo; a falha clássica é um usuário acessar o grupo de outro (política de acesso por linha no banco, com teste automatizado).
- **Convite:** token único, expirável, de uso único e guardado só como hash. Como o link pode ser reencaminhado pelo WhatsApp, exigir aprovação do administrador do grupo ou confirmação do convidado.
- **Sessão:** login persistente no PWA instalado do iPhone é incerto; o fluxo precisa permitir reentrar sem atrito.
- **Fotos:** armazenamento privado com URL assinada de curta duração; remover metadados.
- **Vazamento:** exposição de dado de saúde de idoso é alta gravidade e exige comunicação à ANPD.
- **Cuidador contratado:** acesso limitado ao grupo e revogável, para a saída do cuidador não deixar acesso aberto.

## Custo de operação estimado

Câmbio assumido: US$ 1 = R$ 5,50 (PREMISSA, não consultado). Preços consultados nas páginas oficiais em 23/10/2026.

| Item | Início (mês) | Com o volume esperado (mês) | Fonte |
|---|---|---|---|
| Hospedagem do front (PWA estático/funções) | R$ 0 a R$ 110 | R$ 0 a R$ 110 | vercel.com/pricing (Hobby só uso não comercial; Pro US$ 20); alternativas não pesquisadas a fundo |
| Banco, auth, realtime e storage (Supabase) | R$ 0 (gratuito, com pausa por inatividade) ou R$ 138 (Pro) | R$ 138 a R$ 195 (Pro + conexões extras) | supabase.com/pricing |
| E-mail de login | R$ 0 | R$ 10 a R$ 110 (SES ou Resend Pro) | aws.amazon.com/ses/pricing; resend.com/pricing |
| **Total** | **R$ 0 a cerca de R$ 250** | **cerca de R$ 150 a R$ 415** | |

- Com login por WhatsApp no lugar do e-mail: cerca de R$ 500 a R$ 600 no teto (preço não confirmado). Com SMS: mais de R$ 3.400.
- Exclui domínio, advogado, monitoramento e erros.
- O gratuito do Supabase não sustenta o primeiro ano (banco de 500 MB e pausa por inatividade).

## Stack candidata (não decidida)

- **PWA + Supabase (região São Paulo):** Postgres com isolamento por linha para o grupo, autenticação por link de e-mail, realtime e storage privado para fotos num único serviço, com região no Brasil. O front pode ser qualquer framework web; hospedagem do front a definir.
- **PWA + Firebase (Firestore em São Paulo):** autenticação e realtime prontos, mas o storage exige o plano pago e a cota gratuita só vale nos EUA; o custo é variável e as leituras de listeners passam do gratuito. Menos previsível.
- **Cloudflare (Workers, D1, R2):** o mais barato, mas sem região no Brasil para D1 e R2, o que traz a questão da transferência internacional. Só entra com cláusulas-padrão.
- **Descartada por ora:** Neon em São Paulo, sem realtime nem storage na região.

## Riscos e mitigação

| Risco | Impacto | Probabilidade | Mitigação |
|---|---|---|---|
| Base legal frágil: consentimento por idoso sem discernimento e sem curatela | alto | alta | Consulta a advogado antes de lançar; desenho do cadastro com declaração do responsável; lançar só em teste fechado até resolver |
| Dado de saúde vaza ou um grupo acessa outro | alto | média | Isolamento por linha no banco, testes de autorização, auditoria de segurança na fase 10, fotos privadas |
| Login e convite no iPhone falham (link abre no Safari, sessão cai) | alto | alta | Fluxo que não depende do PWA instalado; login por e-mail; spike em aparelho real antes de fechar o desenho |
| App passa a ser enquadrado como dispositivo médico | alto | baixa | Manter a v1 sem alertas, dose sugerida ou orientação clínica; revisar a comunicação do produto |
| Usuários 50+ não conseguem usar o e-mail como login | médio | média | Testar com usuários reais; avaliar WhatsApp ou Google como alternativa, pesando custo |
| Registro perdido com wifi ruim ou o iOS encerrando o app | médio | média | Fila local, envio ao abrir e botão de reenviar; registro só de inclusão com ID do cliente |
| Custo sobe com mais conexões e fotos | baixo | média | Pro cobre o teto estimado; limitar tamanho e quantidade de fotos; revisar com dados reais |
| Pesquisa baseada em resumos, sem leitura do texto oficial | médio | média | Validar LGPD e RDC 657 com advogado e com os textos oficiais antes do lançamento |

## Veredito e motivo

**Viável com riscos.** Nada do que a Opção B exige precisa ser inventado: um serviço único (Postgres, autenticação, realtime e armazenamento) em São Paulo cobre o essencial por cerca de R$ 150 a R$ 415 por mês no teto do primeiro ano, e o volume é pequeno. Os riscos relevantes não são de engenharia pura. O maior é jurídico: a validade do consentimento por um idoso sem discernimento e sem curatela e o papel da plataforma, que só um advogado resolve. O segundo é a experiência no iPhone (convite, sessão, fila offline), que só se confirma em aparelho real. Não há incerteza crítica que torne a opção inviável, desde que a v1 continue sem alertas e a exposição fique restrita a teste fechado até a validação jurídica.

Lacunas conhecidas: PlanetScale e a tarifa de WhatsApp não foram pesquisados; o texto oficial da LGPD e da RDC 657 não foi aberto; WebAPK, `getUserMedia` e contraste WCAG ficaram de fora.
