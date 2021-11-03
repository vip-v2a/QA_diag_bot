# Dialogflow chatbot
The chatbot answers the most frequent user's questions from telegram or VK.

## Example
VK bot answers ([vk community](https://vk.com/club204811960)):
![](https://github.com/vip-v2a/QA_diag_bot/blob/959617b8b53b0b1694e6016d6cb71849c18078b2/ext/vk_bot_dialog.gif)

Telegram bot answers ([telegram bot](https://t.me/QA_diag_bot)):
![](https://github.com/vip-v2a/QA_diag_bot/blob/959617b8b53b0b1694e6016d6cb71849c18078b2/ext/tg_bot_dialog.gif)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need create environment variables:
- `BOT_TOKEN` from @Bot_father.
- `GOOGLE_APPLICATION_CREDENTIALS` contains `private_key.json`. 
How to get json key see below.
- `PROJECT_ID` Project ID from Project Info in your google cloud console.
- `TELEGRAM_ID` your telegram id from @userinfobot (type command: "/start").
- `VK_BOT_ID` number XXXXXXXXX from URL of your community: "https://vk.com/clubXXXXXXXXX"
- `VK_TOKEN` your VK community token. How to get vk community token see below.

You need install `requirements.txt`
```    
pip install -r requirements.txt
```

### Create JSON KEY

Create a service account:

- In the Cloud Console, go to the Create service account page.
- Go to Create service account
-> Select a project.
- In the Service account name field, enter a name. The Cloud Console fills in the Service account ID field based on this name.
- In the Service account description field, enter a description. For example, Service account for quickstart.
- Click Create.
- Click the Select a role field.
- Under Quick access, click Basic, then click Owner.

Note: The Role field affects which resources your service account can access in your project. You can revoke these roles or grant additional roles later. In production environments, do not grant the Owner, Editor, or Viewer roles. For more information, see Granting, changing, and revoking access to resources.

- Click Continue.
- Click Done to finish creating the service account.
- Do not close your browser window. You will use it in the next step.
- Create a service account key:
- In the Cloud Console, click the email address for the service account that you created.
- Click Keys.
- Click Add key, then click Create new key.
- Click Create. A JSON key file is downloaded to your computer.
- Click Close.

For more infomation, see [Working with Dialogflow using Python Client](https://medium.com/swlh/working-with-dialogflow-using-python-client-cb2196d579a4).

### Get VK community token

You need:
- create community on the ["control" tab](https://vk.com/groups?tab=admin).
- get vk community token: "Manage" - "API usage" - button "Create token" - checkbox "Allow access to community management" and "Allow access to community messages" - add `VK_TOKEN` in `.env`.
- allow to send message: "Manage" - "Messages" - "Community message" is "Enabled" - type "Greeting message" (for example, "Hello, have you questions?") - button "Save".

### Features vk_bot.py

Note: if you want to work with longpoll `bot_longpoll.py` from [vk_api examples](https://github.com/python273/vk_api/tree/master/examples), you need: "Manage" - "API usage" - "LongPoll" set "Enabled" and select version API `>5.80`.

### Fitting of Dialogflow agent
To fit agent you need run `fit_bot.py`. You can add or modify training phrases in `questions.json` file. You can specify questions file path in optional argument `--filepath` (`-fp`):
```
python fit_bot.py -fp "example.json"
```

### Deploy on Heroku
- Repository has `.Procfile` to deploy on Heroku.
- Logs are printed into Telegram (`TELEGRAM_ID`).

To deploy on [Heroku](https://heroku.com/): 
- create a new app on European server.
- create Reveal Config Vars from 'Settings' tab (How to generate a Google credential see below). 
- open 'Deploy' tab on the top menu.
- connect to your github profile.
- select your bots repository.
- choose a branch to deploy 'master' .
- press 'Deploy Branch'.
- waiting 'Your app was successfully deployed'.
- go to 'Recources' tab.
- turn on dynos (if need, edit dino formation -> then switch ON dino app -> confirm).
- drink a cup of tea)

### To generate a Google credential file based on Heroku Config Vars:

1. Create Config Vars key `GOOGLE_CREDENTIALS` and paste the content of service account credential JSON file `private_key.json` as is.
2. Create a key under Config Vars `GOOGLE_APPLICATION_CREDENTIALS` and set a value as `google-credentials.json`.
3. Enter Buildack URL: `https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack`