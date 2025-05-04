# traffic-monitor-api0


Traffic Monitor API - Partes 1, 2, e 3
Descrição
Este projeto é uma API REST desenvolvida com Django REST Framework para monitoramento de tráfego rodoviário, implementando as Partes 1, 2, e 3 de um teste técnico. A API suporta:

Parte 1: Operações CRUD para segmentos de estrada (RoadSegment) e leituras de tráfego (Reading), com cálculo dinâmico de intensidade de tráfego (low, medium, high) baseado em intervalos definidos (TrafficIntensityRange).
Parte 2: Filtros na API para listar segmentos com base na intensidade de qualquer leitura (readings__intensity) ou da última leitura (last_reading_intensity).
Parte 3: Integração com sensores de tráfego, permitindo o envio de registros de passagens de veículos (VehiclePassage) em bulk via POST autenticado por API Key, e consulta de passagens por matrícula nas últimas 24 horas, restrita a administradores.

A API é documentada com Swagger (drf-spectacular) e usa PostgreSQL como banco de dados, rodando em um ambiente Docker.
Estrutura do Projeto
traffic_monitor_part1/
├── data/
│   ├── traffic_speed.csv         # Dados de segmentos e leituras iniciais
│   └── sensors.csv               # Dados de sensores (id,name,uuid)
├── docs/
│   └── README.md                 # Instruções do projeto
├── src/
│   ├── manage.py                 # Script de gerenciamento do Django
│   ├── requirements.txt          # Dependências Python
│   ├── Dockerfile                # Configuração do Docker
│   ├── docker-compose.yml        # Configuração do Docker Compose
│   ├── wait-for-db.sh            # Script para aguardar o banco de dados
│   ├── traffic_monitor/          # Configurações do projeto Django
│   │   ├── settings.py           # Configurações do Django
│   │   ├── urls.py               # Rotas da API
│   │   └── wsgi.py              # Configuração WSGI
│   ├── road_traffic/             # App Django para monitoramento de tráfego
│   │   ├── admin.py              # Configuração do Django Admin
│   │   ├── models.py             # Modelos de dados
│   │   ├── permissions.py        # Permissões personalizadas
│   │   ├── serializers.py        # Serializadores da API
│   │   ├── views.py              # Views da API
│   │   ├── tests.py              # Testes unitários
│   │   └── management/commands/  # Comandos personalizados
│   │       ├── import_data.py    # Importa traffic_speed.csv
│   │       └── import_sensors.py # Importa sensors.csv

Tecnologias

Django 4.2.11
Django REST Framework 3.14.0
PostgreSQL 13 (via psycopg2-binary==2.9.9)
drf-spectacular 0.27.1 (para documentação Swagger)
django-filter 24.2 (para filtros na API)
Docker e Docker Compose

Instalação

Crie o diretório do projeto:cd C:\Users\wache\OneDrive\Ambiente de Trabalho
mkdir traffic_monitor_part1
cd traffic_monitor_part1
mkdir src data docs


Salve traffic_speed.csv e sensors.csv em traffic_monitor_part1/data/.
Salve todos os arquivos fornecidos em seus respectivos caminhos sob src/ e docs/.
Instale o Docker Desktop.
Navegue até src/ e execute:cd traffic_monitor_part1/src
docker-compose up --build


Acesse os serviços:
API: http://localhost:8000/
Swagger: http://localhost:8000/api/docs/
Django Admin: http://localhost:8000/admin/ (crie um superusuário com docker-compose exec web python manage.py createsuperuser)



Endpoints
A API oferece os seguintes endpoints, documentados no Swagger (http://localhost:8000/api/docs/):

GET /api/road-segments/: Lista todos os segmentos de estrada com dados geográficos, velocidade média (speed), e contagem de leituras (total_readings).

Filtros:
?readings__intensity=<intensity>: Filtra por intensidade de qualquer leitura (high, medium, low).
?last_reading_intensity=<intensity>: Filtra por intensidade da última leitura.


Exemplo:curl -v "http://localhost:8000/api/road-segments/?last_reading_intensity=medium"

Resposta:[
  {
    "id": 1,
    "name": "Segment 1",
    "long_start": 40.7128,
    "lat_start": -74.006,
    "long_end": 40.7129,
    "lat_end": -74.005,
    "length": 100.0,
    "speed": 50.0,
    "total_readings": 2
  }
]




POST/PUT/DELETE /api/road-segments/: Cria, atualiza ou deleta segmentos (administradores apenas).

Exemplo (POST):curl -v -X POST http://localhost:8000/api/road-segments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin-token>" \
  -d '{"name": "New Segment", "long_start": 41.0, "lat_start": -75.0, "long_end": 41.1, "lat_end": -75.1, "length": 200, "speed": 60}'




GET /api/readings/: Lista todas as leituras de tráfego.

Exemplo:curl -v http://localhost:8000/api/readings/




POST/PUT/DELETE /api/readings/: Cria, atualiza ou deleta leituras (administradores apenas).

Exemplo (POST):curl -v -X POST http://localhost:8000/api/readings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin-token>" \
  -d '{"road_segment": 1, "average_speed": 30, "timestamp": "2025-05-04T10:00:00Z"}'




POST /api/vehicle-passages/: Envia registros de passagens de veículos em bulk (sensores apenas, requer API Key 23231c7a-80a7-4810-93b3-98a18ecfbc42 no cabeçalho X-API-Key).

Exemplo:curl -v -X POST http://localhost:8000/api/vehicle-passages/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: 23231c7a-80a7-4810-93b3-98a18ecfbc42" \
  -d '[{
    "road_segment": 1,
    "car__license_plate": "AA16AA",
    "timestamp": "2025-05-04T09:27:26.769Z",
    "sensor__uuid": "270e4cc0-d454-4b42-8682-80e87c3d163c"
  }]'

