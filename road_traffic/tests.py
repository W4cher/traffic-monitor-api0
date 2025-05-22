from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from road_traffic.models import RoadSegment, Reading, TrafficIntensityRange
from django.utils import timezone
import datetime

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@ubiwhere.com'
        )
        self.anonymous_client = APIClient()

        # Configurar intervalos de intensidade
        TrafficIntensityRange.objects.create(min_speed=0, max_speed=20, intensity='high')
        TrafficIntensityRange.objects.create(min_speed=21, max_speed=50, intensity='medium')
        TrafficIntensityRange.objects.create(min_speed=51, max_speed=120, intensity='low')

        # Criar segmento de estrada
        self.segment = RoadSegment.objects.create(
            name='Test Segment',
            long_start=40.0,
            lat_start=-74.0,
            long_end=40.1,
            lat_end=-74.1,
            length=100,
            speed = 0
        )

        # Criar leituras
        self.reading1 = Reading.objects.create(
            road_segment=self.segment,
            average_speed=20,
            timestamp=timezone.now() - datetime.timedelta(hours=1)
        )
        self.reading2 = Reading.objects.create(
            road_segment=self.segment,
            average_speed=50,
            timestamp=timezone.now()
        )

    def test_get_road_segments_anonymous(self):
        response = self.anonymous_client.get('/api/road-segments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Segment')
        self.assertEqual(response.data[0]['total_readings'], 2)

    def test_create_road_segment_anonymous(self):
        data = {
            'name': 'New Segment',
            'long_start': 41.0,
            'lat_start': -75.0,
            'long_end': 41.1,
            'lat_end': -75.1,
            'length': 200,
            'speed': 0
        }
        response = self.anonymous_client.post('/api/road-segments/', data)
        self.assertEqual(response.status_code, 403)  # Forbidden for anonymous

    def test_create_road_segment_admin(self):
        self.client.login(username='admin', password='admin123')
        data = {
            'name': 'New Segment',
            'long_start': 41.0,
            'lat_start': -75.0,
            'long_end': 41.1,
            'lat_end': -75.1,
            'length': 200,
            'speed':0
        }
        response = self.client.post('/api/road-segments/', data)
        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(RoadSegment.objects.count(), 2)
        self.assertEqual(RoadSegment.objects.last().name, 'New Segment')

    def test_update_road_segment_admin(self):
        self.client.login(username='admin', password='admin123')
        data = {'name': 'Updated Segment'}
        response = self.client.patch(f'/api/road-segments/{self.segment.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.segment.refresh_from_db()
        self.assertEqual(self.segment.name, 'Updated Segment')

    def test_delete_road_segment_admin(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.delete(f'/api/road-segments/{self.segment.id}/')
        self.assertEqual(response.status_code, 204)  # No Content
        self.assertEqual(RoadSegment.objects.count(), 0)

    def test_get_readings_anonymous(self):
        response = self.anonymous_client.get('/api/readings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['intensity'], 'high')
        self.assertEqual(response.data[1]['intensity'], 'medium')

    def test_create_reading_anonymous(self):
        data = {
            'road_segment': self.segment.id,
            'average_speed': 30,
            'timestamp': '2023-05-29T10:00:00Z'
        }
        response = self.anonymous_client.post('/api/readings/', data)
        self.assertEqual(response.status_code, 403)  # Forbidden for anonymous

    def test_create_reading_admin(self):
        self.client.login(username='admin', password='admin123')
        data = {
            'road_segment': self.segment.id,
            'average_speed': 30,
            'timestamp': '2023-05-29T10:00:00Z'
        }
        response = self.client.post('/api/readings/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Reading.objects.count(), 3)
        self.assertEqual(Reading.objects.last().intensity, 'medium')

    def test_filter_by_intensity(self):
        response = self.anonymous_client.get('/api/road-segments/?readings__intensity=medium')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Segment')

    def test_filter_by_last_reading_intensity(self):
        response = self.anonymous_client.get('/api/road-segments/?last_reading_intensity=medium')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Última leitura é 50 km/h (medium)
        self.assertEqual(response.data[0]['name'], 'Test Segment')

        # Testar com intensidade diferente
        response = self.anonymous_client.get('/api/road-segments/?last_reading_intensity=high')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)  # Não há leituras recentes com high