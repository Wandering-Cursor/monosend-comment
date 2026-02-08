"""
This module contains environment variables and settings for the application.

Here we're using os.getenv, to make the runtime minimally bloated for better Lambda performance.
"""

import os

BOT_TOKEN_NULLABLE = os.getenv("BOT_TOKEN", None)

USE_POOLING: bool = os.getenv("USE_POOLING", "false").lower() == "true"
LISTEN_IP: str = os.getenv("LISTEN_IP", "127.0.0.1")
LISTEN_PORT: int = int(os.getenv("LISTEN_PORT", "8443"))

SECRET_NULLABLE = os.getenv("SECRET", None)
WEBHOOK_BASE_URL_NULLABLE = os.getenv("WEBHOOK_BASE_URL", None)

SET_WEBHOOK_ON_STARTUP: bool = os.getenv("SET_WEBHOOK_ON_STARTUP", "true").lower() == "true"

if not BOT_TOKEN_NULLABLE:
    raise ValueError("Gather a Telegram Bot Token from @BotFather and set it as the BOT_TOKEN environment variable.")

BOT_TOKEN: str = BOT_TOKEN_NULLABLE

if not SECRET_NULLABLE:
    raise ValueError("Generate a password-like string and set it as the SECRET environment variable.")

SECRET: str = SECRET_NULLABLE

if not WEBHOOK_BASE_URL_NULLABLE:
    raise ValueError(
        "Set the WEBHOOK_BASE_URL environment variable to the base URL of your webhook endpoint, "
        "e.g. https://yourdomain.com; https://yourdomain.com/webhook;",
    )

WEBHOOK_BASE_URL: str = WEBHOOK_BASE_URL_NULLABLE
