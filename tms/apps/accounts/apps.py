from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tms.apps.accounts"

    def ready(self):
        import tms.apps.accounts.signals
