from rank_bm25 import BM25Okapi
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from collections import defaultdict
from scipy.sparse import csr_matrix

path = 'data'
files = os.listdir(path)

def get_text_list():
    return [open(os.path.join(path, f), encoding='utf-8').read() for f in files]

def get_bag(texts):
    bag = TfidfVectorizer(token_pattern=r'\b\w+\b')
    count = bag.fit_transform(texts)
    count = csr_matrix(count)  # 转换为稀疏矩阵
    return bag, count

def generate_inverse_index(text_list, bag, count):
    result = defaultdict(dict)

    bm25 = BM25Okapi(text_list)

    for i, word in enumerate(bag.get_feature_names_out()):
        for j, score in zip(*count[:, i].nonzero()):
            if score > 0:
                positions = [m.span() for m in re.finditer(r'\b{}\b'.format(word), text_list[j])]
                result[word][j] = (j, bm25.get_score(text_list[j], word), positions)
    return result
