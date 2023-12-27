import argparse
import pytest
import json
import random


def choice(choices: dict[str, float]) -> str:
    """ Takes in a dictionary of choices and their transition probabilities
    and returns a random choice based on the probabilities.
    """
    rand_val = random.random()
    total = 0

    for choice, prob in choices.items():
        total += prob
        if rand_val <= total:
            return choice
    


def generate(pfsa: dict[str, dict[str, float]], word_count: int) -> str:
    """Takes in the PFSA and generates a string of `word_count` number of words

    The following string is when the input has only "Cat" as in it's PFSA with
    count of 4.
    """
    # TODO: FILE IN THIS FUNCTION

    if pfsa == {"*": {}}:
        return ""
    
    # initialize the output string
    output_string = ""
    current_state = "*"

    count = 0
    while count < word_count:
        if current_state in pfsa:
            # choose the next state based on their probabilities
            next_state = choice(pfsa[current_state])
            if next_state == "*":
                continue
            if next_state[-1] == '*':
                output_string += next_state[:-1] + " "
                count += 1
                current_state = "*"
            else:
                current_state = next_state  
        else:
            break

    return output_string[:-1]


def main():
    """
    The command for running is `python generator.py text.json 5`. This will
    generate a file `text_sample.txt` which has 5 randomly sampled words.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    parser.add_argument("count", type=int, help="Sample size to gen")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        data = json.load(file)
        output = generate(data, args.count)

    # data = {"*": {"m": 1.0}, "m": {"ma": 0.5, "me": 0.3, "mo": 0.2}, "ma": {"mat": 0.6, "mai": 0.2, "man": 0.2}, "mat": {"mat*": 0.3333333333333333, "mate": 0.3333333333333333, "mati": 0.3333333333333333}, "mate": {"mate*": 1.0}, "mati": {"matin": 1.0}, "matin": {"mating": 1.0}, "mating": {"mating*": 1.0}, "mai": {"mail": 1.0}, "mail": {"mail*": 1.0}, "me": {"men": 0.3333333333333333, "mes": 0.6666666666666666}, "men": {"men*": 1.0}, "man": {"man*": 1.0}, "mes": {"mess": 1.0}, "mess": {"mess*": 0.5, "messa": 0.5}, "messa": {"messag": 1.0}, "messag": {"message": 1.0}, "message": {"message*": 1.0}, "mo": {"mos": 0.5, "mom": 0.5}, "mos": {"moss": 1.0}, "moss": {"moss*": 1.0}, "mom": {"mom*": 1.0}}
    # output = generate(data, 10)

    # print(output)

    name = args.file.split(".")[0]

    with open(f"{name}_sample.txt", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()


DICTIONARIES = [
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"c": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
]
STRINGS = [
    "a",
    "a a a a a",
    "",
    "cat cat cat cat",
]
COUNT = [1, 5, 0, 4]

COMBINED = [(d, s, c) for d, (s, c) in zip(DICTIONARIES, zip(STRINGS, COUNT))]


@pytest.mark.parametrize("pfsa, string, count", COMBINED)
def test_output_match(pfsa, string, count):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = generate(pfsa, count)
    assert result == string
