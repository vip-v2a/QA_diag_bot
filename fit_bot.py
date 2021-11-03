import os
import json
import argparse
import logging
from Dialogflow import create_intent, PROJECT_ID, train_agent

logger = logging.getLogger(__file__)


def main():
    logger.setLevel(logging.INFO)
    
    ch = logging.StreamHandler()
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    parser = argparse.ArgumentParser(
        description="Fitting the Dialogflow agent by questions"
    )
    parser.add_argument(
        "-fp",
        "--filepath",
        help="questions filepath",
        default="questions.json"
    )
    args = parser.parse_args()

    questions_filepath = args.filepath

    if not os.path.isfile(questions_filepath):
        logger.info("Incorrect filepath")
        exit()

    try:
        with open(questions_filepath, "r") as my_file:
            questions = json.load(my_file)
    except Exception:
        logger.exception()

    for intent_name, intent in questions.items():
        intent_questions = intent["questions"]
        intent_answer = intent["answer"]

        create_intent(
            PROJECT_ID,
            intent_name,
            intent_questions,
            (intent_answer,)
        )
        train_agent(PROJECT_ID)
        logger.info("Agent training started")


if __name__ == "__main__":
    main()