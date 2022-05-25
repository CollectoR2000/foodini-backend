#! /usr/bin/env python3
from core import settings


def healtcheck_api() -> None:
    import requests

    result = requests.get(f"http://localhost:{settings.UVICORN_PORT}{settings.API_HEALTH_PREFIX}/running", timeout=15)
    result.raise_for_status()


if __name__ == "__main__":
    # Run API healthcheck.
    healtcheck_api()
