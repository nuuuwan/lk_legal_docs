import sys

from utils import Log

from lld import ByYearPage, DocFactory, ReadMe

log = Log("pipeline")


def main(max_n_hot):
    log.debug(f"{max_n_hot=}")
    if max_n_hot > 0:
        for doc_cls in DocFactory.list_all_cls():
            doc_cls.cleanup()
            ByYearPage(doc_cls).run_pipeline(max_n_hot)
    ReadMe().build()


if __name__ == "__main__":
    max_n_hot = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(max_n_hot)
