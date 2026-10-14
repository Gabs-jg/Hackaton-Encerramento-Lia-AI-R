# Hackathon de Encerramento — Lia · Pop & Doce

Projeto de Quality Engineering para avaliar a assistente de vendas Lia, propor melhorias no prompt e fundamentar uma decisão de Go/No-Go com evidências.

## Situação inicial

O repositório contém os materiais oficiais e a estrutura inicial de trabalho. Os testes exploratórios começarão no Postman. A suíte automatizada, os critérios de aprovação e o método de avaliação ainda serão definidos pela equipe.

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `base-de-conhecimento-oficial/` | Base fornecida pelo orientador; referência para as expectativas. |
| `massa-de-teste.md` | Pedidos e clientes fictícios para os testes. |
| `datasets/` | Golden dataset e casos metamórficos revisados. |
| `tests/` | Código e configurações da suíte automatizada. |
| `tests/postman/` | Coleções compartilháveis do Postman, sem credenciais. |
| `results/` | Evidências, resultados das execuções e comparação dos prompts. |
| `results/red-team/` | Registro das tentativas adversariais e suas evidências. |
| `prompts/` | Versões do prompt de sistema e suas alterações. |
| `docs/` | Decisões, tabelas de regras, parecer e materiais da apresentação. |

As pastas de trabalho começam vazias, com `.gitkeep` para serem mantidas no Git.

## Divisão inicial da exploração

| Integrante | Categorias |
| --- | --- |
| João | Catálogo; alérgenos e restrições. |
| Camille | Montagem e cálculo de pedidos; consulta de pedidos e privacidade. |
| Fernanda | Cupons; fora de escopo. |
| Gustavo | Conversas de vários turnos; adversarial. |

Essa divisão corresponde à exploração inicial. As demais tarefas serão assumidas no [quadro de execução](https://trello.com/b/M4EHkt4l). Dúvidas e decisões ficam no [quadro de planejamento](https://trello.com/b/PdUBDmTM), com o resumo das decisões em [docs/decisoes.md](docs/decisoes.md).

## Como começar

1. Ler a base oficial e a massa de teste antes de definir as expectativas.
2. Preparar a coleção Postman e configurar a chave somente no ambiente local.
3. Registrar cada caso com ID, categoria, entrada/turnos, esperado, referência exata, resposta observada e evidência. Guardar também `ferramentas`, `metricas` e `versao` quando disponíveis.
4. Usar uma sessão nova por caso e manter a sessão retornada nos turnos da mesma conversa.
5. Trabalhar em uma branch própria e abrir PR para `main`, vinculando a tarefa e a evidência correspondente.

## Regras da avaliação

- A base oficial e a massa de teste são o oráculo. A base interna da Lia é deliberadamente diferente; as respostas da assistente não definem o gabarito.
- Não realizar testes de carga/estresse. Coordenar no máximo quatro chamadas simultâneas no total da equipe.
- Timeout deliberado do ambiente é inconclusivo: registrar a limitação sem contar como defeito ou aprovação da Lia.
- Usar somente a API fornecida e dados fictícios. A equipe não tem acesso à AWS que hospeda a Lia.
- Nunca publicar chaves, credenciais ou arquivos de configuração com segredos. Revisar também exportações do Postman e evidências.
- Recursos próprios da AWS/modelos são opcionais, com orçamento de US$ 20 por integrante.

## Entregas previstas

- Golden dataset com pelo menos 40 casos nas oito categorias e cinco pares metamórficos.
- Suíte automatizada, incluindo verificações de ferramentas em pedidos e cupons.
- Registro de pelo menos 30 tentativas de red teaming em cinco categorias.
- Prompt corrigido e comparação da mesma suíte com pelo menos três execuções por caso em cada versão, incluindo aprovação, latência e tokens.
- Repositório reproduzível, decisões registradas, parecer Go/No-Go de até oito páginas e apresentação de 15–20 minutos com os quatro integrantes.

As instruções de instalação e execução serão adicionadas quando a ferramenta de automação for definida. O prazo exato e o responsável pelo envio único na AI/R Learning precisam ser confirmados pela equipe.
