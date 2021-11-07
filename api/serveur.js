const express = require('express');
const app = express();
const fs = require('fs');

let cartes = require('./AuthorizedCard.json');

app.use(express.json());

app.get('/cartes', (req,res) => {
    console.log("[GET] /cartes ...");
    res.status(200).json(cartes);
});

app.get('/carte/:numero', (req,res) => {
    console.log("[GET] /cartes/:nom ... nom: "+req.params.numero);
    const numero = req.params.numero;
    const carte = cartes.find(carte => carte.numero === numero)
    res.status(200).json(carte)
});


app.post('/makeOperation', (req,res) => {    
    console.log("[POST] /makeOperation ... body: "+JSON.stringify(req.body));
    const numero = req.body.numero;
    const montant = parseInt(req.body.montant);
    var carte = cartes.find(carte => carte.numero === numero)
    if(carte.solde >= montant){
        var reponse = {
            status:"valide"
        };
        carte.solde -= montant;
        fs.writeFile('AuthorizedCard.json', JSON.stringify(cartes), (err) => {
            if (err) {
                throw err;
            }
            console.log("JSON sauvegardé");
        });
        console.log("Opération validée")        
    }else{
        reponse = {
            status:"refus"
        };
        console.log("opération refusée")
    }
    res.status(200).json(JSON.stringify(reponse))
});

app.post('/addCarte', (req,res) => {
    console.log("[POST] /addCarte ... body: "+JSON.stringify(req.body));
    cartes.push(req.body);

    fs.writeFile('AuthorizedCard.json', JSON.stringify(cartes), (err) => {
        if (err) {
            throw err;
        }
        console.log("JSON sauvegardé");
    });
    res.status(200).json(cartes)
});

app.post('/addMoney', (req,res) => {
    console.log("[POST] /addMoney ... body: "+JSON.stringify(req.body));
    const numero = req.body.numero;
    const montant = parseInt(req.body.montant);
    var carte = cartes.find(carte => carte.numero === numero)
    
    carte.solde+=montant;

    fs.writeFile('AuthorizedCard.json', JSON.stringify(cartes), (err) => {
        if (err) {
            throw err;
        }
        console.log("JSON sauvegardé");
    });
    res.status(200).json(cartes)
});


const port = 3333;
app.listen(port, () => {
    console.log('Serveur à l\'écoute su r le port '+port)
});