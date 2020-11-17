from pathlib import Path
from functools import partial
from PyInquirer import prompt
import yaml


def answers_lookup(answers, key):
    return answers[key]


def when_preprocessor(questions):
    """Replaces when statement in question by function
    that lookup in previous answers

    Args:
        questions: list of questions

    Returns:
        Generator with preprocessed questions
    """
    for question in questions:
        if "when" in question:
            question["when"] = partial(answers_lookup, key=question["when"])
        yield question


def load_questions(filename="questions.yaml"):
    """Loads questions from file
    and prepare to use them in PyInquirer
    """
    questions_text = Path(filename).read_text()
    questions_yaml = yaml.safe_load(questions_text)
    questions = when_preprocessor(questions_yaml)
    return questions


if __name__ in "__main__":
    answers = prompt(load_questions())
    print(yaml.dump(answers))
