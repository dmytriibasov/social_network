from django.contrib.auth import get_user_model
from django.db import models

from posts.managers import LikesManager


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(to=get_user_model(), through='Like', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Like(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='users')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Likes'

    objects = LikesManager()
