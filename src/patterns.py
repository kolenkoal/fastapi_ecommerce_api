from re import compile


PHONE_MATCH_PATTERN = compile(
    r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$"
)
LETTER_MATCH_PATTERN = compile(r"^[а-яА-Яa-zA-Z\s\-]+$")

ALPHA_NUMERIC_PATTERN = compile(r"^(?=.*\d)[а-яА-ЯA-Za-z\d]+$")

STREET_NUMBER_PATTERN = compile(r"^[0-9_-]*$")

ALPHA_NUMBERS_PATTERN = compile(r"^[a-zA-Z0-9]+$")

NUMBER_PATTERN = compile(r"^\d+$")


def REMOVE_WHITESPACES(value):
    return compile(r"\s+").sub(" ", value).strip()
