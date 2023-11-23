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
      `CREATE TABLE IF NOT EXTISTS config (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      tempMin INTEGER NOT NULL,
      tempMax INTEGER NOT NULL,
      date TEXT NOT NULL
    )`,
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

app.post(`/config/:tempMIN,:tempMAX`, (req, res) => {
  const { tempMin, tempMax } = req.body;
  const query = `INSERT INTO config (tempMin, tempMax, date) VALUES (?, ?, ?)`;
  const date = new Date();
  const formateedDate = date.toISOString();
  const params = [tempMin, tempMax, formateedDate];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Configuração cadastrada com sucesso!");
    }
  });
});

app.get(`/config`, (req, res) => {
  const query = `SELECT * FROM config ORDER BY id DESC LIMIT 1`;
  db.get(query, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

const port = 3020;
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
