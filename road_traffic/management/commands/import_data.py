import csv
from django.core.management.base import BaseCommand
from road_traffic.models import RoadSegment, Reading
from django.utils import timezone

class Command(BaseCommand):
    help = 'Import initial data from CSV'

    def handle(self, *args, **kwargs):
        with open('data/traffic_speed.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in  reader:
                # Criar ou atualizar RoadSegment
                segment, _ = RoadSegment.objects.update_or_create(
                
                    long_start=float(row['Long_start']),
                    lat_start=float(row['Lat_start']),
                    long_end=float(row['Long_end']),
                    lat_end=float(row['Lat_end']),
                    length=float(row['Length']),
                    speed=float(row['Speed']),

                    defaults={
                        'name': f"Segment {row['ID']}"
                    }    
                )
                # Criar Reading
                Reading.objects.create(
                    road_segment=segment,
                    average_speed=float(row['Speed']),
                    timestamp=timezone.now()  # Usar data/hora atual
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))