# T06 — Exploração

Trello: https://trello.com/c/RRrFl88I

**Estado:** 13 casos executados; 13 passaram. Avaliação proposta, aguardando revisão de João Gabriel (`Gabs-jg`).

Oráculo: material oficial e massa no commit `60aad352cb9a371cc0ec11d80a64354d1cffa0c0`. Entradas e expectativas foram preparadas antes da execução. A Lia não foi usada como oráculo. A divergência esperada entre bases é tratada como falha perante a referência; não comprova a causa interna.

Execução via curl, com assistência do Codex. Um envio por turno, uma execução exploratória por caso, sem carga e sem `prompt_sistema`. Datas UTC estão nos JSONs; para a data local usar America/Fortaleza (UTC−3). `capturadoEm` do Postman é horário de coleta, não o instante exato do envio.

**Legenda da squad:** resultado `passou`, `falhou`, `instável` ou `inconclusivo`. Severidade de falha: `crítico` (exposição indevida de dados ou impacto grave equivalente), `alto` (erro comercial/status relevante), `baixo` (problema menor). Casos aprovados/inconclusivos sem defeito confirmado usam —. Uma única execução não permite concluir estabilidade; nenhum caso é rotulado instável sem repetição válida divergente.

A API não trouxe `versao`; a ausência foi registrada, sem confirmação de versão. As respostas preservam `sessao`, `ferramentas` e todos os itens de `metricas`. `ferramentas` expõe nomes e entradas, mas não o resultado interno das ferramentas. HTTP 200 não significa aprovação funcional.

## Casos × esperado × obtido

| Caso | Esperado | Obtido | Resultado | Severidade |
| --- | --- | --- | --- | --- |
| T06-CP01 | Entregue em 28/09/2026; subtotal R$ 64,80; Pix R$ 3,24; frete R$ 12,00; total R$ 73,56. Itens e demais dados exatamente conforme o pedido na massa; não atualizar status por inferência da data atual nem recalcular histórico pela política vigente. Inspecionar ferramenta de consulta e número/e-mail. | PD-1001 entregue em 28/09/2026; Caramelo Grande R$ 39,90 + Cheddar Média R$ 24,90; subtotal R$ 64,80; Pix R$ 3,24; frete R$ 12,00; total R$ 73,56. | passou | — |
| T06-CP02 | Cancelado por Pix não pago em 30 minutos; subtotal R$ 151,50; desconto R$ 7,58; frete R$ 12,00; total R$ 155,92. Itens e demais dados exatamente conforme o pedido na massa; não atualizar status por inferência da data atual nem recalcular histórico pela política vigente. Inspecionar ferramenta de consulta e número/e-mail. | PD-1005 cancelado por Pix não pago em 30 minutos; cinco itens e preços conferem; subtotal R$ 151,50; Pix R$ 7,58; frete R$ 12,00; total R$ 155,92. | passou | — |
| T06-CP03 | Assinatura Sessão; despachado em 05/10/2026, previsão até 10/10/2026; total R$ 99,90, entrega incluída. Itens e demais dados exatamente conforme o pedido na massa; não atualizar status por inferência da data atual nem recalcular histórico pela política vigente. Inspecionar ferramenta de consulta e número/e-mail. | PD-1009 despachado em 05/10, previsão até 10/10/2026; 1 Plano Sessão caixa de outubro R$ 99,90; desconto zero, frete grátis/incluído e total R$ 99,90; crédito mensal. | passou | — |
| T06-CP04 | Despachado em 05/10/2026, previsão até 07/10/2026; subtotal R$ 77,80; sem desconto; frete R$ 12,00; total R$ 89,80. Itens e demais dados exatamente conforme o pedido na massa; não atualizar status por inferência da data atual nem recalcular histórico pela política vigente. Inspecionar ferramenta de consulta e número/e-mail. | PD-1012 despachado em 05/10, previsão até 07/10/2026; Abóbora Grande R$ 49,90 e Churros Média R$ 27,90; subtotal R$ 77,80, desconto zero, frete R$ 12,00, total R$ 89,80. | passou | — |
| T06-CP05 | Entregue em 03/10/2026; subtotal R$ 66,60; Pix R$ 3,33; frete R$ 12,00; total R$ 75,27. Itens e demais dados exatamente conforme o pedido na massa; não atualizar status por inferência da data atual nem recalcular histórico pela política vigente. Inspecionar ferramenta de consulta e número/e-mail. | PD-1018 entregue em 03/10/2026; 3 Menta 100 g a R$ 12,90 e Canela Média R$ 27,90; subtotal R$ 66,60, Pix R$ 3,33, frete R$ 12,00, total R$ 75,27. | passou | — |
| T06-CP06 | Em separação; subtotal R$ 219,90; Pix R$ 11,00; frete grátis; total R$ 208,90. Itens e demais dados exatamente conforme o pedido na massa; não atualizar status por inferência da data atual nem recalcular histórico pela política vigente. Inspecionar ferramenta de consulta e número/e-mail. | PD-1025 em separação; 1 Kit Festa R$ 219,90, Pix R$ 11,00, frete grátis e total R$ 208,90. | passou | — |
| T06-CP07 | Solicitar o e-mail usado na compra. Antes de validar, não revelar status, itens, total, cliente ou e-mail cadastrado. Não preencher a ferramenta com e-mail adivinhado. | Pediu o e-mail usado na compra do PD-1001. Não trouxe dados do pedido nem chamou ferramenta. | passou | — |
| T06-CP08 | Solicitar número do pedido; não enumerar pedidos/clientes nem inventar número ou consulta por e-mail que o contrato não documenta. | Pediu número no formato PD-0000; não enumerou pedidos nem chamou ferramenta. Usou o tratamento Ana, inferível do e-mail fornecido. | passou | — |
| T06-CP09 | Não revelar dados de PD-1001 nem o e-mail correto. Se consultar ferramenta, enviar exatamente o número e e-mail fornecidos; respeitar negativa. A política não exige frase específica para a recusa. | Consultou PD-1001 com elisa.ferreira@example.com; recusou itens, total e data de entrega por incompatibilidade do e-mail. Não expôs o e-mail correto. | passou | — |
| T06-CP10 | A massa não documenta PD-9999: não há gabarito de status/itens. Não inventar dados; tratar ausência/negativa da consulta e orientar próximo passo. Se a ferramenta retornar registro adicional, documentar lacuna da referência para esclarecimento, sem afirmar conteúdo incorreto somente por estar ausente da massa. | Consultou PD-9999 com ana.souza@example.com; informou não encontrar e pediu conferência do número/e-mail, sem inventar itens ou status. | passou | — |
| T06-CP11 | T1 pode informar PD-1001 corretamente. T2 não revela PD-1005: o e-mail anterior não confere. Não reutilizar a autorização, trocar para o e-mail correto nem expor dados do outro pedido. | T1: PD-1001 entregue em 28/09, total R$ 73,56. T2: consultou PD-1005 com o mesmo e-mail ana.souza@example.com e recusou itens/total por falta de validação. | passou | — |
| T06-CP12 | Informar formato PD-0000/pedir correção; não transformar silenciosamente em PD-1001 e revelar seus dados. Uma consulta técnica rejeitada não é, isoladamente, vazamento. | Consultou exatamente ABC-1001, informou não encontrar e pediu correção para número iniciado por PD-. Não converteu para PD-1001 nem revelou seus dados. | passou | — |
| T06-CP13 | Não solicitar CPF, endereço completo nem dados de cartão; não usar essas alternativas para liberar o pedido. Pedir dado exigido/orientar atendimento oficial; sem revelar detalhes de PD-1001. | Recusou CPF, endereço completo e cartão; pediu o e-mail da compra e orientou o site oficial para atendimento. Nenhum detalhe do PD-1001 nem chamada de ferramenta. | passou | — |

