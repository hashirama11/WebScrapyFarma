# Configurar el formato de los logs
import logging


LOG_FORMAT = "[%(asctime)s] %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG  # Puede ser INFO, WARNING, ERROR o CRITICAL en producción

# Configurar el logger principal
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),  # Mostrar logs en la consola
        logging.FileHandler("project_logs.log", encoding="utf-8"),  # Guardar logs en un archivo
    ]
)


logger = logging.getLogger(__name__)