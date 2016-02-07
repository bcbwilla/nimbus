from plugin import CommandPlugin, PluginException
import json

class Poll(CommandPlugin):

    """Creates a poll on a question based on emoji reactions provided by the bot"""

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['poll', 'vote']
        self.short_help = 'Create a poll'
        self.help = self.short_help
        self.help_example = ['!poll What are better, dogs or cats? :cat: :dog:']

    def on_command(self, event, response):
        args = event['text']
        if args:
            # Split the command in parts where '!vote' already gets removed so arg 0 would be emoji1, and arg1 emoji2.
            parts = event['text'].split(' ')
            motion = event['text'].split(':')[0]

            therest = args.replace(motion + ' ', '')
            emojis = therest.split(' ')

            response['link_names'] = 1  # Enables linking of names
            attach = Poll.build_slack_attachment(emojis, motion, event)
            response.update(attachments=json.dumps([attach]))
            message = self.bot.sc.api_call('chat.postMessage', **response)
            message = json.loads(message)

            # Create and send first emoji reaction
            for emoji in emojis:
                self.bot.sc.api_call('reactions.add', **{'name': emoji.replace(':', ''), 'channel': response['channel'], 'timestamp': result['ts']})
        else:
            raise PluginException('Invalid syntax! E.g. `!vote <question> <emoji...>`')

    @staticmethod
    def build_slack_attachment(emojis, motion, event):
        message = {
            'text': '',
            'title': ':chart_with_upwards_trend: New poll created by <@%s>! ' % event['user'],
            'mrkdwn_in': ['text']
        }

        message['text'] += '*Motion:* %s \n' % motion
        message['text'] += '*You get to choose between:*'
        options = ''
        for emoji in emojis:
            options += emoji + ' '

        message['text'] += ' %s' % options.replace(motion, '')

        return message
