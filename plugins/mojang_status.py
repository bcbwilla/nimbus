#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests

from plugin import CommandPlugin


class MojangStatus(CommandPlugin):
    """
    Prints the status of Mojang's services
    """
    mojang_status_link = 'http://status.mojang.com/check'

    server_name = {
        'minecraft.net': 'Website',
        'account.mojang.com': 'Accounts',
        'authserver.mojang.com': 'Login',
        'sessionserver.mojang.com': 'Sessions',
        'textures.minecraft.net': 'Skins',
        'api.mojang.com': 'API'
    }

    status = {
        'green': ':white_check_mark:',
        'yellow': ':warning:',
        'red': ':x:',
    }

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['mojang', 'mcstatus']
        self.short_help = 'Prints the status of Mojang\'s services'
        self.help = self.short_help
        self.help_example = ['!mojang']

    @staticmethod
    def build_slack_attachment(data):
        response = {
            'title': 'Mojang Status Summary',
            'title_link': 'https://help.mojang.com/',
            'mrkdwn_in': ['text']
        }

        formatted = list()
        for service in data:
            service_link = next(iter(service.keys()))

            if service_link in MojangStatus.server_name:
                color = service[service_link]
                stat = MojangStatus.status.get(color, ':question:')
                formatted.append('%s *<http://%s|%s>*' % (stat, service_link, MojangStatus.server_name[service_link]))

        response.update(text=' - '.join(formatted))

        return response

    @staticmethod
    def get_mojang_status():
        r = requests.get(MojangStatus.mojang_status_link)

        if r.status_code != 200:
            print "Can't get Mojang Status!"
            return
        else:
            status = r.json()

            return MojangStatus.build_slack_attachment(status)

    def on_command(self, bot, event, response):
        response.update(attachments=json.dumps([MojangStatus.get_mojang_status()]))
        bot.sc.api_call('chat.postMessage', **response)
