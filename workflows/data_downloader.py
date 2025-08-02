import argparse
import os
import time

from utils import Log, Parallel

from lld import AbstractDoc, DocFactory

log = Log("data_downloader")
N_BATCH = 8
DEFAULT_MAX_DELTA_T = 1_200


def get_worker(doc):
    def worker(doc=doc):
        log.debug(f"Working on {doc.id}.")
        is_hot = doc.download_all_data()
        if is_hot:
            log.info(f"✅ {doc.id}")
        return is_hot

    return worker


def get_doc_list(decade):
    doc_list = DocFactory.list_all()
    doc_list_for_decade = [doc for doc in doc_list if doc.decade == decade]
    return doc_list_for_decade


def main(max_delta_t, decade):
    max_delta_t = max_delta_t or DEFAULT_MAX_DELTA_T
    log.debug(f"{max_delta_t=:,.1f}s")
    log.debug(f"{decade=}")
    log.debug(f"{N_BATCH=}")
    assert os.path.exists(AbstractDoc.DIR_TEMP_DATA)

    t_start = time.time()
    doc_list = get_doc_list(decade)
    n_doc_list = len(doc_list)
    log.debug(f"{n_doc_list=:,}")

    i_doc = 0
    while i_doc < n_doc_list:
        workers = []
        for _ in range(N_BATCH):
            if i_doc >= n_doc_list:
                break
            doc = doc_list[i_doc]
            i_doc += 1
            workers.append(get_worker(doc=doc))

        Parallel.run(
            workers,
            max_threads=N_BATCH,
        )
        delta_t = time.time() - t_start
        if delta_t > max_delta_t:
            log.warning(
                f"⛔️ Stopping after. ⏰ {delta_t:.1f}s > {max_delta_t:.1f}s."
            )
            return
    log.info("⛔️🛑 Downloaded ALL pdfs.")


def get_options():
    parser = argparse.ArgumentParser(
        description="Download all data for the lk_legal_docs project."
    )
    parser.add_argument(
        "--max_delta_t",
        type=str,
        default="",
        help="Maximum time to run the downloader in seconds.",
    )
    parser.add_argument(
        "--decade",
        type=str,
        default="2020s",
        help="Decade to download data for.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()
    main(max_delta_t=options.max_delta_t, decade=options.decade)
