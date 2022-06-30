from random import randint

import numpy as np


def get_text(text, words, equal_chance, endl_break_chance):
    try:
        # Pre process text for dictionarization
        if len(text.split('\n')) < 50:
            raise Exception()
        preprocess = '\n'.join([process_line(line) for line in text.split('\n')])
        final = __get_text(preprocess, words, equal_chance, endl_break_chance)
    except Exception as e:
        print(e)
        final = 'aMarkov was unable to generate a message! This is likely due to your log not having enough messages to generate.'
    return final

def process_line(line): 
    return line.split(':')[1]
    
def __get_text(text, words, equal_chance, endl_break_chance):
    corpus = text.split()

    def make_pairs(corpus):
        for i in range(len(corpus)-1):
            yield (corpus[i], corpus[i+1])
        yield (corpus[len(corpus)-1], None)
            
    pairs = make_pairs(corpus)
    word_dict = {}

    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            if word_2 in word_dict[word_1] and equal_chance:
                continue
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]
    first_word = np.random.choice(corpus)
    chain = [first_word]

    for _ in range(words):
        choice = np.random.choice(word_dict[chain[-1]])
        if choice is None:
            if randint(1, 100) < endl_break_chance:
                break
        chain.append(choice)
    return ' '.join(chain)