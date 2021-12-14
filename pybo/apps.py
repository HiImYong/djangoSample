from django.apps import AppConfig


class PyboConfig(AppConfig):  #config.settings.py의 INSTALLED APP 에 기록됨
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pybo'
