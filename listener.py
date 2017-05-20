from slackeventsapi import SlackEventAdapter
import BotInstance as Instance


botInstances = {}
slack_bot_token = input("Please enter your SLACK_BOT_TOKEN: ")
slack_verification_token = input("Please enter your SLACK_VERIFICATION_TOKEN: ")

slack_events_adapter = SlackEventAdapter(slack_verification_token, endpoint="/slack_events")

@slack_events_adapter.on("message")
def message(event_data):
    event = event_data["event"]
    #print("event received: " + str(event))
    print("channel: " + event["channel"])


    channel = event['channel']

    if channel not in botInstances:
        print("Premiere conversation, creation de l'user et de son instance du bot")
        botInstances[channel] = Instance.BotInstance(slack_bot_token)

    # Call the bot instance function for the message
    print("event received from channel " + str(channel) + " using his own instance: " + str(botInstances[channel]))
    botInstances[channel].message_im(event_data)

slack_events_adapter.start(port=3000)
