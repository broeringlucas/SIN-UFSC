const express = require("express");
const sqlite3 = require("sqlite3");
const app = express();
const math = require("mathjs");

const bodyParser = require("body-parser");
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const db = new sqlite3.Database("database.db", (err) => {
  if (err) {
    console.log(err.message);
  } else {
    console.log("Conectado ao banco de dados com sucesso!");
    db.run(
      `CREATE TABLE IF NOT EXISTS patinetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial INTEGER NOT NULL,
            status TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
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

app.post(`/patinetes`, (req, res) => {
  const { serial, status, latitude, longitude } = req.body;
  const query = `INSERT INTO patinetes (serial, status, latitude, longitude) VALUES (?, ?, ?, ?)`;
  const params = [serial, status, latitude, longitude];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Patinete cadastrado com sucesso!");
    }
  });
});

app.get(`/patinetes`, (req, res) => {
  const query = `SELECT * FROM patinetes`;
  db.all(query, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.get("/patinetes/:serial", (req, res) => {
  const query = `SELECT * FROM patinetes WHERE serial = ?`;
  const params = [req.params.serial];
  db.get(query, params, (err, result) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).json(result);
    }
  });
});

app.patch("/patinetes/:serial", (req, res) => {
  const query = `UPDATE patinetes SET status = COALESCE(?,status), latitude = COALESCE(?,latitude), longitude = COALESCE(?,longitude) WHERE serial = ?`;
  const params = [
    req.body.status,
    req.body.latitude,
    req.body.longitude,
    req.params.serial,
  ];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Patinete atualizado com sucesso!");
    }
  });
});

app.delete("/patinetes/:serial", (req, res) => {
  const query = `DELETE FROM patinetes WHERE serial = ?`;
  const params = [req.params.serial];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Patinete deletado com sucesso!");
    }
  });
});

app.get("/patinetes/proximos/:lat,:long", (req, res) => {
  const { lat, long } = req.params;
  const raioKm = 1;

  function haversine(lat1, lon1, lat2, lon2) {
    const radius = 6371;
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * (Math.PI / 180)) *
        Math.cos(lat2 * (Math.PI / 180)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = radius * c;

    console.log(distance + " km");
    return distance;
  }

  const queryLatLong = `SELECT * FROM patinetes;`;

  db.all(queryLatLong, (err, rows) => {
    if (err) {
      console.error(err.message);
      res.status(500).send(err.message);
    } else {
      const patinetesProximos = [];

      for (const row of rows) {
        const distancia = haversine(lat, long, row.latitude, row.longitude);
        if (distancia <= raioKm && row.status === "disponivel") {
          patinetesProximos.push(row);
        }
      }

      res.status(200).json(patinetesProximos);
    }
  });
});

app.put("/patinetes/:serial", (req, res) => {
  const query = `UPDATE patinetes SET status = ? WHERE serial = ?`;
  const params = [req.body.status, req.params.serial];
  db.run(query, params, (err) => {
    if (err) {
      console.log(err.message);
      res.status(500).send(err.message);
    } else {
      res.status(200).send("Patinete atualizado com sucesso!");
    }
  });
});

let port = 8090;
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
