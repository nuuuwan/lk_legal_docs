import os
import unittest

from utils_future import PDF

TEST_PDF_PATH = os.path.join("tests", "test_data", "test.pdf")


class TestCase(unittest.TestCase):
    def test_is_valid(self):
        pdf = PDF(TEST_PDF_PATH)
        self.assertTrue(pdf.is_valid())

        invalid_pdf_path = os.path.join(
            "tests", "test_data", "test-invalid.pdf"
        )
        invalid_pdf = PDF(invalid_pdf_path)
        self.assertFalse(invalid_pdf.is_valid())

    def test_compress(self):
        output_path = os.path.join(
            "tests", "test_data", "test-compressed.pdf"
        )
        if os.path.exists(output_path):
            os.remove(output_path)

        PDF(TEST_PDF_PATH).compress(output_path)

        size_before = os.path.getsize(TEST_PDF_PATH)
        size_after = os.path.getsize(output_path)

        self.assertEqual(size_before, 339_235)
        self.assertLess(size_after, size_before * 0.75)

        PDF(output_path).compress()
        size_after_again = os.path.getsize(output_path)
        self.assertLess(size_after_again, size_after * 1.1)
        self.assertGreater(size_after_again, size_after * 0.9)

    def test_extract_text(self):
        output_txt_path = os.path.join(
            "tests", "test_data", "test-extracted.txt"
        )
        if os.path.exists(output_txt_path):
            os.remove(output_txt_path)

        PDF(TEST_PDF_PATH).extract_text(output_txt_path)
        file_size = os.path.getsize(output_txt_path)
        self.assertEqual(file_size, 24_078)
