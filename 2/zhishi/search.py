import math


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
    return a.dot(b.T) / (math.sqrt(a.dot(a.T)) * math.sqrt(b.dot(b.T)))


def run_search(search_str, inverse_index, files, text_list, bag, count):
    s_list = search_str.split()
    temp = [inverse_index.get(s, {}) for s in s_list]
    freq = [sum(i[1] for i in t.values()) for t in temp]

    result_dict = {}
    for index, t in enumerate(temp):
        for j, (file_index, word_count, positions) in t.items():
            item = result_dict.get(file_index, ResultItem(file_index, files[file_index], text_list[file_index]))
            item.count += 1
            item.freq += word_count
            item.rank += word_count * 100 / (freq[index] + 1e-6)
            item.occurrence.extend(positions)
            result_dict[file_index] = item

    result_list = list(result_dict.values())

    search_vec = bag.transform([search_str]).toarray()
    for i in result_list:
        i.similarity = get_similarity(search_vec[0], count[i.index].A[0])

    result_list.sort(key=lambda x: -x.rank * x.count)
    return result_list
