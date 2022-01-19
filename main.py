#!/usr/bin/env python3
import click
from wordle import Wordle


@click.command()
@click.option(
    "--filename", "-f", default="wordle-answers-alphabetical.txt", help="wordle list"
)
def main(filename):
    with open(filename, "r") as fh:
        word_list = fh.read()

    wordle = Wordle(word_list)
    wordle.prompt()


if __name__ == "__main__":
    main()
