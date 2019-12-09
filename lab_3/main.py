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
        identifier = 0
        if word not in self.storage and type(word) is str:
            identifier += 1
            # while identifier not in self.storage.values() and identifier is None:
            #    identifier += 1
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
        self.gram_frequencies = {}  # ключами выступают кортежи из чисел, а значения - частота возникновения
        # соответствующего кортежа в тексте.
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:
        if not isinstance(sentence, tuple) or self.size > len(sentence):
            return 'ERROR'
        for identifier in sentence:
            if type(identifier) is not int:
                return 'ERROR'
        gram = []
        for i in range(len(sentence)):
            if len(sentence) - i > self.size:
                gram.append(sentence[i: i + self.size])
            elif len(sentence) - i == self.size:
                gram.append(sentence[i:])
        for elem in gram:
            if elem not in self.gram_frequencies:
                self.gram_frequencies[elem] = 1
            else:
                self.gram_frequencies[elem] += 1
        return 'OK'

    def calculate_log_probabilities(self):
        for gram in self.gram_frequencies:
            total = 0
            for key in self.gram_frequencies:
                if gram[0] == key[0]:
                    total += self.gram_frequencies[key]
            self.gram_log_probabilities[gram] = math.log(self.gram_frequencies[gram] / total)

    def predict_next_sentence(self, prefix: tuple) -> list:
        if type(prefix) is not tuple or len(prefix) != self.size - 1:
            return []
        predicted_sentence = list(prefix)
        while True:
            log_prob = []
            for gram in list(self.gram_log_probabilities.keys()):
                if gram[:-1] == prefix:
                    log_prob.append(self.gram_log_probabilities[gram])
            if not log_prob:
                break
            next_word_prob = max(log_prob)
            for gram, prob in list(self.gram_log_probabilities.items()):
                if next_word_prob == prob:
                    next_word_prob = gram[-1]
            predicted_sentence.append(next_word_prob)
            prefixes = list(prefix[1:])
            prefixes.append(next_word_prob)
            prefix = tuple(prefixes)

        return predicted_sentence


def encode(storage_instance, corpus) -> list:
    enc_sentences = []
    for sentence in corpus:
        enc_each_sentence = []
        for word in sentence:
            word = storage_instance.get_id_of(word)
            enc_each_sentence.append(word)
        enc_sentences.append(enc_each_sentence)
    return enc_sentences


def split_by_sentence(text) -> list:
    if not text or '.' not in text:
        return []

    text = text.lower()
    text = text.replace('\n', ' ')
    text = text.replace('!', '.')
    text = text.replace('?', '.')
    text = text.replace('  ', ' ')

    plain_text = ''
    corpus_output = []

    for s in text:
        if s.isalpha() or s == '.' or s == ' ':
            plain_text += s
    plain_text_sentences = plain_text.split(".")

    for sentence in plain_text_sentences:
        if sentence != '':
            new_sentence = ['<s>']
            sentence = sentence.split()
            for word in sentence:
                if word != sentence:
                    new_sentence.append(word)
            new_sentence.append('</s>')
            corpus_output.append(new_sentence)

    return corpus_output


