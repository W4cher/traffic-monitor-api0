from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import RoadSegment, Reading
from .serializers import RoadSegmentSerializer, ReadingSerializer
from .permissions import IsAdminOrReadOnly
import logging

logger = logging.getLogger(__name__)

class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['readings__intensity']

    def get_queryset(self):
        logger.info("Accessing RoadSegmentViewSet")
        return super().get_queryset()

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        logger.info("Accessing ReadingViewSet")
        return super().get_queryset()