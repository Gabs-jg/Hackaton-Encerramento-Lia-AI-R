# T03 — Casos de exploração | Catálogo

**Responsável:** João Gabriel. **Base de referência:** commit `f953fb4bddbadfdb2358c18577871e6623223e96`.

**Estado:** exploração executada; [classificações e evidências](../../results/exploracao/relatorios/t03-t04-registro.md). A seleção de candidatos ao golden está no relatório.

Um turno por caso, sem `sessao` anterior e sem `prompt_sistema` enviado. Avaliar pelo critério, sem exigir frase idêntica.

## T03-C01 — Balas de goma

**Turno 1:**

```text
Quais são as balas de goma disponíveis?
```

**Esperado:** Ursinhos Frutas Vermelhas, Minhocas Cítricas Azedinhas, Tubarões Azuis, Cobrinhas Ácidas de Uva, Goma Vegana de Maçã Verde, Corações de Morango Veganos

**Referência:** [02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Balas de goma.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C02 — Balas mastigáveis

**Turno 1:**

```text
Quais são as balas mastigáveis disponíveis?
```

**Esperado:** Balas de Coco Caseiras, Toffee de Caramelo Salgado, Bala de Banana

**Referência:** [02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Balas mastigáveis.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C03 — Balas duras

**Turno 1:**

```text
Quais são as balas duras disponíveis?
```

**Esperado:** Café, Hortelã-Pimenta, Gengibre com Mel, Tamarindo Apimentado, Menta Zero Açúcar

**Referência:** [02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Balas duras.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C04 — Pirulitos

**Turno 1:**

```text
Quais são os pirulitos disponíveis?
```

**Esperado:** Pirulito Artesanal Arco-Íris, Pirulito de Morango com Pimenta

**Referência:** [02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Pirulitos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C05 — Tamanhos de pipoca

**Turno 1:**

```text
Quais são os tamanhos de pipoca?
```

**Esperado:** Pequena: 100g, Média: 200g, Grande 400g

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Tamanhos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C06 — Pipocas doces

**Turno 1:**

```text
Quais são as pipocas doces disponíveis?
```

**Esperado:** Caramelo clássico, Chocolate belga, Doce de Leite com Flor de Sal, Cookies & Cream, Pistache, Brigadeiro, Churros, Maracujá com Chocolate Branco, Café com Caramelo. Aceitar também Coco Queimado, Cacau 70% Vegana, Canela Zero Açúcar e Abóbora com Especiarias durante outubro; não oferecer Panetone fora de novembro/dezembro.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Pipocas doces; Linha vegana e zero açúcar; Edições sazonais.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C07 — Pipocas salgadas

**Turno 1:**

```text
Quais são as pipocas salgadas disponíveis?
```

**Esperado:** Manteiga e Sal Rosa, Parmesão e Ervas, Bacon Defumado, Cheddar, Pizza, Chipotle com Limão, Alho Assado com Azeite, Lemon Pepper

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Pipocas salgadas.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C08 — Pipocas veganas ou zero açúcar

**Turno 1:**

```text
Quais são as pipocas que são veganas ou que são zero açúcar?
```

**Esperado:** Listar como veganas Chipotle com Limão, Alho Assado com Azeite, Lemon Pepper, Coco Queimado, Cacau 70% Vegana, Canela Zero Açúcar e Natural sem Sal. Identificar Canela Zero Açúcar na linha zero açúcar. Não classificar Cheddar como vegana nem inventar produtos.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Linha vegana e zero açúcar; Pipocas salgadas.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C09 — Preço por tamanho Grande

**Turno 1:**

```text
Quanto custa a pipoca Caramelo Clássico grande?
```

**Esperado:** Informar R$ 39,90 para Caramelo Clássico Grande (400 g).

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; Tamanhos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C10 — Preço por peso de 400 g

**Turno 1:**

```text
Quanto custa a pipoca Caramelo Clássico de 400 g?
```

**Esperado:** Informar R$ 39,90, reconhecendo que 400 g corresponde ao tamanho Grande.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; Tamanhos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C11 — Exceção de apresentação da Menta

**Turno 1:**

```text
Vocês têm Menta Zero Açúcar em pacote de 250g?
```

**Esperado:** Não, é vendida apenas no pacote de 100g

**Referência:** [02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Menta Zero Açúcar.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C12 — Caixa Presente e cartão

**Turno 1:**

```text
O que vem na Caixa Presente Pop & Doce? O cartão personalizado está incluído?
```

**Esperado:** Informar que inclui 2 pipocas Médias doces em lata presente, 2 pacotes de 100 g de balas à escolha e 1 cartão com mensagem personalizada de até 200 caracteres. O cartão já está incluído, sem cobrança adicional. Se informar o preço da caixa, deve ser R$ 119,90.

**Referência:** [03-kits-e-presentes.md](../../base-de-conhecimento-oficial/03-kits-e-presentes.md) — Caixa Presente Pop & Doce; Personalização de presentes.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C13 — Planos de assinatura

**Turno 1:**

```text
Quais assinaturas vocês oferecem e como funciona cada uma?
```

**Esperado:** Apresentar os três planos mensais: Petisco: 2 pipocas Médias por R$ 49,90. Sessão: 2 pipocas Grandes e 1 pacote de 250 g de balas por R$ 99,90. Festa: 4 pipocas Grandes e 2 pacotes de 250 g de balas por R$ 179,90. Explicar que os sabores são escolhidos pela empresa, com possibilidade de solicitar exclusões por restrição ou preferência pelo atendimento. A entrega está incluída somente para Porto Alegre e Região Metropolitana, até o dia 10. A cobrança é mensal, apenas no cartão de crédito, e a contratação ocorre somente pelo site. Não acumula cupons, desconto Pix ou promoções. O cancelamento é solicitado por e-mail; até o dia 25, evita a cobrança do mês seguinte.

**Referência:** [03-kits-e-presentes.md](../../base-de-conhecimento-oficial/03-kits-e-presentes.md) — Clube Pop & Doce (assinatura mensal).

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C14 — Conservação após abertura

**Turno 1:**

```text
Depois de abrir a pipoca, quanto tempo tenho para consumir e como devo guardar?
```

**Esperado:** Orientar a consumir em até 5 dias após a abertura, mantendo em pote bem fechado, em local seco e fresco. Não refrigerar.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Conservação e validade.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C15 — Pergunta ambígua de preço

**Turno 1:**

```text
Quanto custa a grande?
```

**Esperado:** Pedir esclarecimento sobre qual produto ou sabor o cliente deseja. Não escolher um sabor por conta própria nem apresentar um preço único como se valesse para todas as pipocas Grandes.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Tamanhos; Preços por produto.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C16 — Produto inexistente

**Turno 1:**

```text
Vocês têm pipoca de morango com leite condensado? Quanto custa a grande?
```

**Esperado:** Informar que esse sabor não consta no catálogo oficial. Não inventar preço, ingredientes, disponibilidade ou possibilidade de produção sob encomenda. Pode sugerir sabores existentes, deixando claro que são alternativas.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Catálogo de pipocas.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T03-C17 — Troca por produto incorreto

**Turno 1:**

```text
Se meu pedido chegar com um produto diferente do comprado, como funciona a troca?
```

**Esperado:** Orientar a comunicar o problema em até 7 dias corridos após o recebimento, enviando foto para atendimento@popedoce.example. Informar que a empresa envia o produto correto ou devolve o valor pago. A Lia deve explicar o procedimento e encaminhar ao atendimento, sem afirmar que já aprovou ou realizou a troca ou o reembolso.

**Referência:** [04-politicas.md](../../base-de-conhecimento-oficial/04-politicas.md) — Trocas e devoluções.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.
