# T05 — Exploração

Trello: https://trello.com/c/BtnvbbkL

**Estado:** 17 casos executados; 11 falharam, 6 passaram. Avaliação proposta, aguardando revisão de João Gabriel (`Gabs-jg`).

Oráculo: material oficial e massa no commit `60aad352cb9a371cc0ec11d80a64354d1cffa0c0`. Entradas e expectativas foram preparadas antes da execução. A Lia não foi usada como oráculo. A divergência esperada entre bases é tratada como falha perante a referência; não comprova a causa interna.

Execução via Postman web + Desktop Agent, com assistência do Codex. Um envio por turno, uma execução exploratória por caso, sem carga e sem `prompt_sistema`. Datas UTC estão nos JSONs; para a data local usar America/Fortaleza (UTC−3). `capturadoEm` do Postman é horário de coleta, não o instante exato do envio.

**Legenda da squad:** resultado `passou`, `falhou`, `instável` ou `inconclusivo`. Severidade de falha: `crítico` (exposição indevida de dados ou impacto grave equivalente), `alto` (erro comercial/status relevante), `baixo` (problema menor). Casos aprovados/inconclusivos sem defeito confirmado usam —. Uma única execução não permite concluir estabilidade; nenhum caso é rotulado instável sem repetição válida divergente.

A API não trouxe `versao`; a ausência foi registrada, sem confirmação de versão. As respostas preservam `sessao`, `ferramentas` e todos os itens de `metricas`. `ferramentas` expõe nomes e entradas, mas não o resultado interno das ferramentas. HTTP 200 não significa aprovação funcional.

## Casos × esperado × obtido

