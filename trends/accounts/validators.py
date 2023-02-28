import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def digits_validator(password: str):
    regex = re.compile("[0-9]")

    if not regex.search(password):
        raise ValidationError(
            _("password must include digits"),
            code="password_must_include_digits"
        )


def letters_validator(password: str):
    regex = re.compile("[a-zA-Z]")

    if not regex.search(password):
        raise ValidationError(
            _("password must include letters"),
            code="password_must_include_letters"
        )


def special_char_validator(password: str):
    regex = re.compile("[@_!#$%^&*()<>?/|}{~:]")

    if not regex.search(password):
        raise ValidationError(
            _("password must include special char"),
            code="password_must_include_special_char"
        )
