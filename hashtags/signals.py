from django.db.models.signals import pre_save
from django.dispatch import receiver
from hashtags.models import Hashtag
from utils.funcs import unique_slug_generator


@receiver(pre_save, sender=Hashtag)
def pre_save_hashtag(sender, instance: Hashtag, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
