# BlockPay

## 🧱 Modelos (Entidades) do Sistema

- Modelos que estarão no Database da Blockchain

---

### 1. 🛍️ **Transação - Database da Blockchain**
```js
{
  id: string,
  id_usuario: string,
  nome: string,
  descricao: string,
  preco: number,
  tipo: String, {"Alimentação", "Moradia", "Transporte", "Saúde", "Educação", "Lazer", "Vestuário", "Serviços financeiros", "Doações", "Dívidas", "Outros"}
  valida: booleano {"Por padrão True, se a transação for deletada, False"}
}
```
- Estará no Database do Servidor de Sinalização

---

### 2. 👤 **Usuário (User)**


```js
{
  id: string,
  nome: string,
  email: string,
  senha: string,
  peer: string
}
```

### 3. **Server**

```js
{
  ip_id: string,
  ip_peers: List[string]
}
```

# Casos de Uso

- CRUD de Usuario
- CRUD de Transações
- CRUD de Server
- Usuário pode ver os seus gastos e os gastos dos outros
- Relatórios de gastos dos usuários (Dashboard).

