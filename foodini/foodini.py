#! /usr/bin/env python3
from core import settings


def migrate() -> None:
    """ Import Alembic and run database migrations. """
    import random
    import time

    import alembic.config
    time.sleep(round(random.uniform(0.1, 3.0), 1))
    alembic.config.main(argv=("upgrade", "head"))


def uvicorn() -> None:
    """ Import Uvicorn and run the API. """
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=settings.UVICORN_PORT,
        reload=settings.RELOAD,
        use_colors=True,
        log_config="logging.json",
        proxy_headers=True,
        forwarded_allow_ips="*"
    )


if __name__ == "__main__":
    import preboot

    if settings.DEBUG:
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "pip", "install", "debugpy"])

        import debugpy
        debugpy.listen(("0.0.0.0", settings.DEBUG_PORT))

    # Run preboot to check the database connection.
    preboot.check_database_connection()

    # Run database migrations.
    migrate()
    # Start Uvicorn ASGI server.
    uvicorn()
