class Chunker:
    @staticmethod
    def chunk(
        content: str, max_chunk_size: int, min_overlap_size: int
    ) -> list[str]:
        text_list = content.split("\n\n")
        chunks = []
        current_sentences = []
        current_size = 0
        for text in text_list:
            text = text.strip()

            if current_size + len(text) + 1 > max_chunk_size:
                current = "\n\n".join(current_sentences).strip()
                chunks.append(current)
                rem_overlap = 0
                new_sentences = []
                i = 1
                while (
                    rem_overlap < min_overlap_size
                    and len(current_sentences) >= i
                ):
                    new_sentences.append(current_sentences[-i])
                    rem_overlap += len(current_sentences[-i]) + 1
                    i += 1
                new_sentences.reverse()
                current_sentences = new_sentences
                current_size = sum(len(s) for s in current_sentences)
            else:
                current_sentences.append(text)
                current_size += len(text) + 1

        if current_sentences:
            current = "\n\n".join(current_sentences).strip()
            chunks.append(current)

        return chunks
