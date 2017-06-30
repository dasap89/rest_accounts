from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re

class CustomPasswordValidator(object):
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"

        params = {
            'min_length': self.min_length,
            'special_characters': special_characters.replace('\\', '')
        }
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _('Password must contain at least %(min_length)d digit.'),
                code='password_needs_digits',
                params={'min_length': self.min_length},
            )
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _('Password must contain at least %(min_length)d letter.'),
                code="password_needs_alhpas",
                params = params
            )
        if not any(char in special_characters for char in password):
            raise ValidationError(
                _('Password must contain at least %(min_length)d special '
                  'character. List of such characters %(special_characters)s.'),
                code='password_needs_special_chars',
                params=params
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters."
            % {'min_length': self.min_length}
        )
