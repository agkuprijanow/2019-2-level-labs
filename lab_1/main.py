"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


import string
import collections


text = """High Altitude Specifics Au@dience. As you plan out what you want to do with your time, divide it into \
three roughly equal categories. "High altitude" are those questions where you g##ive your panelists a chance \
to discuss what is happening in the world at a 30,000-foot level. Spec1ifics are where you invite them to \
share funny anecdotes, war stories, or concrete examples - things that the aud$ience can really relate to. \
Audience means not just leaving time for Q&A, but also coming up with creative ways to bring the audience \
into your conversation. After  you've asked panelists about the worst hire t.hey ever made, for instance, \
you might ask people in the audience to share their stories. If you have a panel of venture capitalists \
and an audience of entrepreneurs, try asking a few bold entrepreneurs to deliver their elev.ator pitches \
and get the VCs to suggest ways to improve it."""


stop_words = ('as', 'to', 'it', 'are', 'is', 'in', 'what', 'the', 'a', 'your', 'with', 'into', 'over', 'but', 'also', 3)


top_n = 5


def calculate_frequences(text):
    if text is None or type(text) is int:
        frequencies = {}
        return frequencies
    else:
        text = text.replace('\n', ' ')
        text_lower = text.lower()
        text_split = text_lower.split(' ')
        text_clean = []
        for word in text_split:
            word_clean = ''
            for symbol in word:
                if symbol not in string.punctuation and symbol not in string.digits:
                    word_clean += symbol
            if word_clean is not '':
                text_clean.append(word_clean)
        counts = collections.Counter(text_clean)
        frequencies = dict(counts.copy())
        return frequencies


def filter_stop_words(frequencies: dict, stop_words: tuple):
    if stop_words is None or frequencies is None:
        frequencies = {}
        return frequencies
    else:
        frequencies_filtered = dict(frequencies.copy())
        keys_to_remove = [key for key in frequencies_filtered.keys() if type(key) != str]
        for key in keys_to_remove:
            del frequencies_filtered[key]
        for key in stop_words:
            if key in frequencies_filtered:
                del frequencies_filtered[key]
        for key, value in frequencies_filtered.items():
            frequencies_filtered[key] = value
        return frequencies_filtered


def get_top_n(frequencies_filtered: dict, top_n: int):
    if len(frequencies_filtered) == 0 or top_n <= 0:
        top_n_tuple = ()
        return top_n_tuple
    top_n_tuple = tuple(sorted(frequencies_filtered, key=frequencies_filtered.get, reverse=True))
    return top_n_tuple[:top_n]
