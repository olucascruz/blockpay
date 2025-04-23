import { getUsuarioLogado } from "./authentication.js";
import { getTransacoesPorUsuario } from "./transaction.js";
import { irParaOutraPagina } from './navigation.js';

export async function carregarTransacoesNaPagina() {
  console.log("teste"); // Debugging
  if (!window.location.pathname.includes("transactions.html")) return;

  const usuario = getUsuarioLogado();
  if (!usuario) {
    alert("Você precisa estar logado para ver as transações.");
    window.location.href = "/front/src/html/login.html";
    return;
  }

  try {
    const transacoes = await getTransacoesPorUsuario(usuario.id);
    const lista = document.getElementById("transacoes-lista");

    console.log("Transações:", transacoes); // Debugging

    if (!lista) {
      console.error("Elemento 'transacoes-lista' não encontrado.");
      return;
    }

    if (transacoes.length === 0) {
      lista.innerHTML = "<li>Nenhuma transação encontrada.</li>";
      return;
    }

    transacoes.forEach(transacao => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${transacao.nome}</strong> - R$ ${parseFloat(transacao.preco).toFixed(2)}<br>
        <em>${transacao.tipo}</em> - ${transacao.descricao}
      `;
      lista.appendChild(li);
    });
  } catch (err) {
    console.error("Erro ao carregar transações:", err);
    alert("Erro ao carregar transações.");
  }
}

const botoesERotas = {
  "btn-home": "/front/src/html/home.html",
  "btn-add-transacao": "/front/src/html/add_transaction.html",
};

document.addEventListener("DOMContentLoaded", () => {

  Object.entries(botoesERotas).forEach(([id, rota]) => {
    document.getElementById(id)?.addEventListener("click", () => {
      irParaOutraPagina(rota);
    });
  });
}
);