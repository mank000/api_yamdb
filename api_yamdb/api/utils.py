import random
import string

from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_ADRESS, EMAIL_HEAD_LETTER


def make_confirmation_code():
    """Возвращает случайную строку из 6 символов."""
    return ''.join(random.choice(
        string.ascii_letters + string.digits) for _ in range(6))


def send_to_email(email, code):
    """Отправляет письмо с кодом подтверждения."""
    return send_mail(
        EMAIL_HEAD_LETTER,
        code,
        EMAIL_ADRESS,
        [email],
        fail_silently=False,
    )
