from django.core.exceptions import ValidationError
import re


def slug_validator(value):
    """Валидатор для slug field."""
    regex = r"^[-a-zA-Z0-9_]+$"
    if not re.match(regex, value):
        raise ValidationError("Слаг содержит недопустимый символ")
