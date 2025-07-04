import unittest

from lld import ActMetadata

TEST_ACT_METADATA = ActMetadata(
    act_num="32/2024",
    date="2024-06-18",
    description="International Institute of Theravadha (Incorporation)",
    source_url_en="https://documents.gov.lk/view/acts/2024/6/32-2024_E.pdf",
    source_url_si="https://documents.gov.lk/view/acts/2024/6/32-2024_S.pdf",
    source_url_ta="https://documents.gov.lk/view/acts/2024/6/32-2024_T.pdf",
)


class TestCase(unittest.TestCase):
    def test_download_all(self):
        TEST_ACT_METADATA.download_all()

    def test_write(self):
        TEST_ACT_METADATA.write()
