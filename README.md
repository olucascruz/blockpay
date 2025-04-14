# BlockPay
---

## 🧱 Modelos (Entidades) do Sistema

- Estará no Database da Blockchain

---

### 1. 🛍️ **Transação**
```js
{
  id: string,
  id_usuario: string,
  nome: string,
  descricao: string,
  preco: number,
  tipo: String,  # Usaremos para fazer a Lógica dos relatórios
  valida: booleano # Usaremos para fazer a Logica do Delete
}
```

---

### 2. 👤 **Usuário (User)**

- Estará no Database do Servidor de Sinalização

```js
{
  id: string,
  nome: string,
  email: string,
  senha: string,
  dataCadastro: string,
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



- Relatórios de gastos dos usuários.
- Usuário pode ver os seus gastos e os gastos dos outros
- CRUD de
