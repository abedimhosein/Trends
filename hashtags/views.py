from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from hashtags.models import (
    Hashtag,
    Like,
    Dislike,
    Report
)
from hashtags.serializers import (
    HashtagSerializer,
    LikeSerializer,
    DislikeSerializer,
    ReportSerializer,
)


class HashtagListCreate(ListCreateAPIView):
    queryset = Hashtag.objects.filter(is_active=True)
    serializer_class = HashtagSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HashtagDetail(RetrieveUpdateDestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer

    def delete(self, request, *args, **kwargs):
        hashtag = get_object_or_404(Hashtag, pk=1)
        if hashtag.likes.count() > 0 or hashtag.dislikes.count() > 0:
            return Response({'error': 'Hashtag cannot be deleted.'})
        hashtag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeList(ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DislikeList(ListCreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReportList(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
