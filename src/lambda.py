import json
from telegram import Update
from telegram.ext import ContextTypes
from src.operations import process


async def main(event: dict) -> dict:
    body = json.loads(event["body"])
    update = Update.de_json(body)

    await process.query_callback(update, ContextTypes.DEFAULT_TYPE)  # type: ignore

    return {"statusCode": 200, "body": json.dumps("OK")}
