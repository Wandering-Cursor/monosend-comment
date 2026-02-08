import telegram
from src.translations import ua, en

MAP = {
    "ua": ua.Translation,
    "en": en.Translation,
}


def translate(
    string: "en.Translation",
    update: "telegram.Update | None" = None,
    language_code: str | None = None,
    **kwargs: str,
) -> str:
    """
    Translates a given string to the user's language, if possible.

    If `update` is provided, the user's language will be determined from it. Otherwise, `language_code` will be used.
    If neither are provided or specified - defaults to English.

    If string is not found in the target language, it will fall back to English.
    """
    if update and update.effective_user:
        language_code = update.effective_user.language_code or language_code

    if not language_code:
        language_code = "en"

    language = MAP.get(language_code, en.Translation)

    return getattr(language, string.name, string.value).format(**kwargs)
