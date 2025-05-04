from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from road_traffic.views import RoadSegmentViewSet, ReadingViewSet, VehiclePassageViewSet, VehiclePassageByPlateList
from django.conf import settings
from django.conf.urls.static import static
import logging

logger = logging.getLogger(__name__)
logger.info("Loading URLs...")

router = DefaultRouter()
router.register(r'road-segments', RoadSegmentViewSet)
router.register(r'readings', ReadingViewSet)
router.register(r'vehicle-passages', VehiclePassageViewSet)
logger.info(f"Registered API routes: {router.urls}")

def home(request):
    logger.info("Accessed root endpoint")
    return HttpResponse("Welcome to Traffic Monitor API")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/vehicle-passages/by-plate/', VehiclePassageByPlateList.as_view(), name='vehicle-passage-by-plate'),
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

logger.info("URLs loaded successfully")



