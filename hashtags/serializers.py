from rest_framework import serializers
from hashtags.models import Hashtag, Like, Dislike
from accounts.serializers import BasicUserSerializer


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['title', 'description', 'creator', 'likes_count', 'dislike_count']

    creator = BasicUserSerializer()
    likes_count = serializers.SerializerMethodField(method_name='get_likes_count', read_only=True)
    dislike_count = serializers.SerializerMethodField(method_name='get_dislike_count', read_only=True)

    def get_likes_count(self, obj: Hashtag):
        return obj.likes.count()

    def get_dislikes_count(self, obj: Hashtag):
        return obj.dislikes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['hashtag', 'user', 'created_at']

    hashtag = HashtagSerializer()
    user = BasicUserSerializer()


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['hashtag', 'user', 'created_at']

    hashtag = HashtagSerializer()
    user = BasicUserSerializer()