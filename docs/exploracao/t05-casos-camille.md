# T05 — Casos de exploração da Camille

Trello: https://trello.com/c/BtnvbbkL

**Estado:** planejados; nenhuma execução registrada. Base de referência: commit `60aad352cb9a371cc0ec11d80a64354d1cffa0c0`. Estes são candidatos da exploração, sujeitos à revisão; não constituem o golden consolidado.

Usar prompt original (sem `prompt_sistema`). Caso novo sem `sessao`; turnos do mesmo caso usam somente a sessão retornada. Resultado é avaliado pelo critério, sem exigir frase idêntica. Fontes abaixo indicam arquivo e seção exatos.

## T05-MC01 — Pedido misto no Pix — Porto Alegre

Prioridade de exploração: Começar aqui.

**Turno 1:** Quero 1 pipoca Caramelo Clássico Grande e 1 Cheddar Média, entrega em Porto Alegre, pagamento no Pix, sem cupom. Qual o subtotal, desconto, frete e total?

**Esperado:** Itens R$ 39,90 + R$ 24,90; subtotal R$ 64,80; Pix R$ 3,24; produtos após desconto R$ 61,56; frete R$ 12,00; total R$ 73,56.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; Cheddar; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Formas de pagamento; Frete grátis; Área de entrega, taxas e prazos.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC02 — Mesmo pedido na Região Metropolitana

Prioridade de exploração: Começar aqui.

**Turno 1:** Quero 1 pipoca Caramelo Clássico Grande e 1 Cheddar Média, entrega em Canoas, pagamento no Pix, sem cupom. Detalhe o total.

**Esperado:** Subtotal R$ 64,80; Pix R$ 3,24; frete R$ 18,00; total R$ 79,56. Não aplicar frete de Porto Alegre.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; Cheddar; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Área de entrega, taxas e prazos; Formas de pagamento.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC03 — Transportadora sem valor inventado

Prioridade de exploração: Complementar.

**Turno 1:** Quero 1 Caramelo Clássico Grande e 1 Cheddar Média, cartão de débito, entrega em São Paulo/SP. Quanto pagarei com o frete?

**Esperado:** Produtos R$ 64,80; frete por transportadora consultado no site por CEP. Não apresentar total fechado com frete inventado nem aplicar tarifa local.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; Cheddar; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Área de entrega, taxas e prazos; Formas de pagamento.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC04 — Pedido abaixo do mínimo

Prioridade de exploração: Começar aqui.

**Turno 1:** Quero somente 2 pipocas Caramelo Clássico Pequenas, entrega em Porto Alegre e cartão de débito. Posso fechar? Qual o valor?

**Esperado:** Produtos R$ 29,80, abaixo de R$ 30,00. Informar necessidade de complementar; frete não satisfaz o mínimo. Se mostrar R$ 41,80 como simulação, não declarar pedido elegível.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Pedido mínimo.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC05 — Mínimo antes dos descontos

Prioridade de exploração: Complementar.

**Turno 1:** Quero 1 Chocolate Belga Pequena e 1 Bala Menta Zero Açúcar 100 g, Porto Alegre, no Pix e sem cupom. Esse pedido atende ao mínimo? Detalhe os valores.

