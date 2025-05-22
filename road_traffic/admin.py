from django.contrib import admin
from .models import RoadSegment, Reading, TrafficIntensityRange

@admin.register(RoadSegment)
class RoadSegmentAdmin(admin.ModelAdmin):
    list_display = ('length', 'created_at')


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('road_segment', 'average_speed', 'intensity', 'timestamp')
    list_filter = ('intensity', 'timestamp')


@admin.register(TrafficIntensityRange)
class TrafficIntensityRangeAdmin(admin.ModelAdmin):
    list_display = ('intensity', 'min_speed', 'max_speed')