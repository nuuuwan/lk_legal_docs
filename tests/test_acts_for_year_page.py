import unittest

from lld import ActsForYearPage


class TestCase(unittest.TestCase):
    def test_get_metadata_list(self):
        page = ActsForYearPage(
            "https://documents.gov.lk/view/acts/acts_2024.html"
        )
        act_metadata_list = page.get_metadata_list()
        self.assertEqual(len(act_metadata_list), 32)
        act_metadata = act_metadata_list[0]
        self.assertEqual(act_metadata.doc_num, "32/2024")
        self.assertEqual(act_metadata.date, "2024-06-18")
        self.assertEqual(
            act_metadata.description,
            "International Institute of Theravadha (Incorporation)",
        )
        self.assertEqual(
            act_metadata.source_url_en,
            "https://documents.gov.lk/view/acts/2024/6/32-2024_E.pdf",
        )
        self.assertEqual(
            act_metadata.source_url_si,
            "https://documents.gov.lk/view/acts/2024/6/32-2024_S.pdf",
        )
        self.assertEqual(
            act_metadata.source_url_ta,
            "https://documents.gov.lk/view/acts/2024/6/32-2024_T.pdf",
        )
