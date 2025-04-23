const API_URL = "http://localhost:3001/usuarios";

export async function getUsuariosSalvos() {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error("Erro ao buscar usuários");
  return await res.json();
}

export async function cadastrarUsuario(nome, email, senha, confirmarSenha) {
  if (senha !== confirmarSenha) {
    throw new Error("As senhas não coincidem.");
  }

  const usuarios = await getUsuariosSalvos();
  const usuarioExistente = usuarios.find(u => u.email === email);

  if (usuarioExistente) {
    throw new Error("E-mail já cadastrado.");
  }

  const novoUsuario = { nome, email, senha };

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novoUsuario)
  });

  if (!res.ok) throw new Error("Erro ao cadastrar usuário");
}

// Login
export async function autenticarUsuario(email, senha) {
  const usuarios = await getUsuariosSalvos();
  const usuario = usuarios.find(u => u.email === email && u.senha === senha);

  if (!usuario) {
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
