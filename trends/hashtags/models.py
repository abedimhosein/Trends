from django.conf import settings
from django.db import models

from trends.common.models import BaseDateTimeModel

User = settings.AUTH_USER_MODEL


class Hashtag(BaseDateTimeModel, models.Model):
    class HashtagState(models.TextChoices):
        DRAFT = 'D', 'Draft'
        PUBLISHED = 'P', 'Published'

    slug = models.SlugField(unique=True, blank=True)
    state = models.CharField(max_length=1, choices=HashtagState.choices, default=HashtagState.DRAFT)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='hashtags')

    def __str__(self):
        return self.title


class Like(BaseDateTimeModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.PROTECT, related_name='likes')

    class Meta:
        unique_together = [('user', 'hashtag')]
        ordering = ['-created_at']


class Dislike(BaseDateTimeModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.PROTECT, related_name='dislikes')

    class Meta:
        unique_together = [('user', 'hashtag')]
        ordering = ['-created_at']


class Report(BaseDateTimeModel, models.Model):
    class ReportType(models.TextChoices):
        SPAM = 'S', 'Spam'
        INSULT = 'I', 'Insult'
        VIOLENCE = 'V', 'Violence'
        OTHER = 'O', 'Other'

        @staticmethod
        def to_reportType_obj(report_type: str):
            report_type = report_type.strip().upper()
            return Report.ReportType.__members__.get(report_type)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.PROTECT, related_name='reports')
    type = models.CharField(max_length=1, choices=ReportType.choices, default=ReportType.OTHER)
    description = models.TextField()

    class Meta:
        unique_together = [('user', 'hashtag')]
        ordering = ['-created_at']
