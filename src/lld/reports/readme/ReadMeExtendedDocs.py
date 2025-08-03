from utils_future import Markdown


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
        return None

    @staticmethod
    def add_totals(json_data_list):
        total_n_docs = sum(data["n_docs"] for data in json_data_list)
        total_n_docs_with_pdfs = sum(
            data["n_docs_with_pdfs"] for data in json_data_list
        )
        total_n_docs_with_pdfs_fail = sum(
            data["n_docs_with_pdfs_fail"] for data in json_data_list
        )
        total_n_pdfs = sum(data["n_pdfs"] for data in json_data_list)
        total_file_size = sum(
            data["total_file_size"] for data in json_data_list
        )

        json_data_list.append(
            {
                "decade": "Total",
                "n_docs": total_n_docs,
                "n_docs_with_pdfs": total_n_docs_with_pdfs,
                "n_docs_with_pdfs_fail": total_n_docs_with_pdfs_fail,
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
            n_docs_with_pdfs = json_data["n_docs_with_pdfs"]
            p_progress = n_docs_with_pdfs / n_docs
            total_file_size_g = json_data["total_file_size"] / 1_000_000_000
            complete_emoji = "✅" if n_docs == n_docs_with_pdfs else ""

            decade_md = json_data["decade"]
            if decade_md != "Total":
                remote_dir_url = json_data["remote_dir_url"]
                decade_md = f"[{decade_md}]({remote_dir_url})"

            data = dict(
                decade=decade_md + complete_emoji,
                n_docs=f"{n_docs:,}",
                n_docs_with_pdfs=f"{n_docs_with_pdfs:,}",
                p_progress=format_percent(p_progress),
                n_pdfs=f"{json_data['n_pdfs']:,}",
                total_file_size_g=f"{total_file_size_g:,.1f} GB",
            )

            if json_data["decade"] == "Total":
                self.make_bold(data)

            data_list.append(data)

        return data_list

    def get_lines_for_extended_data_table(self):
        data_list = self.get_extended_data_list()
        return Markdown.table(data_list) + [""]

    def get_lines_for_extended_docs(self):
        return (
            [
                "## Summary of Extended Data",
                "",
            ]
            + self.get_lines_for_extended_data_table()
            + ["(✅ = All published documents have been downloaded.)", ""]
        )
