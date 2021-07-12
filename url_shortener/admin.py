from django.contrib import admin
from django.apps import apps
from .models import Url

# De-register all models from other apps
for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        if admin.site.is_registered(model):
            admin.site.unregister(model)

class UrlAdmin(admin.ModelAdmin):
    list_display = ('code', 'original', 'created', 'expires')
    list_per_page = 10

admin.site.register(Url, UrlAdmin)
