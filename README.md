# MetriCal

Implementación en Python del **Calendario Republicano Francés** (también conocido como Calendario Métrico Francés) para la conversión de fechas desde el calendario gregoriano y la generación de archivos `.ics` compatibles con aplicaciones de calendario estándar.

## Características

- **Sin dependencias externas:** Utiliza únicamente la librería estándar de Python 3.
- **Cálculo exacto:** Basado en el conteo de días desde el inicio del calendario (`22 de septiembre de 1792`, *1 de Vendémiaire, Año 1*) y la **regla de Romme** para los años sextiles (bisiestos).
- **Generación automática de 5 años:** Al ejecutar el script se generan eventos de día completo desde la fecha actual hasta los próximos 5 años.
- **Compatibilidad ICS (RFC 5545):** Genera archivos válidos con saltos de línea `CRLF`, `DTSTAMP`, `VALUE=DATE` y `TRANSP:TRANSPARENT`, listos para importar en Apple Calendar, Google Calendar, Nextcloud y otros clientes.
- **Información detallada:** Incluye el nombre del mes republicano, su descripción, el día de la década (*Primidi* a *Décadi*) y los días complementarios (*Jours complémentaires*, incluido el *Jour de la Révolution* en años sextiles).

## Requisitos

- Python 3.7 o superior.

## Uso

Clona el repositorio y ejecuta el script:

```bash
git clone [https://github.com/PunKoding/MetriCal.git](https://github.com/PunKoding/MetriCal.git)
cd MetriCal
python3 MetriCal.py
