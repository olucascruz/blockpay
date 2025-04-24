const API_URL = "http://localhost:8000/";

// export async function getUsuariosSalvos() {
//   const res = await fetch(API_URL);
//   if (!res.ok) throw new Error("Erro ao buscar usuários");
//   return await res.json();
// }

export async function cadastrarUsuario(nome, email, senha, confirmarSenha) {
  if (senha !== confirmarSenha) {
    throw new Error("As senhas não coincidem.");
  }

  const novoUsuario = { nome, email, senha };

  const res = await fetch(API_URL+"register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novoUsuario)
  });

  if (!res.ok) throw new Error("Erro ao cadastrar usuário");
}

// Login
export async function autenticarUsuario(email, senha) {
  const novoUsuario = { email, senha };
  const res = await fetch(API_URL+"login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novoUsuario)
  });


  const usuario = await res.json()
  if (!res.ok) {
    throw new Error("Email ou senha inválidos.");
  }

  localStorage.setItem("usuarioLogado", JSON.stringify(usuario));
}

export function getUsuarioLogado() {
  const dados = localStorage.getItem("usuarioLogado");
  return dados ? JSON.parse(dados) : null;
}

export function logoutUsuario() {
  localStorage.removeItem("usuarioLogado");
}

export function verificarAutenticacao() {
    const usuario = getUsuarioLogado();
    if (!usuario) {
      alert("Você precisa estar logado para acessar essa página.");
      window.location.href = "/front/src/html/login.html";
    }
  }
