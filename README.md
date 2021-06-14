# CREATE JSON KEY

Create a service account:

In the Cloud Console, go to the Create service account page.

Go to Create service account
Select a project.
In the Service account name field, enter a name. The Cloud Console fills in the Service account ID field based on this name.

In the Service account description field, enter a description. For example, Service account for quickstart.

Click Create.
Click the Select a role field.

Under Quick access, click Basic, then click Owner.

Note: The Role field affects which resources your service account can access in your project. You can revoke these roles or grant additional roles later. In production environments, do not grant the Owner, Editor, or Viewer roles. For more information, see Granting, changing, and revoking access to resources.
Click Continue.
Click Done to finish creating the service account.

Do not close your browser window. You will use it in the next step.

Create a service account key:

In the Cloud Console, click the email address for the service account that you created.
Click Keys.
Click Add key, then click Create new key.
Click Create. A JSON key file is downloaded to your computer.
Click Close.

#links
https://medium.com/swlh/working-with-dialogflow-using-python-client-cb2196d579a4

#VK bot

you need
- create community on the ["control" tab](https://vk.com/groups?tab=admin)
- get token community: "Manage" - "API usage" - button "Create token" - checkbox "Allow access to community management" and "Allow access to community messages" - add `VK_TOKEN` in `.env`
- allow to send message: "Manage" - "Messages" - "Community message" is "Enabled" - type "Greeting message" (for example, "Hello, have you questions?") - button "Save"

if you want to work with longpoll `bot_longpoll.py` from [vk_api examples](https://github.com/python273/vk_api/tree/master/examples), you need: "Manage" - "API usage" - "LongPoll" set "Enabled" and select version API `>5.80`

