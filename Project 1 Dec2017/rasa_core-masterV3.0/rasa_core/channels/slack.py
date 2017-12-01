from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from builtins import str
from flask import Blueprint, request, jsonify
#from pymessenger.bot import Bot
from slackclient import SlackClient

from rasa_core.channels.channel import InputChannel
from rasa_core import utils

from rasa_core.channels.channel import UserMessage, OutputChannel
from rasa_core.channels.rest import HttpInputComponent

logger = logging.getLogger(__name__)


class MessengerBot(SlackClient, OutputChannel):
    """A bot that uses slack-messenger to communicate."""

    def __init__(self, slack_token="xoxb-274915650144-79SUtKxqc3KekyPsnjWrD0ev"):
        super(MessengerBot, self).__init__(slack_token)
        print(slack_token)

  
    def send_custom_message(self):
       # sc = SlackClient("xoxb-274915650144-79SUtKxqc3KekyPsnjWrD0ev")
        print(self.api_call("chat.postMessage",channel="D84K3G6T1",text="Hello from deepak Python! :tada:"))
    


class SlackInput(HttpInputComponent):
    def __init__(self,slack_token="xoxb-274915650144-79SUtKxqc3KekyPsnjWrD0ev", debug_mode):
        #self.slack_verify = slack_verify
        #self.slack_secret = slack_secret
        self.debug_mode = debug_mode
        self.slack_token = slack_token

    @staticmethod
    def _is_user_message(slack_event):
        return (slack_event.get('message') and
                slack_event['message'].get('text') and
                not slack_event['message'].get("is_echo"))

          
    def blueprint(self, on_new_message):
       # from pymessenger.utils import validate_hub_signature

        slack_webhook = Blueprint('slack_webhook', __name__)

        @slack_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @slack_webhook.route("/app", methods=['GET', 'POST'])
        def hello():
            #if request.method == 'GET':
             #   if request.args.get("hub.verify_token") == self.slack_verify:
              #      return request.args.get("hub.challenge")
               # else:
                #    return "failure, invalid token"
            if request.method == 'POST':

               # signature = request.headers.get("X-Hub-Signature") or ''
               # if not validate_hub_signature(self.slack_secret, request.data,
                #                              signature):
                #    return "not validated"

                output = request.json
                Channel = output['entry'][0]['id']
                event = output['entry'][0]['messaging']
                for x in event:
                    if self._is_user_message(x):
                        text = x['message']['text']
                   
                    else:
                        continue
                
                    try:
                        sender = x['sender']['id']
                        if page_id in self.slack_token:
                            out_channel = MessengerBot(self.slack_token])
                            user_msg = UserMessage(text, out_channel, sender)
                            on_new_message(user_msg)
                        else:
                            raise Exception("Unknown page id '{}'. Make sure to"
                                            " add a page token to the "
                                            "configuration.".format(page_id))
                    except Exception as e:
                        logger.error("Exception when trying to handle "
                                     "message.{0}".format(e))
                        if self.debug_mode:
                            raise
                        pass

                return "success"

        return slack_webhook
