"""
Labour work #3
 Building an own N-gram model
"""

import math

reference_text = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        reference_text = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        identifier = None
        if word not in self.storage and type(word) is str:
            identifier = 0
            while identifier not in self.storage.keys() and identifier is None:
                identifier += 1
            self.storage[word] = identifier
        return identifier

    def get_id_of(self, word: str) -> int:
        if word in self.storage:
            return self.storage.get(word)
        return -1

    def get_original_by(self, word_id: int) -> str:
        if word_id in self.storage.values() and type(word_id) is int:
            word_id = list(self.storage.values()).index(word_id)
            return list(self.storage.keys())[word_id]
        return 'UNK'

    def from_corpus(self, corpus: tuple):
        if type(corpus) is tuple:
            for word in corpus:
                self.put(word)
        return corpus


class NGramTrie:
    def __init__(self, size=2):
        self.size = size
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:
        if not isinstance(sentence, tuple) or self.size > len(sentence):
            return 'ERR'
        for identifier in sentence:
            if type(identifier) is not int:
                return 'ERR'

        to_fill = []

        for i in range(len(sentence)):
            if len(sentence) > self.size + 1:
                to_fill.append(sentence[i: i + self.size])
            elif len(sentence) - i == self.size:
                to_fill.append(sentence[i:])
        for elem in to_fill:
            if elem not in self.gram_frequencies:
                self.gram_frequencies[elem] = 1
            else:
                self.gram_frequencies[elem] += 1
        return 'OK'

    def calculate_log_probabilities(self):
        pass

    def predict_next_sentence(self, prefix: tuple) -> list:
        if type(prefix) is not tuple or len(prefix) + 1 != self.size:
            return []


def encode(storage_instance, corpus) -> list:
    coded_1 = []
    for sentence in corpus:
        coded_2 = []
        for word in sentence:
            word = storage_instance.get_id_of(word)
            coded_2.append(word)
        coded_1.append(coded_2)
    return coded_1


def split_by_sentence(text: str) -> list:
    if not text or '.' not in text:
        return []

    text = text.lower()
    text = text.replace('\n', ' ')
    text = text.replace('!', '.')
    text = text.replace('?', '.')
    while '  ' in text:
        text = text.replace('  ', ' ')

    sentence = ''
    text_sentences = []
    sentences_list = []

    for s in text:
        if s.isalpha() or s == '.' or s == ' ':
            sentence += s
    sentence = sentence.split(".")

    for each_word in sentence:
        text_sentences.append(each_word)

    for sentence in text_sentences:
        if sentence != '':
            new_sentence = ['<s>']
            sentence = sentence.split()
            for word in sentence:
                if word != sentence:
                    new_sentence.append(word)
            new_sentence.append('</s>')
            sentences_list.append(new_sentence)

    return sentences_list
