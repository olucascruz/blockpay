import { getUsuarioLogado } from "./authentication.js";

const API_URL = "http://localhost:3001/grupos";

// Buscar grupo do usuário
export async function getGrupoDoUsuario(idCriador) {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error("Erro ao buscar grupos.");
    const grupos = await res.json();
    return grupos.find(g => g.participantes.includes(idCriador));
  } catch (error) {
    console.error("Erro ao buscar grupo do usuário:", error);
    throw error;
  }
}

// Criar novo grupo
export async function criarGrupo(idCriador) {
  const novoGrupo = {
    id: crypto.randomUUID(),
    criador: idCriador,
    participantes: [idCriador]
  };

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novoGrupo)
  });

  if (!res.ok) throw new Error("Erro ao criar grupo.");
}

// Entrar em grupo existente
export async function entrarNoGrupo(idGrupo, idCriador) {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error("Erro ao buscar grupos.");
  const grupos = await res.json();
  const grupo = grupos.find(g => g.id === idGrupo);

  if (!grupo) throw new Error("Grupo não encontrado.");
  if (grupo.participantes.includes(idCriador)) throw new Error("Você já está neste grupo.");

  grupo.participantes.push(idCriador);

  const resUpdate = await fetch(`${API_URL}/${grupo.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(grupo)
  });

  if (!resUpdate.ok) throw new Error("Erro ao entrar no grupo.");
}

// Lógica da Home para exibir info do grupo e ações
document.addEventListener("DOMContentLoaded", async () => {
  const usuario = getUsuarioLogado();
  const infoGrupo = document.getElementById("info-grupo");
  const grupoActions = document.getElementById("grupo-actions");
  const btnVerTransacoesGrupo = document.getElementById("btn-ver-transacoes-grupo");

  if (!usuario) {
    infoGrupo.textContent = "Usuário não autenticado.";
    return;
  }

  try {
    const grupo = await getGrupoDoUsuario(usuario.id);

    if (grupo && grupo.id) {
      infoGrupo.innerHTML = `
        <p>Você já está em um grupo.</p>
        <p><strong>ID do grupo:</strong> ${grupo.id}</p>
      `;
      grupoActions.style.display = "none";

      // Mostrar botão de ver transações do grupo
      btnVerTransacoesGrupo.style.display = "inline-block";
      btnVerTransacoesGrupo.addEventListener("click", () => {
        location.href = "group-transactions.html";
      });

    } else {
      infoGrupo.textContent = "Você não está em nenhum grupo.";
      grupoActions.style.display = "block";

      // Criar grupo
      document.getElementById("btn-criar-grupo").addEventListener("click", async () => {
        try {
          await criarGrupo(usuario.id);
          alert("Grupo criado com sucesso!");
          location.reload();
        } catch (error) {
          alert("Erro ao criar grupo: " + error.message);
        }
      });

      // Abrir pop-up de entrar em grupo
      document.getElementById("btn-entrar-grupo").addEventListener("click", () => {
        document.getElementById("popup-entrar-grupo").style.display = "block";
      });

      // Confirmar entrada no grupo
      document.getElementById("confirmar-entrada").addEventListener("click", async () => {
        const idGrupo = document.getElementById("input-id-grupo").value.trim();
        if (!idGrupo) {
          alert("Por favor, insira um ID de grupo.");
          return;
        }

        try {
          await entrarNoGrupo(idGrupo, usuario.id);
          alert("Você entrou no grupo com sucesso!");
        } catch (error) {
          alert("Erro: " + error.message);
        } finally {
          location.reload();
        }
      });

      // Cancelar pop-up
      document.getElementById("cancelar-popup").addEventListener("click", () => {
        document.getElementById("popup-entrar-grupo").style.display = "none";
      });
    }

  } catch (e) {
    console.error("Erro ao carregar informações do grupo:", e);
    infoGrupo.textContent = "Erro ao carregar grupo.";
  }
});
