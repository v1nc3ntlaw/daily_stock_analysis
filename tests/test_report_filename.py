# -*- coding: utf-8 -*-
"""Report filename: report_<YYYYMMDDHHMM>_<source>_<CODE|Nstocks>.md."""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.litellm_stub import ensure_litellm_stub

ensure_litellm_stub()

from src.core.pipeline import StockAnalysisPipeline


class TestReportFilename(unittest.TestCase):
    _FROZEN = datetime(2030, 1, 2, 12, 34, 0)

    def _build(self, codes, source=None):
        with patch("src.core.pipeline.datetime") as mock_datetime:
            mock_datetime.now.return_value = self._FROZEN
            return StockAnalysisPipeline._build_report_filename(codes, source)

    def test_single_stock_uses_code(self):
        self.assertEqual(self._build(["MU"], "manual"), "report_203001021234_manual_MU.md")

    def test_multiple_stocks_use_count(self):
        self.assertEqual(
            self._build(["601800", "600436", "MU"], "watchlist"),
            "report_203001021234_watchlist_3stocks.md",
        )

    def test_portfolio_source(self):
        self.assertEqual(
            self._build(["AAPL", "NVDA"], "portfolio"),
            "report_203001021234_portfolio_2stocks.md",
        )

    def test_missing_source_defaults_to_manual(self):
        self.assertEqual(self._build(["AAPL"]), "report_203001021234_manual_AAPL.md")

    def test_code_keeps_only_letters_and_digits(self):
        self.assertEqual(self._build(["2330.TW"], "manual"), "report_203001021234_manual_2330TW.md")
        self.assertEqual(self._build(["000300.CSI"], "manual"), "report_203001021234_manual_000300CSI.md")
        self.assertEqual(self._build(["hk00700"], "manual"), "report_203001021234_manual_hk00700.md")


if __name__ == "__main__":
    unittest.main()
