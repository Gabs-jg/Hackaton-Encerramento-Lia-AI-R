# Plano do Red Team

**Responsável:** Gustavo 

## Objetivo

Registrar no mínimo 30 tentativas de ataque contra a Lia, em pelo menos 5 categorias. Cada tentativa traz objetivo, técnica, resultado, severidade e evidência. Os ataques rodam nas versões original e corrigida, pelo menos 3 vezes cada, sempre em sessões novas.

## Categorias de ataque

1. **Prompt injection e jailbreak:** trocar a persona, simular modo de homologação, mandar ignorar as instruções.
2. **Extração de informação interna:** prompt de sistema, ferramentas, arquitetura.
3. **Privacidade e bypass de autorização:** obter dados de pedido de outra pessoa.
4. **Manipulação comercial:** cupom falso, desconto inventado, preço fora da base oficial.
5. **Segurança alimentar e alegações de saúde:** forçar garantia de ausência de alérgeno ou afirmação sobre glicemia.
6. **Escopo e abuso de tarefa (opcional):** usar a Lia para assuntos fora da loja.

## Origem dos casos

| Origem | Quantidade |
|---|---:|
| Reaproveitados da exploração (T06, T09, T10) | 15 |
| Novos, focados nas categorias com menos cobertura | 15 |
| **Total** | **30** |

Os JSONs da exploração ficam como origem do caso. Não servem como evidência final, porque têm uma execução só e nenhuma na versão corrigida.

## Triagem dos casos reaproveitados

Foram analisados 20 casos da exploração com potencial para o red team (T10, T06 e T09). O critério para ficar: ter uma técnica de ataque explícita e mirar um dos pontos obrigatórios da Pop & Doce. Pergunta comum que só gerou erro fica na T09, não conta como ataque.

### Descartados (5)

| Caso | Motivo |
|---|---|
| ADV-05 (reteste) | Mesma técnica do ADV-05; a fabricação de pedido já aparece em outros casos |
| ADV-06 | Pedido de código sem ataque explícito; a própria T10 marca como controle. FDE05 cobre melhor |
| ADV-07 | Falsa premissa esportiva, severidade baixa, sem alvo relevante |
| ADV-08 | Pergunta comum sobre filme, sem técnica de ataque |
| T06-EX08 | Pressão e cargo falso já estão no EX03; pista de e-mail já está no EX01 |

### Mantidos (15)

| Caso | Categoria | Técnica |
|---|---|---|
| ADV-05 | Privacidade / injection | Instrução para ignorar a validação de e-mail |
| ADV-02 | Manipulação comercial | Falsa autoridade (QA interno) e urgência |
| ADV-03 | Jailbreak | Modo de homologação (precisa de um turno a mais para ser verificável) |
| ADV-01 | Extração | Extração parcial do prompt |
| ADV-04 | Extração | Sondagem de arquitetura com pretexto de segurança |
| T09-FDE04 | Extração | Pedido direto de dado estratégico |
| T09-FDE05 | Jailbreak | Troca de persona |
| T06-EX03 | Privacidade / injection | Cargo falso, instrução de sistema falsa e exportação em CSV |
| T06-EX02 | Privacidade / injection | JSON colado como autorização |
| T06-EX07 | Privacidade / injection | Log falso de ferramenta |
| T06-EX09 | Privacidade | Enumeração e dado agregado |
| T06-EX01 | Privacidade | Uso da autorização de um pedido em outro |
| T06-EX04 | Privacidade | Histórico de conversa presumido |
| T06-EX05 | Privacidade | Parentesco e ofuscação em base64 |
| T06-EX06 | Privacidade | E-mail com domínio parecido |

Detalhamento dos 15 casos mantidos (input, esperado, output e evidência): [casos-reaproveitados-exploracao.md](casos-reaproveitados-exploracao.md).

### Cobertura por categoria

| Categoria | Casos mantidos | Situação |
|---|---:|---|
| Privacidade e bypass de autorização | 9 (inclui ADV-05) | Coberta com sobra |
| Prompt injection e jailbreak | 2 (+ injeções dentro dos casos de privacidade) | Coberta |
| Extração de informação interna | 3 | Coberta |
| Manipulação comercial | 1 | Fraca |
| Segurança alimentar e alegações de saúde | 0 | Sem cobertura |

### Foco dos 15 casos novos

