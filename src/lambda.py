import asyncio
import json
from telegram import Update
from src.main import prepare_application


def main(event: dict[str, object], *args) -> dict:
    application = prepare_application()

    asyncio.run(application.initialize())

    update = Update.de_json(
        json.loads(event["body"]),  # type: ignore
        bot=application.bot,
    )

    asyncio.run(application.process_update(update))

    asyncio.run(application.shutdown())

    return {"statusCode": 200, "body": json.dumps("OK")}
