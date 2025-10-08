from scraper import GlobalReadMe


def main():
    GlobalReadMe(
        {
            "lk_legal_docs": [
                "lk_acts",
                "lk_bills",
                "lk_extraordinary_gazettes_2020s",
                "lk_extraordinary_gazettes_2010s",
                "lk_extraordinary_gazettes_2000s",
                "lk_extraordinary_gazettes_1990s",
                "lk_extraordinary_gazettes_1980s",
            ]
        }
    ).build()


if __name__ == "__main__":
    main()
