import os
import time

from utils import Log

log = Log("AbstractDocPipelineExtendedDataMixin")


class AbstractDocPipelineExtendedDataMixin:
    @classmethod
    def scrape_all_extended_data(cls, max_dt):
        t_start = time.time()
        for doc in cls.list_all():
            try:
                doc.scrape_extended_data_for_doc()
            except Exception as e:
                log.error(f"Error scraping extended data for {doc}: {e}")

            dt = time.time() - t_start
            if dt > max_dt:
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        log.info("🛑 All extended data scraped.")

    def scrape_extended_data_for_doc(self):
        if not os.path.exists(self.text_path):
            self.extract_text()
