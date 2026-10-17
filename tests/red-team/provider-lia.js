// Provider do promptfoo para a API da Lia.
//
// Por que existe: a API continua uma conversa pelo campo `sessao`, devolvido a cada
// resposta. O provider HTTP padrão do promptfoo envia uma mensagem por teste, então
// casos de vários turnos precisam deste provider para repassar a sessão entre turnos.
//
// Cada teste informa os turnos em `vars.t1`, `vars.t2`, ... (um por variável).
// Não usamos uma lista: o promptfoo expande listas em vários testes. Todo teste começa em sessão nova.

const fs = require('fs');
const path = require('path');

const URL_LIA = 'https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/';
const TENTATIVAS = 3;
const MAX_TURNOS = 10; // trava: nenhum caso tem mais que 5 turnos
const ESPERA_MS = 5000;

const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

// Junta t1, t2, t3... em ordem. Valida antes de chamar a API para não gastar chamadas com caso mal escrito.
function lerTurnos(vars = {}) {
  const turnos = Object.keys(vars)
    .filter((k) => /^t\d+$/.test(k))
    .sort((a, b) => Number(a.slice(1)) - Number(b.slice(1)))
    .map((k) => vars[k]);
  if (turnos.length === 0) throw new Error('Caso sem turnos: defina vars.t1 (e t2, t3... se houver).');
  if (turnos.length > MAX_TURNOS) throw new Error(`Caso com ${turnos.length} turnos; máximo ${MAX_TURNOS}.`);
  if (turnos.some((t) => typeof t !== 'string' || !t.trim())) throw new Error('Todo turno precisa ser um texto não vazio.');
  return turnos;
}

// 429 (muitas chamadas) e 502 (falha ao chamar a Lia) são temporários segundo o enunciado:
// espera alguns segundos e tenta de novo. Outros erros voltam na hora.
async function enviar(corpo, chave) {
  let ultimoErro;
  for (let i = 1; i <= TENTATIVAS; i++) {
    const resp = await fetch(URL_LIA, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': chave },
      body: JSON.stringify(corpo),
    });
    if (resp.ok) return resp.json();
    ultimoErro = `HTTP ${resp.status}: ${await resp.text()}`;
    if (![429, 502].includes(resp.status)) break;
    await esperar(ESPERA_MS * i);
  }
  throw new Error(ultimoErro);
}

class LiaProvider {
  constructor(options = {}) {
    this.config = options.config || {};
    this.versao = this.config.versao || 'original';
    // Versão corrigida: o prompt vem de um arquivo, para as duas suítes usarem o mesmo texto.
    if (this.config.promptSistemaArquivo) {
      this.promptSistema = fs.readFileSync(path.resolve(__dirname, this.config.promptSistemaArquivo), 'utf-8');
    }
  }

  id() {
    return `lia-${this.versao}`;
  }

  async callApi(prompt, context) {
    const chave = process.env.LIA_API_KEY;
    if (!chave) return { error: 'Variável de ambiente LIA_API_KEY não definida.' };

    let turnos;
    try {
      turnos = lerTurnos(context?.vars);
    } catch (erro) {
      return { error: erro.message };
    }
    const registro = [];
    let sessao;

    try {
      for (const mensagem of turnos) {
        const corpo = { mensagem };
        if (sessao) corpo.sessao = sessao;
        if (this.promptSistema) corpo.prompt_sistema = this.promptSistema;

        const dados = await enviar(corpo, chave);
        sessao = dados.sessao;
        registro.push({
          mensagem,
          resposta: dados.resposta,
          ferramentas: dados.ferramentas ?? null, // null = campo ausente, diferente de lista vazia
          metricas: dados.metricas ?? [],
        });
      }
    } catch (erro) {
      // Erro de transporte é inconclusivo: não conta como falha nem acerto da Lia.
      return { error: `Turno ${registro.length + 1}: ${erro.message}`, metadata: { versao: this.versao, turnos: registro } };
    }

    // Em vários turnos, a saída avaliada junta todos: um vazamento em qualquer turno reprova o ataque.
    const output = registro.length === 1
      ? registro[0].resposta
      : registro.map((t, i) => `T${i + 1}: ${t.resposta}`).join('\n\n');

    const metricas = registro.flatMap((t) => t.metricas);
    const soma = (f) => metricas.reduce((acc, m) => acc + (f(m) || 0), 0);

    return {
      output,
      tokenUsage: {
        prompt: soma((m) => m.usage?.inputTokens),
        completion: soma((m) => m.usage?.outputTokens),
        total: soma((m) => m.usage?.totalTokens),
      },
      metadata: {
        versao: this.versao,
        sessao,
        ferramentas: registro.flatMap((t) => t.ferramentas ?? []),
        latenciaModeloMs: soma((m) => m.metrics?.latencyMs),
        turnos: registro,
      },
    };
  }
}

module.exports = LiaProvider;
