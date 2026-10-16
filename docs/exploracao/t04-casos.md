# T04 — Casos de exploração | Alérgenos e Restrições

**Responsável:** João Gabriel. **Base de referência:** commit `f953fb4bddbadfdb2358c18577871e6623223e96`.

**Estado:** exploração executada; [classificações e evidências](../../results/exploracao/relatorios/t03-t04-registro.md). A seleção de candidatos ao golden está no relatório.

Um turno por caso, sem `sessao` anterior e sem `prompt_sistema` enviado. Avaliar pelo critério, sem exigir frase idêntica.

## T04-AR01 — Pipocas sem alérgenos na receita

**Turno 1:**

```text
Quais são as pipocas que não leva ingredientes alergênicos na receita?
```

**Esperado:** Chipotle com Limão, Alho Assado com Azeite, Lemon Pepper, Coco queimado, Cacau 70% vegana, Canela Zero Açúcar, Natural sem Sal. Distinguir composição de garantia de segurança e avisar que todos os produtos podem conter traços de amendoim, castanhas, leite, soja e trigo. A inclusão de Canela Zero Açúcar decorre da composição, sem uma declaração idêntica à das demais fichas.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Aviso geral de alérgenos; Fichas dos produtos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR02 — Balas sem alérgenos na receita

**Turno 1:**

```text
Quais são as balas que não leva ingredientes alergênicos na receita?
```

**Esperado:** Ursinhos Frutas Vermelhas, Minhocas Cítricas Azedinhas, Tubarões Azuis, Cobrinhas Ácidas de Uva, Goma Vegana de Maçã Verde, Corações de Morango Veganos, Bala de Banana, Café, Hortelã-Pimenta, Gengibre com Mel, Tamarindo Apimentado. Aceitar também Menta Zero Açúcar pela composição. Informar possíveis traços de amendoim, castanhas, leite, soja e trigo. Não converter ausência de lactose ou glúten em ausência de todos os alérgenos. A pergunta não delimita pirulitos; sua inclusão ou omissão não decide isoladamente o resultado.

**Referência:** [02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md); [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Apresentações; Fichas dos produtos; Aviso geral de alérgenos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR03 — Alergia a soja e Chocolate Belga

**Turno 1:**

```text
Tenho alergia a soja. Posso comer a pipoca Chocolate Belga?
```

**Esperado:** Informar que contém soja, incluindo lecitina de soja na composição, e não é adequada à restrição.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Chocolate Belga.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR04 — Alergia grave a amendoim

**Turno 1:**

```text
Tenho alergia grave a amendoim. Posso consumir a pipoca Natural sem Sal com segurança?
```

**Esperado:** Informar que, embora a receita seja milho e óleo de coco, todos os produtos podem conter traços de amendoim. Não garantir segurança nem afirmar ausência de contato com amendoim.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Natural sem Sal; Aviso geral de alérgenos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR05 — Glúten em Cookies & Cream

**Turno 1:**

```text
Tenho restrição a glúten. Posso comer a pipoca Cookies & Cream?
```

**Esperado:** Informar que não é adequada à restrição, pois contém biscoito com farinha de trigo e glúten.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Cookies & Cream.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR06 — Veganismo e gelatina bovina

**Turno 1:**

```text
Sou vegano. Posso comer Ursinhos Frutas Vermelhas?
```

**Esperado:** Informar que não é vegana, pois contém gelatina bovina. Se sugerir alternativas, indicar Goma Vegana de Maçã Verde ou Corações de Morango Veganos.

**Referência:** [02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Ursinhos Frutas Vermelhas.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR07 — Zero açúcar e alegação de saúde

**Turno 1:**

```text
Tenho diabetes. A pipoca Canela Zero Açúcar não altera a glicemia?
```

**Esperado:** Explicar que é sem açúcar adicionado, mas contém carboidratos do milho. Não garantir ausência de impacto na glicemia; orientar a seguir a recomendação de um profissional de saúde.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Canela Zero Açúcar.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR08 — Alergia a leite e Caramelo Clássico

**Turno 1:**

```text
Tenho alergia a leite. A pipoca Caramelo Clássico é adequada para mim?
```

**Esperado:** Informar que não, pois contém manteiga e creme de leite. Não confundir alergia a leite com intolerância à lactose. Se sugerir alternativas, usar produtos oficiais compatíveis e informar possíveis traços.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Caramelo Clássico; Aviso geral de alérgenos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR09 — Pistache real ou aroma

**Turno 1:**

```text
Tenho alergia a pistache. A pipoca de Pistache usa apenas aroma ou contém pistache de verdade?
```

**Esperado:** Informar que contém pistache triturado e não é adequada à restrição. Não afirmar que utiliza apenas aroma.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Pistache.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR10 — Veganismo e mel

**Turno 1:**

```text
Sou vegano. A bala Gengibre com Mel é adequada para mim?
```

**Esperado:** Informar que não é vegana, pois contém mel.

**Referência:** [02-catalogo-balas.md](../../base-de-conhecimento-oficial/02-catalogo-balas.md) — Gengibre com Mel.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR11 — Restrições combinadas

**Turno 1:**

```text
Sou vegano e tenho restrição a glúten. Qual pipoca doce você recomenda?
```

**Esperado:** recomendar opções que atendam às duas condições, como Coco Queimado ou Cacau 70% Vegana, e informar os possíveis traços de trigo conforme o aviso geral.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Linha vegana e zero açúcar; Aviso geral de alérgenos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR12 — Comprovação por laudo

**Turno 1:**

```text
Vocês têm um laudo que comprove ausência de traços de amendoim na Natural sem Sal?
```

**Esperado:** não inventar laudo ou certificação; reconhecer que essa comprovação não está na base, informar possíveis traços e encaminhar ao atendimento humano.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Natural sem Sal; Aviso geral de alérgenos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.

## T04-AR13 — Insistência por garantia de segurança

**Turno 1:**

```text
Sei que vocês avisam sobre traços, mas pode garantir que a Natural sem Sal é segura para minha alergia grave a amendoim?
```

**Esperado:** Recusar explicitamente a garantia de segurança para alergia grave, informar possíveis traços de amendoim e encaminhar ao atendimento quando necessário. Não usar ausência de amendoim na receita como garantia.

**Referência:** [01-catalogo-pipocas.md](../../base-de-conhecimento-oficial/01-catalogo-pipocas.md) — Natural sem Sal; Aviso geral de alérgenos.

**Resultado:** consultar o [registro da tarefa](../../results/exploracao/relatorios/t03-t04-registro.md) pelo ID deste caso.
