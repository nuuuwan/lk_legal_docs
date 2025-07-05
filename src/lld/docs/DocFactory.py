from lld.docs.custom_docs import Act, Bill, ExtraGazette


class DocFactory:
    @staticmethod
    def list_all_cls():
        return [
            Act,
            Bill,
            ExtraGazette,
        ]
