class Markdown:

    @staticmethod
    def get_sep(key: str) -> str:
        for num_prefix in ["n", "p", "total", "v", "  "]:
            if key.startswith(num_prefix + "_") or key == num_prefix:
                return "--:"

        return ":--"

    @staticmethod
    def table(d_list: list[dict]) -> list[str]:
        if not d_list:
            return []
        if len(d_list) == 1:
            d_list = [{" ": k, "  ": v} for k, v in d_list[0].items()]

        keys = d_list[0].keys()
        header = "| " + " | ".join(keys) + " |"
        separator = (
            "| " + " | ".join([Markdown.get_sep(key) for key in keys]) + " |"
        )
        rows = [
            "| " + " | ".join(str(d[k]) for k in keys) + " |" for d in d_list
        ]

        return [header, separator] + rows
