from django.urls import path
from hashtags import views

urlpatterns = [
    path('likes/', views.LikeList.as_view()),
    path('dislikes/', views.DislikeList.as_view()),
    path('reports/', views.ReportList.as_view()),
    path('hashtags/', views.HashtagList.as_view()),
    path('hashtags/<int:pk>/', views.HashtagDetail.as_view())
]
