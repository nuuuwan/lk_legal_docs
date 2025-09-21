import time

from utils import Log, Parallel

log = Log("AbstractDocPipelineMetadataMixin")


class AbstractDocPipelineMetadataMixin:
    BATCH_SIZE = 4
    MAX_THREADS = 4

    @staticmethod
    def __log_processed_doc__(docs, dt):
        n_docs = len(docs)
        log.info(f"🛑 Processed {n_docs:,} docs in {dt:,.1f}s")

    @classmethod
    def gen_doc_batches_for_scrape_all_metadata(cls):
        current_batch = []
        for doc in cls.gen_docs():
            current_batch.append(doc)
            if len(current_batch) >= cls.BATCH_SIZE:
                yield current_batch
                current_batch = []

        if current_batch:
            yield current_batch

    @classmethod
    def process_batch_for_scrape_all_metadata(cls, doc_batch):
        processed_doc_list = []

        def process_doc(doc):
            try:
                doc.write()
                return doc
            except Exception as e:
                log.error(f"Error processing {doc}: {e}")
                return None

        processed_doc_list = Parallel.map(
            process_doc,
            doc_batch,
            max_threads=cls.MAX_THREADS,
        )
        processed_doc_list = [
            doc for doc in processed_doc_list if doc is not None
        ]

        return processed_doc_list

    @classmethod
    def scrape_all_metadata(cls, max_dt):
        log.debug(f"BATCH_SIZE={cls.BATCH_SIZE}")
        log.debug(f"MAX_THREADS={cls.MAX_THREADS}")
        t_start = time.time()
        docs = []
        dt = 0
        for doc_batch in cls.gen_doc_batches_for_scrape_all_metadata():
            processed_doc_list = cls.process_batch_for_scrape_all_metadata(
                doc_batch
            )
            docs.extend(processed_doc_list)

            dt = time.time() - t_start
            if dt > max_dt:
                cls.__log_processed_doc__(docs, dt)
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        cls.__log_processed_doc__(docs, dt)
        log.info("🛑 All docs processed.")
