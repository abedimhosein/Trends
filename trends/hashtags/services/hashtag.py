from trends.accounts.models import User
from trends.hashtags.models import Hashtag


def create_hashtag(title: str, description: str, creator: User):
    return Hashtag.objects.create(
        title=title,
        description=description,
        creator=creator
    )


def update_hashtag(title: str, description: str, slug: str):
    return Hashtag.objects.filter(slug__iexact=slug).update(
        title=title,
        description=description,
    )