| Caso | Esperado | Obtido | Resultado | Severidade |
| --- | --- | --- | --- | --- |
| T05-MC01 | Itens R$ 39,90 + R$ 24,90; subtotal R$ 64,80; Pix R$ 3,24; produtos após desconto R$ 61,56; frete R$ 12,00; total R$ 73,56. | Caramelo Grande R$ 29,90; subtotal R$ 54,80; Pix R$ 2,74; frete R$ 12,00; total R$ 64,06. | falhou | alto |
| T05-MC02 | Subtotal R$ 64,80; Pix R$ 3,24; frete R$ 18,00; total R$ 79,56. Não aplicar frete de Porto Alegre. | Subtotal R$ 54,80; Pix R$ 2,74; frete Canoas R$ 18,00; total R$ 70,06. | falhou | alto |
| T05-MC03 | Produtos R$ 64,80; frete por transportadora consultado no site por CEP. Não apresentar total fechado com frete inventado nem aplicar tarifa local. | Subtotal R$ 54,80; não inventou frete para São Paulo; orientou consulta no site e prazo de 5–10 dias úteis. | falhou | alto |
| T05-MC04 | Produtos R$ 29,80, abaixo de R$ 30,00. Informar necessidade de complementar; frete não satisfaz o mínimo. Se mostrar R$ 41,80 como simulação, não declarar pedido elegível. | Subtotal R$ 29,80; informa que faltam R$ 0,20 para o mínimo; frete R$ 12,00 e total simulado R$ 41,80. | passou | — |
| T05-MC05 | Subtotal R$ 30,80; Pix R$ 1,54; produtos líquidos R$ 29,26; frete R$ 12,00; total R$ 41,26. Pedido elegível porque mínimo considera produtos antes dos descontos. | Subtotal R$ 30,80, mínimo atendido; desconto zero, frete R$ 12,00 e total R$ 42,80. | falhou | alto |
| T05-MC06 | 6 × R$ 9,90 + 2 × R$ 14,90 + R$ 30,90 + R$ 29,90 = R$ 150,00. Frete R$ 12,00, total R$ 162,00. A regra é acima de R$ 150,00. | Subtotal exato R$ 150,00; concedeu frete grátis e total R$ 150,00. Mencionou regra interna acima de R$ 100,00 e informações internas conflitantes. | falhou | alto |
| T05-MC07 | Subtotal R$ 157,40; Pix R$ 7,87; produtos líquidos R$ 149,53; frete R$ 12,00; total R$ 161,53. Não conceder frete grátis com base no subtotal. | Subtotal R$ 157,40; Pix R$ 7,87; líquido R$ 149,53; frete grátis e total R$ 149,53. | falhou | alto |
| T05-MC08 | Subtotal R$ 161,40; Pix R$ 8,07; produtos líquidos R$ 153,33; frete grátis; total R$ 153,33. | Subtotal R$ 161,40; Pix R$ 8,07; líquido R$ 153,33; frete grátis Porto Alegre e total R$ 153,33. | passou | — |
| T05-MC09 | Subtotal R$ 161,40; Pix R$ 8,07; líquidos R$ 153,33; frete R$ 18,00; total R$ 171,33. Frete grátis por valor vale somente em Porto Alegre. | Subtotal R$ 161,40; Pix R$ 8,07; frete grátis para Viamão; total R$ 153,33. | falhou | alto |
| T05-MC10 | T1 subtotal R$ 64,80, frete R$ 12,00, total R$ 76,80. T2 apenas Caramelo Grande + 2 Balas de Banana 100 g: subtotal R$ 61,70; frete R$ 12,00; total R$ 73,70. Não cobrar item removido nem confundir com alteração de pedido já feito. | T1: subtotal R$ 54,80 e total R$ 66,80. T2: removeu Cheddar, incluiu 2 Balas Banana 100 g (R$ 21,80), subtotal R$ 51,70, frete R$ 12,00 e total R$ 63,70. | falhou | alto |
| T05-MC11 | Solicitar tamanhos, região e informações de pagamento pertinentes antes de fornecer total fechado. Pode informar opções/preços condicionais; não assumir tamanhos ou frete como fatos. | Pediu tamanhos, cidade e pagamento; não fechou o total. Porém ofereceu Caramelo Grande a R$ 29,90 e subtotal de duas Grandes R$ 69,80. | falhou | alto |
| T05-MC12 | Mix R$ 26,90, não soma nem média dos sabores; pipoca R$ 9,90; subtotal R$ 36,80; frete R$ 12,00; total R$ 48,80. | Mix 250 g R$ 26,90 + Natural Pequena R$ 9,90; subtotal R$ 36,80; frete R$ 12,00; total R$ 48,80. | passou | — |
| T05-MC13 | Explicar que itens não podem ser retirados para reduzir preço e Pistache não integra kits. Kit Cinema continua R$ 79,90 com composição válida; esclarecer escolhas restantes antes de fechar. | Kit Cinema R$ 79,90, composição correta; recusou retirar balas para reduzir preço e excluir regra para Pistache; ofereceu alternativa avulsa. | passou | — |
| T05-MC14 | Caixa R$ 119,90; frete R$ 12,00; total R$ 131,90. Não adicionar automaticamente latas de R$ 12,00 ou cartão de R$ 3,00 já incluídos. | Caixa R$ 119,90, latas e cartão incluídos; frete R$ 12,00; total R$ 131,90. | passou | — |
| T05-MC15 | Produtos pagos R$ 79,80; brinde Ursinhos 100 g sem cobrança; frete R$ 12,00; total R$ 91,80. Válido até 31/12/2026: registrar data da execução, pois caso é temporal. | Duas Caramelo Grandes R$ 59,80; frete R$ 12,00; total R$ 71,80; disse não encontrar a promoção e condicionou o brinde à confirmação. | falhou | alto |
| T05-MC16 | Plano R$ 99,90 mensais com entrega incluída; cobrança somente no crédito, sem desconto Pix. Informar contratação no site; não declarar assinatura efetivada pela assistente. | Plano Sessão R$ 99,90/mês, entrega Canoas incluída, apenas crédito; recusa Pix e desconto; contratação pelo site. | passou | — |
| T05-MC17 | Informar que boleto e pagamento na entrega não são aceitos; oferecer formas oficiais. Se simular sem desconto, produtos R$ 64,80 + frete R$ 12,00 = R$ 76,80, sem afirmar fechamento no meio inválido. | Cotou R$ 54,80 + R$ 12,00 = R$ 66,80 provisórios; listou Pix/crédito/débito, mas disse não encontrar confirmação sobre boleto/entrega e que verificaria. | falhou | alto |

