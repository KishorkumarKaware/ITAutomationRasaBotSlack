from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from flask import Blueprint, request, jsonify
import requests
from rasa_core.channels.channel import UserMessage, OutputChannel
from rasa_core.channels.rest import HttpInputComponent

logger = logging.getLogger(__name__)


class CustomOutput(OutputChannel):
    """A bot that uses a custom channel to communicate."""

    def __init__(self, url, access_token):
        self.access_token = access_token
        self.url = url

    def send_text_message(self, recipient_id, message):
        # you probably use http to send a message
        url = self.url
        if self.access_token is not None:
            headers = {"Auth-token": self.access_token}
        else:
            headers = {}

        requests.post(
                url,
                message,
                headers=headers
        )


class CustomInput(HttpInputComponent):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    def __init__(self, url, access_token=None):
        self.out_channel = CustomOutput(url='https://vyomtalk.slack.com/messages/D83FA57AL/team/U6KEL2807/', access_token='xoxb-274915650144-79SUtKxqc3KekyPsnjWrD0ev')

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/app", methods=['POST'])
        def receive():
            print("Received POST Request on endpoint /app")
            print("Request ", request);
            payload = request.json
            print(payload)
            sender = payload.get("sender", None)
            text = payload["text"]
            print(text)
            on_new_message(UserMessage(text, self.out_channel, sender))
            return "success"

        return custom_webhook
