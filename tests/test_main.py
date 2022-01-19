import unittest
from main import Wordle

class TestWordle(unittest.TestCase):

    def setUp(self):
        wordle_list = [
                'tents',
                'tests',
                'tanks',
                'truth',
                ]
        wordle = Wordle(wordle_list)
        self.answer = 'tests'

    def test_case(self):
        self.assertTrue(1 == 1)


if __name__ == '__main__':
    unittest.main()
