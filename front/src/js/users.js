const API_URL = "http://localhost:3001/usuarios";

export async function getUserById(id) {
  try {
    const response = await fetch(`${API_URL}?id=${id}`);
    if (!response.ok) throw new Error("Usuário não encontrado");
    const usuario = await response.json();
    return usuario;
  } catch (error) {
    console.error("Erro ao obter ID do usuário:", error);
    return null;
  }
}