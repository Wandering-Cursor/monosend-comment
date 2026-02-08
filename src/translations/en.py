from enum import StrEnum


class Translation(StrEnum):
    EMPTY_QUERY_TITLE = "Supply a link with send.monobank.ua"
    EMPTY_QUERY_MESSAGE = "Your message is empty. Please supply a link with send.monobank.ua in it."

    EMPTY_QUERY_ARGUMENT_EXAMPLE_TITLE = "Use arguments: Link, Amount, Comment"
    EMPTY_QUERY_ARGUMENT_EXAMPLE_MESSAGE = "You can enter: send.monobank.ua/test 100 Carousel ride"

    EMPTY_QUERY_IN_TEXT_EXAMPLE_TITLE = "Link scattered in the text"
    EMPTY_QUERY_IN_TEXT_EXAMPLE_MESSAGE = "If a link is otherwise scattered in the text, we'll use the following text (one sentence after the link) as the description."  # noqa: E501

    INVALID_QUERY_TITLE = "Invalid query"
    INVALID_QUERY_MESSAGE = "Your message has to contain send.monobank.ua, to use this bot."

    CORRECT_QUERY_TITLE = "Updated the link"
    CORRECT_QUERY_DESCRIPTION = "Link contains:\nAmount: {amount}\nComment: {comment}"
    CORRECT_QUERY_MESSAGE = "Payment request for:\nAmount: {amount}\nComment: {comment}\n\nLink: {link}"

    ITEM_UNSPECIFIED = "Unspecified"
