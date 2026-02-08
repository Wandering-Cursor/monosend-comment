import asyncio
from telegram.ext import (
    Application,
    InlineQueryHandler,
)

from src.settings import BOT_TOKEN, LISTEN_IP, LISTEN_PORT, WEBHOOK_BASE_URL, SECRET, USE_POOLING
from src.operations import process


def prepare_application():
    application = (
        Application.builder()
        .token(
            BOT_TOKEN,
        )
        .build()
    )

    application.add_handler(
        InlineQueryHandler(
            process.query_callback,
        ),
    )

    return application


async def run_webhook():
    application = prepare_application()

    application.run_webhook(
        listen=LISTEN_IP,
        port=LISTEN_PORT,
        webhook_url=f"{WEBHOOK_BASE_URL}/{BOT_TOKEN}/{SECRET}",
        drop_pending_updates=True,
    )


def run_pooling():
    application = prepare_application()
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    if USE_POOLING:
        run_pooling()
    else:
        asyncio.run(run_webhook())