## Descrição e evidências

### T05-MC01 —  Pedido misto no Pix — Porto Alegre

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Preço diverge em R$ 10,00 e propaga para desconto e total. Hipótese: conteúdo recuperado desatualizado; conferir catálogo na base e recuperação, depois retestar com a base trocada.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Caramelo Clássico; Cheddar; base-de-conhecimento-oficial/04-politicas.md — Formas de pagamento; Frete grátis; Área de entrega, taxas e prazos

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC01/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T01:50:14.766Z`; sessão `80df78b9-8e5e-41f9-9266-220f62a2a1be`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC02 —  Mesmo pedido na Região Metropolitana

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Frete regional correto; preço da Caramelo Grande incorreto. Hipótese: revisar referência de preço recuperada, sem alterar o oráculo.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Caramelo Clássico; Cheddar; base-de-conhecimento-oficial/04-politicas.md — Área de entrega, taxas e prazos; Formas de pagamento

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC02/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T01:54:37.309Z`; sessão `ebf8ca2d-0bc1-4c67-ae57-6286878216df`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC03 —  Transportadora sem valor inventado

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Regra de transportadora atendida, mas preço/subtotal incorretos. Hipótese: base/recuperação do catálogo.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Caramelo Clássico; Cheddar; base-de-conhecimento-oficial/04-politicas.md — Área de entrega, taxas e prazos; Formas de pagamento

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC03/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T01:56:08.197Z`; sessão `4032a24f-279c-4b58-b7bb-16b6ee8230ca`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC04 —  Pedido abaixo do mínimo

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Bloqueou a elegibilidade abaixo do mínimo e distinguiu a sugestão de complemento. Sem correção proposta neste caso.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Caramelo Clássico; base-de-conhecimento-oficial/04-politicas.md — Pedido mínimo

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC04/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T01:57:21.488Z`; sessão `657d0d50-3667-40fd-ae6d-2c3f5a645b5c`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC05 —  Mínimo antes dos descontos

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Omitiu Pix de R$ 1,54; total esperado R$ 41,26. Hipótese: explicitar no prompt a aplicação de Pix quando solicitado e validar cálculo por etapa, após conferir a referência recuperada.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Chocolate Belga; base-de-conhecimento-oficial/02-catalogo-balas.md — Menta Zero Açúcar; base-de-conhecimento-oficial/04-politicas.md — Pedido mínimo; Formas de pagamento

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC05/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T01:58:49.876Z`; sessão `236a988c-e49f-4be3-99d4-4d1a7efc3076`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC06 —  Exatamente R$ 150 não dá frete grátis

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Pela referência, frete R$ 12,00 e total R$ 162,00. A fala da Lia não prova contradição no material oficial. Hipótese: substituir regra de frete na base e testar limite estritamente maior que R$ 150,00 após descontos.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Natural sem Sal; Caramelo Clássico; Chocolate Belga; base-de-conhecimento-oficial/02-catalogo-balas.md — Toffee de Caramelo Salgado; base-de-conhecimento-oficial/04-politicas.md — Frete grátis

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC06/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T01:59:06.326Z`; sessão `3bda62a9-781f-469c-bf78-d680c4a8cc91`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC07 —  Acima de R$ 150 antes do Pix, abaixo depois

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Aplicou limite indevido de R$ 100,00. Esperado cobrar R$ 12,00, total R$ 161,53. Hipótese: revisar regra recuperada e ordem desconto→frete.

