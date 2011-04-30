import sys
import re
import random

class Hangman():
    def __init__(self):
        self.word = self.choose_word()
        self.shown = list('_'* len(self.word))
        self.score = 0
    def guess(self,letter):
        if letter in self.word:
            for part in self.list_pos(letter):
                self.shown[part] = letter
            self.score += 1
        else:
            self.score -= 1
    def list_pos(self,letter):
        for x in re.finditer(letter, self.word):
            yield x.start()
    def choose_word(self):
        f = open("/usr/share/dict/words")
        return random.choice([x for x in f]).lower().strip()
    

if __name__ == '__main__':
    hangman = Hangman()
    while hangman.score > -5:
        print ''.join(hangman.shown) + ' ' + str(hangman.score)
        hangman.guess(raw_input('Guess? ').lower())
        

    if hangman.score == -5:
        print "the word was: %s" % hangman.word
    else:
        print "You're a winner!"