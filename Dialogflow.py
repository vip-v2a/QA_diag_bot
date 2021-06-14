import os

PRJ_ID = os.getenv("PRJ_ID")
TELEGRAM_ID = os.getenv("TELEGRAM_ID")
LANGUAGE_CODE = "ru"


def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'private_key.json'
    )

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print("Session path: {}\n".format(session))

    # for text in texts:
    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

        # print("=" * 20)
        # print("Query text: {}".format(response.query_result.query_text))
    query_text = response.query_result.query_text
    is_fallback = response.query_result.intent.is_fallback
    """print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )"""
    intent_display_name = response.query_result.intent.display_name
    intent_detection_confidence = response.query_result.intent_detection_confidence
        # print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    fulfillment_text = response.query_result.fulfillment_text
    return (
        fulfillment_text,
        intent_display_name,
        intent_detection_confidence,
        is_fallback
    )


# my_text = input('texts to bot: ')
# print(detect_intent_texts(PRJ_ID, TELEGRAM_ID, my_text, LANGUAGE_CODE))


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))

def train_agent(project_id):
    from google.cloud import dialogflow

    agents_client = dialogflow.AgentsClient()
    parent = dialogflow.AgentsClient.common_project_path(project_id)
    response = agents_client.train_agent(
        request={"parent": parent}
    )

    print(f"Обучение выполнено: {response.done()}")



