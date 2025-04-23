import { irParaOutraPagina } from './navigation.js';
import {
  cadastrarUsuario,
  autenticarUsuario,
  getUsuarioLogado,
  logoutUsuario
} from './authentication.js';
import { adicionarTransacao, getTransacoesPorUsuario } from "../js/transaction.js";

const botoesERotas = {
  "btn-login": "/front/src/html/login.html",
  "btn-cadastro": "/front/src/html/cadastro.html",
  "btn-home": "/front/src/html/home.html",
  "btn-perfil": "/front/src/html/perfil.html",
  "btn-landpage": "/front/src/html/landpage.html",
  "btn-logout": "/front/src/html/login.html",
  "btn-transactions": "/front/src/html/transactions.html",
  "btn-add-transacao": "/front/src/html/add_transaction.html",
  "btn-ver-transacoes-grupo": "/front/src/html/gtransactions.html",
};

function converterParaBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result); // inclui tipo MIME
    reader.onerror = (error) => reject(error);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // Verificar se o usuário está logado
  const usuarioAtual = getUsuarioLogado();

  Object.entries(botoesERotas).forEach(([id, rota]) => {
    document.getElementById(id)?.addEventListener("click", () => {
      irParaOutraPagina(rota);
    });
  });

  if (usuarioAtual) {
    const nomeSpan = document.getElementById("nome-usuario");
    const emailSpan = document.getElementById("email-usuario");

    if (nomeSpan) nomeSpan.textContent = usuarioAtual.nome;
    if (emailSpan) emailSpan.textContent = usuarioAtual.email;
  }

  // Logout
  document.getElementById("btn-logout")?.addEventListener("click", () => {
    logoutUsuario();
    alert("Logout realizado!");
    irParaOutraPagina("/front/src/html/login.html");
  });

  // Cadastro
  document.getElementById("form-cadastro")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    const confirmar = document.getElementById("confirmar").value;

    try {
      await cadastrarUsuario(nome, email, senha, confirmar);
      alert("Cadastro realizado com sucesso!");
      irParaOutraPagina("/front/src/html/login.html");
    } catch (err) {
      alert(err.message);
    }
  });

  // Login
  document.getElementById("form-login")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
      await autenticarUsuario(email, senha);
      alert("Login realizado!");
      irParaOutraPagina("/front/src/html/home.html");
    } catch (err) {
      alert(err.message);
    }
  });

  // Adicionar transação
  const formTransacao = document.getElementById("form-transacao");
  if (formTransacao) {
    formTransacao.addEventListener("submit", async (e) => {
      e.preventDefault();

      const nome = document.getElementById("nome").value;
      const descricao = document.getElementById("descricao").value;
      const preco = parseFloat(document.getElementById("preco").value);
      const tipo = document.getElementById("tipo").value;
      const data = document.getElementById("data").value;
      const arquivoInput = document.getElementById("arquivo");
      const arquivo = arquivoInput.files[0];

      let base64 = null;
      if (arquivo) {
        base64 = await converterParaBase64(arquivo);
      }

      try {
        await adicionarTransacao({ nome, descricao, preco, tipo, data, base64 });
        alert("Transação adicionada com sucesso!");
        irParaOutraPagina("/front/src/html/transactions.html");
      } catch (err) {
        alert("Erro ao adicionar transação: " + err.message);
      }
    });
  }
});