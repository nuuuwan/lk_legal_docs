from utils import File, Log, Time, TimeFormat
from lld.www import ActMetadata
log = Log('ReadMe')


class ReadMe:
    PATH = 'README.md'

    def __init__(self):
        self.time_str = TimeFormat.TIME.format(Time.now())


    @staticmethod
    def get_act_metadata_md(act_metadata):
        return f'- [{act_metadata.act_num}] '+f'[{act_metadata.description}]({act_metadata.dir_data})'

    @property 
    def lines_acts(self):
        act_metadata_list = ActMetadata.list_all()
        n = len(act_metadata_list)
        return [
            f'## Acts ({n:,})',
            "",
        ] + [
            ReadMe.get_act_metadata_md(act_metadata) for act_metadata in act_metadata_list
        ] + [""]

    @property
    def lines(self):
        return [
            "# Legal Documents - #SriLanka 🇱🇰" ,
            "",
            f"*Last updated {self.time_str}*.",
            "",
            "Legal Gazettes, Extra-Gazettes, Acts, Bills and other documents"
            + " scraped from [documents.gov.lk](https://documents.gov.lk).",
            "",
        ] + self.lines_acts

    def build(self):
        File(self.PATH).write('\n'.join(self.lines))
        log.info(f'Wrote {len(self.lines)} lines to {self.PATH}.')