import math

reference_texts = []  # заполнен текстами из файлов


def clean_tokenize_corpus(reference_texts: list) -> list:

    # каждый текст - строка

    if not reference_texts or not isinstance(reference_texts, list):
        return []
    ref_texts_tokenized = []
    for each_text in reference_texts:
        if each_text and isinstance(each_text, str):
            while '<br />' in each_text:
                each_text = each_text.replace("<br />", " ")
            each_text = each_text.lower()
            each_text = each_text.replace('\n', ' ')
            ref_text_clean = []
            words_to_clean = each_text.split(" ")
            for word in words_to_clean:
                new_word = ""
                if not word.isalpha():
                    for symbol in word:
                        if symbol.isalpha():
                            new_word += symbol
                    if new_word:
                        ref_text_clean.append(new_word)
                else:
                    ref_text_clean.append(word)
            ref_texts_tokenized += [ref_text_clean]
    return ref_texts_tokenized


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus  # список из строк
        self.tf_values = []  # cписок из словарей
        self.idf_values = {}
        self.tf_idf_values = []
        self.file_names = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']

    def calculate_tf(self):
        if self.corpus:
            for text in self.corpus:
                tf_values = {}
                if text:
                    len_text = len(text)
                    for word in text:
                        if type(word) is not str:
                            len_text = len_text - 1
                    for word in text:
                        if isinstance(word, str) and word not in tf_values:
                            count = text.count(word)
                            tf_values[word] = count / len_text
                    self.tf_values += [tf_values]
        return self.tf_values

    def calculate_idf(self):
        if self.corpus:
            for text in self.corpus:
                if not text:
                    continue
                all_texts = []
                for word in text:
                    if word not in all_texts and type(word) is str:
                        all_texts += [word]
                word_counter = {}
                for word in all_texts:
                    word_count = 0
                    '''word freq in whole corpus'''
                    for text2 in self.corpus:
                        if not text2 or word in text2:
                            word_count += 1
                    word_counter[word] = word_count
                    if word_counter.get(word) > 0:
                        len_corpus = len(self.corpus)
                        self.idf_values[word] = math.log(len_corpus / word_counter.get(word))
            return self.idf_values

    def calculate(self):
        if self.idf_values and self.tf_values:
            for w_tf in self.tf_values:
                tf_idf_values = {}
                for word, tf in w_tf.items():
                    tf_idf_values[word] = tf * self.idf_values.get(word)
                self.tf_idf_values += [tf_idf_values]
        return self.tf_idf_values

    def report_on(self, word, document_index):  # doc_index - номер токенизир. текста из списка
        if not self.tf_idf_values or document_index >= len(self.corpus):
            return ()
        tf_idf = self.tf_idf_values[document_index][word]
        sort = sorted(self.tf_idf_values[document_index],
                      key=lambda x: self.tf_idf_values[document_index][x], reverse=True)
        rating = sort.index(word)
        res = (tf_idf, rating + 1)
        return tuple(res)

    def dump_report_csv(self):
        file = open('report.csv', 'w')
        headline = 'word'
        for name in self.file_names:
            headline += ',tf_' + name
        headline += ",idf"
        for name in self.file_names:
            headline += ',tf-idf_' + name
        file.write(headline)
        duplicates = []
        for text in self.corpus:
            for word in text:
                string = '\n'
                string += word
                if word in duplicates:
                    continue
                for i, _ in enumerate(self.tf_values):
                    string += ','
                    if word in self.tf_values[i]:
                        string += str(self.tf_values[i][word])  # i - index, word - key
                    else:
                        string += '0'
                string += ',' + str(self.idf_values[word])
                for i, _ in enumerate(self.tf_idf_values):
                    string += ','
                    if word in self.tf_idf_values[i]:
                        string += str(self.tf_idf_values[i][word])
                    else:
                        string += '0'
                duplicates.append(word)
                file.write(string)


if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            reference_texts.append(f.read())


def run():
    tfidf = TfIdfCalculator(clean_tokenize_corpus(reference_texts))
    print(tfidf.calculate_tf())
    print(tfidf.calculate_idf())
    print(tfidf.calculate())
    print(tfidf.report_on('only', 0))
    print(tfidf.report_on('i', 0))
    tfidf.dump_report_csv()


run()
