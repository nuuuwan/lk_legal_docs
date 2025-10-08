import sys

from lk_legal_docs import ExtraordinaryGazette

if __name__ == "__main__":
    doc_class_label = sys.argv[1]
    for doc_class in [ExtraordinaryGazette]:
        if doc_class.get_doc_class_label() == doc_class_label:
            doc_class.run_pipeline()
            sys.exit(0)
    raise ValueError(f"Unknown doc_class_label: {doc_class_label}")
