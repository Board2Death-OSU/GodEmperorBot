import json
import sys
sys.path.append('lib/')

import bot_helper.bot.client as client
import bot_helper.resources.message_handler as message_handler
import bot_helper.resources.spreadsheet as spreadsheet


def sample_function(message):
    return 'Message from {0.author}: {0.content}'.format(message), message.channel


def processes_wrapper(message, handler):
    return handler.process_message(message.content), message.channel


# Get API Keys
secret_input = open('data/secret.json')
keys = json.load(secret_input)
secret_input.close()

# Get Responses
response_input = open('data/responses.json')
responses = json.load(response_input)
response_input.close()

# Create Message Handler
handler = message_handler.get_handler(responses)

# Create Bot
client = client.Client()

# Register Callback Functions
client.register_on_message_callback(sample_function, [])
client.register_on_message_callback(processes_wrapper, [handler])

# Make Spreadsheet
sheet = spreadsheet.Spreadsheet(keys['sheet_id'], 'data/token.json', 'data/credentials.json')

# Start Client
client.run(keys['discord_token'])
