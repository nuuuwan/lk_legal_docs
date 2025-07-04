import unittest

from lld.www.acts.ActsByYearPage import ActsByYearPage


class TestCase(unittest.TestCase):
    def test_get_acts_for_year_page_list(self):
        page = ActsByYearPage()
        acts_for_year_page_list = page.get_acts_for_year_page_list()
        self.assertGreater(len(acts_for_year_page_list), 10)
        self.assertEqual(
            acts_for_year_page_list[0].url,
            "https://documents.gov.lk/view/acts/acts_2025.html",
        )