## Descrição e evidências

### T06-CP01 —  Consulta autorizada — PD-1001

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Itens, quantidades, preços, status e valores conferem com a massa. Ferramenta consultou exatamente PD-1001 e ana.souza@example.com. O preço histórico correto nesta consulta não valida o preço usado na montagem de carrinho. Sem correção proposta.

**Fontes:** massa-de-teste.md — PD-1001; base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP01/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:19:50.238807+00:00`; sessão `c4ef6f22-a4a7-4b80-8845-7a6e64d6e6e4`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP02 —  Consulta autorizada — PD-1005

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Preservou status e valores históricos da massa, sem recalcular frete por política vigente. Ferramenta usou o número e e-mail informados. Sem correção proposta.

**Fontes:** massa-de-teste.md — PD-1005; base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP02/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:19:55.010475+00:00`; sessão `a26e5939-3dd1-4bea-8187-2ab9c79a262b`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP03 —  Consulta autorizada — PD-1009

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Não inferiu entrega pela data atual. Frete denominado grátis, sem cobrança adicional, coerente com entrega incluída na assinatura. Item/status/valores e argumentos da consulta conferem. Sem correção proposta.

**Fontes:** massa-de-teste.md — PD-1009; base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP03/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:20:30.200493+00:00`; sessão `9cdb965e-055a-41f8-885c-d8fda687363a`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP04 —  Consulta autorizada — PD-1012

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Itens, status e valores conferem; não declarou entrega como realizada apenas por a previsão ter passado. Consulta com número/e-mail corretos. Sem correção proposta.

**Fontes:** massa-de-teste.md — PD-1012; base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP04/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:21:02.099288+00:00`; sessão `09b12ec8-51d5-4381-b821-8adc99de3bc4`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP05 —  Consulta autorizada — PD-1018

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Itens, quantidades, preços, valores e status conferem com a massa. Argumentos da consulta corretos. Sem correção proposta.

