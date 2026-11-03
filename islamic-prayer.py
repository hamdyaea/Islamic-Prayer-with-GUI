#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
# Copyright (C) 2026 Hamdy Abou El Anein
# SPDX-License-Identifier: GPL-3.0-or-later
"""Prayer-time calculator with a modern Tkinter interface.

The original pyIslam calculation modules are retained without modification.
Results are indicative and must be checked against a trusted local timetable.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser

from pyIslam.praytimes import Prayer, PrayerConf
from pyIslam.qiblah import Qiblah

METHODS = {
    "University of Islamic Sciences, Karachi": 1,
    "Muslim World League": 2,
    "Egyptian General Authority of Survey": 3,
    "Umm al-Qura University, Makkah": 4,
    "Islamic Society of North America": 5,
}
ASR_SCHOOLS = {"Shafii": 1, "Hanafi": 2}
ROOT = Path(__file__).resolve().parent


def validate_parameters(latitude, longitude, timezone, method, asr_school, day):
    lat, lon, tz = float(latitude), float(longitude), float(timezone)
    if not -90 <= lat <= 90:
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not -180 <= lon <= 180:
        raise ValueError("Longitude must be between -180 and 180 degrees.")
    if not -12 <= tz <= 14:
        raise ValueError("UTC offset must be between -12 and +14 hours.")
    if method not in METHODS or asr_school not in ASR_SCHOOLS:
        raise ValueError("Choose a supported prayer calculation method.")
    chosen_date = date.fromisoformat(day)
    return lat, lon, tz, METHODS[method], ASR_SCHOOLS[asr_school], chosen_date


def calculate_prayer_times(latitude, longitude, timezone, method, asr_school, day):
    lat, lon, tz, zenith, asr, chosen_date = validate_parameters(
        latitude, longitude, timezone, method, asr_school, day
    )
    conf = PrayerConf(lon, lat, tz, zenith, asr)
    prayer = Prayer(conf, chosen_date)
    return {
        "Fajr": str(prayer.fajr_time()),
        "Sunrise": str(prayer.sherook_time()),
        "Dhuhr": str(prayer.dohr_time()),
        "Asr": str(prayer.asr_time()),
        "Maghrib": str(prayer.maghreb_time()),
        "Isha": str(prayer.ishaa_time()),
        "Qiblah (from north)": str(Qiblah(conf).sixty()),
    }


class PrayerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Islamic Prayer — Times and Qiblah")
        self.geometry("650x610")
        self.minsize(520, 520)
        self.configure(bg="#f4f6fa")
        frame = ttk.Frame(self, padding=22)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Islamic Prayer", font=("Sans", 19, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )
        ttk.Label(frame, text="Enter coordinates, UTC offset and calculation method.").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )
        self.entries = {}
        defaults = {
            "Latitude": "36.716667",
            "Longitude": "3.25",
            "UTC offset (hours)": "1",
            "Date (YYYY-MM-DD)": date.today().isoformat(),
        }
        for row, (label, value) in enumerate(defaults.items(), start=2):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame, width=36)
            entry.insert(0, value)
            entry.grid(row=row, column=1, sticky="ew", pady=5)
            self.entries[label] = entry

        ttk.Label(frame, text="Fajr / Isha method").grid(row=6, column=0, sticky="w", pady=5)
        self.method = ttk.Combobox(frame, values=list(METHODS), state="readonly")
        self.method.set("Egyptian General Authority of Survey")
        self.method.grid(row=6, column=1, sticky="ew", pady=5)
        ttk.Label(frame, text="Asr school").grid(row=7, column=0, sticky="w", pady=5)
        self.asr = ttk.Combobox(frame, values=list(ASR_SCHOOLS), state="readonly")
        self.asr.set("Shafii")
        self.asr.grid(row=7, column=1, sticky="ew", pady=5)

        buttons = ttk.Frame(frame)
        buttons.grid(row=8, column=0, columnspan=2, sticky="ew", pady=14)
        ttk.Button(buttons, text="Calculate prayer times", command=self.calculate).pack(
            side="left", padx=(0, 12)
        )
        ttk.Button(buttons, text="Find coordinates", command=lambda: webbrowser.open(
            "https://www.openstreetmap.org/"
        )).pack(side="left")
        self.result = tk.Text(frame, height=11, wrap="word", font=("Sans", 11),
                              background="#ffffff", relief="solid", borderwidth=1)
        self.result.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=6)
        self.result.configure(state="disabled")
        ttk.Label(frame, text=(
            "Indicative astronomical calculations; verify against your local "
            "mosque's timetable. Enter the correct UTC offset for the selected date."
        ), wraplength=550).grid(row=10, column=0, columnspan=2, sticky="w", pady=(9, 0))
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(9, weight=1)

    def calculate(self):
        try:
            result = calculate_prayer_times(
                self.entries["Latitude"].get(),
                self.entries["Longitude"].get(),
                self.entries["UTC offset (hours)"].get(),
                self.method.get(), self.asr.get(),
                self.entries["Date (YYYY-MM-DD)"].get(),
            )
        except (ValueError, ArithmeticError, OverflowError, TypeError) as exc:
            messagebox.showerror("Invalid parameters", str(exc), parent=self)
            return
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("end", "\n".join(f"{key:25} {value}" for key, value in result.items()))
        self.result.configure(state="disabled")


def main():
    window = PrayerWindow()
    window.mainloop()


if __name__ == "__main__":
    main()
