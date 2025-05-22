from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

class RoadSegment(models.Model):
    name = models.CharField(max_length=100, blank=True)
    long_start = models.FloatField()
    lat_start = models.FloatField()
    long_end = models.FloatField()
    lat_end = models.FloatField()
    length = models.FloatField()
    speed = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.speed}"
        
    @property
    def total_readings(self):
        return self.readings.count()

class TrafficIntensityRange(models.Model):
    INTENSITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    min_speed = models.FloatField()
    max_speed = models.FloatField()
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES)
    
    def __str__(self):
        return f"{self.intensity} ({self.min_speed}-{self.max_speed})"

class Reading(models.Model):
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='readings')
    average_speed = models.FloatField()
    intensity = models.CharField(max_length=10, choices=TrafficIntensityRange.INTENSITY_CHOICES, default='medium')
    timestamp = models.DateTimeField(default=timezone.now)
    
    def calculate_intensity(self):
        try:
            intensity_range = TrafficIntensityRange.objects.get(
                min_speed__lte=self.average_speed,
                max_speed__gte=self.average_speed
            )
            return intensity_range.intensity
        except TrafficIntensityRange.DoesNotExist:
            if TrafficIntensityRange.objects.exists():
                if self.average_speed < TrafficIntensityRange.objects.order_by('min_speed').first().min_speed:
                    return 'low'  
                else:
                    return 'high'  
            return 'medium'  
    
    def save(self, *args, **kwargs):
        ranges = TrafficIntensityRange.objects.all()
        
        for range_obj in ranges:
            if range_obj.min_speed <= self.average_speed <= range_obj.max_speed:
                self.intensity = range_obj.intensity
                break
        else:
            self.intensity = self.calculate_intensity()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.road_segment} - {self.average_speed} km/h ({self.intensity})"

# part 3 do exercício
class Sensor(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.uuid)

class Car(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.license_plate

class VehiclePassage(models.Model):
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='passages')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='passages')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='passages')
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return f"{self.car} on {self.road_segment} at {self.timestamp}"