from django.db import models
from django.utils import timezone

class RoadSegment(models.Model):
    long_start = models.FloatField()
    lat_start = models.FloatField()
    long_end = models.FloatField()
    lat_end = models.FloatField()
    length = models.FloatField()
    speed = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.speed}"

class TrafficIntensityRange(models.Model):
    INTENSITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    min_speed = models.IntegerField()
    max_speed = models.IntegerField()
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES)

    def __str__(self):
        return f"{self.intensity} ({self.min_speed}-{self.max_speed})"

class Reading(models.Model):
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='readings')
    average_speed = models.IntegerField()
    intensity = models.CharField(max_length=10, choices=TrafficIntensityRange.INTENSITY_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def calculate_intensity(self):
        try:
            intensity_range = TrafficIntensityRange.objects.get(
                min_speed__lte=self.average_speed,
                max_speed__gte=self.average_speed
            )
            return intensity_range.intensity
        except TrafficIntensityRange.DoesNotExist:
            return 'unknown'

    def save(self, *args, **kwargs):
        self.intensity = self.calculate_intensity()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.road_segment} - {self.average_speed} km/h ({self.intensity})"