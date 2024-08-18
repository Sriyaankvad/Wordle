"""A python class recreating The New York Times' Wordle"""

import random
from typing import Set


class Wordle:
    """The class handling anything related to the list of valid solutions."""

    def __init__(self, wordfile: str):
        self.words: Set[str] = set()  # set containing all the valid solutions
        self.target: str = ""  # the word the player is attempting to guess
        self.load_words(wordfile)
        self.find_target()

    def load_words(self, wordfile: str):
        """Reads the words in words.text and assigns it to a set.
        These words are the only words that can appear as wordle solutions."""

        with open(wordfile, "r", encoding="utf8") as file:
            self.words = {word.lower().strip() for word in file}

    def find_target(self):
        """Picks a random word in the set.
        The player is attempting to guess this word."""

        wordlist = list(self.words)
        self.target = random.choice(wordlist)

    def is_valid(self, guess: str) -> bool:
        """Checks if the player's guess is in the list of valid words."""
        return guess.casefold() in self.words


class Game:
    """The class handling the actual playing of Wordle."""

    def __init__(self, wordle: Wordle, guesses: int = 6):
        self.wordle: Wordle = wordle  # Wordle object
        self.guesses: int = guesses  # Number of guesses allowed
        self.length: int = len(self.wordle.target)  # Length of word
        self.progress: list = ['_'] * self.length  # Letters correctly guessed
        self.misplaced: set = set()  # Letters in the word but in wrong spot
        self.absent: set = set()  # Letters not in the word

    def play(self):
        """The method that conducts the playing of the game."""

        print('Welcome to Wordle!')
        print(f'The word has {self.length} letters\n')

        for count in range(0, self.guesses):
            # Ask player for a guess
            guess = input('Guess the word: ').strip()

            # Force player to provide a valid guess
            while len(guess) != self.length:
                guess = input(f'Your guess must be {self.length} letters: ')
            while not self.wordle.is_valid(guess):
                guess = input('Your guess must be a valid word: ')

            # End game if guessed correctly (game won), continue if wrong
            if guess.casefold() == self.wordle.target.casefold():
                print('You guessed correctly!')
                return
            print(f'Your guess was incorrect. {5-count} guesses remain')
            self.letters(guess)
            print()

        print(f'Game Over. The correct word was {self.wordle.target}')

    def letters(self, guess):
        """Outputs letters that are in the right spot and which ones aren't."""

        # Make target and guess uppercase for convenience
        target = self.wordle.target.upper()
        guess = guess.upper()

        # Assign the letter to either progress, misplaced, or absent
        for i in range(0, self.length):
            letter = guess[i]
            if letter == target[i]:
                self.progress[i] = letter
                self.misplaced.discard(letter)
            elif letter not in self.misplaced and letter not in self.progress:
                if letter in self.wordle.target.upper():
                    self.misplaced.add(letter)
                elif letter not in self.absent:
                    self.absent.add(letter)

        # Print progress, misplaced, and absent
        print(f'Current Progress: {"".join(self.progress)}')
        if self.misplaced:
            print(f'In the wrong spot: {" ".join(sorted(self.misplaced))}')
        if self.absent:
            print(f'Not in word: {" ".join(sorted(self.absent))}')

    def sort_letters(self, string: set) -> str:
        """Sorts a string alphabetically, separated by spaces."""

        return " ".join(sorted(string))


# game = Game(Wordle("words.txt"))
# game.play()

pokemon = Game(Wordle("pokemon.txt"))
pokemon.play()
