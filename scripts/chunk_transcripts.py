CHUNK_SIZE = 4000
OVERLAP = 300


def split_text_into_chunks(text):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + CHUNK_SIZE

        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        start += CHUNK_SIZE - OVERLAP

    return chunks