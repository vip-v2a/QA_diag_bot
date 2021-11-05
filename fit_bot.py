import json
import argparse
import logging
from Dialogflow import create_intent, PROJECT_ID, train_agent

logger = logging.getLogger(__file__)


def main():
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

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

    with open(args.filepath, "r") as my_file:
        questions = json.load(my_file)

    for intent_name, intent in questions.items():

        create_intent(
            PROJECT_ID,
            intent_name,
            intent["questions"],
            (intent["answer"],)
        )
        train_agent(PROJECT_ID)
        logger.info("Agent training started")


if __name__ == "__main__":
    main()
