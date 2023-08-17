import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict

path = 'data'
files = os.listdir(path)

def get_text_list():
    return [open(os.path.join(path, f), encoding='utf-8').read() for f in files]

def get_bag(texts):
    bag = CountVectorizer(token_pattern=r'\b\w+\b')
    count = bag.fit_transform(texts)
    return bag, count

def generate_inverse_index(text_list, bag, count):
    result = defaultdict(dict)
    for i, word in enumerate(bag.get_feature_names_out()):
        for j in range(count.shape[0]):
            if count[j, i] > 0:
                positions = [m.span() for m in re.finditer(r'\b{}\b'.format(word), text_list[j])]
                result[word][j] = (j, count[j, i], positions)
    return result
