# 🚦 Traffic Monitor API

API REST para monitoramento de tráfego rodoviário, desenvolvida com Django REST Framework. Este projeto implementa as **Partes 1, 2 e 3** com foco em operações CRUD, filtros, e integração com sensores.

---

## 📋 Funcionalidades

### Parte 1

* CRUD para `RoadSegment` (segmentos de estrada)
* CRUD para `Reading` (leituras de tráfego)
* Cálculo automático da intensidade de tráfego (`low`, `medium`, `high`) via `TrafficIntensityRange`

### Parte 2

* Filtros por intensidade de qualquer leitura ou da última leitura de um segmento

### Parte 3

* Envio de `VehiclePassage` (passagens de veículos) autenticado via API Key
* Consulta de passagens por matrícula nas últimas 24h (admin)

---

## ⚙️ Tecnologias

* Django 4.2.11
* Django REST Framework 3.14.0
* PostgreSQL 13
* drf-spectacular (Swagger)
* django-filter
* Docker e Docker Compose

---

## 📦 Instalação

```bash
# Clone e crie as pastas
mkdir traffic_monitor0 && cd traffic_monitor0
mkdir src && cd src
mkdir data

# Coloque os arquivos CSV:
# - traffic_speed.csv
# - sensors.csv
# dentro de traffic_monitor0/src/data/

# Acesse a pasta do projeto e rode:
cd src
docker-compose up --build
```

---

## 🔗 Endpoints Principais

### 🔍 Listar Segmentos de Estrada

```
GET /api/road-segments/
```

#### Filtros:

* `?readings__intensity=<low|medium|high>`
* `?last_reading_intensity=<low|medium|high>`

### ➕ Criar Segmento (Admin)

```bash
POST /api/road-segments/
Authorization: Bearer <admin-token>
```

### 📈 Listar Leituras

```
GET /api/readings/
```

### ➕ Criar Leitura (Admin)

```bash
POST /api/readings/
Authorization: Bearer <admin-token>
```

### 🚘 Enviar Passagens (Sensor via API Key)

```bash
POST /api/vehicle-passages/
X-API-Key: 23231c7a-80a7-4810-93b3-98a18ecfbc42
```

### 🔍 Buscar por Matrícula (Admin)

```bash
GET /api/vehicle-passages/by-plate/?license_plate=AA16AA
Authorization: Bearer <admin-token>
```

---

## 🔐 Permissões

| Perfil           | Permissões                                        |
| ---------------- | ------------------------------------------------- |
| Anônimo          | `GET` em road-segments e readings                 |
| Administrador    | Total acesso (CRUD + leitura por matrícula)       |
| Sensor (API Key) | Enviar passagens (`POST` em `/vehicle-passages/`) |

---

## 🧺 Testes

Execute os testes unitários:

```bash
docker-compose exec web python manage.py test
```

---

## 📅 Importação de Dados

### 📄 `traffic_speed.csv`

```csv
ID,Long_start,Lat_start,Long_end,Lat_end,Length,Speed
```

Importa RoadSegments + Reading inicial.

### 📄 `sensors.csv`

```csv
id,name,uuid
```

Importa sensores (ex: nome + UUID).

### Comandos manuais:

```bash
docker-compose exec web python manage.py import_data
docker-compose exec web python manage.py import_sensors
```

---

## 🛠 Django Admin

```bash
docker-compose exec web python manage.py createsuperuser
```

Acesse: [http://localhost:8000/admin/](http://localhost:8000/admin/)

Modelos registrados:

* `RoadSegment`
* `Reading`
* `TrafficIntensityRange`

> Modelos `Sensor`, `Car` e `VehiclePassage` disponíveis apenas via API/banco.

---

## 🔎 Depuração

```bash
docker-compose logs web
docker-compose exec db psql -U user -d traffic_db -c "SELECT * FROM road_traffic_roadsegment;"
```

---

## ♻️ Resetar Ambiente

```bash
docker-compose down
docker volume rm traffic_monitor_part1_postgres_data
docker-compose up --build
```

---

## 💡 Notas

* Para incluir o nome do sensor no retorno da API, edite `SensorSerializer`:

```python
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['uuid', 'name']
```

* O campo `speed` em `RoadSegment` armazena a velocidade média inicial (do CSV).

---

## 📚 Documentação Swagger

Acesse: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## 👨‍💼 Autor

Garcia Lisboa Mateus
Software Engineering | UBIWHERE
