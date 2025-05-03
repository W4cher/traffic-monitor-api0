from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import RoadSegment, Reading
from .serializers import RoadSegmentSerializer, ReadingSerializer
from .permissions import IsAdminOrReadOnly
from django.db.models import Max, Subquery, OuterRef
import logging

logger = logging.getLogger(__name__)


class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['readings__intensity']

    def get_queryset(self):
        logger.info("Accessing ReadingViewSet")
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


    