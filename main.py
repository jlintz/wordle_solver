#!/usr/bin/env python3
"""
Main program
"""
import logging
import sys

import click
from wordle import Wordle


@click.command()
@click.option("--filename", "-f", default="word_list", help="wordle list")
@click.option(
    "--answer",
    "-a",
    help="Provide an answer and have system autosolve",
)
@click.option("--debug", default=False, is_flag=True, help="debugging")
def main(filename: str, debug: bool, answer: str):
    """
    main
    """
    with open(filename, "r", encoding="utf-8") as fh:
        word_list = fh.read().splitlines()

    wordle = Wordle(word_list, answer)
    wordle.logger.setLevel(logging.INFO)
    if debug:
        wordle.logger.setLevel(logging.DEBUG)
    wordle.logger.addHandler(logging.StreamHandler(sys.stdout))
    wordle.prompt()


if __name__ == "__main__":
    main()
