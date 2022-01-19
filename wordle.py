import string


class Wordle:
    """
    Instantiate wordle class
    """

    def __init__(self, wordle_list: list = None):
        self.alphabet_list = list(string.ascii_lowercase)

        self.current_score = ["_"] * 6
        self.found_chars = set()
        self.word_list = wordle_list


    def guess_word(self):
        pass

    def _validate_score(self, guess: str, score: str) -> bool:
        """
        @guess: current word being guessed
        @score: color coded score given to the @guess by wordle. Valid chars are b == black, y == yellow, g == green

        @return bool, return True if the score entered is valid
        """
        char_list = ["b", "y", "g"]
        if len(guess) != 5:
            return False

        for a in range(5):
            if guess[a] not in char_list:
                print(f"Invalid char in score, valid list {char_list}")
                return False
            if (
                self.current_score[a] != "_"
                and self.current_score[a] != guess[a]
                and score[a] == "g"
            ):
                print(f"Invalid score, found a valid guess at position {a + 1} already")
                return False
            if score[a] in ["y", "g"] and score[a] not in self.alphabet_list:
                print(f"{score[a]} was already marked not found")
                return False

        return True

    def update_score(self, word_guess: str, word_score: str) -> None:
        # track found letters
        for a in range(5):
            score = word_score[a]
            guess = word_guess[a]

            if score == "b":
                self.alphabet_list.remove(guess)
            elif score == "g":
                self.current_score[a] = guess
                self.found_chars.add(guess)
            elif score == "y":
                self.found_chars.add(guess)

    def prompt(self):
        while True:
            word_guess = input("Enter word guess: ")
            if len(word_guess) != 5:
                print("Invalid word size")
                continue

            while True:
                word_score = input("Enter word score: ")
                if self._validate_score(word_score, word_guess, current_score):
                    break
                else:
                    print("Invalid score")

            self.update_score(word_guess, word_score)
