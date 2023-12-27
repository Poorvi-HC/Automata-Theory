import argparse
import pytest
import json


def construct(file_str: str) -> dict[str, dict[str, float]]:
    """Takes in the string representing the file and returns pfsa

    The given example is for the statement "A cat"
    """
    # TODO: FILE IN THIS FUNCTION

    # store all the strings in contents
    contents = file_str.split() 
    
    # create a dictionary to store the pfsa
    pfsa = {}

    if contents == []:
        pfsa["*"] = {}
        return pfsa
    
    # iterate through the contents
    for word in contents:
        current_state = "*" # reset the current state
        word = word.lower() 
        # iterate through the word
        prefix = ""
        for char in word:
            prefix += char
            # if the current state is not in the pfsa, add it
            if current_state not in pfsa:
                pfsa[current_state] = {}
            # if the character is not in the current state, add it
            if prefix not in pfsa[current_state]:
                pfsa[current_state][prefix] = 1.0
            # if the character is in the current state, increment it
            else:
                pfsa[current_state][prefix] += 1.0
            # update the current state
            current_state = prefix
        # add the end state
        prefix += "*"
        if current_state not in pfsa:
                pfsa[current_state] = {}
        # if the character is not in the current state, add it
        if prefix not in pfsa[current_state]:
            pfsa[current_state][prefix] = 1.0
        # if the character is in the current state, increment it
        else:
            pfsa[current_state][prefix] += 1.0

    # Normalize transition probabilities
    for state, transitions in pfsa.items():
        total = sum(transitions.values())
        for prefix in transitions.keys():
            transitions[prefix] /= total
            round(transitions[prefix], 2)

    return pfsa


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)



if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    assert result == pfsa