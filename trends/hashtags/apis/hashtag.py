from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from trends.hashtags.models import Hashtag
from ..services.hashtag import create_hashtag
from ..selectors.hashtag import hashtag_list


class HashtagApi(APIView):
    permission_classes = (IsAuthenticated,)

    class InputHashtagSerializer(serializers.Serializer):
        def create(self, validated_data):
            return super().create(validated_data)

        title = serializers.CharField(max_length=255)
        description = serializers.CharField(max_length=500)

    class OutputHashtagDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Hashtag
            fields = ('slug', 'title', 'description', 'creator')

    class OutputHashtagListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Hashtag
            fields = ('slug', 'title', 'summary', 'creator')

        summary = serializers.SerializerMethodField(read_only=True)

        def get_summary(self, obj: Hashtag):
            return f"{obj.description[:15]}..."

    @extend_schema(request=InputHashtagSerializer, responses=OutputHashtagDetailSerializer)
    def post(self, request):
        # create a new hashtag
        serializer_obj = self.InputHashtagSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)

        try:
            hashtag = create_hashtag(
                title=serializer_obj.validated_data.get("title"),
                description=serializer_obj.validated_data.get("description"),
                creator=request.user
            )
        except Exception as e:
            return Response(
                f"Database Error {e}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputHashtagDetailSerializer(hashtag).data)

    @extend_schema(responses=OutputHashtagListSerializer)
    def get(self, request):
        queryset = hashtag_list()
        return Response(self.OutputHashtagListSerializer(queryset, many=True).data)


class HashtagDetailApi(APIView):
    def patch(self, request, slug):
        ...

    def get(self, request, slug):
        ...

    def delete(self, request, slug):
        ...
