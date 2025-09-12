from django.apps import AppConfig


class MainPageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_page'

    def ready(self):
        from .tasks import app_runtime
        from .scheduler import main_page_scheduler
        print('started')
        main_page_scheduler.add_job(
            id='app runtime',
            func=app_runtime,
            trigger='interval',
            seconds=15,
        )
        main_page_scheduler.start()
    #     import main_page.signals
