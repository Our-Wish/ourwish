from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'

    def ready(self):
        # drf-spectacular 인증 확장 등록(임포트만으로 등록됨)
        from . import schema  # noqa: F401
