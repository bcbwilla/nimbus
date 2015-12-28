import random
from plugin import CommandPlugin, PluginException


class Ball8(CommandPlugin):
    """
    8ball command (by javipepe :))
    """

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['8ball']
        self.short_help = 'Ask me a question'
        self.help = 'Ask me a question, I\'ll decide what the answer should be. Based on https://en.wikipedia.org/wiki/Magic_8-Ball'
        self.help_example = ['!8ball Is linux better than windows?']
        #                                ^ obviously yes.

    def on_command(self, event, response):
        args = event['text']
        if not args or not args[-1:].__contains__('?'):
            raise PluginException('Invalid argument! Ask me a question!')
        else:
            possible_answers = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Do\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']

            response['text'] = ':8ball: says *_%s_*!' % random.choice(possible_answers)
            self.bot.sc.api_call('chat.postMessage', **response)
