import unittest

from lld.www.acts.ActsByYearPage import ActsByYearPage


class TestCase(unittest.TestCase):
    def test_get_acts_for_year_page_list(self):
        page = ActsByYearPage()
        acts_for_year_page_list = page.get_for_year_page_list()
        self.assertEqual(len(acts_for_year_page_list), 45)
        self.assertEqual(
            acts_for_year_page_list[-1].url,
            "https://documents.gov.lk/view/acts/acts_1981.html",
        )
