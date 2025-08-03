import argparse
import os
import random
import time
from multiprocessing import Pool, cpu_count

from utils import Log

from lld import AbstractDoc, DocFactory

log = Log("data_downloader")
N_BATCH = 8


def worker(doc):
    is_hot = doc.download_all_data()
    if is_hot:
        log.info(f"✅ {doc.id}")
        log.debug("-" * 32)
    return is_hot


def get_doc_list(decade):
    doc_list = DocFactory.list_all()
    doc_list_for_decade = [doc for doc in doc_list if doc.decade == decade]
    if random.random() < 0.5:
        random.shuffle(doc_list_for_decade)
    return doc_list_for_decade


def download(max_delta_t, decade):
    t_start = time.time()
    doc_list = get_doc_list(decade)
    n_doc_list = len(doc_list)
    log.debug(f"{n_doc_list=:,}")

    n_cpu = cpu_count()
    log.debug(f"{n_cpu=:,}")
    i_doc = 0
    while i_doc < n_doc_list:
        docs_for_processing = []
        for _ in range(N_BATCH):
            if i_doc >= n_doc_list:
                break
            doc = doc_list[i_doc]
            i_doc += 1
            docs_for_processing.append(doc)

        Pool(n_cpu).map(worker, docs_for_processing)
        delta_t = time.time() - t_start
        log.debug(f"⏰ {delta_t=:,.1f}s")
        if delta_t > max_delta_t:
            log.warning(
                f"⛔️ Stopping after. ⏰ {delta_t:.1f}s > {max_delta_t:.1f}s."
            )
            return
    log.info("⛔️🛑 Downloaded ALL pdfs.")


def cleanup_legacy():
    for file_path in [
        "all.json",
        "latest-100.json",
        "temp_data_summary.json",
    ]:
        if os.path.exists(file_path):
            os.remove(file_path)
            log.debug(f"Removed legacy file: {file_path}")


def build_summary(decade):
    cleanup_legacy()
    DocFactory.write_all(decade)
    DocFactory.write_temp_data_summary(decade)


def main(max_delta_t, decade):
    log.debug(f"{max_delta_t=:,.1f}s")
    log.debug(f"{decade=}")
    log.debug(f"{N_BATCH=}")
    assert os.path.exists(AbstractDoc.DIR_TEMP_DATA)

    download(max_delta_t, decade)
    build_summary(decade)


def get_options():
    parser = argparse.ArgumentParser(
        description="Download all data for the lk_legal_docs project."
    )
    parser.add_argument(
        "--max_delta_t",
        type=int,
        default=1_200,
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
