import shutil
import time

from utils import Log

log = Log("AbstractScraper")


class AbstractScraper:

    def get_metadata_scraper_name(self):
        raise NotImplementedError

    def gen_docs(self, traverse_random):
        raise NotImplementedError

    @staticmethod
    def __process_doc__(doc):

        is_hot = doc.is_hot()
        if is_hot:
            doc.write_metadata()

        # HACK-Cleanup
        if not doc.has_sources() and doc.is_stored_in_data():
            log.warning(f"[HACK] ❌ Deleting {doc.doc_num}. No sources.")
            shutil.rmtree(doc.dir_data, ignore_errors=True)

        return is_hot

    def run_metadata_scraper(self, max_delta_t, traverse_random):
        log.debug("-" * 80)
        scraper_name = self.get_metadata_scraper_name()
        log.info(f'🤖 Running metadata_scraper for "{scraper_name}".')
        n_hot = 0
        t_start = time.time()
        for doc in self.gen_docs(traverse_random):
            is_hot = self.__process_doc__(doc)
            if is_hot:
                n_hot += 1
                log.info(f"✅ ({n_hot}) Downloaded {doc}")

            delta_t = time.time() - t_start
            if delta_t > max_delta_t:
                log.debug(f"{n_hot=:,}")
                log.warning(
                    f"⛔️ Stopping. ⏰ {delta_t:.1f}s > {max_delta_t:.1f}s."
                )
                log.debug("-" * 80)
                return n_hot
        log.debug(f"{n_hot=:,}")
        log.info(f"⛔️🛑 Downloaded ALL {self.get_metadata_scraper_name()}.")
        log.debug("=" * 80)
        return n_hot
