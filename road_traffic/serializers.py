from rest_framework import serializers
from .models import RoadSegment, Reading, Sensor, Car, VehiclePassage,TrafficIntensityRange

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
        fields = ['id', 'name','long_start', 'lat_start', 'long_end', 'lat_end', 'length','speed', 'total_readings']

# serialicao da part 3 do exercio 

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['uuid']

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['license_plate', 'registered_at']

class VehiclePassageSerializer(serializers.ModelSerializer):
    car__license_plate = serializers.CharField(source='car.license_plate', write_only=True)
    sensor__uuid = serializers.UUIDField(source='sensor.uuid', write_only=True)
    car = CarSerializer(read_only=True)
    sensor = SensorSerializer(read_only=True)
    road_segment = RoadSegmentSerializer(read_only=True)

    class Meta:
        model = VehiclePassage
        fields = ['id', 'road_segment', 'car', 'car__license_plate', 'sensor', 'sensor__uuid', 'timestamp']
        read_only_fields = ['id', 'car', 'sensor', 'road_segment']

    def create(self, validated_data):
        car_license_plate = validated_data.pop('car')['license_plate']
        sensor_uuid = validated_data.pop('sensor')['uuid']
        
        # Registrar ou obter carro
        car, created = Car.objects.get_or_create(
            license_plate=car_license_plate,
            defaults={'registered_at': timezone.now()}
        )
        
        # Obter sensor
        try:
            sensor = Sensor.objects.get(uuid=sensor_uuid)
        except Sensor.DoesNotExist:
            raise serializers.ValidationError("Sensor with given UUID does not exist.")
        
        # Obter segmento de estrada
        road_segment_id = validated_data['road_segment'].id
        try:
            road_segment = RoadSegment.objects.get(id=road_segment_id)
        except RoadSegment.DoesNotExist:
            raise serializers.ValidationError("Road segment with given ID does not exist.")
        
        # Criar passagem
        passage = VehiclePassage.objects.create(
            road_segment=road_segment,
            car=car,
            sensor=sensor,
            timestamp=validated_data['timestamp']
        )
        return passage