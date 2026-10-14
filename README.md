# *Hackathon* de Encerramento – Desafio 3 (Pop & Doce + *chatbot* Lia)

> **STATUS:** Projeto iniciado.

Projeto de Quality Engineering para avaliar a assistente de vendas Lia, propor melhorias no prompt e fundamentar uma decisão de Go/No-Go com evidências.

## Situação Inicial

O repositório conta com os materiais oficiais (fornecidos pelo nosso instrutor [Jacques de Jesus Figueredo Schmitz Jr.](https://github.com/juniorschmitz)) e a estrutura inicial de trabalho. Os testes exploratórios começarão em breve utilizando o *framework* do Postman. A suíte automatizada, os critérios de aprovação e o método de avaliação ainda serão definidos pela equipe da *Squad* 2, composta por Camille Marcele P. de Araújo, Fernanda B. dos Santos, Gustavo L. Brasileiro e João Gabriel O. Magalhães.

## Arquitetura do Projeto

| CAMINHO | CONTEÚDO |
| :---: | :---: |
| `base-de-conhecimento-oficial/` | Base fornecida pelo orientador; Referência para os próximos passos e escolhas estratégicas de desenvolvimento |
| `massa-de-teste.md` | Pedidos e clientes fictícios fornecidos para os testes |
| `datasets/` | *Golden dataset* e casos metamórficos revisados |
| `tests/` | Código e configurações da suíte automatizada |
| `tests/postman/` | Coleções compartilháveis do Postman, sem credenciais (critério obrigatório) |
| `results/` | Evidências, resultados das execuções e comparação dos *prompts* |
| `results/red-team/` | Registro das tentativas adversariais e as respectivas evidências |
| `prompts/` | Versões do *prompt* de sistema, seguidas das alterações |
| `docs/` | Decisões, tabelas de regras, pareceres e materiais da apresentação |

As pastas de trabalho começam vazias, com `.gitkeep` para serem mantidas no Git.

## Divisão da Exploração Inicial

| Integrante | Categorias |
| :---: | :---: |
| João O. | Catálogo; Alérgenos e restrições |
| Camille P. | Montagem e cálculo de pedidos; Consulta de pedidos e privacidade |
| Fernanda B. | Cupons; Fora de escopo |
| Gustavo L. | Conversas de vários turnos; Adversarial |

Essa divisão corresponde à exploração inicial. As demais tarefas serão assumidas no [quadro de execução](https://trello.com/b/M4EHkt4l). Já, no caso de dúvidas e decisões, estão presentes no [quadro de planejamento](https://trello.com/b/PdUBDmTM), com o resumo das decisões em [docs/decisoes.md](docs/decisoes.md).

---

## Como Começar

1. Ler a base oficial e a massa de teste antes de definir as expectativas;
2. Preparar a coleção Postman e configurar a chave somente no ambiente local;
3. Registrar cada caso com ID, categoria, entrada/turnos, esperado, referência exata, resposta observada e evidência. Guardar também `ferramentas`, `metricas` e `versao` quando disponíveis;
4. Usar uma sessão nova por caso e manter a sessão retornada nos turnos da mesma conversa;
5. Trabalhar em uma branch própria e abrir PR para `main`, vinculando a tarefa e a evidência correspondente;

## Regras de Avaliação

- A base oficial e a massa de teste são o **oráculo**. A base interna da Lia é deliberadamente diferente; as respostas da assistente não definem o gabarito.
- Não realizar testes de carga/estresse. Coordenar no máximo quatro chamadas simultâneas no total da equipe.
- Timeout deliberado do ambiente é inconclusivo: registrar a limitação sem contar como defeito ou aprovação da Lia.
- Usar somente a API fornecida e dados fictícios. A equipe não tem acesso à AWS que hospeda a Lia.
- Nunca publicar chaves, credenciais ou arquivos de configuração com segredos. Revisar também exportações do Postman e evidências.
- Recursos próprios da AWS/modelos são opcionais, com orçamento de US$ 20 por integrante.

## Entregas Previstas

- *Golden dataset* com pelo menos 40 casos nas oito categorias e cinco pares metamórficos.
- Suíte automatizada, incluindo verificações de ferramentas em pedidos e cupons.
- Registro de pelo menos 30 tentativas de *red teaming* em cinco categorias.
- *Prompt* corrigido e comparação da mesma suíte com pelo menos três execuções por caso em cada versão, incluindo aprovação, latência e tokens.
- Repositório reproduzível, decisões registradas, parecer *Go/No-Go* de até oito páginas e apresentação de 15–20 minutos com os quatro integrantes.

As instruções de instalação e execução serão adicionadas quando a ferramenta de automação for definida. O prazo exato e o responsável pelo envio único na AI/R Learning precisam ser confirmados pela equipe.

## Autoria

Este projeto foi desenvolvido pelos membros da *Squad 2*, durante o **ESTÁGIO | AWS AI FDE DRIVEN QUALITY ENGINEERING** na [Compass UOL / AI/R Company](https://aircompany.ai/pt/home/).
