from django.contrib import admin
from hashtags.models import Hashtag, Like, Dislike


class HashtagAdmin(admin.ModelAdmin):
    class Meta:
        model = Hashtag

    list_display = ('title', 'created_at')


class LikeAdmin(admin.ModelAdmin):
    class Meta:
        model = Like

    list_display = ('title', 'username',)

    def username(self, obj: Like):
        return obj.user.username

    def title(self, obj: Like):
        return obj.hashtag.title


class DislikeAdmin(admin.ModelAdmin):
    class Meta:
        model = Dislike

    list_display = ('title', 'username',)

    def username(self, obj: Dislike):
        return obj.user.username

    def title(self, obj: Dislike):
        return obj.hashtag.title


admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)
