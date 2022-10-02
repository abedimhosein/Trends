from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class Hashtag(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='hashtags')

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.PROTECT, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if Dislike.objects.filter(user=self.user, hashtag=self.hashtag).exists():
            raise ValidationError("You're not allowed to like and dislike for a hashtag at the same time.")
        super(Like, self).clean()

    class Meta:
        unique_together = [('user', 'hashtag')]
        ordering = ['created_at']


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.PROTECT, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if Like.objects.filter(user=self.user, hashtag=self.hashtag).exists():
            raise ValidationError("You're not allowed to like and dislike for a hashtag at the same time.")
        super(Dislike, self).clean()

    class Meta:
        unique_together = [('user', 'hashtag')]
        ordering = ['created_at']
