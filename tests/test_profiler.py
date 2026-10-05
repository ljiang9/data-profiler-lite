"""data-profiler-lite 单元测试。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from profiler import profile_csv, report  # noqa: E402

CSV = """name,age,city
Alice,30,Beijing
Bob,,Beijing
Carol,25,Shanghai
Dave,30,"""


class TestProfiler(unittest.TestCase):
    def test_row_count(self):
        p = profile_csv(CSV)
        self.assertEqual(p["row_count"], 4)

    def test_type_number(self):
        p = profile_csv(CSV)
        age = [c for c in p["columns"] if c["name"] == "age"][0]
        self.assertEqual(age["type"], "number")

    def test_missing(self):
        p = profile_csv(CSV)
        age = [c for c in p["columns"] if c["name"] == "age"][0]
        self.assertEqual(age["missing"], 1)

    def test_unique(self):
        p = profile_csv(CSV)
        city = [c for c in p["columns"] if c["name"] == "city"][0]
        self.assertEqual(city["unique"], 2)

    def test_top(self):
        p = profile_csv(CSV)
        city = [c for c in p["columns"] if c["name"] == "city"][0]
        self.assertEqual(city["top"][0], ("Beijing", 2))

    def test_report(self):
        self.assertIn("数据画像", report(CSV))


if __name__ == "__main__":
    unittest.main()
