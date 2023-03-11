from trends.hashtags import apis
from django.urls import path

urlpatterns = [
    path('hashtag/', apis.HashtagApi.as_view(), name='hashtag'),
]
