import logging


class DebugFilter(logging.Filter):
    def filter(self, record):
        from django.conf import settings
        return settings.DEBUG


class ProductionFilter(logging.Filter):
    def filter(self, record):
        from django.conf import settings
        return not settings.DEBUG


class SecurityFilter(logging.Filter):
    def filter(self, record):
        return record.name == 'django.security'


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR


class RequestServerFilter(logging.Filter):
    def filter(self, record):
        return record.name in ['django.request', 'django.server']


class DatabaseTemplateFilter(logging.Filter):
    def filter(self, record):
        return record.name in ['django.template', 'django.db.backends']
