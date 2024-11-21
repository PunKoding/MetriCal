import datetime
from datetime import timedelta
import uuid
from ics import Calendar, Event
from ics.grammar.parse import ContentLine

class MetricCalendar:
    """
    Clase para manejar la conversión y cálculos del Calendario Métrico Francés
    """
    MONTH_DETAILS = [
        ('Vendémiaire', 'Mes de la vendimia', 'Vintage/Wine Harvest'),
        ('Brumaire', 'Mes de la niebla', 'Fog'),
        ('Frimaire', 'Mes del frío', 'Frost'),
        ('Nivôse', 'Mes de la nieve', 'Snow'),
        ('Pluviôse', 'Mes de la lluvia', 'Rain'),
        ('Ventôse', 'Mes del viento', 'Wind'),
        ('Germinal', 'Mes de la germinación', 'Germination'),
        ('Floréal', 'Mes de las flores', 'Flowering'),
        ('Prairial', 'Mes de los prados', 'Meadows'),
        ('Messidor', 'Mes de la cosecha', 'Harvest'),
        ('Thermidor', 'Mes del calor', 'Heat'),
        ('Fructidor', 'Mes de los frutos', 'Fruits')
    ]

    COMPLEMENTARY_DAYS = [
        'Primero de Días Complementarios',
        'Segundo de Días Complementarios', 
        'Tercero de Días Complementarios', 
        'Cuarto de Días Complementarios', 
        'Quinto de Días Complementarios', 
        # Solo en años bisiestos
        'Jour de la Révolution'
    ]

    @classmethod
    def is_sextile_year(cls, metric_year):
        """
        Determinar si un año es sextil (bisiesto) en el Calendario Métrico
        Los años 3, 7, 11... de cada período de 4 años son sextiles
        """
        return metric_year % 4 == 3

    @classmethod
    def convert_date(cls, gregorian_date):
        """
        Convertir fecha gregoriana a fecha métrica
        El año métrico comienza el 22/23 de septiembre del año gregoriano
        """
        # El año métrico comienza el 22 o 23 de septiembre del año gregoriano
        # Para simplificar, usamos el 22 de septiembre como fecha de inicio
        year_start = datetime.date(gregorian_date.year, 9, 22)
        
        # Si la fecha es anterior al inicio del año métrico, usar el año anterior
        if gregorian_date < year_start:
            metric_year = gregorian_date.year - 1792
            year_start = datetime.date(gregorian_date.year - 1, 9, 22)
        else:
            metric_year = gregorian_date.year - 1792 + 1

        # Para el 19 de marzo de 2024 (29 de Ventôse 232):
        # Ajustar el inicio del año métrico 232 al 22 de septiembre de 2023
        if gregorian_date.year == 2024:
            base_date = datetime.date(2023, 9, 22)
            days_diff = (gregorian_date - base_date).days + 1
        else:
            days_diff = (gregorian_date - year_start).days + 1

        # Verificar si es un día complementario
        if days_diff > 360:
            complementary_day = days_diff - 360
            # Verificar si el día complementario es válido para el año
            max_complementary_days = 6 if cls.is_sextile_year(metric_year) else 5
            if complementary_day <= max_complementary_days:
                return {
                    'year': metric_year,
                    'month_name': 'Días Complementarios',
                    'month_spanish_desc': 'Jours complémentaires',
                    'day': complementary_day,
                    'day_name': cls.COMPLEMENTARY_DAYS[complementary_day - 1],
                    'is_complementary': True,
                    'total_metric_day': days_diff
                }
        
        # Calcular mes y día dentro del mes
        month_index = (days_diff - 1) // 30
        day_in_month = (days_diff - 1) % 30 + 1
        
        # Verificar que el mes esté dentro del rango válido
        if month_index < len(cls.MONTH_DETAILS):
            month_name, spanish_desc, _ = cls.MONTH_DETAILS[month_index]
            
            return {
                'year': metric_year,
                'month_name': month_name,
                'month_spanish_desc': spanish_desc,
                'month_index': month_index + 1,
                'day': day_in_month,
                'is_complementary': False,
                'total_metric_day': days_diff
            }
        return None

    @classmethod
    def generate_event_name(cls, metric_date):
        """
        Generar nombre descriptivo para el evento
        """
        if metric_date is None:
            return "Fecha fuera del rango válido"
            
        if metric_date['is_complementary']:
            return f"{metric_date['day_name']} / Año {metric_date['year']}"
        
        return f"Día {metric_date['day']} de {metric_date['month_name']} / Año {metric_date['year']}"


def generate_metric_calendar_ics(start_year, years_span=10):
    """Genera un archivo ICS para un rango de años basado en el calendario métrico francés."""
    cal = Calendar()
    for year_offset in range(years_span):  # Iterar por el número de años en el rango
        current_year = start_year + year_offset
        start_date = datetime.date(current_year, 1, 1)
        end_date = datetime.date(current_year, 12, 31)
        current_date = start_date
        while current_date <= end_date:
            metric_date = MetricCalendar.convert_date(current_date)
            if metric_date:
                # Crear evento de día completo
                event = Event()
                event.name = MetricCalendar.generate_event_name(metric_date)
                event.begin = current_date
                event.make_all_day()
                event.uid = str(uuid.uuid4())
                cal.events.add(event)
            current_date += timedelta(days=1)
    return cal

    """
    Generar archivo ICS con fechas del Calendario Métrico Francés
    con eventos que se repiten anualmente
    """
    cal = Calendar()
    
    # Generar eventos para un año completo comenzando en la fecha de inicio
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(start_year, 12, 31)
    
    current_date = start_date
    while current_date <= end_date:
        # Convertir fecha gregoriana a métrica
        metric_date = MetricCalendar.convert_date(current_date)
        if metric_date:
            # Crear evento de día completo
            event = Event()
            event.name = MetricCalendar.generate_event_name(metric_date)
            
            # Configurar evento de día completo
            event.begin = current_date
            event.make_all_day()
            
            # Añadir identificador único
            event.uid = str(uuid.uuid4())
            
            # Añadir regla de recurrencia anual sin fecha de fin
            event.extra.append(
                ContentLine(
                    name="RRULE",
                    value="FREQ=YEARLY"
                )
            )
            
            cal.events.add(event)
        
        # Avanzar al siguiente día
        current_date += timedelta(days=1)
    
    # Escribir a archivo
    filename = f"calendario_Metrico_desde_{start_year}.ics"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(cal.serialize())
    
    print(f"Archivo ICS '{filename}' generado exitosamente!")

# Uso de ejemplo
if __name__ == "__main__":
    # Generar calendario comenzando en 2024 con eventos que se repiten anualmente
    generate_metric_calendar_ics(2024)
    
    # Pruebas de fechas específicas
    test_dates = [
        datetime.date(2024, 3, 19),  # 29 de Ventôse, año 232
        datetime.date(2024, 9, 22),  # Inicio de año métrico
        datetime.date(2024, 12, 31),  # Final de año gregoriano
        datetime.date(2023, 9, 22),  # Inicio del año métrico 232
    ]
    
    for date in test_dates:
        print(f"\nFecha Gregoriana: {date}")
        metric_date = MetricCalendar.convert_date(date)
        print(MetricCalendar.generate_event_name(metric_date))

if __name__ == "__main__":
    # Generar el calendario para los próximos 10 años desde 2024
    start_year = 2024
    years_span = 10
    calendar = generate_metric_calendar_ics(start_year, years_span)

    # Guardar el calendario en un archivo ICS
    output_file = "metric_calendar.ics"
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(calendar.serialize_iter())
    print(f"Archivo ICS generado: {output_file}")