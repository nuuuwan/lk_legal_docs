class Format:
    TIME_FORMAT = "%Y-%m-%d %H:%M"

    @staticmethod
    def badge(x) -> str:
        for before, after in [("-", "--"), (" ", "_")]:
            x = x.replace(before, after)
        return x

    @staticmethod
    def and_list(x_list) -> str:
        if len(x_list) == 0:
            return ""
        if len(x_list) == 1:
            return x_list[0]
        return ", ".join(x_list[:-1]) + " & " + x_list[-1]

    @staticmethod
    def title(x) -> str:
        title = x.title().replace("_", " ")
        title = title.replace("Lk", "#SriLanka 🇱🇰")
        return title
