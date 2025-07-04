import sys

from utils import Log

from lld import ActsByYearPage, ReadMe

log = Log('pipeline')


def download_acts(max_n_hot):
    acts_by_year_page = ActsByYearPage()
    acts_for_year_page_list = acts_by_year_page.get_acts_for_year_page_list()
    n = 0
    n_hot = 0
    for acts_for_year_page in acts_for_year_page_list:
        act_metadata_list = acts_for_year_page.get_act_metadata_list()
        for act_metadata in act_metadata_list:
            if n_hot >= max_n_hot:
                log.info(f'🛑 Already downloaded {n_hot} new acts.')
                return

            is_hot = act_metadata.download_all()
            logger = log.info if is_hot else log.debug
            emoji = '🟢' if is_hot else '⚪️'
            logger(f'{emoji} {n_hot}/{max_n_hot}) {act_metadata.act_num}')
            act_metadata.write()
            n += 1
            if is_hot:
                n_hot += 1
               

if __name__ == '__main__':
    max_n_hot = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    log.debug(f'{max_n_hot=}')
    download_acts(max_n_hot)
    ReadMe().build()
