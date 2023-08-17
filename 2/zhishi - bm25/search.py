import math
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ResultItem:
    def __init__(self, index, name, text):
        self.index = index
        self.name = name
        self.head, *_, self.text = text.split('\n', maxsplit=1)
        self.rank = self.freq = self.count = self.similarity = 0.0
        self.occurrence = []

    def __str__(self):
        s = f"file: {self.name}\nhead: {self.head}\nfreq: {self.freq}\n"
        s += f"rank: {self.rank}\nsimilarity: {self.similarity}\n"
        for j in self.occurrence:
            s += f"> ...{self.text[max(0, j[0] - 50):j[0] + 50]}...\n"
        return s


def get_similarity(a, b):
    return cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))[0, 0]


def run_search(search_str, inverse_index, files, text_list, bag, count):
    s_list = search_str.split()
    temp = [inverse_index.get(s, {}) for s in s_list]

    result_dict = {}
    for index, t in enumerate(temp):
        for j, (file_index, score, positions) in t.items():
            item = result_dict.get(file_index, ResultItem(file_index, files[file_index], text_list[file_index]))
            item.count += 1
            item.freq += score
            item.rank += score
            item.occurrence.extend(positions)
            result_dict[file_index] = item

    result_list = list(result_dict.values())

    search_vec = bag.transform([search_str])
    search_vec = search_vec.tocsr()

    num_documents = count.shape[0]  # 获取稀疏矩阵的行数

    corpus = count.toarray().tolist()  # 将稀疏矩阵转换为普通列表形式

    bm25 = BM25Okapi(corpus)  # 使用修正后的参数

    for i in result_list:
        doc_vec = count[i.index].tocsr()
        i.similarity = bm25.get_scores(search_vec, doc_vec)[0]

    result_list.sort(key=lambda x: -x.rank * x.count)
    return result_list
