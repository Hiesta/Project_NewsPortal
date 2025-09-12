from datetime import datetime

start_time = datetime.now()


# Вместо отправки писем - рантайм сервера
def app_runtime():
    print(f'Runtime -- {datetime.now()-start_time}')
