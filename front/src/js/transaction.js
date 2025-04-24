const API_URL = "http://localhost:8000";



export async function getTransacoesPorUsuario(idUsuario) {
    try {
      const response = await fetch(`${API_URL}/pagamento?id_usuario=${idUsuario}`);
      if (!response.ok) {
        if (response.status == 404){
          return []
        }
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

  const res = await fetch(`${API_URL}/registrar_pagamento`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novaTransacao)
  });

  if (!res.ok) throw new Error("Erro ao adicionar transação.");
}

