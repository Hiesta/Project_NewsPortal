import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')
django.setup()

import logging
logger = logging.getLogger('django')
logger.info("Тест логирования INFO")
logger.warning("Тест логирования WARNING")
logger.error("Тест логирования ERROR")
print("Тест завершен")
