from datetime import datetime, timedelta
from django.core.mail import mail_admins
from .models import Post


# XXX: Рассылка новостей закомментирована
def admin_email_message():
    email_posts = []
    for post in Post.objects.all():
        if datetime.now() - post.time_post < timedelta(weeks=1):
            email_posts.append(post.header[:50])

    if email_posts:
        mail_admins(
            subject='Еженедельная рассылка новостей',
            message='В течении этой недели вышли такие новости, как:\n'+'\n'.join(email_posts)
        )
    else:
        mail_admins(
            subject='У нас для вас плохие новости...',
            message='Дорогие админы, за всю неделю - ни одной новости'
        )

