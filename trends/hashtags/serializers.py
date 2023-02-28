from rest_framework import serializers

from trends.accounts.serializers import BasicUserSerializer
from trends.hashtags.models import Hashtag, Like, Dislike, Report


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('slug', 'title', 'state', 'description', 'creator', 'created_at',
                  'likes_count', 'dislikes_count', 'reports_count')
        read_only_fields = ('slug', 'state', 'created_at')

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
        fields = ('hashtag', 'user', 'created_at')
        read_only_fields = ('created_at',)

    hashtag = serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.filter(is_active=True))
    user = BasicUserSerializer(read_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if Dislike.objects.filter(user=user, hashtag=attrs.get('hashtag')).exists():
            raise serializers.ValidationError("You're not allowed to like and dislike for a hashtag at the same time.")

        if Like.objects.filter(user=user, hashtag=attrs.get('hashtag')).exists():
            raise serializers.ValidationError("You're not allowed to like the same hashtag twice.")
        return attrs


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ('hashtag', 'user', 'created_at')
        read_only_fields = ('created_at',)

    hashtag = serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.filter(is_active=True))
    user = BasicUserSerializer(read_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if Like.objects.filter(user=user, hashtag=attrs.get('hashtag')).exists():
            raise serializers.ValidationError("You're not allowed to like and dislike for a hashtag at the same time.")

        if Dislike.objects.filter(user=user, hashtag=attrs.get('hashtag')).exists():
            raise serializers.ValidationError("You're not allowed to dislike the same hashtag twice.")

        return attrs


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('hashtag', 'user', 'description', 'type', 'created_at')
        read_only_fields = ('created_at',)

    hashtag = serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.filter(is_active=True))
    user = BasicUserSerializer(read_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if Report.objects.filter(user=user, hashtag=attrs.get('hashtag')).exists():
            raise serializers.ValidationError("You're not allowed to report the same hashtag twice.")

        return attrs
