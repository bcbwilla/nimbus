from plugin import Plugin
import re


class React(Plugin):
    """
    Adds Slack emoji reactions to messages based on certain keywords
    """

    def on_event(self, event, response):
        text = event['text']
        response.update(timestamp=event['ts'])
        morethanonereaction = false

        # Add a cloud emoji if anyone mentions Overcast Network
        if re.search(r'(overcast|ocn)', text, re.IGNORECASE):
            response.update(name='cloud')
        
        # Add hammer and ok emoticon reaction if someone says "appropriate?" (for staff voting)
        
        if re.search(r'(appropriate?)', text, re.IGNORECASE):
            # So that :ok: doesn't get run twice, as we'll call the api on each emoji.
            morethanonereaction = true
            # Emoji #1
            response.update(name='hammer')
            self.bot.sc.api_call('reactions.add', **response)
            # Emoji #2
            response.update(name='ok')
            self.bot.sc.api_call('reactions.add', **response)
            
        # Add more reactions here!
        

        # Post reaction if we have an emoji set
        if response.get('name') and not morethanonereaction:
            self.bot.sc.api_call('reactions.add', **response)
