from scraper import GlobalReadMe


def main():
    GlobalReadMe(
        {
            "lk_legal_docs": [
                "lk_acts",
                "lk_bills",
                "lk_extraordinary_gazettes",
            ]
        }
    ).build()


if __name__ == "__main__":
    main()
