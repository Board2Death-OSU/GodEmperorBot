import json
import sys
sys.path.append('lib/')

import bot_helper.bot.client as client
import utl.power_table as power_table
import utl.powerkeeper as powerkeeper
import utl.marriage_handler as marriage_handler
import signal
import sys


def score_callback(msg, keeper):
    """
    The Callbaquck to handle message processing for the score keeping functionality.
    """

    # Gather information from the message object
    channel = msg.channel
    message = msg.content.upper()
    time = str(msg.created_at)

    author = str(msg.nick)
    if author is None:
        author = str(msg.author)
    response = ''

    # Check if this is a kill command
    if str(msg.channel) == 'logistics':
        response += keeper.check_player_deaths(message, author, time)
        # Don't add score based on the house of those that died.
        if response == '' and '!' not in message:
            response += keeper.process_score_message(
                message, author, time)

    # Check if a score table was requested.
    if '!SCORE' in message:
        response += keeper.display_scores()
    return response, channel


# Get API Keys
secret_input = open('data/secret.json')
keys = json.load(secret_input)
secret_input.close()

# Create Bot
client = client.Client()

# Make Spreadsheet
sheet = power_table.PowerTable(
    keys['sheet_id'], 'data/token.json', 'data/credentials.json')

# Create Score Keeper
keeper = powerkeeper.get_inst(sheet)

# Register Score Keeping Callback
client.register_on_message_callback(score_callback, [keeper])

# Create Marriage Handler
marriage_fun, marriage_args = marriage_handler.get_callback_function(
    keeper.houses, keeper.spreadsheet)
client.register_on_message_callback(marriage_fun, marriage_args)
keeper.register_marriage_handler(marriage_args[0])

# Start Client
client.run(keys['discord_token'])
