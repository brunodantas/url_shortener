from datetime import date, datetime, timedelta
from rest_framework import status
from rest_framework import mixins
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import pytz
from . import models
from . import serializers


class RetrieveUrlViewSet(ViewSet, mixins.RetrieveModelMixin):
    """Endpoint for retrieving a URL from its short code.

    Parameters:
        code (str): short code

    Returns:
        (str): url redirect, if it exists
    """
    @method_decorator(cache_page(60*60))  # cache for 1 hour
    def retrieve(self, request, pk):
        # code = request['code']
        try:
            url = models.Url.objects.get(pk=pk)
            if url.expires <= timezone.now():  # if expired
                url.delete()
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            content = {'msg': 'URL was not found or expired.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return redirect(url.original)
        # HTTP_302_FOUND

class CreateUrlViewSet(ViewSet, mixins.CreateModelMixin):
    """Endpoint for creating short URLs.

    Parameters:
        original (str): original url
        code (str): desired url code (optional)
        expires (str): desired expiry date (ISO 8601) (optional)

    Returns:
        (str): code of the short URL
        (str): expiration date
    """
    serializer_class = serializers.UrlSerializer

    def create(self, request):
        try:
            original = request.data['original']  # validate URL
            validator = URLValidator()
            validator(original)
        except (KeyError, ValidationError) as e:
            content = {'msg': 'Invalid URL.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        code = request.data['code'] if 'code' in request.data else None
        expires = request.data['expires'] if 'expires' in request.data else None

        if code is not None and len(code) > 0:  # validate code
            valid = models.Url.validate_code(code)
            if not valid:
                content = {'msg': 'The short URL code must be a 5-character alphanumeric string.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            code = models.Url.generate_code()

        if expires is not None and len(expires) > 0:  # validate expires
            try:
                expires_datetime = datetime.fromisoformat(expires).replace(tzinfo=pytz.UTC)
            except Exception as e:
                print(e)
                content = {'msg': 'Invalid ISO 8601 expiry date.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            if not models.Url.validate_expiration_date(expires_datetime):
                content = {'msg': 'The expiration date must be at least 10 seconds in the future.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            expires_datetime = models.Url.generate_expiration_date()

        try:
            url = models.Url.objects.get(pk=code)  # check if url code exists
            if url.expires <= timezone.now():  # if expired
                url.delete()
            else:                              # if not expired
                content = {'msg': 'The short URL code {} already exists.'.format(code)}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:  # unique url code
            pass

        models.Url.objects.create(original=original, code=code, expires=expires_datetime)
        # content = {'url': '{}/{}'.format(Site.objects.get_current().domain, code)}
        content = {'url': '{}/{}'.format("0.0.0.0:8000", code),  # TODO: set a domain
                   'expiration_date': expires_datetime}
        return Response(content, status=status.HTTP_201_CREATED)
