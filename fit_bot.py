import json
from Dialogflow import create_intent, PRJ_ID, train_agent

with open("questions.json", "r") as my_file:
    questions = json.load(my_file)

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
