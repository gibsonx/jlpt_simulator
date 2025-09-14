import logging
import os
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
load_dotenv()

# Create logs folder
LOG_FOLDER = os.path.join(os.getenv("PROJECT_PATH"),"logs")
os.makedirs(LOG_FOLDER, exist_ok=True)

# Log file path
LOG_FILE = os.path.join(LOG_FOLDER, "jlpt.log")

# Create a rotating file handler (daily rotation)
file_handler = TimedRotatingFileHandler(
    LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=7,  # keep 7 days of logs
    encoding="utf-8"
)
file_handler.suffix = "%Y-%m-%d"

# Console handler
console_handler = logging.StreamHandler()

# Common log format
log_format = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

file_handler.setFormatter(log_format)
console_handler.setFormatter(log_format)

# Create global logger
logger = logging.getLogger("jlpt")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers if re-imported
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)