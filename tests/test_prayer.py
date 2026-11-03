#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline regression tests for the original pyIslam astronomical calculations."""
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[1]
module = runpy.run_path(str(ROOT / "islamic-prayer.py"), run_name="prayer_tests")
calculate = module["calculate_prayer_times"]
validate = module["validate_parameters"]
METHOD = "Egyptian General Authority of Survey"


class PrayerTests(unittest.TestCase):
    def test_known_location_and_date(self):
        result = calculate("46.8", "7.15", "1", METHOD, "Shafii", "2026-11-03")
        self.assertEqual(result["Fajr"], "05:25:30")
        self.assertEqual(result["Sunrise"], "07:17:28")
        self.assertIn("Qiblah", next(iter(k for k in result if "Qiblah" in k)))

    def test_reject_invalid_latitude(self):
        with self.assertRaises(ValueError):
            validate("95", "7", "1", METHOD, "Shafii", "2026-11-03")

    def test_reject_invalid_longitude(self):
        with self.assertRaises(ValueError):
            validate("46", "-181", "1", METHOD, "Shafii", "2026-11-03")

    def test_reject_bad_date(self):
        with self.assertRaises(ValueError):
            validate("46", "7", "1", METHOD, "Shafii", "2026-02-30")

    def test_reject_invalid_timezone(self):
        with self.assertRaises(ValueError):
            validate("46", "7", "20", METHOD, "Shafii", "2026-11-03")


if __name__ == "__main__":
    unittest.main()
