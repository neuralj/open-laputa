import logging

import typer

from demo_app.config import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

app = typer.Typer(help="demo-app command line application")


@app.command()
def run(name: str = "system") -> None:
    logger.info("Application started")
    print(f"Hello {name}")
