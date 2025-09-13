from datetime import datetime, timedelta
from django.core.mail import send_mail, mail_admins
from django.conf import settings
from celery import shared_task
from .models import Post, UserSubs, Category


@shared_task
def send_news_notification(post_id):
    try:
        post = Post.objects.get(id=post_id)
        categories = post.category.all()
        
        subscribers_emails = []
        for category in categories:
            subscribers = category.subscribers.all()
            subscribers_emails.extend([user.email for user in subscribers])
        subscribers_emails = list(set(subscribers_emails))
        
        if subscribers_emails:
            subject = f'Новая {post.get_news_type_display().lower()} в категории: {", ".join([c.category_name for c in categories])}'
            message = f'{post.header}\n\n{post.body[:200]}...\n\nЧитать полностью: http://127.0.0.1:8000/{post.news_type.lower()}/{post.id}/'
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=subscribers_emails,
                fail_silently=False,
            )
            
            print(f'Отправлено уведомлений: {len(subscribers_emails)} для поста {post_id}')
        else:
            print(f'Нет подписчиков для поста {post_id}')
            
    except Post.DoesNotExist:
        print(f'Пост с ID {post_id} не найден')
    except Exception as e:
        print(f'Ошибка при отправке уведомлений для поста {post_id}: {e}')


@shared_task
def weekly_news_digest():
    try:
        week_ago = datetime.now() - timedelta(days=7)
        recent_posts = Post.objects.filter(time_post__gte=week_ago).order_by('-time_post')
        
        if recent_posts.exists():
            categories_with_posts = {}
            for post in recent_posts:
                for category in post.category.all():
                    if category not in categories_with_posts:
                        categories_with_posts[category] = []
                    categories_with_posts[category].append(post)
            
            for category, posts in categories_with_posts.items():
                subscribers = category.subscribers.all()
                
                if subscribers:
                    subject = f'Еженедельная рассылка: {category.category_name}'
                    
                    message_parts = [f'За последнюю неделю в категории "{category.category_name}" вышло {len(posts)} новостей:\n']
                    
                    for post in posts[:5]:  
                        message_parts.append(f'• {post.header}')
                        message_parts.append(f'  {post.body[:100]}...')
                        message_parts.append(f'  Читать: http://127.0.0.1:8000/{post.news_type.lower()}/{post.id}/\n')
                    
                    if len(posts) > 5:
                        message_parts.append(f'И еще {len(posts) - 5} новостей...')
                    
                    message_parts.append('\nСпасибо за подписку!')
                    
                    message = '\n'.join(message_parts)
                    
                    subscriber_emails = [user.email for user in subscribers]
                    
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=subscriber_emails,
                        fail_silently=False,
                    )
                    
                    print(f'Отправлена еженедельная рассылка для категории {category.category_name}: {len(subscriber_emails)} подписчиков')
        
        else:
            mail_admins(
                subject='У нас для вас плохие новости...',
                message='Дорогие админы, за всю неделю - ни одной новости'
            )
            
    except Exception as e:
        print(f'Ошибка при выполнении еженедельной рассылки: {e}')


def app_runtime():
    print(f'Celery worker активен: {datetime.now()}')
    return f'Worker active at {datetime.now()}'
