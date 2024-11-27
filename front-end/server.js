const express = require('express');
const path = require('path');
const app = express();
const port = 5500;

// Middleware para servir arquivos estáticos
app.use(express.static(path.join(__dirname, 'src/pages/editor/Login')));
app.use(express.static(path.join(__dirname, 'src/pages/editor/Dashboard')));
app.use(express.static(path.join(__dirname, 'src/pages/editor/PesquisaProducoes')));

// Rota para servir o arquivo Login.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/pages/editor/Login/Login.html'));
});

app.get('/login', (req  , res) => {
    res.sendFile(path.join(__dirname,'src/pages/editor/Login', 'Login.html'));
});

app.get('/healthcheck', (req, res) => {
    res.send('Server is running');
});

app.listen(port, () => {
    console.log(`Server is running on http://127.0.0.1:${port}`);
});
