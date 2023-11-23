const httpProxy = require("express-http-proxy");
const express = require("express");
const app = express();
var logger = require("morgan");

app.use(logger("dev"));

function selectProxyHost(req) {
  if (req.path.startsWith("/config")) {
    return "http://localhost:3020";
  } else if (req.path.startsWith("/log")) {
    return "http://localhost:3030";
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

const port = 3000;
app.listen(port, () => {
  console.log(`API Gateway rodando na porta ${port}`);
});
