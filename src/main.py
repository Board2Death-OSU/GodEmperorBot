import json
import sys
sys.path.append('lib/')

import bot_helper.bot.client as client
import power_table
import powerkeeper


def score_callback(msg, keeper):
    """
    The Callback to handle message processing for the score keeping functionality.
    """

    # Gather information from the message object
    channel = msg.channel
    message = msg.content.upper()
    time = str(msg.created_at)
    author = str(msg.author)
    response = ''

    # Check if this is a kill command
    response += keeper.check_player_deaths(message, author, time)

    # Don't add score based on the house of those that died.
    if response == '':
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

# Start Client
client.run(keys['discord_token'])
