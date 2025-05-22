from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import RoadSegment, Reading, VehiclePassage
from .serializers import RoadSegmentSerializer, ReadingSerializer, VehiclePassageSerializer
from .permissions import IsAdminOrReadOnly, HasSensorAPIKey
from django.db.models import Max, Subquery, OuterRef
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    # Defina explicitamente os campos permitidos para filtrar
    filterset_fields = {
        'readings__intensity': ['exact'],
        # Não inclua 'name' aqui
    }

    def get_queryset(self):
        logger.info("Accessing RoadSegmentViewSet")  # Corrigi de ReadingViewSet para RoadSegmentViewSet
        queryset = super().get_queryset()

        # Filtro por última leitura
        last_reading_intensity = self.request.query_params.get('last_reading_intensity')
        if last_reading_intensity:
            # Subquery para obter a leitura mais recente por segmento
            latest_reading = Reading.objects.filter(
                road_segment=OuterRef('pk')
            ).order_by('-timestamp').values('intensity')[:1]
            queryset = queryset.annotate(
                last_intensity=Subquery(latest_reading)
            ).filter(last_intensity=last_reading_intensity)
        return queryset

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        logger.info("Accessing ReadingViewSet")
        return super().get_queryset()

class VehiclePassageViewSet(viewsets.ModelViewSet):
    queryset = VehiclePassage.objects.all()
    serializer_class = VehiclePassageSerializer
    permission_classes = [HasSensorAPIKey]
    http_method_names = ['post']

    def get_queryset(self):
        logger.info("Accessing VehiclePassageViewSet")
        return super().get_queryset()

class VehiclePassageByPlateList(generics.ListAPIView):
    serializer_class = VehiclePassageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        logger.info("Accessing VehiclePassageByPlateList")
        license_plate = self.request.query_params.get('license_plate')
        if not license_plate:
            logger.warning("Missing license_plate parameter")
            return VehiclePassage.objects.none()
        
        # Filtrar passagens das últimas 24 horas
        time_threshold = timezone.now() - timedelta(hours=24)
        queryset = VehiclePassage.objects.filter(
            car__license_plate=license_plate,
            timestamp__gte=time_threshold
        ).select_related('road_segment', 'car', 'sensor')
        return queryset