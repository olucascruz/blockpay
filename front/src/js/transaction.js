const API_URL = "http://localhost:3001/transacoes";

export async function getIdPorEmail(email) {
  try {
    const response = await fetch(`${API_URL}/usuarios?id=${email}`);
    if (!response.ok) throw new Error("Usuário não encontrado");
    const usuario = await response.json();
    return usuario.id;  // Supondo que o ID esteja no campo 'id'
  } catch (error) {
    console.error("Erro ao obter ID do usuário:", error);
    return null;
  }
}


export async function getTransacoesSalvas() {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error("Erro ao buscar transações.");
  const data = await res.json();
  return data || [];
}

export async function getTransacoesPorUsuario(idUsuario) {
    try {
      console.log("ID do usuário:", idUsuario); // Debugging
      const response = await fetch(`${API_URL}?id_usuario=${idUsuario}`);
      if (!response.ok) {
        console.error("Erro ao buscar transações:", response.status); // Debugging
        throw new Error(`Erro ao buscar transações: ${response.status}`);
      }
  
      const transacoes = await response.json();
      console.log("Transações recebidas:", transacoes); // Debugging
      return transacoes.filter(t => t.valida);
    } catch (error) {
      console.error("Erro em getTransacoesPorUsuario:", error);
      throw error;
    }
}
  

export async function adicionarTransacao({ nome, descricao, preco, tipo, data, base64 }) {
  const usuario = JSON.parse(localStorage.getItem("usuarioLogado"));
  if (!usuario || !usuario.id) {
    throw new Error("Usuário não autenticado.");
  }

  const novaTransacao = {
    id: crypto.randomUUID(),
    id_usuario: usuario.id,
    nome,
    descricao,
    preco: parseFloat(preco),
    tipo,
    data,
    base64: base64 || null,
    valida: true
  };

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novaTransacao)
  });

  if (!res.ok) throw new Error("Erro ao adicionar transação.");
}

