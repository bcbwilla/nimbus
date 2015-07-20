#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from utils import valid_minecraft_username
from plugin import CommandPlugin

mojang_profile_link = 'https://api.mojang.com/profiles/minecraft'


def lookup_username(name):
    if not valid_minecraft_username(name):
        return build_slack_attachment(name, None, valid_name=False)

    payload = json.dumps(name)
    header = {'Content-type': 'application/json'}
    r = requests.post(mojang_profile_link, headers=header, data=payload)

    if r.status_code != requests.codes.ok:
        print "Can't get lookup Minecraft username %s!" % name
        return
    else:
        return build_slack_attachment(name, r.json())


def build_slack_attachment(name, response, valid_name=True):
    message = {
        'title': 'Minecraft Username Lookup',
        'mrkdwn_in': ['text']
    }

    if not valid_name:
        message['text'] = ':warning: Username `%s` is not a valid username!' % name
    elif not response:
        message['text'] = ':white_check_mark: Username `%s` is available!' % name
    elif 'legacy' in response[0]:
        message['text'] = ':x: Username `%s` is taken but not premium!' % name
    else:
        message['text'] = ':x: Username `%s` is taken!' % name

    return message


class MCName(CommandPlugin):
    """Checks if a Minecraft username is registered"""

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['mcname']
        self.short_help = 'Checks whether a Minecraft username is available'
        self.help = self.short_help
        self.help_example = ['!mcname Plastix', '!mcname Apple']

    def on_command(self, bot, event, response):
        split = event['text'].split(' ')
        response.update(attachments=json.dumps([lookup_username(split[0])]))
        bot.sc.api_call('chat.postMessage', **response)
