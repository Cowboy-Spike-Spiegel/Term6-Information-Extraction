import os
import jieba
import thulac
from pyltp import SentenceSplitter, Segmentor, NamedEntityRecognizer, Postagger
from rank_bm25 import BM25Okapi

class Chinese:
    def __init__(self):
        self.segmentor = Segmentor(os.path.abspath('.')+"\\ltp_data_v3.4.0\\cws.model")
        self.postagger = Postagger(os.path.abspath('.')+"\\ltp_data_v3.4.0\\pos.model")
        self.recognizer = NamedEntityRecognizer(os.path.abspath('.')+"\\ltp_data_v3.4.0\\ner.model")

    def sentence_split(self, text):
        sentence_splitter = SentenceSplitter()
        sentences = sentence_splitter.split(text)
        return sentences

    def word_tokenize_sentences(self, sentences):
        tokenized_sentences = [self.segmentor.segment(sentence) for sentence in sentences]
        return tokenized_sentences

    def pos_tag_sentences(self, tokenized_sentences):
        postags_sentences = [self.postagger.postag(tokens) for tokens in tokenized_sentences]
        return postags_sentences

    def extract_named_entities(self, tokenized_sentences, postags_sentences):
        ne_results = []
        for i, tokens in enumerate(tokenized_sentences):
            postags = list(postags_sentences[i])
            netags = self.recognizer.recognize(tokens, postags)
            ne_results.append(list(zip(tokens, netags)))
        named_entities = []
        for result in ne_results:
            named_entities.extend([token[0] for token in result if token[1] != 'O'])
        return named_entities

    def get_tag(self):
        return tag_dict

    def generate_bm25(self, tokenized_sentences):
        # 创建BM25模型并训练
        bm25 = BM25Okapi(tokenized_sentences)
        return bm25


tag_dict = {
    "a": "adjective 美丽",
    "ni": "organization name 保险公司",
    "b": "other noun-modifier 大型, 西式",
    "nl": "location noun 城郊",
    "c": "conjunction 和, 虽然",
    "ns": "geographical name 北京",
    "d": "adverb 很",
    "nt": "temporal noun 近日, 明代",
    "e": "exclamation 哎",
    "nz": "other proper noun 诺贝尔奖",
    "g": "morpheme 茨, 甥",
    "o": "onomatopoeia 哗啦",
    "h": "prefix 阿, 伪",
    "p": "preposition 在, 把",
    "i": "idiom 百花齐放",
    "q": "quantity 个",
    "j": "abbreviation 公检法",
    "r": "pronoun 我们",
    "k": "suffix 界, 率",
    "u": "auxiliary 的, 地",
    "m": "number 一, 第一",
    "v": "verb 跑, 学习",
    "n": "general noun 苹果",
    "wp": "punctuation ，。！",
    "nd": "direction noun 右侧",
    "ws": "foreign words CPU",
    "nh": "person name 杜甫, 汤姆",
    "x": "non-lexeme 萄, 翱"
}
