import re
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext

from src.translations.translate import translate
from src.translations.en import Translation
import urllib.parse


async def reply_to_empty_query(update: Update) -> None:
    if not update.inline_query:
        raise RuntimeError("Expected an inline query update")

    await update.inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id="empty_query",
                title=translate(
                    Translation.EMPTY_QUERY_TITLE,
                    update=update,
                ),
                description=translate(
                    Translation.EMPTY_QUERY_MESSAGE,
                    update=update,
                ),
                input_message_content=InputTextMessageContent(
                    translate(
                        Translation.EMPTY_QUERY_MESSAGE,
                        update=update,
                    ),
                ),
            ),
            InlineQueryResultArticle(
                id="empty_query_argument_example",
                title=translate(
                    Translation.EMPTY_QUERY_ARGUMENT_EXAMPLE_TITLE,
                    update=update,
                ),
                description=translate(
                    Translation.EMPTY_QUERY_ARGUMENT_EXAMPLE_MESSAGE,
                    update=update,
                ),
                input_message_content=InputTextMessageContent(
                    translate(
                        Translation.EMPTY_QUERY_ARGUMENT_EXAMPLE_MESSAGE,
                        update=update,
                    ),
                ),
            ),
            InlineQueryResultArticle(
                id="empty_query_in_text_example",
                title=translate(
                    Translation.EMPTY_QUERY_IN_TEXT_EXAMPLE_TITLE,
                    update=update,
                ),
                description=translate(
                    Translation.EMPTY_QUERY_IN_TEXT_EXAMPLE_MESSAGE,
                    update=update,
                ),
                input_message_content=InputTextMessageContent(
                    translate(
                        Translation.EMPTY_QUERY_IN_TEXT_EXAMPLE_MESSAGE,
                        update=update,
                    ),
                ),
            ),
        ],
    )


async def reply_to_invalid_query(update: Update) -> None:
    if not update.inline_query:
        raise RuntimeError("Expected an inline query update")

    await update.inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id="invalid_query",
                title=translate(
                    Translation.INVALID_QUERY_TITLE,
                    update=update,
                ),
                description=translate(
                    Translation.INVALID_QUERY_MESSAGE,
                    update=update,
                ),
                input_message_content=InputTextMessageContent(
                    translate(
                        Translation.INVALID_QUERY_MESSAGE,
                        update=update,
                    ),
                ),
            ),
        ],
    )


async def query_callback(update: Update, context: CallbackContext) -> None:
    if not update.inline_query:
        return

    query = update.inline_query.query

    if not query:
        return await reply_to_empty_query(update)

    match = re.match(
        r"^.*(?P<link>send\.monobank\.ua\/\S+).*$",
        query,
        flags=re.IGNORECASE,
    )

    if not match:
        return await reply_to_invalid_query(update)

    link = match.group("link")

    parse = urllib.parse.urlparse(link)

    query_params = urllib.parse.parse_qs(parse.query)

    new_link_params = {
        "account": parse.path,
        "query": {
            "a": None,
            "t": None,
        },
    }

    if "a" in query_params:
        new_link_params["query"]["a"] = query_params["a"][0]

    if "t" in query_params:
        new_link_params["query"]["t"] = query_params["t"][0]

    amount_usecase_match = re.match(
        r"^.*{link}\s(?P<amount>\d+[.,]?\d+)(\s(?P<comment>[^.\n]+))?\.?\n?".format(link=re.escape(link)),
        query,
    )
    if amount_usecase_match:
        new_link_params["query"]["a"] = amount_usecase_match.group("amount")
        new_link_params["query"]["t"] = amount_usecase_match.group("comment")
    else:
        in_text_usecase_match = re.match(
            r"^.*{link}\s(?P<comment>[^.\n]+)\.?\n?".format(link=re.escape(link)),
            query,
        )
        if in_text_usecase_match:
            new_link_params["query"]["t"] = in_text_usecase_match.group("comment")

    for key in new_link_params["query"].copy().keys():
        if new_link_params["query"][key] is None:
            del new_link_params["query"][key]

    new_link = "https://{account}?{query}".format(
        account=new_link_params["account"],
        query=urllib.parse.urlencode(new_link_params["query"]),
    )

    await update.inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id="result",
                title=translate(
                    Translation.CORRECT_QUERY_TITLE,
                    update=update,
                ),
                description=translate(
                    Translation.CORRECT_QUERY_DESCRIPTION,
                    update=update,
                    amount=new_link_params["query"].get(
                        "a",
                        translate(Translation.ITEM_UNSPECIFIED, update=update),
                    ),
                    comment=new_link_params["query"].get(
                        "t",
                        translate(Translation.ITEM_UNSPECIFIED, update=update),
                    ),
                ),
                input_message_content=InputTextMessageContent(
                    translate(
                        Translation.CORRECT_QUERY_MESSAGE,
                        update=update,
                        amount=new_link_params["query"].get(
                            "a",
                            translate(Translation.ITEM_UNSPECIFIED, update=update),
                        ),
                        comment=new_link_params["query"].get(
                            "t",
                            translate(Translation.ITEM_UNSPECIFIED, update=update),
                        ),
                        link=new_link,
                    ),
                ),
            ),
        ],
    )
