from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from trends.hashtags import serializers
from trends.hashtags.models import Hashtag, Like, Dislike, Report


class HashtagModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Hashtag.objects.filter(is_active=True)
    serializer_class = serializers.HashtagSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        if instance.likes.count() > 0 or instance.dislikes.count() > 0:
            return Response({'error': 'Hashtag cannot be deleted.'})
        instance.delete()

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None):
        hashtag: Hashtag = get_object_or_404(Hashtag, pk=pk)
        hashtag.state = Hashtag.HashtagState.PUBLISHED
        hashtag.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None):
        hashtag: Hashtag = get_object_or_404(Hashtag, pk=pk)
        hashtag.is_active = False
        hashtag.save()
        return Response(status=status.HTTP_200_OK)


class LikeModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DislikeModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Dislike.objects.all()
    serializer_class = serializers.DislikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReportModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Report.objects.all()
    serializer_class = serializers.ReportSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
