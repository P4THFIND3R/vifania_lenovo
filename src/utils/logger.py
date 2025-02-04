import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("vifania_lenovo")
logging.getLogger("vifania_lenovo").setLevel(logging.WARNING)
