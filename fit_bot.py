import os
import json
import argparse
import logging
from Dialogflow import create_intent, PRJ_ID, train_agent

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

    intent_display_names = list(questions.keys())

    for intent_name in intent_display_names:
        intent_questions = questions[intent_name]["questions"]
        intent_answer = questions[intent_name]["answer"]
        create_intent(
            PRJ_ID,
            intent_name,
            intent_questions,
            (intent_answer,)
        )
        train_agent(PRJ_ID)
        logger.info("Agent training started")


if __name__ == "__main__":
    main()