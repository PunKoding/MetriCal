#!/usr/bin/env python3
import datetime
from dataclasses import dataclass
from datetime import date, timedelta, timezone
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class RepublicanDate:
    year: int
    month: Optional[int]
    day: int
    month_name: str
    month_desc: str
    day_of_year: int
    is_complementary: bool
    complementary_name: Optional[str] = None
    decade_day: Optional[str] = None

    @property
    def summary(self) -> str:
        if self.is_complementary:
            return f"{self.complementary_name} — Año {self.year}"
        return f"{self.day} de {self.month_name} — Año {self.year}"

    @property
    def description(self) -> str:
        if self.is_complementary:
            return f"Día complementario {self.day} ({self.complementary_name}), Año {self.year} del Calendario Republicano Francés."
        return f"{self.decade_day}, {self.day} de {self.month_name} ({self.month_desc}), Año {self.year}."


class FrenchRepublicanCalendar:
    """Conversor del Calendario Republicano Francés usando la regla de Romme."""

    EPOCH = date(1792, 9, 22)

    MONTHS = (
        ("Vendémiaire", "Mes de la vendimia"),
        ("Brumaire", "Mes de la niebla"),
        ("Frimaire", "Mes del frío"),
        ("Nivôse", "Mes de la nieve"),
        ("Pluviôse", "Mes de la lluvia"),
        ("Ventôse", "Mes del viento"),
        ("Germinal", "Mes de la germinación"),
        ("Floréal", "Mes de las flores"),
        ("Prairial", "Mes de los prados"),
        ("Messidor", "Mes de la cosecha"),
        ("Thermidor", "Mes del calor"),
        ("Fructidor", "Mes de los frutos"),
    )

    COMPLEMENTARY_DAYS = (
        "Jour de la Vertu (Día de la Virtud)",
        "Jour du Génie (Día del Genio)",
        "Jour du Travail (Día del Trabajo)",
        "Jour de l'Opinion (Día de la Opinión)",
        "Jour des Récompenses (Día de las Recompensas)",
        "Jour de la Révolution (Día de la Revolución)",
    )

    DECADE_DAYS = (
        "Primidi", "Duodi", "Tridi", "Quartidi", "Quintidi",
        "Sextidi", "Septidi", "Octidi", "Nonidi", "Décadi",
    )

    @staticmethod
    def is_sextile(year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @classmethod
    def days_in_year(cls, year: int) -> int:
        return 366 if cls.is_sextile(year) else 365

    @classmethod
    def from_gregorian(cls, g_date: date) -> RepublicanDate:
        days_since_epoch = (g_date - cls.EPOCH).days
        if days_since_epoch < 0:
            raise ValueError("La fecha debe ser igual o posterior al 22 de septiembre de 1792.")

        year = 1
        while True:
            year_len = cls.days_in_year(year)
            if days_since_epoch < year_len:
                break
            days_since_epoch -= year_len
            year += 1

        day_of_year = days_since_epoch + 1

        if day_of_year > 360:
            comp_day = day_of_year - 360
            return RepublicanDate(
                year=year,
                month=None,
                day=comp_day,
                month_name="Jours complémentaires",
                month_desc="Días complementarios",
                day_of_year=day_of_year,
                is_complementary=True,
                complementary_name=cls.COMPLEMENTARY_DAYS[comp_day - 1],
            )

        month_idx = (day_of_year - 1) // 30
        day_in_month = (day_of_year - 1) % 30 + 1
        month_name, month_desc = cls.MONTHS[month_idx]
        decade_day = cls.DECADE_DAYS[(day_in_month - 1) % 10]

        return RepublicanDate(
            year=year,
            month=month_idx + 1,
            day=day_in_month,
            month_name=month_name,
            month_desc=month_desc,
            day_of_year=day_of_year,
            is_complementary=False,
            decade_day=decade_day,
        )


def _ics_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _add_years(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(year=d.year + years, day=28)


def generate_ics_next_years(years: int = 5, output_path: Path = Path("calendario_republicano.ics")) -> None:
    dtstamp = datetime.datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    start_date = date.today()
    end_date = _add_years(start_date, years)

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//MetriCal//Calendario Republicano Frances//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Calendario Republicano Francés",
    ]

    current = start_date
    while current <= end_date:
        rep = FrenchRepublicanCalendar.from_gregorian(current)
        dtstart = current.strftime("%Y%m%d")
        dtend = (current + timedelta(days=1)).strftime("%Y%m%d")
        uid = f"metrical-{dtstart}@republican-calendar"

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART;VALUE=DATE:{dtstart}",
            f"DTEND;VALUE=DATE:{dtend}",
            f"SUMMARY:{_ics_escape(rep.summary)}",
            f"DESCRIPTION:{_ics_escape(rep.description)}",
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ])
        current += timedelta(days=1)

    lines.append("END:VCALENDAR")
    output_path.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")
    print(f"Generado: {output_path.resolve()} ({start_date.isoformat()} a {end_date.isoformat()})")


if __name__ == "__main__":
    generate_ics_next_years(years=5)