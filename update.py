from __future__ import annotations

import os
from logging import (
    INFO,
    ERROR,
    Formatter,
    LogRecord,
    FileHandler,
    StreamHandler,
    getLogger,
    basicConfig,
)
from pathlib import Path
from datetime import datetime
from subprocess import CompletedProcess, run

from pytz import timezone


class CustomFormatter(Formatter):
    def formatTime(  # noqa: N802
        self: CustomFormatter,
        record: LogRecord,
        datefmt: str | None,
    ) -> str:
        dt: datetime = datetime.fromtimestamp(
            record.created,
            tz=timezone("Asia/Dhaka"),
        )
        return dt.strftime(datefmt)

    def format(self: CustomFormatter, record: LogRecord) -> str:
        return super().format(record).replace(record.levelname, record.levelname[:1])


formatter: Formatter = CustomFormatter(
    "[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
)

file_handler: FileHandler = FileHandler("log.txt")
file_handler.setFormatter(formatter)

stream_handler: StreamHandler = StreamHandler()
stream_handler.setFormatter(formatter)

basicConfig(handlers=[file_handler, stream_handler], level=INFO)

LOGGER = getLogger(__name__)
getLogger("pyrogram").setLevel(ERROR)
getLogger("pymongo").setLevel(ERROR)
getLogger("httpx").setLevel(ERROR)

# Fetch repository and branch from environment variables
UPSTREAM_REPO: str = os.environ["UPSTREAM_REPO"]
UPSTREAM_BRANCH: str = os.environ["UPSTREAM_BRANCH"]

if Path(".git").exists():
    run(["rm", "-rf", ".git"], check=False)

update: CompletedProcess = run(
    [
        f"git init -q \
            && git config --global user.email yesiamshojib@gmail.com \
            && git config --global user.name 5hojib \
            && git add . \
            && git commit -sm update -q \
            && git remote add origin {UPSTREAM_REPO} \
            && git fetch origin -q \
            && git reset --hard origin/{UPSTREAM_BRANCH} -q",
    ],
    shell=True,
    check=False,
)

if update.returncode == 0:
    LOGGER.info("Repository updated successfully.")
else:
    LOGGER.error("Failed to update the repository.")