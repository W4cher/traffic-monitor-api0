import csv
import os
from django.core.management.base import BaseCommand
from road_traffic.models import Sensor
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import sensors from CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('data', 'sensors.csv')
        logger.info(f"Importing sensors from {file_path}")
        
        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Sensor.objects.get_or_create(
                        uuid=row['uuid'],
                        defaults={'name': row['name']}
                    )
                logger.info("Sensors imported successfully")
        except FileNotFoundError:
            logger.error(f"Sensor file not found at {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error importing sensors: {str(e)}")
            raise