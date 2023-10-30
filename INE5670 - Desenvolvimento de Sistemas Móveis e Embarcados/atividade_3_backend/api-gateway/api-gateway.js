const httpProxy = require("express-http-proxy");
const express = require("express");
const app = express();
var logger = require("morgan");

app.use(logger("dev"));

function selectProxyHost(req) {
  if (req.path.startsWith("/clientes")) {
    return "http://localhost:8080";
  } else if (req.path.startsWith("/patinetes")) {
    return "http://localhost:8090";
  } else if (req.path.startsWith("/alugueis")) {
    return "http://localhost:80";
  } else if (req.path.startsWith("/controle")) {
    return "http://localhost:500";
  } else return null;
}

app.use((req, res, next) => {
  var proxyHost = selectProxyHost(req);
  if (proxyHost == null) {
    res.status(404).send("Not found");
  } else {
    httpProxy(proxyHost)(req, res, next);
  }
});

app.listen(3000, () => {
  console.log("API Gateway rodando na porta 3000");
});