Resposta:[
  {
    "id": 1,
    "road_segment": { "id": 1, "name": "Segment 1", ... },
    "car": { "license_plate": "AA16AA", "registered_at": "2025-05-04T..." },
    "sensor": { "uuid": "270e4cc0-d454-4b42-8682-80e87c3d163c" },
    "timestamp": "2025-05-04T09:27:26.769Z"
  }
]




GET /api/vehicle-passages/by-plate/: Lista passagens de uma matrícula nas últimas 24 horas (administradores apenas).

Parâmetro: ?license_plate=<plate>
Exemplo:curl -v "http://localhost:8000/api/vehicle-passages/by-plate/?license_plate=AA16AA" \
  -H "Authorization: Bearer <admin-token>"




GET /api/docs/: Documentação Swagger interativa.


Permissões

Anônimo: Acesso de leitura (GET) a road-segments e readings.
Administrador: Acesso completo (CRUD) a road-segments, readings, e vehicle-passages/by-plate. Requer autenticação via token (obtido no Django Admin ou Swagger).
Sensor: Acesso POST a vehicle-passages com a API Key 23231c7a-80a7-4810-93b3-98a18ecfbc42 no cabeçalho X-API-Key.

Importação de Dados

traffic_speed.csv: Importado automaticamente na inicialização via python manage.py import_data. Contém segmentos de estrada e leituras iniciais.
Formato: ID,Long_start,Lat_start,Long_end,Lat_end,Length,Speed.
Cada linha cria um RoadSegment (nomeado como Segment <ID>) e uma Reading com average_speed e timestamp atual.


sensors.csv: Importado automaticamente via python manage.py import_sensors.
Formato: id,name,uuid.
Cria Sensor com uuid e name (ex.: Gorgeous Flamingo, 270e4cc0-d454-4b42-8682-80e87c3d163c).



Para reimportar manualmente:
docker-compose exec web python manage.py import_data
docker-compose exec web python manage.py import_sensors

Django Admin

Crie um superusuário:docker-compose exec web python manage.py createsuperuser


Acesse: http://localhost:8000/admin/.
Modelos disponíveis:
RoadSegment: Exibe length e created_at.
Reading: Exibe road_segment, average_speed, intensity, timestamp, com filtros por intensity e timestamp.
TrafficIntensityRange: Exibe intensity, min_speed, max_speed.


Nota: Sensor, Car, e VehiclePassage não estão registrados no Django Admin. Para gerenciá-los, use a API ou o banco de dados diretamente.

Testes Unitários
Valide a funcionalidade da API com testes unitários:
cd traffic_monitor_part1/src
docker-compose exec web python manage.py test

Os testes cobrem:

CRUD de RoadSegment e Reading.
Permissões (anônimo, administrador, sensor).
Filtros por readings__intensity e last_reading_intensity.
Envio e consulta de VehiclePassage.

Depuração
Se encontrar problemas:

Verifique os logs:docker-compose logs web
docker-compose logs db


Teste o endpoint raiz:curl -v http://localhost:8000/


Teste endpoints da API:curl -v http://localhost:8000/api/road-segments/


Verifique arquivos estáticos:curl -v http://localhost:8000/static/admin/css/base.css


Inspecione o banco de dados:docker-compose exec db psql -U user -d traffic_db -c "SELECT * FROM road_traffic_roadsegment;"
docker-compose exec db psql -U user -d traffic_db -c "SELECT * FROM road_traffic_sensor;"


Resetar o ambiente:cd traffic_monitor_part1/src
docker-compose down
docker volume rm traffic_monitor_part1_postgres_data
docker-compose up --build



Exemplos

Listar segmentos com última leitura medium:curl -X GET "http://localhost:8000/api/road-segments/?last_reading_intensity=medium"


Enviar passagem de veículo (sensor):curl -X POST http://localhost:8000/api/vehicle-passages/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: 23231c7a-80a7-4810-93b3-98a18ecfbc42" \
  -d '[{
    "road_segment": 1,
    "car__license_plate": "AA16AA",
    "timestamp": "2025-05-04T09:27:26.769Z",
    "sensor__uuid": "270e4cc0-d454-4b42-8682-80e87c3d163c"
  }]'


Listar passagens por matrícula (administrador):curl -X GET "http://localhost:8000/api/vehicle-passages/by-plate/?license_plate=AA16AA" \
  -H "Authorization: Bearer <admin-token>"



Notas

Limitação do SensorSerializer: Atualmente, o campo name do modelo Sensor (ex.: Gorgeous Flamingo) não é retornado na API, pois o SensorSerializer inclui apenas uuid. Para incluir o name, atualize serializers.py:class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['uuid', 'name']


Campo speed: O modelo RoadSegment inclui um campo speed, usado para armazenar a velocidade média inicial do segmento, conforme importado de traffic_speed.csv.

