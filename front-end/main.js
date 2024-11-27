const { app, BrowserWindow } = require('electron');
const axios = require('axios');
const path = require('path');

let mainWindow;

async function preheatBackend() {
  try {
    const response = await axios.post('http://127.0.0.1:8000/healthcheck/', {}); // Substitua pela URL do seu endpoint de saúde
    console.log('Backend preheated', response.status);
  } catch (error) {
    console.error('Error preheating backend:', error);
  }
}
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    frame: true,
    fullscreenable: true,
    minimizable: true,
    maximizable: true,
    icon: path.join(__dirname, 'src/pages/editor/Login/Imagens/Sapoo 2.png')
  });

  // Carregar o arquivo HTML principal
  mainWindow.loadFile(path.join(__dirname, 'src/pages/editor/Login/Login.html'));

  // Maximize a janela na inicialização
  mainWindow.maximize();

  // Opcional: remover a barra de menus
  mainWindow.setMenuBarVisibility(false);
}

app.whenReady().then(async () => {
  await preheatBackend();
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

