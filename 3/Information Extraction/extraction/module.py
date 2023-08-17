import os
import operator
import json
import re
import pickle
from .en import English
from .ch import Chinese


class Module:
    def __init__(self):
        self.folder_path = os.path.abspath('.') + '\\data\\'
        self.analyze = {}
        self.bm25 = {}
        self.ch_extraction = Chinese()
        self.en_extraction = English()

        # 解析已分析的数据
        list = os.listdir(self.folder_path + 'analyze')
        for file_name in list:
            with open(self.folder_path + 'analyze\\' + file_name, "r") as file:
                self.analyze[file_name[:-5]] = json.load(file)
        # 解析bm25文件
        list = os.listdir(self.folder_path + 'bm25')
        for file_name in list:
            with open(self.folder_path + 'bm25\\' + file_name, "rb") as file:
                self.bm25[file_name[:-4]] = pickle.load(file)

    # 获取tag
    def get_tag(self, language):
        if language == "Chinese":
            return self.ch_extraction.get_tag()
        elif language == "English":
            return self.en_extraction.get_tag()
        return False

    # 获取常用正则表达式
    def get_re(self):
        return re_dict

    # 执行解析
    def generate(self, name, language) -> str:
        analyze = self.analyze.get(name)
        bm25 = self.bm25.get(name)
        # 本地没找到
        if analyze == None or bm25 == None:
            with open(self.folder_path + language + '\\' + name + ".txt", 'r', encoding='utf-8') as file:
                content = file.read()
            # 解析文件内容
            if language == "English":
                sentences = self.en_extraction.sentence_split(content)
                tokenized_sentences = self.en_extraction.word_tokenize_sentences(sentences)
                postags_sentences = self.en_extraction.pos_tag_sentences(tokenized_sentences)
                named_entities = self.en_extraction.extract_named_entities(postags_sentences)
                bm25 = self.en_extraction.generate_bm25(tokenized_sentences)
            elif language == "Chinese":
                sentences = self.ch_extraction.sentence_split(content)
                tokenized_sentences = self.ch_extraction.word_tokenize_sentences(sentences)
                postags_sentences = self.ch_extraction.pos_tag_sentences(tokenized_sentences)
                named_entities = self.ch_extraction.extract_named_entities(tokenized_sentences, postags_sentences)
                bm25 = self.ch_extraction.generate_bm25(tokenized_sentences)

            # 本地storage存储解析结果
            analyze = {
                "language": language,
                "sentences": sentences,
                "tokenized_sentences": tokenized_sentences,
                "postags_sentences": postags_sentences,
                "named_entities": named_entities,
            }
            self.analyze[name] = analyze
            self.bm25[name] = bm25

            # 保存该分析数据
            with open(self.folder_path + 'analyze\\' + name + '.json', "w") as file:
                json.dump(analyze, file)
            # 保存该bm25模型
            with open(self.folder_path + 'bm25\\' + name+'.pkl', "wb") as file:
                pickle.dump(bm25, file)

            return "Analyze from local files."

        return "Analyze from software storage."

    # bm25查询
    def search_bm25(self, name, query):
        if self.analyze.get(name) == None:
            return False, False
        # 将查询字符串拆分为单词列表
        query_tokens = query.split()
        # 使用BM25模型计算相似度得分
        scores = self.bm25[name].get_scores(query_tokens)
        # 根据得分对文本进行排序
        sorted_indices = sorted(range(len(self.analyze[name]["sentences"])), key=lambda i: scores[i], reverse=True)
        # 返回排序后的文本列表和得分
        sorted_texts = [self.analyze[name]["sentences"][i] for i in sorted_indices]
        sorted_scores = [scores[i] for i in sorted_indices]

        return sorted_texts, sorted_scores

    # 词性查询
    def search_byTag(self, name, query_tag):
        ans = []
        language = self.analyze[name]["language"]
        # 英文
        if language == "English":
            postags_sentences = self.analyze[name]["postags_sentences"]
            for i in range(len(postags_sentences)):
                for token in postags_sentences[i]:
                    if query_tag == '' or token[1] == query_tag:
                        ans.append(token[0])
        # 中文
        elif language == "Chinese":
            tokenized_sentences = self.analyze[name]["tokenized_sentences"]
            postags_sentences = self.analyze[name]["postags_sentences"]
            for i in range(len(tokenized_sentences)):
                sentence = tokenized_sentences[i]
                tags = postags_sentences[i]
                for token, tag in zip(sentence, tags):
                    if query_tag == '' or tag == query_tag:
                        ans.append(token)
        return ans

    # 正则表达式提取（在本地数据根据名称提取）
    def search_reByName(self, name, pattern):
        data = self.analyze[name]["sentences"]
        print(pattern)
        result = []
        for item in data:
            result = result + re.findall(pattern, item)
        return result

    # 正则表达式提取（在提供数据中提取）
    def search_reByData(self, data, pattern):
        print(pattern)
        print(data)
        result = []
        for item in data:
            result = result + re.findall(pattern, item)
        return result

    # 命名实体查询
    def filter_named_entities(self, name, data): #r'Tencent|产品'
        entities = self.analyze[name]["named_entities"]
        ans = []
        for token in data:
            if token in entities:
                ans.append(token)
        return ans

re_dict = {
    "时间": r"\d{4}-\d{2}-\d{2}",
    "书籍": r"《.*》"
}