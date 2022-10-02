from accounts.models import User
from rest_framework import serializers


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'fullname']


class AdvancedUserSerializer(BasicUserSerializer):
    class Meta(BasicUserSerializer.Meta):
        fields = BasicUserSerializer.Meta.fields + ['email', 'created_at']
        read_only_fields = ('created_at',)
