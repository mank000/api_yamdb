from django.core.exceptions import ValidationError

from api_yamdb.const import BLOCKED_WORD


def validate_no_me(value):
    """Проверка на слово 'me'."""
    if BLOCKED_WORD == value:
        raise ValidationError(
            ("Нельзя использовать слово 'me'"),
            params={'value': value},
        )
    return value
