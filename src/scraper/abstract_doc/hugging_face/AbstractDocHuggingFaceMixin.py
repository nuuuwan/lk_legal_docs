import os

import pandas as pd
from datasets import Dataset
from utils import Hash, Log

from utils_future import BigJSONFile, Chunker

log = Log("AbstractDocHuggingFaceMixin")


class AbstractDocHuggingFaceMixin:
    MAX_CHUNK_SIZE = 2000
    MIN_OVERLAP_SIZE = 200
    HUGGING_FACE_USERNAME = os.environ.get("HUGGING_FACE_USERNAME")
    HUGGING_FACE_TOKEN = os.environ.get("HUGGING_FACE_TOKEN")

    @classmethod
    def get_dir_hugging_face_data(cls):
        # E.g. # e.g. ../lk_acts_data/data/lk_acts/hugging_face_data
        return os.path.join(cls.get_dir_docs_for_cls(), "hugging_face_data")

    @classmethod
    def get_docs_json_path(cls):
        return os.path.join(cls.get_dir_hugging_face_data(), "docs")

    @classmethod
    def build_docs(cls):
        d_list = [doc.to_dict() for doc in cls.list_all()]
        BigJSONFile(cls.get_docs_json_path()).write(d_list)
        return d_list

    @classmethod
    def get_data_list_for_doc(cls, doc):
        chunks = Chunker.chunk(
            doc.get_text(),
            cls.MAX_CHUNK_SIZE,
            cls.MIN_OVERLAP_SIZE,
        )
        d_list = []
        for chunk_index, chunk_text in enumerate(chunks):
            chunk_id = f"{doc.doc_id}-{chunk_index:04d}"
            d = doc.to_dict() | dict(
                chunk_id=chunk_id,
                chunk_index=chunk_index,
                language=doc.lang,
                md5=Hash.md5(chunk_text),
                chunk_size_bytes=len(chunk_text.encode("utf-8")),
                chunk_text=chunk_text,
            )
            d_list.append(d)

        return d_list

    @classmethod
    def get_chunks_json_path(cls):
        return os.path.join(cls.get_dir_hugging_face_data(), "chunks")

    @classmethod
    def build_chunks(cls):
        d_list = []
        for doc in cls.list_all():
            d_list.extend(cls.get_data_list_for_doc(doc))

        BigJSONFile(cls.get_chunks_json_path()).write(d_list)
        return d_list

    @classmethod
    def get_hugging_face_project(cls):
        label = cls.get_doc_class_label().replace("_", "-").lower()
        return f"{cls.HUGGING_FACE_USERNAME}/{label}"

    @classmethod
    def get_dataset_id(cls, label_suffix: str) -> str:
        return f"{cls.get_hugging_face_project()}-{label_suffix}"

    @classmethod
    def get_dataset_url(cls, label_suffix: str) -> str:
        return (
            "https://huggingface.co/datasets"
            + f"/{cls.get_dataset_id(label_suffix)}"
        )

    @classmethod
    def upload_to_hugging_face(cls):
        docs_df = pd.DataFrame(cls.build_docs())
        chunks_df = pd.DataFrame(cls.build_chunks())
        docs_ds = Dataset.from_pandas(docs_df)
        chunks_ds = Dataset.from_pandas(chunks_df)
        assert cls.HUGGING_FACE_USERNAME
        assert cls.HUGGING_FACE_TOKEN

        for ds, suffix in [(docs_ds, "docs"), (chunks_ds, "chunks")]:
            dataset_id = cls.get_dataset_id(suffix)
            repo_id = ds.push_to_hub(dataset_id, token=cls.HUGGING_FACE_TOKEN)
            log.info(f"🤗 Uploaded {dataset_id} to {repo_id}")

    @classmethod
    def build_and_upload_to_hugging_face(cls):
        assert cls.list_all()
        cls.upload_to_hugging_face()