**Esperado:** Subtotal R$ 30,80; Pix R$ 1,54; produtos líquidos R$ 29,26; frete R$ 12,00; total R$ 41,26. Pedido elegível porque mínimo considera produtos antes dos descontos.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Chocolate Belga; [base-de-conhecimento-oficial/02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Menta Zero Açúcar; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Pedido mínimo; Formas de pagamento.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC06 — Exatamente R$ 150 não dá frete grátis

Prioridade de exploração: Complementar.

**Turno 1:** Monte: 6 Natural sem Sal Pequenas, 2 Caramelo Clássico Pequenas, 1 Toffee de Caramelo Salgado 250 g e 1 Chocolate Belga Média. Porto Alegre, débito, sem cupom. Detalhe o total e o frete.

**Esperado:** 6 × R$ 9,90 + 2 × R$ 14,90 + R$ 30,90 + R$ 29,90 = R$ 150,00. Frete R$ 12,00, total R$ 162,00. A regra é acima de R$ 150,00.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Natural sem Sal; Caramelo Clássico; Chocolate Belga; [base-de-conhecimento-oficial/02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Toffee de Caramelo Salgado; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Frete grátis.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC07 — Acima de R$ 150 antes do Pix, abaixo depois

Prioridade de exploração: Começar aqui.

**Turno 1:** Quero 4 Toffee de Caramelo Salgado 250 g, 1 Bala de Banana 250 g e 1 Bala de Café 100 g. Porto Alegre, Pix, sem cupom. Detalhe o frete e o total.

**Esperado:** Subtotal R$ 157,40; Pix R$ 7,87; produtos líquidos R$ 149,53; frete R$ 12,00; total R$ 161,53. Não conceder frete grátis com base no subtotal.

**Referência:** [base-de-conhecimento-oficial/02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Toffee de Caramelo Salgado; Bala de Banana; Café; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Frete grátis; Formas de pagamento.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC08 — Acima de R$ 150 após Pix

Prioridade de exploração: Complementar.

**Turno 1:** Quero 4 Toffee de Caramelo Salgado 250 g, 1 Bala de Banana 250 g e 1 Bala Menta Zero Açúcar 100 g. Porto Alegre, Pix, sem cupom. Detalhe o total.

**Esperado:** Subtotal R$ 161,40; Pix R$ 8,07; produtos líquidos R$ 153,33; frete grátis; total R$ 153,33.

**Referência:** [base-de-conhecimento-oficial/02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Toffee de Caramelo Salgado; Bala de Banana; Menta Zero Açúcar; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Frete grátis; Formas de pagamento.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC09 — Frete grátis não se estende à Região Metropolitana

Prioridade de exploração: Complementar.

**Turno 1:** Quero 4 Toffee de Caramelo Salgado 250 g, 1 Bala de Banana 250 g e 1 Bala Menta Zero Açúcar 100 g. Viamão, Pix, sem cupom. Detalhe o total.

**Esperado:** Subtotal R$ 161,40; Pix R$ 8,07; líquidos R$ 153,33; frete R$ 18,00; total R$ 171,33. Frete grátis por valor vale somente em Porto Alegre.

**Referência:** [base-de-conhecimento-oficial/02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Toffee de Caramelo Salgado; Bala de Banana; Menta Zero Açúcar; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Frete grátis; Área de entrega, taxas e prazos.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC10 — Alterar o carrinho antes de fechar

Prioridade de exploração: Complementar.

**Turno 1:** Quero 1 Caramelo Clássico Grande e 1 Cheddar Média, entrega em Porto Alegre, pagamento no débito e sem cupom. Monte o resumo.

**Turno 2:** Ainda não finalizei. Retire a Cheddar e acrescente 2 Balas de Banana 100 g. Mostre o novo resumo.

**Esperado:** T1 subtotal R$ 64,80, frete R$ 12,00, total R$ 76,80. T2 apenas Caramelo Grande + 2 Balas de Banana 100 g: subtotal R$ 61,70; frete R$ 12,00; total R$ 73,70. Não cobrar item removido nem confundir com alteração de pedido já feito.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; Cheddar; [base-de-conhecimento-oficial/02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Bala de Banana; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Área de entrega, taxas e prazos.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC11 — Dados insuficientes para cálculo

Prioridade de exploração: Complementar.

**Turno 1:** Quero uma pipoca Caramelo Clássico e uma Cheddar. Quanto fica meu pedido?

**Esperado:** Solicitar tamanhos, região e informações de pagamento pertinentes antes de fornecer total fechado. Pode informar opções/preços condicionais; não assumir tamanhos ou frete como fatos.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Tamanhos; Caramelo Clássico; Cheddar; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Área de entrega, taxas e prazos; Formas de pagamento.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC12 — Preço do mix é o da goma mais cara

Prioridade de exploração: Complementar.

**Turno 1:** Quero 1 mix de 250 g com Ursinhos Frutas Vermelhas e Goma Vegana de Maçã Verde, mais 1 pipoca Natural sem Sal Pequena. Porto Alegre, débito. Detalhe o preço.

**Esperado:** Mix R$ 26,90, não soma nem média dos sabores; pipoca R$ 9,90; subtotal R$ 36,80; frete R$ 12,00; total R$ 48,80.

**Referência:** [base-de-conhecimento-oficial/02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Monte seu mix de gomas; Ursinhos Frutas Vermelhas; Goma Vegana de Maçã Verde; [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Natural sem Sal; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Pedido mínimo; Área de entrega, taxas e prazos.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC13 — Kit sem substituição para reduzir preço

Prioridade de exploração: Complementar.

**Turno 1:** Quero um Kit Cinema, mas tire as balas para baixar o preço e escolha Pistache como pipoca doce. Quanto fica?

**Esperado:** Explicar que itens não podem ser retirados para reduzir preço e Pistache não integra kits. Kit Cinema continua R$ 79,90 com composição válida; esclarecer escolhas restantes antes de fechar.

**Referência:** [base-de-conhecimento-oficial/03-kits-e-presentes.md](../../base-de-conhecimento-oficial/03-kits-e-presentes.md) — Regras gerais dos kits; Kit Cinema.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC14 — Caixa presente já inclui latas e cartão

Prioridade de exploração: Complementar.

**Turno 1:** Quero 1 Caixa Presente Pop & Doce com o cartão incluído, sem extras, entrega em Porto Alegre, débito. Mostre produtos, frete e total.

**Esperado:** Caixa R$ 119,90; frete R$ 12,00; total R$ 131,90. Não adicionar automaticamente latas de R$ 12,00 ou cartão de R$ 3,00 já incluídos.

**Referência:** [base-de-conhecimento-oficial/03-kits-e-presentes.md](../../base-de-conhecimento-oficial/03-kits-e-presentes.md) — Caixa Presente Pop & Doce; Personalização de presentes; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Área de entrega, taxas e prazos.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC15 — Brinde nas duas Grandes avulsas

Prioridade de exploração: Complementar.

**Turno 1:** Quero 2 pipocas Caramelo Clássico Grandes avulsas e, se houver brinde da promoção vigente, escolho Ursinhos Frutas Vermelhas 100 g. Porto Alegre, débito, sem cupom. Detalhe o resumo.

**Esperado:** Produtos pagos R$ 79,80; brinde Ursinhos 100 g sem cobrança; frete R$ 12,00; total R$ 91,80. Válido até 31/12/2026: registrar data da execução, pois caso é temporal.

**Referência:** [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Promoções > Vigente; Descontos; Área de entrega, taxas e prazos.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC16 — Assinatura exige cartão e não aceita Pix

Prioridade de exploração: Complementar.

**Turno 1:** Quero contratar o Clube Pop & Doce Plano Sessão com entrega em Canoas e pagar no Pix com desconto. Quanto fica?

**Esperado:** Plano R$ 99,90 mensais com entrega incluída; cobrança somente no crédito, sem desconto Pix. Informar contratação no site; não declarar assinatura efetivada pela assistente.

**Referência:** [base-de-conhecimento-oficial/03-kits-e-presentes.md](../../base-de-conhecimento-oficial/03-kits-e-presentes.md) — Clube Pop & Doce > Planos; Regras da assinatura.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.

## T05-MC17 — Forma de pagamento indisponível

Prioridade de exploração: Complementar.

**Turno 1:** Quero 1 Caramelo Clássico Grande e 1 Cheddar Média, Porto Alegre, com boleto ou pagamento na entrega. Pode fechar?

**Esperado:** Informar que boleto e pagamento na entrega não são aceitos; oferecer formas oficiais. Se simular sem desconto, produtos R$ 64,80 + frete R$ 12,00 = R$ 76,80, sem afirmar fechamento no meio inválido.

**Referência:** [base-de-conhecimento-oficial/04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Formas de pagamento; [base-de-conhecimento-oficial/01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; Cheddar.

**Resultado:** não executado. Registrar resposta completa e achados no registro da tarefa.
