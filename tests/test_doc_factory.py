import unittest

from lld import DocFactory


class TestCase(unittest.TestCase):
    def test_list_all(self):
        doc_list = DocFactory.list_all()
        self.assertGreater(len(doc_list), 40_000)

    def test_list_all_first_doc(self):
        doc_list = DocFactory.list_all()
        first_doc = doc_list[-1]
        self.assertEqual(
            first_doc.to_dict(),
            {
                "doc_type_name": "acts",
                "date": "1981-01-22",
                "description": "Parliamentary Elections",
                "lang_to_source_url": {
                    "si": "https://documents.gov.lk"
                    + "/view/acts/1981/1/01-1981_S.pdf"
                },
                "doc_num": "01/1981",
                "id": "01-1981",
                "dir_data": "data/acts/1981/01-1981",
            },
        )

    def test_total_data_size(self):
        size = DocFactory.get_total_data_size()
        self.assertGreater(size, 10_000_000)
