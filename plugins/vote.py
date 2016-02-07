from plugin import CommandPlugin, PluginException


class Vote(CommandPlugin):

    """Establishes a vote on emojis based on two emojis provided in the command"""

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['vote']
        self.short_help = 'Establish a voting'
        self.help = self.short_help
        self.help_example = ['!vote :cat: :dog: What are better, dogs or cats?', '!vote :hammer: :ok: Is `Brottweiler` appropriate?']
        
    def on_command(self, event, response):
        args = event['text']
        if args:
            # Split the command in parts where '!vote' already gets removed so arg 0 would be emoji1, and arg1 emoji2.
            parts = event['text'].split(' ')
            emoji1 = parts[0]
            emoji2 = parts[1]
            
            response.update(timestamp=event['ts'])
            
            # Create and send first emoji reaction
            response.update(name=emoji1)
            self.bot.sc.api_call('reactions.add', **response)
            
            # Create and send second emoji reaction
            response.update(name=emoji2)
            self.bot.sc.api_call('reactions.add', **response)
        else:
            raise PluginException('Invalid syntax! E.g. `!vote <emoji1> <emoji2> <question>`')
