import datetime
from datetime import timedelta
import uuid
from ics import Calendar, Event


class MetricCalendar:
    """
    Clase para manejar la conversión y cálculos del Calendario Republicano Francés
    (Calendario Métrico Francés) usando la regla de Romme desde el 22 de septiembre de 1792.
    """
    EPOCH = datetime.date(1792, 9, 22)  # 1 de Vendémiaire, Año 1

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
        ('Fructidor', 'Mes de los frutos', 'Fruits'),
    ]

    COMPLEMENTARY_DAYS = [
        'Primero de Días Complementarios',
        'Segundo de Días Complementarios',
        'Tercero de Días Complementarios',
        'Cuarto de Días Complementarios',
        'Quinto de Días Complementarios',
        'Jour de la Révolution',  # Solo en años sextiles (bisiestos)
    ]

    @classmethod
    def is_sextile_year(cls, metric_year):
        """
        Determinar si un año es sextil (bisiesto) según la regla de Romme:
        divisible por 4, excepto múltiplos de 100 que no sean múltiplos de 400.
        """
        return (metric_year % 4 == 0 and metric_year % 100 != 0) or (metric_year % 400 == 0)

    @classmethod
    def days_in_year(cls, metric_year):
        return 366 if cls.is_sextile_year(metric_year) else 365

    @classmethod
    def convert_date(cls, gregorian_date):
        """
        Convertir una fecha gregoriana (>= 1792-09-22) a fecha del Calendario Republicano Francés.
        """
        days_since_epoch = (gregorian_date - cls.EPOCH).days
        if days_since_epoch < 0:
            return None

        metric_year = 1
        while True:
            year_length = cls.days_in_year(metric_year)
            if days_since_epoch < year_length:
                break
            days_since_epoch -= year_length
            metric_year += 1

        day_of_year = days_since_epoch + 1

        if day_of_year > 360:
            complementary_day = day_of_year - 360
            return {
                'year': metric_year,
                'month_name': 'Días Complementarios',
                'month_spanish_desc': 'Jours complémentaires',
                'day': complementary_day,
                'day_name': cls.COMPLEMENTARY_DAYS[complementary_day - 1],
                'is_complementary': True,
                'total_metric_day': day_of_year,
            }

        month_index = (day_of_year - 1) // 30
        day_in_month = (day_of_year - 1) % 30 + 1
        month_name, spanish_desc, _ = cls.MONTH_DETAILS[month_index]

        return {
            'year': metric_year,
            'month_name': month_name,
            'month_spanish_desc': spanish_desc,
            'month_index': month_index + 1,
            'day': day_in_month,
            'is_complementary': False,
            'total_metric_day': day_of_year,
        }

    @classmethod
    def generate_event_name(cls, metric_date):
        """
        Generar nombre descriptivo para el evento.
        """
        if metric_date is None:
            return "Fecha fuera del rango válido"

        if metric_date['is_complementary']:
            return f"{metric_date['day_name']} / Año {metric_date['year']}"

        return f"Día {metric_date['day']} de {metric_date['month_name']} / Año {metric_date['year']}"


def generate_metric_calendar_ics(start_year, years_span=10):
    """
    Genera un objeto Calendar (ICS) para un rango de años basado en el calendario métrico francés.
    """
    cal = Calendar()
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(start_year + years_span - 1, 12, 31)

    current_date = start_date
    while current_date <= end_date:
        metric_date = MetricCalendar.convert_date(current_date)
        if metric_date:
            event = Event()
            event.name = MetricCalendar.generate_event_name(metric_date)
            event.begin = current_date
            event.make_all_day()
            event.uid = str(uuid.uuid4())
            cal.events.add(event)
        current_date += timedelta(days=1)

    return cal


if __name__ == "__main__":
    # Pruebas de fechas específicas
    test_dates = [
        datetime.date(2023, 9, 23),  # 1 de Vendémiaire, Año 232
        datetime.date(2024, 3, 19),  # 29 de Ventôse, Año 232
        datetime.date(2024, 9, 22),  # Jour de la Révolution, Año 232 (año sextil)
        datetime.date(2024, 9, 23),  # 1 de Vendémiaire, Año 233
        datetime.date(2024, 12, 31), # 10 de Nivôse, Año 233
    ]

    for date in test_dates:
        metric_date = MetricCalendar.convert_date(date)
        print(f"{date} -> {MetricCalendar.generate_event_name(metric_date)}")

    # Generar el calendario para 10 años desde 2024
    start_year = 2024
    years_span = 10
    calendar = generate_metric_calendar_ics(start_year, years_span)

    output_file = "metric_calendar.ics"
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(calendar.serialize_iter())
    print(f"\nArchivo ICS generado: {output_file}")