const API_URL = "http://localhost:8000/user";

export async function getUserById(id) {
  try {
    const response = await fetch(`${API_URL}?id=${id}`);
    if (response.status == 404) return []
    if (!response.ok) throw new Error("Usuário não encontrado");

    const usuario = await response.json();
    return usuario;
  } catch (error) {
    console.log("Erro ao obter ID do usuário:", error)
    console.error("Erro ao obter ID do usuário:", error);
    return null;
  }
}