from enum import StrEnum


class Translation(StrEnum):
    EMPTY_QUERY_TITLE = "Надайте посилання з send.monobank.ua"
    EMPTY_QUERY_MESSAGE = "Ваше повідомлення порожнє. Будь ласка, надайте посилання з send.monobank.ua."

    EMPTY_QUERY_ARGUMENT_EXAMPLE_TITLE = "З використанням аргументів: Посилання, Сума, Коментар"
    EMPTY_QUERY_ARGUMENT_EXAMPLE_MESSAGE = "Ви можете ввести: send.monobank.ua/test 100 Поїздка на каруселі"

    EMPTY_QUERY_IN_TEXT_EXAMPLE_TITLE = "Посилання розкидане в тексті"
    EMPTY_QUERY_IN_TEXT_EXAMPLE_MESSAGE = "Якщо посилання розкидане в тексті, ми одне речення після посилання як опис."

    INVALID_QUERY_TITLE = "Невірний запит"
    INVALID_QUERY_MESSAGE = "Ваше повідомлення має містити send.monobank.ua, щоб використовувати цього бота."

    CORRECT_QUERY_TITLE = "Оновлено посилання"
    CORRECT_QUERY_DESCRIPTION = "Посилання містить:\nСума: {amount}\nКоментар: {comment}"
    CORRECT_QUERY_MESSAGE = "Запит на оплату:\nСума: {amount}\nКоментар: {comment}\n\nПосилання: {link}"

    ITEM_UNSPECIFIED = "Не вказано"
