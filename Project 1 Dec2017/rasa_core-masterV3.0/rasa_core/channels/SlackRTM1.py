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

class SlackRTMOutputChannel(SlackClient,OutputChannel):
        """Simple bot that outputs the bots messages to the command line."""
        def __init__(self,client,channel):
            self.channel=channel
            self.client=client

        #default_output_color = utils.bcolors.OKBLUE

        def send_text_message(self, recipient_id, message):
            
            #utils.print_color(message, self.default_output_color)
            
            chan = self.client.server.channels.find(self.channel)
            if not chan:
                raise Exception("Channel %s not found." % channel)
            return chan.send_message(message)
        
            # type: (Text, Text) -> None
        

class SlackRTMInputChannel(InputChannel):
    """Input channel that reads the user messages from the command line."""
    def __init__(self,token,debug_mode):
        self.token=token
        self.debug_mode = debug_mode
 
            
    
##################################################################################
    def _record_messages(self, on_message, max_message_limit=None):
        utils.print_color("Bot loaded. Type a message and press enter : ",
                          utils.bcolors.OKGREEN)
        client = None
        my_user_name = ''

        self.client = SlackClient(self.token)
        self.client.rtm_connect()
        self.my_user_name = self.client.server.username
        print("Connected to Slack.")
        num_messages = 0
        while max_message_limit is None or num_messages < max_message_limit: 
            try:
                input = self.client.rtm_read()
                if input:
                    for action in input:
                        if self.debug_mode:
                            print(action)
                        if 'type' in action and action['type'] == "message":
                            # Uncomment to only respond to messages addressed to us.
                            # if 'text' in action
                            #   and action['text'].lower().startswith(self.my_user_name):
                            #print(action['text'])
                            text=action["text"]
                            channel=action["channel"]
                            #print("User said",text)
                            # self.process_message(action)
                            out_channel = SlackRTMOutputChannel(self.client,channel)
                            on_message(UserMessage(text, out_channel))
                            num_messages += 1
                else:
                    sleep(1)
            except Exception as e:
                print("Exception: ", e.message)
                

    def start_async_listening(self, message_queue):
        self._record_messages(message_queue.enqueue)

    def start_sync_listening(self, message_handler):
        self._record_messages(message_handler)

        ########################################################################
        