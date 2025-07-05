from utils import Log

log = Log("AbstractPipelineRunner")


class AbstractPipelineRunner:

    def get_pipeline_name(self):
        raise NotImplementedError

    def gen_docs(self):
        raise NotImplementedError

    @staticmethod
    def __process_doc__(doc):
        try:
            is_hot = doc.download_all()
            if is_hot:
                doc.write()
                doc.write_readme()
                doc.extract_text()
            return is_hot
        except Exception as e:
            log.error(f"❌ Error downloading {doc.doc_num}: {e}")
            return False

    def run_pipeline(self, max_n_hot):
        log.info(f"🤖 Running {self.get_pipeline_name()}.")
        n_hot = 0
        for doc in self.gen_docs():
            if n_hot >= max_n_hot:
                log.info(f"🛑 Downloaded {n_hot} new docs.")
                return

            is_hot = self.__process_doc__(doc)
            if is_hot:
                n_hot += 1
                log.info(f"✅ ({n_hot}/{max_n_hot}) Downloaded {doc}")
        log.info(f"🛑🛑 Downloaded ALL {self.get_pipeline_name()}.")
