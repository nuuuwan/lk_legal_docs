class Format:
    TIME_FORMAT = "%Y-%m-%d %H:%M"

    @staticmethod
    def badge(x) -> str:
        for before, after in [("-", "--"), (" ", "_")]:
            x = x.replace(before, after)
        return x

    @staticmethod
    def and_list(x_list: list[str], max_display: int = 30) -> str:
        assert max_display >= 2
        n = len(x_list)
        assert n > 0
        if n == 1:
            return x_list[0]
        if n <= max_display:
            return ", ".join(x_list[:-1]) + " & " + x_list[-1]

        return (
            ", ".join(x_list[:max_display]) + f" & {n - (max_display)} more"
        )

    @staticmethod
    def title(x) -> str:
        title = x.title().replace("_", " ")
        title = title.replace("Lk", "#SriLanka 🇱🇰")
        return title
