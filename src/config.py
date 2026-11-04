import os

from dotenv import load_dotenv

load_dotenv()

CUENTA = os.getenv("CUENTA")
PASSWORD = os.getenv("PASSWORD")
RECIPIENTS = {
    "to": os.getenv("RECIPIENTS_TO", "").split(","),
    "cc": os.getenv("RECIPIENTS_CC", "").split(","),
    "bcc": os.getenv("RECIPIENTS_BCC", "").split(","),
}
FORCE_SEND = os.getenv("FORCE_SEND", "False").lower() == "true"

# Variable para guardar los registros de envios y descargas
SAVE_DOWNLOAD_DIR_PATH = "downloads"
LOG_DELIVERIES_PATH = "logs/log_deliveries.db"
KEEP_JOB_ACTIVE_PATH = "logs/keep_active.txt"

# Zona horaria para estandarizar fechas y horas en la aplicación
TIMEZONE = os.getenv("TIMEZONE", "America/Mexico_City")
