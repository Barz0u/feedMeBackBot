import os
from slackeventsapi import SlackEventAdapter
import botInstance as Instance

SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, endpoint="/slack_events")

botInstances = {}

@slack_events_adapter.on("message")
def message(event_data):
    event = event_data["event"]
    #print("event received: " + str(event))

    if event.get("subtype") == "bot_message":
        return

    user = event['user']

    if user not in botInstances:
        print("Premiere conversation, creation de l'user et de son instance du bot")
        botInstances[user] = Instance.botInstance()

    # Call the bot instance function for the message
    print("event received from " + str(user) + " using his own instance: " + str(botInstances[user]))
    botInstances[user].message_im(event_data)

slack_events_adapter.start(port=3000)
