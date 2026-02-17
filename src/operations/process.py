import re
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext

from src.operations.storage import add_link, get_links
from src.schemas.link import Link
from src.settings import S3_BUCKET_NAME
from src.translations.translate import translate
from src.translations.en import Translation
import urllib.parse


async def reply_to_empty_query(update: Update) -> None:
    if not update.inline_query:
        raise RuntimeError("Expected an inline query update")

    all_items: list[InlineQueryResultArticle] = []

    if S3_BUCKET_NAME:
        links = get_links(update.inline_query.from_user.id)

        for index, link in enumerate(links):
            all_items.append(
                InlineQueryResultArticle(
                    id=f"saved_{index}",
                    title=translate(
                        Translation.LIST_LINK_TITLE,
                        update=update,
                        index=index + 1,
                        title=link["title"],
                    ),
                    description=translate(
                        Translation.LIST_LINK_DESCRIPTION,
                        update=update,
                        index=index + 1,
                    ),
                    input_message_content=InputTextMessageContent(
                        translate(
                            Translation.LIST_LINK_MESSAGE,
                            update=update,
                            index=index + 1,
                            title=link["title"],
                            url=link["url"],
                        ),
                    ),
                ),
            )

    default_items = [
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
    ]

    all_items.extend(default_items)

    await update.inline_query.answer(
        results=all_items,
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


async def reply_to_saved_link_query(update: Update, match: re.Match) -> None:
    if not update.inline_query:
        raise RuntimeError("Expected an inline query update")

    index = int(match.group("index")) - 1

    links = get_links(update.inline_query.from_user.id)

    if index < 0 or index >= len(links):
        return await reply_to_invalid_query(update)

    link = links[index]

    new_link_params = {
        "account": urllib.parse.urlparse(link["url"]).path,
        "query": {
            "a": match.group("amount"),
            "t": match.group("comment"),
        },
    }
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


async def query_callback(update: Update, context: CallbackContext) -> None:
    if not update.inline_query:
        return

    query = update.inline_query.query

    if not query:
        return await reply_to_empty_query(update)

    save_link_match = re.match(
        r"^(?P<index>\d+)\s(?P<amount>\d+[.,]?\d+)(\s(?P<comment>[^.\n]+))?\.?\n?",
        query,
    )

    if save_link_match:
        return await reply_to_saved_link_query(update, save_link_match)

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


async def add_command_callback(update: Update, context: CallbackContext) -> None:
    if not update.message or not update.message.text or not update.message.from_user:
        return

    if not S3_BUCKET_NAME:
        await update.message.reply_text(
            translate(
                Translation.ADD_COMMAND_S3_BUCKET_NOT_CONFIGURED_MESSAGE,
                update=update,
            ),
        )
        return

    link_match = re.match(
        r"^/add\s+(?P<link>send\.monobank\.ua\/\S+)$",
        update.message.text,
        flags=re.IGNORECASE,
    )

    title_match = re.match(
        r"^/add\s+(?P<link>send\.monobank\.ua\/\S+)\s+(?P<title>.+)$",
        update.message.text,
        flags=re.IGNORECASE,
    )

    if not link_match or not link_match.group("link"):
        await update.message.reply_text(
            translate(
                Translation.ADD_COMMAND_INVALID_MESSAGE,
                update=update,
            ),
        )
        return

    link = link_match.group("link")
    parsed_link = urllib.parse.urlparse(link)

    title = None

    if title_match:
        title = title_match.group("title")

    if title is None:
        title = translate(
            Translation.ADD_LINK_TITLE_FORMAT,
            update=update,
            path=parsed_link.path,
        )

    link_object = Link(
        title=title,
        url=link,
        created_at=int(update.message.date.timestamp()),
    )

    add_link(
        chat_id=update.message.from_user.id,
        link=link_object,
    )

    await update.message.reply_text(
        translate(
            Translation.ADD_COMMAND_MESSAGE,
            update=update,
            link=link_object,
        ),
    )
