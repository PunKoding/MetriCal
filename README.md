# 🗓️ MetriCal

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ICS Support](https://img.shields.io/badge/format-ICS-orange.svg)](https://icalendar.org/)

Una implementación moderna del Calendario Republicano Francés (también conocido como Calendario Métrico Francés) que permite la conversión de fechas y la generación de calendarios ICS.

## 📖 Descripción

El Calendario Republicano Francés fue creado durante la Revolución Francesa como parte del sistema métrico decimal, utilizado oficialmente desde 1793 hasta 1805. Este proyecto moderniza su uso permitiendo:

- Conversión entre fechas gregorianas y republicanas
- Generación de calendarios ICS con eventos detallados
- Información rica sobre cada mes y sus significados
- Detección automática de eventos especiales (inicio/fin de mes/año)
- Soporte multilingüe (francés/español) para nombres y descripciones

## ✨ Características

- 📅 Conversión precisa de fechas entre calendarios
- 📝 Descripciones detalladas de cada mes en español
- 🎯 Detección automática de días especiales y complementarios
- 📤 Generación de archivos ICS compatibles con la mayoría de aplicaciones de calendario
- 🔄 Soporte para años bisiestos (sextiles)
- 🌍 Nombres de meses en francés y español
- 📊 Información contextual sobre el significado de cada mes

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/PunKoding/MetriCal.py

# Instalar dependencias
pip install ics

# Ejecutar script
python3 MetriCal.py
```

## 📋 Requisitos

- Python 3.6+
- Biblioteca `ics` para generación de calendarios

## 💻 Uso

### Conversión de Fechas

```python
from calendario_metrico import RepublicanCalendar
import datetime

# Obtener la fecha actual en el calendario republicano
today = datetime.date.today()
fecha_republicana = RepublicanCalendar.convert_date(today)
print(RepublicanCalendar.generate_event_name(fecha_republicana))
```

### Generación de Calendario ICS

```python
# Generar calendario para los próximos 10 años
generate_republican_calendar_ics(2024, num_years=10)
```

## 📅 Estructura del Calendario

El calendario republicano se organiza en:

- 12 meses de 30 días cada uno
- 5-6 días complementarios al final del año
- Cada mes representa un aspecto de la naturaleza o agricultura

### Meses del Calendario

| Mes | Nombre Francés | Significado |
|-----|----------------|-------------|
| 1 | Vendémiaire | Mes de la vendimia |
| 2 | Brumaire | Mes de la niebla |
| 3 | Frimaire | Mes del frío |
| 4 | Nivôse | Mes de la nieve |
| 5 | Pluviôse | Mes de la lluvia |
| 6 | Ventôse | Mes del viento |
| 7 | Germinal | Mes de la germinación |
| 8 | Floréal | Mes de las flores |
| 9 | Prairial | Mes de los prados |
| 10 | Messidor | Mes de la cosecha |
| 11 | Thermidor | Mes del calor |
| 12 | Fructidor | Mes de los frutos |

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
