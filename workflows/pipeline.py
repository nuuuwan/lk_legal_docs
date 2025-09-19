import sys

from lk_legal_docs import Act, Bill

if __name__ == "__main__":
    doc_class_label = sys.argv[2]
    for doc_class in [Act, Bill]:
        if doc_class.get_doc_class_label() == doc_class_label:
            doc_class.run_pipeline()
            sys.exit(0)
    raise ValueError(f"Unknown doc_class_label: {doc_class_label}")
