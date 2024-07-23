// server.js
const express = require('express');
const axios = require('axios'); // Usar axios en lugar de node-fetch
const { google } = require('googleapis');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Configurar Express para analizar JSON
app.use(express.json());

const SPREADSHEET_ID = '1ZjKyx_YY9hnZtOP9dYBbb31Xyf6lXjO84KPVpqLtxQg';
const KEY_FILE = './botpatentes-f907bd7ff68c.json';

async function appendToSheet(data, sheetName) {
  const auth = new google.auth.GoogleAuth({
    keyFile: KEY_FILE,
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],
  });

  const sheets = google.sheets({ version: 'v4', auth });
  const request = {
    spreadsheetId: SPREADSHEET_ID,
    range: sheetName,
    valueInputOption: 'USER_ENTERED',
    insertDataOption: 'INSERT_ROWS',
    resource: {
      values: [data],
    },
  };

  try {
    const response = await sheets.spreadsheets.values.append(request);
    console.log('Datos agregados a la hoja:', response.data);
  } catch (error) {
    console.error('Error al agregar datos a la hoja:', error.response ? error.response.data : error.message);
    throw new Error('Error al agregar datos a la hoja');
  }
}

app.post('/', async (req, res) => {
  const { user_id, user_name, patente, deuda, observaciones = '', sheet_name, chat_id } = req.body;

  if (!user_id || !user_name || !patente || !deuda || !sheet_name || !chat_id) {
    console.error('Faltan datos en la solicitud:', req.body);
    return res.status(400).json({ result: 'error', message: 'Faltan datos en la solicitud' });
  }

  try {
    await appendToSheet([user_id, user_name, patente, deuda, observaciones], sheet_name);

    const TELEGRAM_TOKEN = '7204444901:AAHd_uT7sK8X_ZH23yxEkhyOB-oEB0c7VJ8';
    const TELEGRAM_CHAT_ID = chat_id;
    const message = `Datos recibidos:\nUser ID: ${user_id}\nNombre: ${user_name}\nPatente: ${patente}\nDeuda: ${deuda}\nObservaciones: ${observaciones}`;

    const url = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`;
    const payload = {
      chat_id: TELEGRAM_CHAT_ID,
      text: message,
    };

    const response = await axios.post(url, payload);
    console.log('Respuesta de Telegram:', response.data);

    res.status(200).json({ result: 'success' });
  } catch (error) {
    console.error('Error en el servidor:', error.response ? error.response.data : error.message);
    res.status(500).json({ result: 'error', message: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
