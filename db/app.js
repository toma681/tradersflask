const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
const urlShortener = require('node-url-shortener');


app.use(bodyParser.urlencoded({extended: true}));
app.use(express.urlencoded());
const port = 3000;

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.post('/url', function(req, res) {
    const url = req.body.url;

    urlShortener.short(url, function(err, shortUrl){
        res.send(shortUrl);
    });
});

app.listen(port, () => console.log(`url-shortener listening on port ${port}!`));