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
      `CREATE TABLE IF NOT EXISTS logs (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          temp INTEGER NOT NULL,
          date TEXT NOT NULL
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

app.post(`/log/:temp`, (req, res) => {
  const { temp } = req.body;
  const query = `INSERT INTO logs (temp, date) VALUES (?, ?)`;
  const date = new Date();
  const formateedDate = date.toISOString();
  const params = [temp, formateedDate];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Log cadastrado com sucesso!");
    }
  });
});

app.get(`/log`, (req, res) => {
  const query = `SELECT * FROM logs ORDER BY id DESC LIMIT 1`;
  db.get(query, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

const port = 3030;
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
