from hashtags import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hashtags', views.HashtagModelViewSet, basename='hashtag')
router.register('likes', views.LikeModelViewSet, basename='like')
router.register('dislikes', views.DislikeModelViewSet, basename='dislike')
router.register('reports', views.ReportModelViewSet, basename='report')

urlpatterns = router.urls