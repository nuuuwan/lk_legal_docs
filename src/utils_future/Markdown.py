class Markdown:

    @staticmethod
    def get_sep(key: str) -> str:
        if key in ["n"]:
            return "--:"

        return ":--"

    @staticmethod
    def table(d_list: list[dict]) -> list[str]:
        if not d_list:
            return []

        keys = d_list[0].keys()
        header = "| " + " | ".join(keys) + " |"
        separator = (
            "| " + " | ".join([Markdown.get_sep(key) for key in keys]) + " |"
        )
        rows = [
            "| " + " | ".join(str(d[k]) for k in keys) + " |" for d in d_list
        ]

        return [header, separator] + rows
