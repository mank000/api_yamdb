from django.core.mail import send_mail
import string
import random


def make_confirmation_code():
    return ''.join(random.choice(
        string.ascii_letters + string.digits) for _ in range(6))


def send_to_email(email, code):
    return send_mail(
        'Письмо с подтверждением регистрации',
        code,
        'kozmin_arti@mail.ru',
        [email],
        fail_silently=False,
    )