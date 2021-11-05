import os
import logging
from google.cloud import dialogflow

PROJECT_ID = os.getenv("PROJECT_ID")
TELEGRAM_ID = os.getenv("TELEGRAM_ID")
LANGUAGE_CODE = "ru"

logger = logging.getLogger(__file__)


def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    is_fallback = response.query_result.intent.is_fallback
    intent_display_name = response.query_result.intent.display_name
    int_detection_accuracy = response.query_result.intent_detection_confidence
    fulfillment_text = response.query_result.fulfillment_text

    return (
        fulfillment_text,
        intent_display_name,
        int_detection_accuracy,
        is_fallback
    )


def create_intent(
    project_id,
    display_name,
    training_phrases_parts,
    message_texts
):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logger.info("Intent created: {}".format(response))


def train_agent(project_id):

    agents_client = dialogflow.AgentsClient()
    parent = dialogflow.AgentsClient.common_project_path(project_id)
    response = agents_client.train_agent(
        request={"parent": parent}
    )

    logger.info(f"Обучение выполнено: {response.done()}")
