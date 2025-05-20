from django.contrib import admin

from video_hosting.models import User, Video, VideoTracker

# Register your models here.

class VideoInline(admin.TabularInline):
    fk_name = 'created_by'
    extra = 1
    model = Video


class VideoTrackerInline(admin.TabularInline):
    fk_name = 'viewer'
    extra = 1
    model = VideoTracker


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active']
    inlines = [VideoInline, VideoTrackerInline]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display_links = ['id']
    list_display = ['id', 'hls_dir_name', 'hash']
    
