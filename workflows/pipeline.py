import sys

from utils import Log

from lld import (
    ActsByYearPage,
    BillsByYearPage,
    ExtraGazettesByYearPage,
    ReadMe,
)

log = Log("pipeline")


def main(max_n_hot):

    for year_page_cls in [
        ActsByYearPage,
        BillsByYearPage,
        ExtraGazettesByYearPage,
    ]:
        year_page_cls().run_pipeline(max_n_hot)

    ReadMe().build()


if __name__ == "__main__":
    max_n_hot = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    log.debug(f"{max_n_hot=}")
    main(max_n_hot)
