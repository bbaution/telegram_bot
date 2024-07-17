# telegram_bot
Este proyecto es una solución personalizada de automatización para un cliente específico. Consiste en un bot de Telegram y un servidor web que trabajan juntos para gestionar datos de patentes y deudas, facilitando la administración de estos datos a través de una hoja de cálculo en Google Sheets.

Características
Bot de Telegram: Permite a los usuarios autorizados enviar información sobre patentes, deudas y observaciones. El bot valida los datos y los envía a un servidor para su procesamiento.
Servidor Web: Recibe datos desde el bot, los valida, los almacena en una hoja de cálculo de Google Sheets y envía una confirmación al usuario a través de Telegram.
Google Sheets: Actúa como base de datos para almacenar la información recibida del bot, permitiendo una gestión fácil y accesible de los datos.
Funcionalidades del Bot
/caba y /prov: Comandos para enviar información sobre patentes y deudas. Los datos enviados son validados y registrados en una hoja de cálculo de Google Sheets.
/start: Mensaje de bienvenida para los usuarios autorizados.
/add: Permite al administrador agregar nuevos usuarios a la lista blanca del bot.
/delete: Permite al administrador eliminar usuarios de la lista blanca.
/echo: Comando de prueba que responde con el ID de usuario.
Cómo Funciona
El Usuario envía un mensaje al bot con el comando /caba o /prov seguido de los datos de patente, deuda y observaciones.
El Bot valida el comando y los datos, y luego envía esta información al Servidor Web.
El Servidor Web procesa los datos, los almacena en Google Sheets, y envía una confirmación al usuario a través del bot de Telegram.
Tecnologías Utilizadas
Node.js: Plataforma para ejecutar el servidor web.
Express: Framework para construir el servidor web.
Google Sheets API: API para interactuar con Google Sheets.
Telegram API: API para interactuar con Telegram y manejar comandos del bot.
Python: Lenguaje de programación para desarrollar el bot de Telegram.
