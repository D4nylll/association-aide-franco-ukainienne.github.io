from django.apps import AppConfig

class CardConfig(AppConfig):
    name = "card"

    def ready(self):
        import card.signals
