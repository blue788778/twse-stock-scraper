import logging
import os

def setup_logger(log_filename):
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", f"{log_filename}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )