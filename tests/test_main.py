import unittest
from main import Wordle


class TestWordle(unittest.TestCase):
    def setUp(self):
        wordle_list = [
            "tents",
            "tests",
            "tanks",
            "truth",
        ]
        self.wordle = Wordle(wordle_list)
        self.answer = "tests"

    def test_score_word(self):
        self.assertEqual(self.wordle.score_word("tests", self.answer), "ggggg")
        self.assertEqual(self.wordle.score_word("fubar", self.answer), "bbbbb")
        self.assertEqual(self.wordle.score_word("resty", self.answer), "bgggb")
        self.assertEqual(self.wordle.score_word("letsb", self.answer), "bgyyb")

    def test_validate_score_length(self):
        self.assertFalse(self.wordle._validate_score("tests", "bbbbbb"))
        self.assertFalse(self.wordle._validate_score("tests", "bbbb"))

    def test_validate_score_duplicate_found_letter(self):
        self.assertTrue(self.wordle.update_score("tests", "gbbbb"))
        self.assertFalse(self.wordle.update_score("foooo", "gbbbb"))

    def test_validate_score_duplicate_not_found_letter(self):
        self.assertTrue(self.wordle.update_score("tests", "gbbbb"))
        self.assertFalse(
            self.wordle.update_score(
                "tests",
                "bbbbb",
            ),
            self.wordle.current_score,
        )

    def test_validate_update_score(self):
        self.wordle.update_score("tests", "gbbbb")
        self.assertEqual(self.wordle.current_score, list("t____"))

        # ensure state doesnt change with same word and score
        self.wordle.update_score("tests", "gbbbb")
        self.assertEqual(self.wordle.current_score, list("t____"))

        # assert current char count
        self.wordle.update_score("books", "bybgb")
        self.assertEqual(self.wordle.current_score, list("t__k_"))
        self.assertEqual(sorted(self.wordle.found_chars), sorted(list("tok")))

    def test_validate_update_score_complete(self):
        self.wordle.update_score("tests", "ggggg")
        self.assertEqual(self.wordle.current_score, list("tests"))
        self.assertEqual(sorted(self.wordle.found_chars), sorted(list("tes")))

    def test_possible_word_found_and_not_found(self):
        self.wordle.found_chars = ["a", "c"]
        self.wordle.not_found_chars = ["b", "e"]

        self.assertFalse(self.wordle.possible_word("chest"))
        self.assertFalse(self.wordle.possible_word("trips"))

        self.assertTrue(self.wordle.possible_word("crack"))
        self.assertFalse(self.wordle.possible_word("flats"))

    def test_possible_word_no_found_yet(self):
        self.wordle.found_chars = []
        self.wordle.not_found_chars = ["b", "e"]

        self.assertTrue(self.wordle.possible_word("crack"))
        self.assertFalse(self.wordle.possible_word("chest"))
        self.assertTrue(self.wordle.possible_word("rants"))

    def test_possible_word_nothing_found_yet(self):
        self.wordle.found_chars = []
        self.wordle.not_found_chars = []

        self.assertTrue(self.wordle.possible_word("crack"))
        self.assertTrue(self.wordle.possible_word("chest"))
        self.assertTrue(self.wordle.possible_word("rants"))

    def test_possible_word_found_positions(self):
        self.wordle.found_chars = ["a", "s", "t"]
        self.wordle.not_found_chars = ["b", "e"]
        self.wordle.current_score = ["_", "_", "_", "s", "t"]

        self.assertFalse(self.wordle.possible_word("whack"))
        self.assertFalse(self.wordle.possible_word("crest"))
        self.assertFalse(self.wordle.possible_word("blast"))

        self.assertTrue(self.wordle.possible_word("rhast"))

    def test_remove_invalid_words(self):
        self.wordle.found_chars = []
        self.wordle.not_found_chars = ["b", "e"]
        self.wordle._remove_invalid_words()
        self.assertListEqual(["tanks", "truth"], self.wordle.word_list)


if __name__ == "__main__":
    unittest.main()
