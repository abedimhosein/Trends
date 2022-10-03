from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Hashtag(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='hashtags')

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.PROTECT, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'hashtag')]
        ordering = ['created_at']


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.PROTECT, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'hashtag')]
        ordering = ['created_at']


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.PROTECT, related_name='reports')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'hashtag')]
        ordering = ['created_at']
