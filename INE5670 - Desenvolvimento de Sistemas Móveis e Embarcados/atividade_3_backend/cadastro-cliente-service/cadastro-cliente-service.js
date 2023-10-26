const express = require("express");
const sqlite3 = require("sqlite3");
const app = express();

const bodyParser = require("body-parser");
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const db = new sqlite3.Database("./database.db", (err) => {
  if (err) {
    console.log(err.message);
  } else {
    console.log("Conectado ao banco de dados com sucesso!");
    db.run(
      `CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf INTEGER NOT NULL UNIQUE,
        email TEXT NOT NULL,
        telefone TEXT NOT NULL
      );`,
      (err) => {
        if (err) {
          console.log(err.message);
        } else {
          console.log("Tabela criada com sucesso!");
        }
      }
    );
  }
});

app.post(`/clientes`, (req, res) => {
  const { nome, cpf, email, telefone } = req.body;
  const query = `INSERT INTO clientes (nome, cpf, email, telefone) VALUES (?, ?, ?, ?)`;
  const params = [nome, cpf, email, telefone];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Cliente cadastrado com sucesso!");
    }
  });
});

app.get(`/clientes`, (req, res) => {
  const query = `SELECT * FROM clientes`;
  db.all(query, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.get("/clientes/:cpf", (req, res) => {
  const query = `SELECT * FROM clientes WHERE cpf = ?`;
  const params = [req.params.cpf];
  db.get(query, params, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.patch("/clientes/:cpf", (req, res) => {
  const query = `UPDATE clientes SET nome = COALESCE(?,nome), email = COALESCE(?,email), telefone = COALESCE(?,telefone) WHERE cpf = ?`;
  const params = [
    req.body.nome,
    req.body.email,
    req.body.telefone,
    req.params.cpf,
  ];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Cliente atualizado com sucesso!");
    }
  });
});

app.delete("/clientes/:cpf", (req, res) => {
  const query = `DELETE FROM clientes WHERE cpf = ?`;
  const params = [req.params.cpf];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Cliente excluído com sucesso!");
    }
  });
});

let port = 8080;
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
