from django.apps import AppConfig


class MainPageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_page'

    def ready(self):
        from .tasks import admin_email_message
        from .scheduler import main_page_scheduler
        print('started')
        main_page_scheduler.add_job(
            id='app runtime',
            func=admin_email_message,
            trigger='interval',
            seconds=604800,
        )
        main_page_scheduler.start()
    #     import main_page.signals
