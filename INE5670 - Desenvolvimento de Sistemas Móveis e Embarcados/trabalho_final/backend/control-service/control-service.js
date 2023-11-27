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
      `CREATE TABLE IF NOT EXISTS config (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      tempLimit INTEGER NOT NULL,
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

app.post(`/config/`, (req, res) => {
  const { tempLimit } = req.body;
  const query = `INSERT INTO config (tempLimit, date) VALUES (?, ?)`;
  const date = new Date();
  const formateedDate = date.toLocaleString();
  const params = [tempLimit, formateedDate];

  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).json({ success: false, message: err.message });
    } else {
      res.status(200).json({
        success: true,
        message: "Novo limite cadastrado!",
      });
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

app.get(`/config/all`, (req, res) => {
  const query = ` SELECT * FROM config `;
  db.all(query, (err, result) => {
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
