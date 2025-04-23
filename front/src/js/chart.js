import { getUsuarioLogado } from "./authentication.js";
import { getTransacoesPorUsuario } from "./transaction.js";

document.addEventListener("DOMContentLoaded", async () => {
  const spanNome = document.getElementById("nome-usuario");
  const spanEmail = document.getElementById("email-usuario");

  const totalGastoElem = document.getElementById("total-gasto");
  const maiorTransacaoElem = document.getElementById("maior-transacao");

  const user = getUsuarioLogado();
  if (!user) return;

  spanNome.textContent = user.nome;
  spanEmail.textContent = user.email;

  const transacoes = await getTransacoesPorUsuario(user.id);

  let totalGasto = 0;
  let maiorTransacao = 0;
  let categorias = {};
  let porData = {};

  if (transacoes.length > 0) {
    // Totais reais
    totalGasto = transacoes.reduce((acc, t) => acc + t.preco, 0);
    maiorTransacao = Math.max(...transacoes.map(t => t.preco));

    // Categorização
    transacoes.forEach(t => {
      categorias[t.tipo] = (categorias[t.tipo] || 0) + t.preco;
    });

    // Agrupamento por data
    transacoes.forEach(t => {
      const data = new Date(t.data).toLocaleDateString();
      porData[data] = (porData[data] || 0) + t.preco;
    });
  } else {
    // Dados zerados
    categorias = { "Sem categoria": 1 };
    porData = { "Sem data": 0 };
  }

  // Mostrar os totais
  totalGastoElem.textContent = totalGasto.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  maiorTransacaoElem.textContent = maiorTransacao.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

  // Pizza - Distribuição por categoria
  new Chart(document.getElementById("pizzaChart"), {
    type: "pie",
    data: {
      labels: Object.keys(categorias),
      datasets: [{
        data: Object.values(categorias),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#9CCC65', '#BA68C8']
      }]
    }
  });

  // Linha - Evolução temporal (por dia)
  new Chart(document.getElementById("linhaChart"), {
    type: "line",
    data: {
      labels: Object.keys(porData),
      datasets: [{
        label: "Gastos por dia",
        data: Object.values(porData),
        fill: false,
        borderColor: 'blue',
        tension: 0.1
      }]
    }
  });

  // Barra - Comparativo entre categorias
  new Chart(document.getElementById("barraChart"), {
    type: "bar",
    data: {
      labels: Object.keys(categorias),
      datasets: [{
        label: "Gasto por categoria",
        data: Object.values(categorias),
        backgroundColor: '#42A5F5'
      }]
    }
  });
});
