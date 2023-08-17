import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk
from rank_bm25 import BM25Okapi

class English:
    def sentence_split(self, text):
        sentences = sent_tokenize(text)
        return sentences

    def word_tokenize_sentences(self, sentences):
        tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
        return tokenized_sentences

    def pos_tag_sentences(self, tokenized_sentences):
        pos_tagged_sentences = [nltk.pos_tag(tokens) for tokens in tokenized_sentences]
        return pos_tagged_sentences

    def extract_named_entities(self, pos_tagged_sentences):
        ne_results = [ne_chunk(pos_tags) for pos_tags in pos_tagged_sentences]
        named_entities = []
        for result in ne_results:
            for entity in result:
                if hasattr(entity, 'label'):
                    named_entities.append(' '.join([leaf[0] for leaf in entity.leaves()]))
        return named_entities

    def get_tag(self):
        return tag_dict

    def generate_bm25(self, tokenized_sentences):
        # 创建BM25模型并训练
        bm25 = BM25Okapi(tokenized_sentences)
        return bm25


tag_dict = {
    "CC": "Coordinating conjunction",
    "CD": "Cardinal number",
    "DT": "Determiner",
    "EX": "Existential there",
    "FW": "Foreign word",
    "IN": "Preposition or subordinating conjunction",
    "JJ": "Adjective",
    "JJR": "Adjective, comparative",
    "JJS": "Adjective, superlative",
    "LS": "List item marker",
    "MD": "Modal",
    "NN": "Noun, singular or mass",
    "NNS": "Noun, plural",
    "NNP": "Proper noun, singular",
    "NNPS": "Proper noun, plural",
    "PDT": "Predeterminer",
    "POS": "Possessive ending",
    "PRP": "Personal pronoun",
    "PRP$": "Possessive pronoun",
    "RB": "Adverb",
    "RBR": "Adverb, comparative",
    "RBS": "Adverb, superlative",
    "RP": "Particle",
    "SYM": "Symbol",
    "TO": "to",
    "UH": "Interjection",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund or present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, non-3rd person singular present",
    "VBZ": "Verb, 3rd person singular present",
    "WDT": "Wh-determiner",
    "WP": "Wh-pronoun",
    "WP$": "Possessive wh-pronoun",
    "WRB": "Wh-adverb",
    "O": "Other"
}

chunk_dict = {
    "B-NP": "Begin noun phrase",
    "I-NP": "Inside noun phrase",
    "B-VP": "Begin verb phrase",
    "I-VP": "Inside verb phrase",
    "B-PP": "Begin prepositional phrase",
    "I-PP": "Inside prepositional phrase",
    "B-ADJP": "Begin adjective phrase",
    "I-ADJP": "Inside adjective phrase",
    "B-ADVP": "Begin adverb phrase",
    "I-ADVP": "Inside adverb phrase",
    "B-SBAR": "Begin subordinating conjunction",
    "I-SBAR": "Inside subordinating conjunction",
    "B-CONJP": "Begin conjunctive phrase",
    "I-CONJP": "Inside conjunctive phrase",
    "B-PRT": "Begin particle",
    "I-PRT": "Inside particle",
    "B-INTJ": "Begin interjection",
    "I-INTJ": "Inside interjection",
    "O": "Other"
}