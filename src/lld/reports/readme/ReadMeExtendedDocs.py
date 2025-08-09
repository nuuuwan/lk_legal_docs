from utils import Log

from utils_future import Markdown

log = Log("ReadMeExtendedDocs")


def format_percent(p: float) -> str:
    if 0.999 < p < 1.0:
        return ">99.9%"

    if p == 1.0:
        return "100%"

    return f"{p:,.1%}"


class ReadMeExtendedDocs:

    DECADES = ["2020s", "2010s", "2000s", "1990s", "1980s"]

    @staticmethod
    def get_json_data_from_url(url):
        import requests

        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        log.error(f"Failed to fetch data from {url}: {response.status_code}")
        return None

    @staticmethod
    def add_totals(json_data_list):
        total_n_docs = sum(data["n_docs"] for data in json_data_list)
        total_all_downloaded = sum(
            data["n_all_downloaded"] for data in json_data_list
        )
        total_some_failed = sum(
            data["n_some_failed"] for data in json_data_list
        )
        total_all_failed = sum(data["n_all_failed"] for data in json_data_list)
        total_queued = sum(data["n_queued"] for data in json_data_list)

        total_n_pdfs = sum(data["n_pdfs"] for data in json_data_list)
        total_file_size = sum(
            data["total_file_size"] for data in json_data_list
        )

        json_data_list.append(
            {
                "decade": "Total",
                "n_docs": total_n_docs,
                "n_all_downloaded": total_all_downloaded,
                "n_some_failed": total_some_failed,
                "n_all_failed": total_all_failed,
                "n_queued": total_queued,
                "n_pdfs": total_n_pdfs,
                "total_file_size": total_file_size,
            }
        )

    def get_raw_remote_dir_url(self, decade: str) -> str:
        return (
            "https://raw.githubusercontent.com"
            + "/nuuuwan/lk_legal_docs_data"
            + f"/refs/heads/data_{decade}"
        )

    def get_remote_dir_url(self, decade: str) -> str:
        return (
            "https://github.com"
            + "/nuuuwan/lk_legal_docs_data"
            + f"/tree/data_{decade}/data"
        )

    def get_json_data_list(self):
        json_data_list = []
        for decade in self.DECADES:
            raw_remote_dir_url = self.get_raw_remote_dir_url(decade)
            url = raw_remote_dir_url + "/temp_data_summary.json"
            remote_dir_url = self.get_remote_dir_url(decade)

            json_data = self.get_json_data_from_url(url)
            if not json_data:
                continue
            json_data_list.append(
                dict(decade=decade, remote_dir_url=remote_dir_url, **json_data)
            )
        self.add_totals(json_data_list)
        return json_data_list

    @staticmethod
    def make_bold(data: dict):
        for key in data:
            data[key] = f"**{data[key]}**"

    def get_extended_data_list(self):
        data_list = []
        for json_data in self.get_json_data_list():
            n_docs = json_data["n_docs"]
            n_all_downloaded = json_data["n_all_downloaded"]
            n_some_failed = json_data["n_some_failed"]
            n_all_failed = json_data["n_all_failed"]
            n_queued = json_data["n_queued"]

            n_complete = n_all_downloaded + n_some_failed + n_all_failed
            p_complete = n_complete / n_docs

            total_file_size_g = json_data["total_file_size"] / 1_000_000_000

            decade_md = json_data["decade"]
            if decade_md != "Total":
                remote_dir_url = json_data["remote_dir_url"]
                decade_md = f"[{decade_md}]({remote_dir_url})"

            data = dict(
                decade=decade_md,
                p_complete=format_percent(p_complete),
                n_docs=f"{n_docs:,}",
                n_pdfs=f"{json_data['n_pdfs']:,}",
                total_file_size_g=f"{total_file_size_g:,.1f} GB",
                n_all_downloaded=f"{n_all_downloaded:,}",
                n_some_failed=f"{n_some_failed:,}",
                n_all_failed=f"{n_all_failed:,}",
                n_queued=f"{n_queued:,}",
            )

            if json_data["decade"] == "Total":
                self.make_bold(data)

            data_list.append(data)

        return data_list

    def get_lines_for_extended_data_table(self):
        data_list = self.get_extended_data_list()
        return Markdown.table(data_list) + [""]

    def get_lines_for_extended_docs(self):
        return [
            "## Summary of Extended Data",
            "",
        ] + self.get_lines_for_extended_data_table()
