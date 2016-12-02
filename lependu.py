from collections import defaultdict


DICT = '/usr/share/dict/words'

words_by_length = {}



def read_words(dict_file):
    words = set()

    for line in open(dict_file):
        word = line.rstrip().lower()
        words.add(word)

    return words


class WordResolver(object):
    def __init__(self, word_length, max_attempts=6, word_dict=DICT):
        self.word_length = word_length
        self.max_attempts = max_attempts

        all_words = read_words(DICT)

        words_by_length = self._word_dict_by_length(all_words)

        self._possible_words = words_by_length[word_length]
        self._attempted_letters = set()
        self._unmatched_letters = set()

        self._resolved_word = [None] * word_length

    def _word_dict_by_length(self, words):
        d = defaultdict(set)

        for word in words:
            word_length = len(word)
            d[word_length].add(word)

        return d

    def is_resolved(self):
        return None not in self._resolved_word

    def was_attempted(self, letter):
        return letter in self._attempted_letters

    @property
    def attempted_letters(self):
        return sorted(self._attempted_letters)

    def attempt(self, letter, position):

        if position is None:
            self._attempted_letters.add(letter)
            self._update_possible_words()
            return

        letter_index = position - 1
#        if self._resolved_word[letter_index] is not None and letter in self._attempted_letters:
#            raise Exception("Letter already attempted!")

        self._resolved_word[letter_index] = letter
        self._attempted_letters.add(letter)
        self._update_possible_words()

    def _update_possible_words(self):
        new_possible_words = set()

        for word in self._possible_words:
            for i, letter in enumerate(word):
                if self._resolved_word[i] not in (None, letter):
                    break

            else:
                new_possible_words.add(word)

        for word in new_possible_words:
            for

        self._possible_words = new_possible_words

    @property
    def possible_words(self):
        return sorted(self._possible_words)


if __name__ == '__main__':

    word_lenght = int(raw_input("How many letters? "))
    wr = WordResolver(word_lenght)

    while not wr.is_resolved():
        next_letter = raw_input("What did you attempt last? (already attempted: %s) " % ", ".join(wr.attempted_letters))
        next_letter = next_letter.lower()
        positions = raw_input("Did this letter match any positions in the word? If yes, which (space-separated position numbers)? [Enter for no match] ")

        if not positions:
            positions = []
            wr.attempt(next_letter, None)
        else:
            positions = [int(pos) for pos in positions.split(" ")]

            for position in positions:
                wr.attempt(next_letter, position)

        print("possible words: %s" % ", ".join(wr.possible_words))
