from collections import defaultdict
from collections import Counter
import random


def get_corpus(path):
    with open(path, 'r', encoding='utf-8') as f:
        tokens = tokenize(f.read())
    return tokens


def tokenize(text):
    return text.split()


def ngram_generator(tokens, n=2):
    for i in range(len(tokens) - (n-1)):
        head = tuple([tokens[i+j] for j in range(n-1)])
        tail = tokens[i+n-1]
        yield head, tail


def get_markov(tokens):
    result = defaultdict(Counter)
    for head, tail in ngram_generator(tokens, n=3):
        result[head].update([tail])
    return result


def get_random_capitalized_word(tokens):
    while True:
        word = random.choice(tokens)
        if word[0][0].isupper() and (word[0][-1] not in '?!.'):
            return word


def generate_sentence(markov):
    while True:
        words = [*get_random_capitalized_word(list(markov.keys()))]
        while words[-1][-1] not in '!?.':
            next_word = tuple(words[-2:])
            tail_counter = markov[next_word]
            tail, count = zip(*tail_counter.items())
            next_word = random.choices(tail, count, k=1)[0]
            words.append(next_word)
        if len(words) < 5:
            continue
        return " ".join(words)


def main():
    path = input()
    tokens = get_corpus(path)
    markov = get_markov(tokens)
    for _ in range(10):
        print(generate_sentence(markov), end='\n\n')


if __name__ == '__main__':
    main()