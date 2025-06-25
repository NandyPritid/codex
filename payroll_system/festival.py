"""Festival helpers.

This module exposes :func:`get_festivals` which returns a dictionary of
festival names mapped to ``datetime`` objects.  If the optional
``panchangam`` library is unavailable, it falls back to reading
``test_data/festivals.csv`` where newcomers can manually edit festival
dates without touching the code.
"""
"""Utility functions for Bengali festival calculations."""

from datetime import datetime
from pathlib import Path
import csv

try:
    from panchangam import compute_festival_list
    PANCHANG_AVAILABLE = True
except Exception:  # fallback if panchangam missing or errors
    PANCHANG_AVAILABLE = False


DEFAULT_FESTIVALS = {
    # These approximate 2025 dates can be edited in test_data/festivals.csv
    "Jamai Shasthi": datetime(2025, 5, 24),
    "Akshay Tritiya": datetime(2025, 5, 1),
    "Rath Yatra": datetime(2025, 7, 3),
    "Ulto Rath": datetime(2025, 7, 11),
    "Janmashtami": datetime(2025, 8, 16),
    "Durga Puja Saptami": datetime(2025, 10, 1),
    "Durga Puja Dashami": datetime(2025, 10, 5),
    "Dhanteras": datetime(2025, 10, 21),
    "Bhai Phonta": datetime(2025, 10, 23),
    "Jagadhatri Puja": datetime(2025, 11, 1),
    "Kali Puja": datetime(2025, 10, 20),
    "Christmas": datetime(2025, 12, 25),
    "Saraswati Puja": datetime(2025, 2, 3),
    "Holi": datetime(2025, 3, 14),
    "Annapurna Puja": datetime(2025, 3, 17),
    "Vishwakarma Puja": datetime(2025, 9, 17),
    "Rakhi": datetime(2025, 8, 9),
    "Poila Boishakh": datetime(2025, 4, 14),
    "New Year": datetime(2025, 1, 1),
}


def get_festivals(year: int = 2025) -> dict:
    """Return a mapping of festival names to ``datetime`` objects."""
    festivals = {}
    if PANCHANG_AVAILABLE:
        try:
            # Actual panchangam usage would populate `festivals`
            festivals = compute_festival_list(year)
        except Exception:
            festivals = {}

    if not festivals:
        csv_path = Path("test_data/festivals.csv")
        if csv_path.exists():
            with csv_path.open() as f:
                reader = csv.DictReader(f)
                festivals = {row["name"]: datetime.fromisoformat(row["date"]) for row in reader}
        else:
            festivals = {name: date.replace(year=year) for name, date in DEFAULT_FESTIVALS.items()}
    return festivals