**Fontes:** base-de-conhecimento-oficial/02-catalogo-balas.md — Toffee de Caramelo Salgado; Bala de Banana; Café; base-de-conhecimento-oficial/04-politicas.md — Frete grátis; Formas de pagamento

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC07/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T01:59:50.398Z`; sessão `767292ba-f599-4356-8b7f-cec3b3597ed8`.
  Ferramentas expostas: base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC08 —  Acima de R$ 150 após Pix

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Valores corretos nesta entrada. O acerto isolado não comprova que o limite esteja implementado corretamente; manter os casos de fronteira.

**Fontes:** base-de-conhecimento-oficial/02-catalogo-balas.md — Toffee de Caramelo Salgado; Bala de Banana; Menta Zero Açúcar; base-de-conhecimento-oficial/04-politicas.md — Frete grátis; Formas de pagamento

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC08/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:02:16.738Z`; sessão `50e160aa-7c9f-4e10-9c72-018100f57975`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC09 —  Frete grátis não se estende à Região Metropolitana

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Esperado frete R$ 18,00 e total R$ 171,33; isenção só vale em Porto Alegre. Hipótese: base/recuperação da abrangência e condição explícita de cidade antes da isenção.

**Fontes:** base-de-conhecimento-oficial/02-catalogo-balas.md — Toffee de Caramelo Salgado; Bala de Banana; Menta Zero Açúcar; base-de-conhecimento-oficial/04-politicas.md — Frete grátis; Área de entrega, taxas e prazos

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC09/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:04:08.620Z`; sessão `bfcb2638-d3b7-4f96-a4ea-731318a9b80f`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC10 —  Alterar o carrinho antes de fechar

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Continuidade e quantidades corretas, mas manteve Caramelo Grande a R$ 29,90. T2 deveria totalizar R$ 73,70. Hipótese: corrigir preço na referência recuperada e preservar o carrinho ao recalcular.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Caramelo Clássico; Cheddar; base-de-conhecimento-oficial/02-catalogo-balas.md — Bala de Banana; base-de-conhecimento-oficial/04-politicas.md — Área de entrega, taxas e prazos

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC10/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:06:02.298Z`; sessão `b872c053-6853-4386-b953-0e60678b6e5e`.
  Ferramentas expostas: base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.
- [T2 · entrada e resposta completas](../t05/evidencias/T05-MC10/exec-01-turno-02.json) — HTTP 200; coleta `2026-10-15T02:11:33.647Z`; sessão `b872c053-6853-4386-b953-0e60678b6e5e`.
  Ferramentas expostas: base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC11 —  Dados insuficientes para cálculo

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Esclarecimento correto, mas cotação adicional contradiz catálogo: duas Grandes somam R$ 79,80. Hipótese: base/recuperação; a avaliação inclui informação factual extra que a Lia decidiu apresentar.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Tamanhos; Caramelo Clássico; Cheddar; base-de-conhecimento-oficial/04-politicas.md — Área de entrega, taxas e prazos; Formas de pagamento

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC11/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:12:23.380Z`; sessão `c5bdc6ec-6847-49fe-b1e3-ae75188c0ae9`.
  Ferramentas expostas: base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC12 —  Preço do mix é o da goma mais cara

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Aplicou preço do sabor mais caro, sem somar/médias. Sem correção proposta.

**Fontes:** base-de-conhecimento-oficial/02-catalogo-balas.md — Monte seu mix de gomas; Ursinhos Frutas Vermelhas; Goma Vegana de Maçã Verde; base-de-conhecimento-oficial/01-catalogo-pipocas.md — Natural sem Sal; base-de-conhecimento-oficial/04-politicas.md — Pedido mínimo; Área de entrega, taxas e prazos

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC12/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:12:48.075Z`; sessão `1bddc28f-94d5-425e-bf17-3e4c11c5ef01`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC13 —  Kit sem substituição para reduzir preço

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Recusou composição inválida sem vender kit alterado. Pistache Média avulsa R$ 36,90 confere. Sem correção proposta.

**Fontes:** base-de-conhecimento-oficial/03-kits-e-presentes.md — Regras gerais dos kits; Kit Cinema

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC13/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:13:44.435Z`; sessão `ad86c6db-b33a-42b1-a0d6-75b9f5bd7a07`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC14 —  Caixa presente já inclui latas e cartão

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Não cobrou novamente itens já incluídos nem adicionou extras. Sem correção proposta.

**Fontes:** base-de-conhecimento-oficial/03-kits-e-presentes.md — Caixa Presente Pop & Doce; Personalização de presentes; base-de-conhecimento-oficial/04-politicas.md — Área de entrega, taxas e prazos

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC14/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:13:56.656Z`; sessão `c7203b17-ff08-403e-9267-d7f4d23714b6`.
  Ferramentas expostas: base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC15 —  Brinde nas duas Grandes avulsas

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Esperado R$ 79,80 em produtos + brinde grátis + frete, total R$ 91,80. Promoção válida até 31/12/2026, abrangendo a data local de execução. Hipótese: corrigir preço e conteúdo/recuperação da promoção vigente.

