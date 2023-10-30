const express = require("express");
const sqlite3 = require("sqlite3");
const moment = require("moment");
const app = express();

const axios = require("axios");

const bodyParser = require("body-parser");
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const db = new sqlite3.Database("database.db", (err) => {
  if (err) {
    console.log(err.message);
  } else {
    console.log("Conectado ao banco de dados com sucesso!");
    db.run(
      `CREATE TABLE IF NOT EXISTS alugueis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        serialPatinete INTEGER NOT NULL,
        inicio TEXT NOT NULL,
        fim TEXT NULL
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

app.get(`/alugueis`, (req, res) => {
  const query = `SELECT * FROM alugueis`;
  db.all(query, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.get(`/alugueis/:id`, (req, res) => {
  const query = `SELECT * FROM alugueis WHERE id = ?`;
  const params = [req.params.id];
  db.all(query, params, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.post(`/alugueis/alugar/:serialPatinete`, (req, res) => {
  axios
    .get(`http://localhost:8090/patinetes/${req.params.serialPatinete}`)
    .then((response) => {
      const { data } = response;
      console.log(data);
      if (data.status == "disponível") {
        const startTime = moment().format("YYYY-MM-DD HH:mm:ss");
        const query = `INSERT INTO alugueis (serialPatinete, inicio) VALUES (?, ?)`;
        const params = [req.params.serialPatinete, startTime];
        db.run(query, params, (err) => {
          if (err) {
            console.log(err.message);
            res.status(500).send(err.message);
          } else {
            res.status(200).send("Patinete alugado!");
          }
        });
        axios
          .put(`http://localhost:8090/patinetes/${req.params.serialPatinete}`, {
            status: "alugado",
          })
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.log(error);
          });
        axios.get(`http://localhost:500/controle/bloqueio`).then((response) => {
          res.status(200).send(response.data);
        });
      } else {
        res.status(400).send(`Patinete ${data.serial} não está disponível`);
      }
    });
});

app.post(`/alugueis/devolver/:serialPatinete`, (req, res) => {
  axios
    .get(`http://localhost:8090/patinetes/${req.params.serialPatinete}`)
    .then((response) => {
      const { data } = response;
      console.log(data);
      if (data.status == "alugado") {
        const endTime = moment().format("YYYY-MM-DD HH:mm:ss");
        const query = `UPDATE alugueis SET fim = ? WHERE serialPatinete = ? AND fim IS NULL`;
        const params = [endTime, req.params.serialPatinete];
        db.run(query, params, (err) => {
          if (err) {
            console.log(err.message);
            res.status(500).send(err.message);
          } else {
            res.status(200).send("Patinete devolvido!");
          }
        });
        axios
          .put(`http://localhost:8090/patinetes/${req.params.serialPatinete}`, {
            status: "disponível",
          })
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.log(error);
          });
        axios
          .get(`http://localhost:500/controle/desbloqueio`)
          .then((response) => {
            res.status(200).send(response.data);
          });
      } else {
        res.status(400).send(`Patinete ${data.serial} não está alugado`);
      }
    });
});

port = 80;
app.listen(port, () => {
  console.log("Servidor rodando na porta 80");
});
