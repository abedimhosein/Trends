from ..models import Hashtag


def hashtag_list():
    return Hashtag.objects.all()
