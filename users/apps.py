from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
