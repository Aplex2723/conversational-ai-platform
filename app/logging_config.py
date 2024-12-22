from loguru import logger
import sys

# Configure loguru
logger.remove()
logger.add(sys.stderr, format="<green>{time}</green> <level>{message}</level>", level="INFO", backtrace=True, diagnose=True)