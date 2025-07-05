import sys

from utils import Log

from lld import Act, Bill, ByYearPage, ExtraGazette, ReadMe

log = Log("pipeline")


def main(max_n_hot):

    for doc_cls in [
        Act,
        Bill,
        ExtraGazette,
    ]:
        ByYearPage(doc_cls).run_pipeline(max_n_hot)

    ReadMe().build()


if __name__ == "__main__":
    max_n_hot = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    log.debug(f"{max_n_hot=}")
    main(max_n_hot)
