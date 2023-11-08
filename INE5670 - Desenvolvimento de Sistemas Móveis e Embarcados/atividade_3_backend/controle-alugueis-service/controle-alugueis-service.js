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

app.post(`/alugueis/alugar/:serialPatinete,:numeroCartao`, (req, res) => {
  axios
    .get(`http://localhost:8090/patinetes/${req.params.serialPatinete}`)
    .then((response) => {
      const { data } = response;

      if (!data) {
        res.send("Patinete não encontrado!");
      } else if (data.status == "disponível") {
        const startTime = new Date();
        const formattedStartTime = startTime.toLocaleString();
        const query = `INSERT INTO alugueis (serialPatinete, inicio) VALUES (?, ?)`;
        const params = [req.params.serialPatinete, formattedStartTime];
        db.run(query, params, (err) => {
          if (err) {
            console.log(err.message);
            res.status(500).send(err.message);
          } else {
            axios
              .get(
                `http://localhost:5000/pagamento/cartao/${req.params.numeroCartao}`
              )
              .then((response) => {
                const cartaoData = response.data;

                if (!cartaoData) {
                  res.status(400).send("Cartão não encontrado!");
                } else {
                  axios
                    .get(`http://localhost:3030/controle/bloqueio`)
                    .then((response) => {
                      res.status(200).send(response.data);
                    })
                    .catch((error) => {
                      console.log(error);
                    });
                  axios
                    .put(
                      `http://localhost:8090/patinetes/${req.params.serialPatinete}`,
                      {
                        status: "alugado",
                      }
                    )
                    .then((response) => {
                      console.log(response.data);
                    })
                    .catch((error) => {
                      console.log(error);
                    });
                  console.log("Patinete alugado!");
                  axios
                    .post(`http://localhost:5000/pagamento/pagamento/inicio`, {
                      numeroCartao: req.params.numeroCartao,
                      serialPatinete: req.params.serialPatinete,
                    })
                    .then((response) => {
                      console.log(response.data);
                    })
                    .catch((error) => {
                      console.log(error);
                    });
                }
              });
          }
        });
      } else {
        res.status(400).send(`Patinete ${data.serial} não está disponível`);
      }
    });
});

app.post(`/alugueis/devolver/:serialPatinete,:numeroCartao`, (req, res) => {
  axios
    .get(`http://localhost:8090/patinetes/${req.params.serialPatinete}`)
    .then((response) => {
      const { data } = response;

      if (!data) {
        res.send("Patinete não encontrado!");
      } else if (data.status == "alugado") {
        const endTime = new Date();
        const formattedEndTime = endTime.toLocaleString();
        const query = `UPDATE alugueis SET fim = ? WHERE serialPatinete = ? AND fim IS NULL`;
        const params = [formattedEndTime, req.params.serialPatinete];
        const getStartTime = `SELECT inicio FROM alugueis WHERE serialPatinete = ? AND fim = ?`;
        db.run(query, params, (err) => {
          if (err) {
            console.log(err.message);
            res.status(500).send(err.message);
          } else {
            axios
              .get(
                `http://localhost:5000/pagamento/cartao/${req.params.numeroCartao}`
              )
              .then((response) => {
                const cartaoData = response.data;
                console.log(req.params.numeroCartao);
                console.log(req.params.serialPatinete);

                if (!cartaoData) {
                  res.status(400).send("Cartão não encontrado!");
                } else {
                  axios
                    .get(
                      `http://localhost:5000/pagamento/pagamento/${req.params.numeroCartao},${req.params.serialPatinete}`
                    )
                    .then((response) => {
                      console.log(response.data);
                      const pagamentoPatinete = response.data.serialPatinete;

                      if (pagamentoPatinete != req.params.serialPatinete) {
                        res
                          .status(400)
                          .send("Patinente não alugado com esse cartão!");
                      } else {
                        axios
                          .get(`http://localhost:3030/controle/desbloqueio`)
                          .then((response) => {
                            res.status(200).send(response.data);
                          });
                        // res.status(200).send("Patinete devolvido!");
                        console.log("Patinete devolvido!");
                        axios
                          .put(
                            `http://localhost:8090/patinetes/${req.params.serialPatinete}`,
                            {
                              status: "disponível",
                            }
                          )
                          .then((response) => {
                            console.log(response.data);
                          })
                          .catch((error) => {
                            console.log(error);
                          });

                        db.get(
                          getStartTime,
                          [req.params.serialPatinete, formattedEndTime],
                          (err, result) => {
                            const startTime2 = new Date(result.inicio);
                            const endTime2 = new Date(formattedEndTime);
                            const diff = endTime2 - startTime2;
                            const diffMinutes = diff / 60000;

                            const valor = (diffMinutes * 0.5).toFixed(2);

                            axios
                              .patch(
                                `http://localhost:5000/pagamento/pagamento/final`,
                                {
                                  numeroCartao: req.params.numeroCartao,
                                  serialPatinete: req.params.serialPatinete,
                                  valor: valor,
                                }
                              )
                              .catch((error) => {
                                console.log(error);
                              });
                          }
                        );
                      }
                    });
                }
              });
          }
        });
      } else {
        res.status(400).send(`Patinete ${data.serial} não está alugado`);
      }
    });
});

port = 8070;
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
