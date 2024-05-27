const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

let global = ["head"];

const getMovieSummary = (movieName) => {
    return new Promise((resolve, reject) => {
        const scraper = spawn('python', ['scraper.py', movieName]);

        let dataString = '';

        scraper.stdout.on('data', (data) => {
            dataString += data.toString();
        });

        scraper.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
            reject(data.toString());
        });

        scraper.on('close', (code) => {
            if (code !== 0) {
                reject(`Process exited with code ${code}`);
            } else {
                resolve(dataString);
            }
        });
    });
};

const app = express();
app.use(express.json());

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
})

app.get('/movies/:movieName', async (req, res) => {
    try {
        const summary = await getMovieSummary(req.params.movieName);
        res.send(summary);
    } catch (error) {
        res.status(500).send(`Error: ${error}`);
    }
})

app.listen(3000, () => {
    console.log("Server is running at http://localhost:3000");
})

module.exports = app;