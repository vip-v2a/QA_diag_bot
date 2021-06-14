import json
from Dialogflow import create_intent, PRJ_ID, train_agent

with open("questions.json", "r") as my_file:
  questions = json.load(my_file)

intent_display_names = list(questions.keys())

for intant_name in intent_display_names:
    intant_questions = questions[intant_name]["questions"]
    intant_answer = questions[intant_name]["answer"]
    create_intent(
        PRJ_ID, 
        intant_name, 
        intant_questions, 
        (intant_answer,)
    )
    train_agent(PRJ_ID)


