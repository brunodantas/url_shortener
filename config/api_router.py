from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from url_shortener.users.api.views import UserViewSet
from url_shortener.views import CreateUrlViewSet, RetrieveUrlViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("user", UserViewSet)
router.register(r'', CreateUrlViewSet, basename='url')
router.register(r'', RetrieveUrlViewSet, basename='url')

# urlpatterns = [
#     path("url", CreateUrl),
# ]

app_name = "api"
urlpatterns = router.urls
