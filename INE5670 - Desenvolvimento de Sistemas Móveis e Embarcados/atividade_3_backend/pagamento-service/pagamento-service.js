const express = require("express");
const sqlite3 = require("sqlite3");
const moment = require("moment");
const app = express();

const bodyParser = require("body-parser");
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const db = new sqlite3.Database("database.db", (err) => {
  if (err) {
    console.log(err.message);
  } else {
    console.log("Conectado ao banco de dados com sucesso!");
    db.run(
      `CREATE TABLE IF NOT EXISTS registroCartao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                nome serial INTEGER NOT NULL,
                numeroCartao VARCHAR NOT NULL UNIQUE
            );`,
      (err) => {
        if (err) {
          console.log(err.message);
        } else {
          console.log("Tabela registroCartao criada com sucesso!");
        }
      }
    );
    db.run(
      `CREATE TABLE IF NOT EXISTS registroPagamento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numeroCartao valor VARCHAR NOT NULL,
                    serialPatinete INTEGER NOT NULL,
                    status VARCHAR NOT NULL,
                    valor REAL,
                    data TEXT NOT NULL
                );`,
      (err) => {
        if (err) {
          console.log(err.message);
        } else {
          console.log("Tabela registroPagamento criada com sucesso!");
        }
      }
    );
  }
});

app.post(`/pagamento/cartao`, (req, res) => {
  const { cpf, nome, numeroCartao } = req.body;
  const query = `INSERT INTO registroCartao (cpf, nome, numeroCartao) VALUES (?, ?, ?)`;
  const params = [cpf, nome, numeroCartao];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Cartão cadastrado com sucesso!");
    }
  });
});

app.get(`/pagamento/cartao`, (req, res) => {
  const query = `SELECT * FROM registroCartao`;
  db.all(query, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.get("/pagamento/cartao/:numeroCartao", (req, res) => {
  const query = `SELECT * FROM registroCartao WHERE numeroCartao = ?`;
  const params = [req.params.numeroCartao];
  db.get(query, params, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.patch("/pagamento/cartao/:numeroCartao", (req, res) => {
  const query = `UPDATE registroCartao SET cpf = COALESCE(?,cpf), nome = COALESCE(?,nome) WHERE numeroCartao = ?`;
  const params = [req.body.cpf, req.body.nome, req.params.numeroCartao];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Cartão atualizado com sucesso!");
    }
  });
});

app.delete("/pagamento/cartao/:numeroCartao", (req, res) => {
  const query = `DELETE FROM registroCartao WHERE numeroCartao = ?`;
  const params = [req.params.numeroCartao];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Cartão deletado com sucesso!");
    }
  });
});

app.get("/pagamento/pagamento", (req, res) => {
  const query = `SELECT * FROM registroPagamento`;
  db.all(query, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.get("/pagamento/pagamento/:numeroCartao,:serialPatinete", (req, res) => {
  const query = `SELECT * FROM registroPagamento WHERE numeroCartao = ? AND serialPatinete = ? AND status = "Pendente"`;
  const params = [req.params.numeroCartao, req.params.serialPatinete];
  db.get(query, params, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.post("/pagamento/pagamento/inicio", (req, res) => {
  const { numeroCartao, serialPatinete } = req.body;
  const query = `INSERT INTO registroPagamento (numeroCartao, serialPatinete, data, status) VALUES (?, ?, ?, ?)`;
  const data = moment().format("YYYY-MM-DD HH:mm:ss");
  const status = "Pendente";
  const params = [numeroCartao, serialPatinete, data, status];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Pagamento inciado!");
    }
  });
});

app.patch("/pagamento/pagamento/final", (req, res) => {
  const query = `UPDATE registroPagamento SET status = COALESCE(?,status), valor = COALESCE(?,valor) WHERE numeroCartao = ? AND serialPatinete = ? AND status = "Pendente"`;
  const status = "finalizado";
  const params = [
    status,
    req.body.valor,
    req.body.numeroCartao,
    req.body.serialPatinete,
  ];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Pagamento realizado com sucesso!");
    }
  });
});

const port = 5000;
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