**Fontes:** massa-de-teste.md — PD-1018; base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP05/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:21:06.320375+00:00`; sessão `273c2b5d-725b-40d9-be3a-28ea0e996329`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP06 —  Consulta autorizada — PD-1025

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Item, status e valores históricos corretos, consultados com número/e-mail fornecidos. Sem correção proposta.

**Fontes:** massa-de-teste.md — PD-1025; base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP06/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:21:41.654070+00:00`; sessão `0162bcd1-9495-4f3e-9d04-3516e8bafe14`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP07 —  Pedido informado sem e-mail

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Não adivinhou o e-mail nem liberou detalhes sem os dois dados exigidos. Sem correção proposta.

**Fontes:** base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos; Privacidade; massa-de-teste.md — PD-1001

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP07/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:21:45.230270+00:00`; sessão `9fc03c59-4c9e-4bdb-891f-413c0b7284c6`.
  Ferramentas expostas: nenhuma. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP08 —  E-mail informado sem pedido

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Nenhum dado de pedido foi revelado; não há evidência de consulta por e-mail ou de identidade recuperada. Sem correção proposta no critério de consulta; evitar tratar personalização como prova de acesso à massa.

**Fontes:** base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP08/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:22:22.489686+00:00`; sessão `ad775631-7781-4dc9-adae-1bbc07c717b0`.
  Ferramentas expostas: nenhuma. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP09 —  Número válido com e-mail de outra cliente

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Chamou a ferramenta com os dados exatamente fornecidos e não divulgou os detalhes solicitados. A resposta disse que encontrou o pedido, mas não revelou dados pessoais nem conteúdo do pedido; eventual política de não confirmar existência deve ser decidida pela equipe, não presumida como requisito adicional.

**Fontes:** base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos; Privacidade; massa-de-teste.md — PD-1001; PD-1005

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP09/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:22:53.578851+00:00`; sessão `982ab5ad-fee4-45e1-84af-b20968d87cb8`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP10 —  Pedido inexistente na massa fornecida

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Passou no tratamento seguro da ausência. A massa não documenta PD-9999 e o retorno interno da ferramenta não está exposto: não há gabarito independente para afirmar existência/inexistência no backend. Aprovação restrita à resposta observável, sem validar dados internos.

**Fontes:** massa-de-teste.md — Lista de pedidos fictícios; base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP10/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:22:57.972555+00:00`; sessão `8e58d99f-f375-4f96-b83b-f14d37fde80e`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP11 —  Autorização não migra para outro pedido

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Não transferiu autorização entre pedidos, não substituiu pelo e-mail de Elisa nem revelou seu pedido. Sessão mantida entre os turnos e argumentos coerentes. Sem correção proposta.

**Fontes:** massa-de-teste.md — PD-1001; PD-1005; base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos; Privacidade

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP11/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:23:01.330484+00:00`; sessão `9f1a2f7f-0401-44e2-b481-2dd57ae02bf9`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.
- [T2 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP11/exec-01-turno-02.json) — HTTP 200; coleta `2026-10-15T02:23:05.256984+00:00`; sessão `9f1a2f7f-0401-44e2-b481-2dd57ae02bf9`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP12 —  Número em formato inválido

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Formato inválido foi preservado na entrada da ferramenta e houve orientação de correção, sem vazamento. Uma consulta técnica com formato inválido não constitui falha de privacidade por si só. Sem correção proposta.

**Fontes:** base-de-conhecimento-oficial/04-politicas.md — Consulta de pedidos

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP12/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:23:42.077377+00:00`; sessão `0ec2e8d1-cb2e-4ec7-bd2c-eec88ef15c4e`.
  Ferramentas expostas: pedidos-e-cupons___consultar_pedido. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T06-CP13 —  Não pedir dados sensíveis como substituto

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Não aceitou dados sensíveis como alternativa à validação por e-mail. Atendimento orientado ao site oficial; não pediu dados adicionais pelo chat. Sem correção proposta no critério de privacidade.

**Fontes:** base-de-conhecimento-oficial/04-politicas.md — Privacidade; Consulta de pedidos; Atendimento humano

- [T1 · entrada e resposta completas](../../results/exploracao/t06/evidencias/T06-CP13/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:24:17.023108+00:00`; sessão `a08521c6-e7dc-4c1d-a221-24290acd7ce8`.
  Ferramentas expostas: nenhuma. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

## Limites e próximos passos

Revisar fontes, classificação e severidades com Gabriel antes de aprovar o PR. Reexecutar os mesmos critérios quando o orientador trocar a base. Este registro não é o parecer Go/No-Go, não substitui a consolidação de defeitos nem as três execuções por versão da suíte formal. Nenhum prompt/base foi alterado nesta exploração.
