import logging
import os

from rich.logging import RichHandler

from smooth_criminal.core import auto_boost


log_level = os.getenv("LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, log_level, logging.INFO)

logging.basicConfig(
    level=numeric_level,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    force=True,
)

logger = logging.getLogger("SmoothCriminal")

@auto_boost(workers=4)
def double(x):
    return x * 2

if __name__ == "__main__":
    numbers = list(range(10_000))
    result = double(numbers)
    logger.info(f"Processed {len(result)} numbers.")
