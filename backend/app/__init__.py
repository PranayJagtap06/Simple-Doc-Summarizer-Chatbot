import os
import sys
import logging

logger_str: str = """[%(asctime)s %(name)s] %(levelname)s: %(module)s : %(message)s"""

log_dir: str = "chatbotApp_logs"
api_log_path = os.path.join(log_dir, "chatbotApp-logs.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logger_str,
    handlers=[
        logging.FileHandler(api_log_path),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('chatbotAIApp')
