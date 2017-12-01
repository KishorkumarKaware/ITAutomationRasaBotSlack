from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
from builtins import input
from typing import Text

from rasa_core.channels.channel import UserMessage
from rasa_core.channels.channel import InputChannel, OutputChannel
from rasa_core import utils
import argparse, configparser, sys, json, os
from slackclient import SlackClient
from time import sleep

class SlackRTMOutputChannel(OutputChannel):
    """Simple bot that outputs the bots messages to the command line."""

   # default_output_color = utils.bcolors.OKBLUE

    def send_text_message(self, recipient_id, message):
        post(channel="D83FA57AL",message=message)
        # type: (Text, Text) -> None
        utils.print_color(message, self.default_output_color)


class SlackRTMInputChannel(InputChannel):
    """Input channel that reads the user messages from the command line."""
    def __init__(self,token,debug_mode):
        self.token=token
        self.debug_mode = debug_mode
        self.connect(self.token)
        self.listen()
 
    client = None
    my_user_name = ''

    def connect(self, token):
        self.client = SlackClient(token)
        self.client.rtm_connect()
        self.my_user_name = self.client.server.username
        print("Connected to Slack.")
    
    def listen(self):
        while True:
            try:
                input = self.client.rtm_read()
                if input:
                    for action in input:
                        if self.debug_mode:
                            print("Action is :" , action, "Action ends here")
                        if 'type' in action and action['type'] == "message":
                            # Uncomment to only respond to messages addressed to us.
                            # if 'text' in action
                            #   and action['text'].lower().startswith(self.my_user_name):
                            #print(action['text'])
                            text=action["text"]
                            print("User said",text)
                            # self.process_message(action)
                            self._record_messages(on_message)
                else:
                    sleep(1)
            except Exception as e:
                print("Exception: ", e.message)
    
##################################################################################
    def _record_messages(self, on_message, max_message_limit=None):
        utils.print_color("Bot loaded. Type a message and press enter : ",
                          utils.bcolors.OKGREEN)
        num_messages = 0
        while max_message_limit is None or num_messages < max_message_limit:
            #text =  input().strip()
#            if six.PY2:
                # in python 2 input doesn't return unicode values
 #               text = text.decode("utf-8")
  #          if text == '_stop':
   #             import os
                # sys.exit(1)
    #            os._exit(1)
            on_message(UserMessage(text, SlackRTMOutputChannel()))
            num_messages += 1

    def start_async_listening(self, message_queue):
        self._record_messages(message_queue.enqueue)

    def start_sync_listening(self, message_handler):
        self._record_messages(message_handler)

        ########################################################################
        