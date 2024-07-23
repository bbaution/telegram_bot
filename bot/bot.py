import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# Configuración
TOKEN = '7204444901:AAHd_uT7sK8X_ZH23yxEkhyOB-oEB0c7VJ8'
# URL del servidor Node.js
WEB_APP_URL = 'http://localhost:3000'
WHITELIST_FILE = 'whitelist.txt'
ADMIN_ID = 6758249289

# Leer la lista blanca desde el archivo
def load_whitelist():
    whitelist = {}
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, 'r') as file:
            for line in file:
                try:
                    user_id, name = line.strip().split(',')
                    whitelist[int(user_id)] = name
                except ValueError:
                    continue  # Saltar líneas mal formadas
    return whitelist

# Escribir la lista blanca al archivo
def save_whitelist(whitelist):
    with open(WHITELIST_FILE, 'w') as file:
        for user_id, name in whitelist.items():
            file.write(f"{user_id},{name}\n")

# Cargar la lista blanca al iniciar el bot
whitelist = load_whitelist()

# Asegurarse de que el ADMIN_ID está en la whitelist
if ADMIN_ID not in whitelist:
    whitelist[ADMIN_ID] = 'Admin'
    save_whitelist(whitelist)

# Comandos del bot

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in whitelist:
        await update.message.reply_text('¡Hola! Usa /caba o /prov para enviar datos.')
    else:
        await update.message.reply_text('No tienes permiso para usar este bot.')

async def handle_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if user_id in whitelist:
        command = update.message.text.split()[0][1:]
        params = update.message.text[len(command)+2:].split(', ')

        if len(params) >= 2:  # Se requiere al menos patente y deuda
            sheet_name = 'provincia' if command == 'prov' else 'caba'
            user_name = whitelist[user_id]
            patente = params[0]
            deuda = params[1]
            observaciones = params[2] if len(params) > 2 else ''  # Si hay más de 2 parámetros, el tercero es observaciones

            data = {
                'user_id': user_id,
                'user_name': user_name,
                'chat_id': chat_id,
                'patente': patente,
                'deuda': deuda,
                'observaciones': observaciones,  # Si no se proporciona, se envía una cadena vacía
                'sheet_name': sheet_name
            }

            # Imprimir para depuración
            print(f"Enviando datos: {data}")

            try:
                # Enviar los datos al servidor Node.js
                response = requests.post(WEB_APP_URL, json=data)
                response.raise_for_status()  # Levanta un error si la respuesta tiene un código de estado 4xx o 5xx

                result = response.json().get('result')
                if result == 'success':
                    await update.message.reply_text('Datos enviados correctamente.')
                else:
                    error_message = response.json().get('message', 'Error desconocido.')
                    await update.message.reply_text(f'Error al enviar los datos: {error_message}')
            except requests.exceptions.RequestException as e:
                await update.message.reply_text(f'Error de conexión con el servidor: {e}')
                print(f"Error al enviar datos al servidor: {e}")
        else:
            await update.message.reply_text('Formato incorrecto. Usa: /comando patente, deuda, [observaciones]')
    else:
        await update.message.reply_text('No tienes permiso para usar este bot.')

async def echo(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(f'Tu ID es {user_id}')

async def add_user(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        if len(context.args) == 2:
            try:
                new_user_id = int(context.args[0])
                new_user_name = context.args[1]
                if new_user_id not in whitelist:
                    whitelist[new_user_id] = new_user_name
                    save_whitelist(whitelist)
                    await update.message.reply_text(f'Usuario {new_user_name} agregado a la lista blanca.')
                else:
                    await update.message.reply_text(f'Usuario {new_user_name} ya está en la lista blanca.')
            except ValueError:
                await update.message.reply_text('Uso: /add <ID de usuario> <Nombre>')
        else:
            await update.message.reply_text('Uso: /add <ID de usuario> <Nombre>')
    else:
        await update.message.reply_text('No tienes permiso para usar este comando.')

async def delete_user(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        if len(context.args) == 1:
            try:
                del_user_id = int(context.args[0])
                if del_user_id in whitelist:
                    del_user_name = whitelist.pop(del_user_id)
                    save_whitelist(whitelist)
                    await update.message.reply_text(f'Usuario {del_user_name} eliminado de la lista blanca.')
                else:
                    await update.message.reply_text(f'Usuario con ID {del_user_id} no está en la lista blanca.')
            except ValueError:
                await update.message.reply_text('Uso: /delete <ID de usuario>')
        else:
            await update.message.reply_text('Uso: /delete <ID de usuario>')
    else:
        await update.message.reply_text('No tienes permiso para usar este comando.')

# Función principal para iniciar el bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("caba", handle_command))
    application.add_handler(CommandHandler("prov", handle_command))
    application.add_handler(CommandHandler("echo", echo))  # Controlador temporal para obtener IDs de usuarios
    application.add_handler(CommandHandler("add", add_user))
    application.add_handler(CommandHandler("delete", delete_user))

    application.run_polling()  # Inicia el bot y espera actualizaciones

if __name__ == '__main__':
    main()
