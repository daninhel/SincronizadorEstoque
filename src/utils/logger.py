import logging
import os

# Garante que a pasta de logs exista
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/sincronizador.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("sincronizador")
