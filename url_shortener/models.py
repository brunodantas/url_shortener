import re
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

URL_CODE_LENGTH = 5

class Url(models.Model):
    """URL entry."""
    original = models.URLField(max_length=1000)
    code = models.CharField(max_length=URL_CODE_LENGTH, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()

    class Meta:
        ordering = ['-created']

    @classmethod
    def generate_code(cls):
        """Generate a random valid unique short URL code
        from a random sampling with replacement.

        Returns:
            code (str): code of the short URL.
        """
        gen = True
        while gen:                                  # ensure unused url code
            try:
                code = ''.join(random.choices(          # random alphanumeric string
                    string.ascii_letters + string.digits, k=URL_CODE_LENGTH))
                Url.objects.get(pk=code)
                gen = True
            except ObjectDoesNotExist:
                gen = False
        return code

    @classmethod
    def validate_code(cls, url_code):
        """Check whether a given code is formatted correctly.

        Parameters:
            url_code (str)

        Returns:
            valid (bool): validity of the formatting.
        """
        code_format = '^[\w]{{{}}}$'.format(URL_CODE_LENGTH)
        match = re.fullmatch(code_format, url_code)
        return match is not None

    @classmethod
    def generate_expiration_date(cls):
        """Generate a default expiration date.

        Returns:
            expiration_date (datetime): default expiration date"""
        return timezone.now() + timedelta(days=7)

    @classmethod
    def validate_expiration_date(cls, expiration_date):
        """Check whether an expiration date is a future date.

        Parameters:
            expiration_date (datetime)

        Returns:
            valid (bool)
        """
        return expiration_date - timezone.now() > timedelta(seconds=10)
