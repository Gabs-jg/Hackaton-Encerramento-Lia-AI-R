# Convenção provisória de arredondamento

Adotamos ROUND_HALF_UP: calcular o desconto sobre o subtotal, arredondar o desconto uma única vez para dois decimais, subtrair do subtotal e somar o frete. Usar aritmética decimal, sem arredondar cada produto separadamente.

Esta é uma decisão da equipe, pendente de orientação, e não uma regra encontrada na base oficial. O golden recebido como 0.3.0 passa a 0.3.1 para identificar esta adaptação. Mantemos 48 casos, 86 turnos e cinco pares; são 112 critérios, pois separamos o arredondamento do ramo Pix em MT04 das regras de escolha do benefício.

| Caso/turno | Subtotal | Desconto Pix | Líquido | Frete | Total |
|---|---:|---:|---:|---:|---:|
| T05-EX01 T3 | 61,70 | 3,09 | 58,61 | 18,00 | 76,61 |
| T05-EX01 T5 | 32,70 | 1,64 | 31,06 | 18,00 | 49,06 |
| T05-EX02 T2 | 149,70 | 7,49 | 142,21 | 12,00 | 154,21 |
| T08-MT04 T3, somente ramo Pix | 219,90 | 11,00 | 208,90 | cidade pendente | não definido |

Divergências nesses critérios ficam registradas como resultado da convenção e exigem justificativa humana. Não são, isoladamente, violação comprovada da base nem bloqueador automático de Go/No-Go. Não há tolerância geral de um centavo: preço, quantidade, percentual, frete, mínimo e não acumulação continuam sendo avaliados normalmente.

O ramo PIPOCA20 mantém líquido de 175,92; não impomos Pix nem prioridade automática. Uma resposta sem cálculo do ramo Pix não comprova seu arredondamento.

Este documento complementa a T12 sem reescrever sua versão histórica. Preservamos o golden v0.2 e todas as evidências anteriores. A primeira run não cobre os novos casos PM02; serão necessárias novas rodadas com o golden definitivo e a configuração correspondente.
