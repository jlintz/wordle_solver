"""
Wordle class
"""
import logging
import random


class WordleException(Exception):
    pass


class Wordle:
    """
    Instantiate wordle class
    """

    def __init__(self, wordle_list: list = None, answer: str = None):

        self.current_score = ["_"] * 5
        self.found_chars = set()
        self.not_found_chars = set()
        self.word_list = wordle_list
        self.answer = answer

        # keep track of guessed words
        self.guessed_words = []

        self.logger = logging.getLogger("wordle")

    @staticmethod
    def score_word(guess: str, answer: str) -> str:
        """
        @guess: word being guessed
        @answer: correct answer
        return color coded string based on @guess and @answer
        """
        color = ["b"] * 5

        for n in range(len(guess)):
            if guess[n] == answer[n]:
                color[n] = "g"
            elif guess[n] in answer:
                color[n] = "y"

        return "".join(color)

    def guess_word(self) -> str:
        """
        select a random word from remaining choices
        """
        if len(self.word_list) == 0:
            self.logger.error("Out of words, not a valid Wordle word?")
            raise WordleException
        guess = random.choice(self.word_list)
        self.word_list.remove(guess)
        return guess

    def _validate_score(self, guess: str, score: str) -> bool:
        """
        @guess: current word being guessed
        @score: color coded score given to the @guess by wordle. Valid chars are b == black, y == yellow, g == green

        @return bool, return True if the score entered is valid
        """
        char_list = ["b", "y", "g"]

        if len(score) != 5:
            self.logger.warning("Invalid score length")
            return False

        for a in range(5):
            self.logger.debug(f"{score[a] =}, {guess[a] =}, {self.current_score[a] =}")
            if score[a] not in char_list:
                self.logger.error(
                    f"Invalid char <{score[a]}> in score, valid list {char_list}"
                )
                return False
            if (
                self.current_score[a] != "_"
                and self.current_score[a] != guess[a]
                and score[a] == "g"
            ):
                self.logger.error(
                    f"Invalid score, found a valid guess at position {a + 1} already"
                )
                return False
            if score[a] in ["y", "g"] and guess[a] in self.not_found_chars:
                self.logger.error(f"{guess[a]} was already marked not found")
                return False
            if score[a] == "b" and guess[a] == self.current_score[a]:
                self.logger.error(f"{guess[a]} was marked as found already")
                return False

        return True

    def possible_word(self, word: str) -> bool:
        """
        @word: word we're checking
        Determine if a word is still possible based on found and not found chars
        """
        # eliminate any words with chars in our not_found_chars list
        if any(letter in word for letter in self.not_found_chars):
            return False
        # remove any words without chars we know ARE in it
        elif any(letter not in word for letter in self.found_chars):
            return False

        # take into account letter positions found
        if self.current_score != ["_"] * 5:
            for idx in range(len(word)):
                if (
                    self.current_score[idx] != "_"
                    and word[idx] != self.current_score[idx]
                ):
                    return False
        return True

    def _remove_invalid_words(self) -> None:
        """
        Eliminate any words in our word_list based on what we know so far
        """
        self.logger.debug(f"{self.not_found_chars = }, {self.found_chars =}")
        # make deep copy, cant iterate and change list size
        word_list = self.word_list[:]
        for word in word_list:
            # remove any words with chars we know arent in it
            if not self.possible_word(word):
                self.word_list.remove(word)

        self.logger.info(f"Possible # of words {len(self.word_list)}\n")

    def update_score(self, word_guess: str, word_score: str) -> bool:
        """
        Track letters that are found and their positions
        @word_guess: Last word guessed
        @word_score: Score given by Wordle in color coded format, [G]reen, [Y]ellow, [B]lack
        return: bool of sucess
        """

        # ensure score is valid before continuing
        if not self._validate_score(word_guess, word_score):
            return False

        # track found letters
        for a in range(5):
            score = word_score[a].lower()
            guess = word_guess[a].lower()

            if score == "b":
                try:
                    self.not_found_chars.add(guess)
                except ValueError:
                    # ignore cases of duplicate letters where first instance is marked as 'b', e.g. word_guess:'tests' word_score:'gbbbb'
                    pass
            elif score == "g":
                self.current_score[a] = guess
                self.found_chars.add(guess)
            elif score == "y":
                self.found_chars.add(guess)
        print(f"Word so far: {self.current_score}")

        self._remove_invalid_words()

        return True

    def prompt(self) -> None:
        """
        Gets input from user until word is guessed with a score of "ggggg"
        or user quits
        """
        if self.answer:
            word_guess = self.guess_word()
            tries = 0
            print(f"Guess: {word_guess}")

            while self.score_word(word_guess, self.answer) != "ggggg":
                self.update_score(
                    word_guess, self.score_word(word_guess, self.answer)
                )  # flake8: ignore
                word_guess = self.guess_word()
                tries += 1
                print(f"Guess: {word_guess}")

            print(f"Correctly guessed: {word_guess} in {tries}")

        else:
            word_guess = input("Enter initial word guess: ")
            if len(word_guess) != 5:
                self.logger.error("Invalid word size")
                return

            while True:
                while True:
                    word_score = input("Enter word score: ")
                    if self.update_score(word_guess, word_score):
                        self.logger.debug("Valid score")
                        break
                    else:
                        self.logger.error("Invalid score")
                if word_score == "g" * 5:
                    print(f"Word correctly guessed: {word_guess}")
                    return

                word_guess = self.guess_word()
                print(f"Guess: {word_guess}")
