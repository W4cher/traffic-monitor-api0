from rest_framework import serializers
from .models import RoadSegment, Reading, TrafficIntensityRange

class TrafficIntensityRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficIntensityRange
        fields = ['id', 'min_speed', 'max_speed', 'intensity']

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ['id', 'road_segment', 'average_speed', 'intensity', 'timestamp']
        read_only_fields = ['intensity']

class RoadSegmentSerializer(serializers.ModelSerializer):
    total_readings = serializers.IntegerField(read_only=True, source='readings.count')

    class Meta:
        model = RoadSegment
        fields = ['id', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length','speed', 'total_readings']