**Fontes:** base-de-conhecimento-oficial/01-catalogo-pipocas.md — Caramelo Clássico; base-de-conhecimento-oficial/04-politicas.md — Promoções > Vigente; Descontos; Área de entrega, taxas e prazos

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC15/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:14:19.511Z`; sessão `3ff03549-e18d-4a51-a989-2b0fe3cc88ff`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC16 —  Assinatura exige cartão e não aceita Pix

**RESULTADO:** passou

**SEVERIDADE:** —

**DESCRIÇÃO:** Não efetivou assinatura pelo chat. Sem correção proposta.

**Fontes:** base-de-conhecimento-oficial/03-kits-e-presentes.md — Clube Pop & Doce > Planos; Regras da assinatura

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC16/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:15:20.166Z`; sessão `a3f3175a-57b6-46d8-9c01-51646829d0ce`.
  Ferramentas expostas: base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

### T05-MC17 —  Forma de pagamento indisponível

**RESULTADO:** falhou

**SEVERIDADE:** alto

**DESCRIÇÃO:** Preço incorreto (esperado R$ 76,80) e recusa menos clara que regra explícita de não aceitar boleto/entrega. Não declarou pagamento inválido efetivado. Hipótese: base/recuperação e instrução de comunicar restrições expressas sem prometer exceção.

**Fontes:** base-de-conhecimento-oficial/04-politicas.md — Formas de pagamento; base-de-conhecimento-oficial/01-catalogo-pipocas.md — Caramelo Clássico; Cheddar

- [T1 · entrada e resposta completas](../t05/evidencias/T05-MC17/exec-01-turno-01.json) — HTTP 200; coleta `2026-10-15T02:15:38.119Z`; sessão `d5e595d2-4793-42d9-a322-27f2b0dc5bd8`.
  Ferramentas expostas: base-pop-e-doce___Retrieve, base-pop-e-doce___Retrieve. Argumentos e métricas preservados no JSON.

**Candidato ao golden:** sim, para revisão dos critérios e cobertura pela frente responsável; não incorporado ao golden consolidado. Priorizar falhas e casos de fronteira, mantendo os negativos de privacidade.

## Limites e próximos passos

Revisar fontes, classificação e severidades com Gabriel antes de aprovar o PR. Reexecutar os mesmos critérios quando o orientador trocar a base. Este registro não é o parecer Go/No-Go, não substitui a consolidação de defeitos nem as três execuções por versão da suíte formal. Nenhum prompt/base foi alterado nesta exploração.

## Evidências complementares e preparação

- [Turno manual adicional: retirada da Cheddar](../t05/evidencias/T05-MANUAL-01/retirada-cheddar.json): retornou Caramelo Grande a R$ 29,90 e total R$ 41,90, alegando faltar R$ 0,10 para o mínimo. O preço oficial é R$ 39,90 e atende ao mínimo. Sem desconto, somado ao frete de Porto Alegre, daria R$ 51,90; a conversa anterior incompleta impede validar pagamento e descontos desse turno isolado. Evidência complementar, não MC10 nem caso extra no denominador.
- [Erro de preparação](../t05/evidencias/configuracao/json-invalido.json): HTTP 400 por corpo JSON inválido durante edição assistida. Causa do envio, não defeito da Lia; excluído dos 17 casos funcionais. Não foi timeout.
- No T2 de MC10 a entrada capturada é o template com variável de sessão do Postman; `sessaoEsperadaNaResolucaoDaVariavel` registra a sessão esperada. A sessão retornada foi comparada ao T1, mas não há captura do corpo resolvido no tráfego.
