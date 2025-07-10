import os
import sys
import time

from utils import Log, Parallel

from lld import AbstractDoc, DocFactory

DEFAULT_MAX_DELTA_T = 15 * 60


log = Log("data_scraper")
N_BATCH = 8


def get_worker(doc):
    def worker(doc=doc):
        is_hot = doc.download_all_data()
        if is_hot:
            log.info(f"✅ {doc.id}")
        return is_hot

    return worker


def main(max_delta_t):
    log.debug(f"{max_delta_t=:,.1f}s")
    log.debug(f"{N_BATCH=}")

    assert os.path.exists(AbstractDoc.DIR_TEMP_DATA)

    t_start = time.time()
    doc_list = DocFactory.list_all()
    n_doc_list = len(doc_list)
    log.debug(f"{n_doc_list=:,}")

    i_doc = 0
    n_hot = 0
    while i_doc < n_doc_list:
        workers = []
        for _ in range(N_BATCH):
            if i_doc >= n_doc_list:
                break
            doc = doc_list[i_doc]
            i_doc += 1
            workers.append(get_worker(doc=doc))

        results = Parallel.run(
            workers,
            max_threads=N_BATCH,
        )
        n_hot += sum([1 for r in results if r])
        delta_t = time.time() - t_start
        speed = n_hot / delta_t
        log.debug(f"{n_hot=:,}, {speed=:.2f}/s")
        if delta_t > max_delta_t:
            log.warning(
                f"⛔️ Stopping after. ⏰ {delta_t:.1f}s > {max_delta_t:.1f}s."
            )
            return
    log.info("⛔️🛑 Downloaded ALL pdfs.")
    return


if __name__ == "__main__":
    main(
        max_delta_t=(
            int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MAX_DELTA_T
        )
    )
