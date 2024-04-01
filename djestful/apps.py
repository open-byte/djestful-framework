from django.apps import AppConfig


class DjestFulConfig(AppConfig):
    name = 'djestful'
    label = 'djestful'
    verbose_name = 'Djestful Framework'

    def ready(self) -> None:
        return super().ready()
