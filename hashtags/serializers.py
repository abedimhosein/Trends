from rest_framework import serializers
from hashtags.models import Hashtag, Like, Dislike, Report
from accounts.serializers import BasicUserSerializer
from accounts.models import User


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['title', 'description', 'creator', 'likes_count', 'dislikes_count', 'reports_count']

    creator = BasicUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField(method_name='get_likes_count', read_only=True)
    dislikes_count = serializers.SerializerMethodField(method_name='get_dislikes_count', read_only=True)
    reports_count = serializers.SerializerMethodField(method_name='get_reports_count', read_only=True)

    def get_likes_count(self, obj: Hashtag):
        return obj.likes.count()

    def get_dislikes_count(self, obj: Hashtag):
        return obj.dislikes.count()

    def get_reports_count(self, obj: Hashtag):
        return obj.reports.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['hashtag', 'user', 'created_at']

    hashtag = serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.filter(is_active=True))
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(usertype=User.Usertype.NORMAL))

    def validate(self, attrs):
        if Dislike.objects.filter(user=attrs.get('user'), hashtag=attrs.get('hashtag')).exists():
            raise serializers.ValidationError("You're not allowed to like and dislike for a hashtag at the same time.")
        return attrs


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['hashtag', 'user', 'created_at']

    hashtag = serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.filter(is_active=True))
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(usertype=User.Usertype.NORMAL))

    def validate(self, attrs):
        if Like.objects.filter(user=attrs.get('user'), hashtag=attrs.get('hashtag')).exists():
            raise serializers.ValidationError("You're not allowed to like and dislike for a hashtag at the same time.")
        return attrs


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['hashtag', 'user', 'description', 'created_at']

    hashtag = serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.filter(is_active=True))
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(usertype=User.Usertype.NORMAL))
