import os
import re
import math
from collections import defaultdict, Counter
from utils import parser

# ----------------------
# Text Processing Utils
# ----------------------
def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.split()

# ----------------------
# TF-IDF Indexing
# ----------------------
def build_tf_idf_index(data_folder='data'):
    tf_index = {}      # filename -> {word: tf}
    df_counts = {}     # word -> doc freq
    file_texts = {}    # filename -> full text
    total_docs = 0

    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)
        text = parser.extract_text_from_file(filepath)
        tokens = clean_and_tokenize(text)
        total_docs += 1

        word_counts = Counter(tokens)
        tf_index[filename] = word_counts
        file_texts[filename] = text  # store full raw text

        for word in set(tokens):
            df_counts[word] = df_counts.get(word, 0) + 1

    return tf_index, df_counts, total_docs, file_texts

# ----------------------
# TF-IDF Scoring
# ----------------------
def compute_tfidf_scores(query, tf_index, df_counts, total_docs):
    """
    Computes cumulative TF-IDF score for multi-word queries.
    """
    query_words = query.lower().split()
    scores = {}

    for filename, word_counts in tf_index.items():
        score = 0
        for word in query_words:
            tf = word_counts.get(word, 0)
            if tf == 0:
                continue
            df = df_counts.get(word, 1)
            idf = math.log(total_docs / df)
            score += tf * idf

        if score > 0:
            scores[filename] = score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def get_snippet(text, query, window=20):
    """
    Returns a snippet around the first keyword found in the query.
    """
    keywords = query.lower().split()
    words = text.split()
    lower_words = [w.lower() for w in words]

    for keyword in keywords:
        if keyword in lower_words:
            idx = lower_words.index(keyword)
            start = max(0, idx - window)
            end = min(len(words), idx + window + 1)
            snippet = ' '.join(words[start:end])
            return f"...{snippet}..."

    return ""