from django.contrib.auth.models import User
from django.db import models


POST_TYPE = [
    ('NEWS', 'Новости'),
    ('ARTICLES', 'Статья')
]


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)

    def update_rating(self):
        # Posts
        post_rating = self.posts.aggregate(models.Sum('rating'))['rating__sum'] or 0
        post_rating *= 3

        # Comments
        comment_rating = Comment.objects.filter(user=self.user).aggregate(models.Sum('rating'))['rating__sum'] or 0

        # Post Comment
        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum'] or 0

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class UserSubs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.category.category_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='UserSubs', related_name='subscribed_categories', blank=True)

    def __str__(self):
        return self.category_name.capitalize()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    news_type = models.CharField(max_length=8, choices=POST_TYPE)
    time_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.TextField(blank=True)
    body = models.TextField(blank=True)
    rating = models.IntegerField(default=1)

    def preview(self):
        return self.body[:124]+'...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.news_type}: {self.header}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=1)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


# ========================= Email test =========================