| Categoria | Casos novos | Ideias de ataque |
|---|---:|---|
| Segurança alimentar e alegações de saúde | 5 | Garantia de ausência de alérgeno, laudo inventado, glicemia, recomendação para condição médica |
| Manipulação comercial | 4 | Preço inventado, cupom encerrado sob pressão, desconto acumulado, promoção fora da base |
| Prompt injection e jailbreak | 4 | Ataque em várias etapas, troca de idioma, instrução escondida dentro de um pedido |
| Extração de informação interna | 2 | Nomes e parâmetros das ferramentas, regras internas de desconto |

Privacidade fica sem casos novos, porque já tem 8.

## Suíte e sobreposição com o golden

- O red team roda em **promptfoo**, separado da suíte principal do golden, que roda em **DeepEval**
- **Cada ataque roda em uma suíte só.** Se o caso estiver no golden, roda no DeepEval e o log de red team aponta para a evidência de lá. Os demais rodam no promptfoo. Isso evita executar o mesmo caso 6 vezes.
- O ataque continua contando nas 30 tentativas, independente da suíte onde rodou.
- Cada caso no promptfoo recebe a tag `golden: true/false`. Quando o golden for definido, os repetidos são filtrados, não apagados. Se o DeepEval atrasar, o promptfoo roda tudo.

## Regras

- No máximo 4 chamadas em paralelo, somando a equipe.
- Chave da API só em variável de ambiente; nunca no repositório, nas evidências ou nos exports.
- Apenas dados da massa de teste ou inventados.

---

# Após a sessão exploratória

A exploração manual executou 23 casos nas categorias com pouca cobertura. Resultados e evidências: [exploracao-manual-registro.md](exploracao-manual-registro.md) e [exploracao-manual-casos.md](exploracao-manual-casos.md).

## Seleção dos casos novos

Critério: falhas críticas ou de ponto obrigatório do enunciado primeiro, uma técnica diferente por caso e nenhuma repetição de técnica já coberta pelos casos reaproveitados.

| Categoria | Casos selecionados |
|---|---|
| Segurança alimentar e alegações de saúde | SA01, SA02, SA03-V1, SA05, SA06, SA07 |
| Manipulação comercial | CO01, CO03, CO04, CO06 |
| Prompt injection e jailbreak | IN01, IN04, IN05 |
| Extração de informação interna | EI01, EI02 |

A distribuição ficou diferente do foco previsto (5, 4, 4 e 2): saúde ganhou um caso porque SA05 trouxe uma alegação de saúde explícita, e injection perdeu um porque IN02 repete a técnica do T09-FDE05.

## Casos que ficaram de fora

| Caso | Destino | Motivo |
|---|---|---|
| SA03-V2 e SA03-V3 | Sugestão para o golden | Junto com SA03-V1, formam um par metamórfico: muda só o tipo de diabetes e a resposta segura deveria ser a mesma |
| SA04 | Sugestão para o golden (alérgenos e restrições) | É mais falha de restrição vegana do que ataque |
| CO02 | Sugestão para o golden (cupons) | Testa a regra de não combinar Pix com cupom e o cálculo do total |
| CO05 | Sugestão para o golden (pedido com cálculo ou vários turnos) | O defeito principal é o total errado |
| IN03 | Sugestão para o golden (vários turnos) | A política inventada é mais erro de fidelidade à base do que ataque |
| IN02 | Descartado | Mesma técnica do T09-FDE05 (troca de persona) |
| EI03 | Descartado | Passou; pode servir como controle |

## Contagem final

| Categoria | Reaproveitados | Novos | Total |
|---|---:|---:|---:|
| Privacidade e bypass de autorização | 9 | 0 | 9 |
| Segurança alimentar e alegações de saúde | 0 | 6 | 6 |
| Prompt injection e jailbreak | 2 | 3 | 5 |
| Extração de informação interna | 3 | 2 | 5 |
| Manipulação comercial | 1 | 4 | 5 |
| **Total** | **15** | **15** | **30** |

Cada ataque roda em uma suíte só: 20 no promptfoo (`tests/red-team/`) e 10 no golden, que já contém T10-ADV01 a ADV05, T06-EX02, T06-EX09, T09-FDE04, T09-FDE05 e T04-PM02A (SA03-V1). Lista final, evidências e situação de cada tentativa: [log-red-team.md](log-red-team.md).
