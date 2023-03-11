from django.urls import path, include

urlpatterns = [
    path('accounts/', include(('trends.accounts.urls', 'accounts'))),
    path('trends/', include(('trends.hashtags.urls', 'hashtags'))),
]
