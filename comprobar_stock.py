
import requests
import time
import os
from datetime import datetime
import random
import logging

# Configurar logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL del producto
url = "https://rosaliastore-es.myshopify.com/products/confidencial-lp-firmado"

# Configuración de Telegram (leída desde las variables de entorno)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_alerta_telegram(mensaje):
    """Envía un mensaje a un canal de Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("Error: Las variables de entorno de Telegram no están configuradas.")
        return

    url_telegram = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': mensaje,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url_telegram, data=payload)
        if response.status_code == 200:
            logging.info("Alerta de Telegram enviada con éxito.")
        else:
            logging.error(f"Error al enviar alerta de Telegram: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al conectar con la API de Telegram: {e}")

def actualizar_descripcion_telegram(descripcion):
    """Actualiza la descripción de un canal de Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("Error: Las variables de entorno de Telegram no están configuradas.")
        return

    url_telegram = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setChatDescription"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'description': descripcion
    }
    try:
        response = requests.post(url_telegram, data=payload)
        if response.status_code == 200:
            logging.info("Descripción del canal actualizada con éxito.")
        else:
            logging.error(f"Error al actualizar la descripción del canal: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al conectar con la API de Telegram para actualizar la descripción: {e}")

# Función para comprobar el stock
def comprobar_stock():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.get(url)
        if "Agotado" not in response.text:
            descripcion = f"¡EN STOCK! | Última comprobación: {now}"
            actualizar_descripcion_telegram(descripcion)
            mensaje = f'¡El vinilo firmado de Lux está disponible!\n<a href="{url}">¡Cómpralo ya!</a>'
            logging.info("¡El vinilo firmado de Lux está disponible!")
            enviar_alerta_telegram(mensaje)
            return True
        else:
            descripcion = f"Agotado | Última comprobación: {now}"
            actualizar_descripcion_telegram(descripcion)
            logging.info("El vinilo de Lux sigue agotado.")
            return False
    except requests.exceptions.RequestException as e:
        descripcion = f"Error de conexión | Última comprobación: {now}"
        actualizar_descripcion_telegram(descripcion)
        error_msg = f"Error al conectar con la web: {e}"
        logging.error(error_msg)
        enviar_alerta_telegram(f"ATENCIÓN: El script de comprobación de stock ha fallado. Error: {e}")
        return False

# Comprobar el stock cada 30 minutos
while not comprobar_stock():
    time.sleep(random.randint(178, 499))
