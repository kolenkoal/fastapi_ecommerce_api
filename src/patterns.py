from re import compile


PHONE_MATCH_PATTERN = compile(
    r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$"
)
LETTER_MATCH_PATTERN = compile(r"^[а-яА-Яa-zA-Z\-]+$")
