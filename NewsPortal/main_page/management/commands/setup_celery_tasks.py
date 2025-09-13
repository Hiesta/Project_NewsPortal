from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from celery import current_app


class Command(BaseCommand):
    help = 'Настройка периодических задач Celery'

    def handle(self, *args, **options):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='8',
            day_of_week='1',  # Понедельник
            day_of_month='*',
            month_of_year='*',
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Создано расписание для еженедельной рассылки')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Расписание для еженедельной рассылки уже существует')
            )

        # периодическая задача
        task, created = PeriodicTask.objects.get_or_create(
            name='Weekly News Digest',
            defaults={
                'task': 'main_page.tasks.weekly_news_digest',
                'crontab': schedule,
                'enabled': True,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Создана периодическая задача "Weekly News Digest"')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Периодическая задача "Weekly News Digest" уже существует')
            )

        # активные задачи
        self.stdout.write('\nАктивные периодические задачи:')
        for task in PeriodicTask.objects.filter(enabled=True):
            self.stdout.write(f'- {task.name}: {task.task}')

        self.stdout.write(
            self.style.SUCCESS('\nНастройка завершена! Теперь еженедельная рассылка будет выполняться каждый понедельник в 8:00 утра.')
        )
