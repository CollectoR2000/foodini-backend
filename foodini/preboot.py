#! /usr/bin/env python3
import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from database.session import SessionLocal
from utils.logger import Logger

log = Logger("preboot", "bright_black")

wait_period = 5
max_attempts = 60


@retry(
    stop=stop_after_attempt(max_attempts),
    wait=wait_fixed(wait_period),
    before=before_log(log, logging.INFO),
    after=after_log(log, logging.ERROR)
)
def check_database_connection() -> None:
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
    except Exception as error:
        log.error(error)
        raise error


def preboot() -> None:
    log.info("Prebooting the application.")
    check_database_connection()
    log.info("Preboot finished.")


if __name__ == "__main__":
    preboot()
