# -*- coding: utf-8 -*-
from slacker import Slacker
# import sys

# reload(sys);
# sys.setdefaultencoding("utf8")

# Linked channels so the bot can call back
linkedChannels = {}


class BotInstance:

    remerciements = "Voulez-vous remerciez l'émetteur? (oui/non)"

    def __init__(self, slack_bot_token):

        self.slack = Slacker(slack_bot_token)

        self.conv_state = {}
        self.feedback_target = {}

    def ask_who_to_notify(self, channel):
        message = 'Je suis le service de commentaire positif! :watermelon:\nQuelle est la personne que vous '\
                'souhaitez notifier? '
        self.slack.chat.post_message(channel, message)

        # Change state of the conversation
        self.conv_state[channel] = 1

    def first_contact(self, channel, user):
        message = "Bonjour <@%s>! :tada:" % user
        self.slack.chat.post_message(channel, message)
        BotInstance.ask_who_to_notify(self, channel)

    def get_username_from_message(self, channel, user, text):
        split = text.split()
        given_user = split[0]

        if given_user.startswith('<@'):
            given_user = given_user[2:-1]
        else:
            message = "Je ne peux pas trouver cet utilisateur. Ecrivez l'utilisateur en utilisant la touche '@'"
            self.slack.chat.post_message(channel, message)
            return

        # Check if the user exists
        found_user = self.slack.users.info(given_user)
        name = found_user.body.get("user").get("name")
        message = "Quel est votre feedback positif à propos de " + str(
            name) + " aujourd'hui? Ecrivez le ci-dessous et il le lui sera envoyé de façon anonyme."
        self.slack.chat.post_message(channel, message)

        self.conv_state[channel] = 2
        self.feedback_target[user] = given_user

    def get_feedback_from_message(self, channel, user, text):
        resp = self.slack.im.open(self.feedback_target[user])
        chan = resp.body.get("channel").get("id")

        # Prepare callback
        linkedChannels[chan] = channel

        positive_feedback = "Vous avez reçu un feedback:\n" + text

        self.slack.chat.post_message(chan, positive_feedback)
        self.slack.chat.post_message(chan, self.remerciements)

        text = "Le message a bien été envoyé. :pray:"
        self.slack.chat.post_message(channel, text)

        # Reset
        self.conv_state[channel] = 0

    def get_thanks_response(self, channel, text):
        split = text.split()
        user_response = split[0]

        if user_response.startswith('o'):
            message = "Votre commentaire a été apprécié! *+3 points* de karma! (solde de karma: 13)"
            self.slack.chat.post_message(linkedChannels[channel], message)
            message = "L'émetteur a été notifié! Vous gagnez *+3 points* de karma! (solde de karma: 19)"
            self.slack.chat.post_message(channel, message)

            self.conv_state[channel] = 0

        elif user_response.startswith('n'):
            message = "Très bien, bonne journée! :water_melon:"
            self.slack.chat.post_message(channel, message)

            self.conv_state[channel] = 0

        else:
            message = "Je n'ai pas compris votre réponse"
            self.slack.chat.post_message(channel, message)
            self.slack.chat.post_message(channel, self.remerciements)

    def message_im(self, event_data):
        message = event_data["event"]
        text = message["text"]
        channel = message["channel"]

        if message.get("subtype") == "bot_message":
            if text == self.remerciements:
                print("MODE MERCI")
                self.conv_state[channel] = 10
                return
            else:
                return

        user = message["user"]

        if channel not in self.conv_state:
            self.conv_state[channel] = 0

        # Different behavior depending on the conversation state
        if self.conv_state[channel] == 0:
            self.first_contact(channel, user)
        elif self.conv_state[channel] == 1:
            self.get_username_from_message(channel, user, text)
        elif self.conv_state[channel] == 2:
            self.get_feedback_from_message(channel, user, text)
        elif self.conv_state[channel] == 10:
            self.get_thanks_response(channel, text)
        else:
            print("fail")
