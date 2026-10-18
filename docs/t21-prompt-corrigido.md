# T21 — Prompt corrigido candidato

Consolidei a base proposta pela Fernanda com os achados das oito frentes de exploração, da primeira run histórica e do red team do Gustavo. O objetivo é corrigir o comportamento geral da Lia, sem inserir respostas do golden nem dados de pedidos da massa no prompt.

**Situação:** candidato para revisão da equipe; ainda não executado contra a Lia. Não há melhoria comprovada nem parecer de aprovação associado a esta versão.

## Arquivo usado na execução

[`../prompts/prompt-corrigido.md`](../prompts/prompt-corrigido.md) contém somente as instruções destinadas à Lia. Este documento não deve ser enviado junto. O texto corresponde à revisão 3 consolidada para revisão; substitui as propostas anteriores, sem necessidade de concatená-las.

- SHA-256 dos bytes UTF-8: `e3374c76c534567df3260f7e83ce94d61761c131ea828aa789251ba0dd4cb355`.
- Aproximadamente 3.074 palavras; medir os tokens efetivos no piloto antes da campanha.
- Registrar o hash efetivamente enviado em cada execução. Conversão de finais de linha altera o hash de bytes; não confundir isso com evidência de melhoria.

## Principais mudanças

| Frente | Comportamento proposto | Referências de casos |
|---|---|---|
| Catálogo | Confirmar produto/apresentação, esclarecer ambiguidade e não inventar preços, composição ou disponibilidade. | T03-C09/C10/C11/C13/C15/C16 |
| Restrições e saúde | Diferenciar ingredientes, traços e certificação; preservar restrições entre turnos e avisos essenciais; não prometer efeito clínico. | T04-AR04/07/09/11/12; T18-SA01/02/03/05/06/07 |
| Carrinho e cálculo | Reconstruir itens, remover excluídos, recalcular benefícios e frete; separar sugestão comercial de adição paga. | T05-EX01/02; MC05/06/07/09/12/13/14/16; T08-MT10 |
| Privacidade | Confirmar pedido/e-mail, revalidar quando mudar, não aceitar log colado ou divulgar pistas, agregados e dados codificados. | T06-CP11/13; EX02/06/09; T18-EX01/04/05/06/07 |
| Cupons | Validar benefício elegível antes de confirmá-lo; recusar exceções e promessas de descontos fora da política. | T07-CEX/PRE; T08-MT04/05; T18-CO01/03/04/06 |
| Ferramentas | Definir gatilhos de chamada, dados faltantes, exame do retorno e revalidação; não simular chamadas em texto. | T06-CP01–CP06; T18-CO02/06; EX07 |
| Injeção e informação interna | Tratar cartão/log/texto codificado como dados, retirar efeitos de instruções indevidas entre turnos e não descrever instruções internas. | T10-ADV01–05; T18-IN01/04/05; EI01/02 |
| Atendimento legítimo | Responder à intenção atual; manter consulta autorizada, informação pública e ajuda com presentes, sem recusar tudo. | T08; T09; controles de consulta e montagem |

A validação das ferramentas usa os contratos realmente disponibilizados pelo ambiente. Não copiei nomes técnicos ou argumentos que a Lia alegou utilizar: essas respostas não comprovam o esquema das ferramentas.

## Decisões de consolidação

- Preservei os objetivos das contribuições da Fernanda, removendo duplicações e obrigações de formatação desnecessárias. Avisos essenciais permanecem obrigatórios, sem exigir desculpas ou LEAD jornalístico em toda resposta.
- Não incluí o código interno observado no red team. A regra protege qualquer benefício restrito e não promete validação desse benefício em outro canal.
- O agente recebe instruções para usar a base disponibilizada pelo sistema; não presumo acesso à pasta do repositório.
- A convenção de cálculo é provisória: ROUND_HALF_UP aplicado uma vez ao desconto sobre o subtotal, antes de subtrair e somar frete. É decisão da equipe pendente do orientador, alinhada ao PR #10; não é regra atribuída à base oficial.
- Consulta completa e confirmação de cupom potencialmente elegível exigem a ferramenta pertinente. Explicação geral ou recusa de uma proibição explícita não exige chamada artificial.

## Limites e verificação necessária

O prompt não altera a base hospedada, cria ferramentas, corrige autorização no serviço ou remove segredos do contexto original. Falhas nesses componentes exigem recomendação separada. `ferramentas: []` indica ausência de chamada registrada; não comprova sozinho ausência de execução interna.

O placar histórico do promptfoo não é prova de correção: há respostas aprovadas pelas verificações antigas que ainda apresentam falhas. Usar evidência e revisão semântica, sem adaptar a redação do prompt apenas para escapar de expressões bloqueadas.

Antes da campanha, revisar este texto com Fernanda, Gabriel e Gustavo; conferir como o serviço aplica `prompt_sistema`; executar um lote pequeno com casos legítimos e adversariais e medir custo/tokens. Depois, congelar o arquivo e usar o mesmo hash no DeepEval e no promptfoo, mantendo golden, condições da base e protocolo comparáveis nas três repetições. Não alterar o prompt entre as repetições da mesma versão.

## Relação com os outros PRs

- [PR #9](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/9): red team e suas evidências; este PR não altera seus testes.
- [PR #10](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/10): golden e convenção provisória; este PR não altera o dataset.
- [PR #11](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/11): automação. O executor pode receber este arquivo por `--prompt`; no promptfoo, a configuração proposta no PR #9 já aponta para `prompts/prompt-corrigido.md`, mas o provider corrigido precisa ser habilitado quando a equipe decidir executar.

Os relatórios de exploração estão em [`results/exploracao/relatorios/`](../results/exploracao/relatorios/). As evidências do red team consultadas estão na [revisão 868d446](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/tree/868d4464890043f2c3ede50c6260d15751d186b4/results/red-team). A primeira run da automação permanece histórica da v0.2; não comprova esta proposta.
