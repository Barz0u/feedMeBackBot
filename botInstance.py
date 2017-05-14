# -*- coding: utf-8 -*-

import os
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter
from slacker import Slacker

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

class botInstance:

    remerciements = "Voulez-vous remerciez l'émetteur? (oui/non)"

    def __init__(self):
        self.bot_token = os.environ.get('SLACK_BOT_TOKEN')
        self.slack_client = SlackClient(self.bot_token)
        self.slack = Slacker(self.bot_token)

        self.SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
        self.slack_events_adapter = SlackEventAdapter(self.SLACK_VERIFICATION_TOKEN, endpoint="/slack_events")

        self.conv_state = {}
        self.feedback_target = {}

    def ask_who_to_notify(self, channel, user, text):
        message = "Je suis le service de commentaire positif! :watermelon:\nQuelle est la personne que vous souhaitez notifier?"
        self.slack.chat.post_message(channel, message)

        # Change state of the conversation
        self.conv_state[channel] = 1;

    def first_contact(self, channel, user, text):
        message = "Bonjour <@%s>! :tada:" % user
        self.slack.chat.post_message(channel, message)
        botInstance.ask_who_to_notify(self, channel, user, text)

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
        chan = "@" + self.feedback_target[user]
        resp = self.slack.im.open(self.feedback_target[user])
        chan = resp.body.get("channel").get("id")

        positive_feedback = "Vous avez reçu un feedback:\n" + text

        self.slack.chat.post_message(chan, positive_feedback)
        self.slack.chat.post_message(chan, self.remerciements)

        text = "Le message a bien été envoyé. :pray:"
        self.slack.chat.post_message(channel, text)

        self.conv_state[channel] = 3

    def get_thanks_choice(self, channel, user, text):
        split = text.split()
        choice = split[0]

        if choice.startswith('o'):
            text = "Remerciement envoyé! :ok_hand:\nVotre karma augmente de *3 points!* (solde karma: 15)"
        elif choice.startswith('n'):
            text = "Bien reçu!"
        else:
            text = "Je n'ai pas compris votre réponse.\nVoulez-vous remerciez l'émetteur? (oui/non)"

        resp = self.slack.im.open(self.feedback_target[user])
        chan = resp.body.get("channel").get("id")

        positive_feedback = "Vous avez reçu un feedback:\n" + text

        self.slack.chat.post_message(chan, positive_feedback)
        text = "Le message a bien été envoyé. :pray:"
        self.slack.chat.post_message(channel, text)

        self.conv_state[channel] = 3

    def message_im(self, event_data):
        message = event_data["event"]
        channel = message["channel"]
        text = message["text"]


        # If the message comes from the bot itself, or another bot
        if message.get("subtype") == "bot_message":
            if text == self.remerciements:
                print("mode remerciements")
                self.conv_state[channel] = 10
                return
            else:
                print("bot message, skip.")
                return
        else:
            user = message["user"]

        if channel not in self.conv_state:
            print("Premiere conversation, creation de l'user dans la map")
            self.conv_state[channel] = 0

        # Different behavior depending on the conversation state
        if self.conv_state[channel] == 0:
            self.first_contact(channel, user, text)
        elif self.conv_state[channel] == 1:
            self.get_username_from_message(channel, user, text)
        elif self.conv_state[channel] == 2:
            self.get_feedback_from_message(channel, user, text)
        elif self.conv_state[channel] == 10:
            self.get_thanks_choice(channel, user, text)
        else:
            print("fail")
