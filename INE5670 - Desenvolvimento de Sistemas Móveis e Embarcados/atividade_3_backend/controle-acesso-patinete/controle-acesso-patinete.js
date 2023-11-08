const express = require("express");
const app = express();

const bodyParser = require("body-parser");
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get(`/controle/bloqueio`, (req, res) => {
  res.status(200).send("Patinete Bloqueado!");
  console.log("Patinete Desbloqueado!");
});

app.get(`/controle/desbloqueio`, (req, res) => {
  res.status(200).send("Patinete Desbloqueado!");
  console.log("Patinete Desbloqueado!");
});

port = 3030;
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
