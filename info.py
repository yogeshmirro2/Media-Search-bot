# import re
# from os import environ

id_pattern = re.compile(r'^.\d+$')

# # Bot information
# SESSION = environ.get('SESSION', 'Media_search')
# USER_SESSION = environ.get('USER_SESSION', 'User_Bot')
# API_ID = int(environ['API_ID'])
# API_HASH = environ['API_HASH']
# BOT_TOKEN = environ['BOT_TOKEN']
# USERBOT_STRING_SESSION = environ.get('USERBOT_STRING_SESSION')

# # Bot settings
# CACHE_TIME = int(environ.get('CACHE_TIME', 300))
# USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))

# # Admins, Channels & Users
# ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]
# CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]
# auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
# AUTH_USERS = (auth_users + ADMINS) if auth_users else []
# auth_channel = environ.get('AUTH_CHANNEL')
# AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel

# # MongoDB information
# DATABASE_URI = environ['DATABASE_URI']
# DATABASE_NAME = environ['DATABASE_NAME']
# COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# # Messages
# default_start_msg = """
# **Hi, I'm Media Search bot**

# Here you can search files in inline mode. Just press following buttons and start searching.
# """

# START_MSG = environ.get('START_MSG', default_start_msg)
# SHARE_BUTTON_TEXT = 'Checkout {username} for searching files'
# INVITE_MSG = environ.get('INVITE_MSG', 'Please join @.... to use this bot')
# Bot information
SESSION = 'Media_search'
USER_SESSION = 'User_Bot'
API_ID = 18860540
API_HASH = '22dd2ad1706199438ab3474e85c9afab'
BOT_TOKEN = '6167341719:AAEiVk9LhPCb38AT6jVkzdDhy_3kk_vEcbI'
USERBOT_STRING_SESSION = 'AQBiMZkAIrYCK0bqxkWlvPkE8RdSTe_zgZap6TqAMUaxvKfJYds63KRABTZoHGQzay9jEsmg3ecFied8JRKexiUcMnrGw5w1XwPd8-Pqpe8nrWJAUY0jHxSVzQ1hM-kDky6Ze0nDykRFH1RaKX3tCuNO94mp75dNfcC6uL6iJXZgPsHTEiX5I_t38DECfzNwquPgv5WJsG1Y1-EvBLCS7ilC2Wc7sUgTBRrFJ4ZnZVolJD4-ot_rTMEG7Sq2sjg8RZFzohIMNMngd-nxz672oR-dfaZAps8LNa3eAghulbJG7tNsv6QhdRYDRUZfC1Am6qVD_8VkgsXk0L9ZmKO-GCWaLrqj8QAAAAE5Jv7jAA'

# Bot settings
CACHE_TIME = 300
USE_CAPTION_FILTER = True

# Admins, Channels & Users
ADMINS = [5123176772]
CHANNELS = [-1001975184173]
AUTH_USERS = []
AUTH_CHANNEL = None

# MongoDB information
DATABASE_URI = "mongodb+srv://ankur560s:ankur560@cluster00.nlwm8ya.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = 'Telegram'
COLLECTION_NAME = 'channel_files'  # If you are using the same database, then use different collection name for each bot

# Messages
START_MSG = """
**Hi, I'm Media Search bot**

Here you can search files in inline mode. Just press follwing buttons and start searching.
"""

SHARE_BUTTON_TEXT = 'Checkout {username} for searching files'
INVITE_MSG = 'Please join @.... to use this bot'
