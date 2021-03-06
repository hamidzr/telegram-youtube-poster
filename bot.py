#! env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import configparser
import re
from modules.poster import *

config = configparser.ConfigParser()
config.read('config.ini')

TARGET_CHAT = config['DEFAULT']['TARGET_CHAT']
TARGET_CHANNEL = config['DEFAULT']['TARGET_CHANNEL']
BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
YOUTUBE_API = config['DEFAULT']['YOUTUBE_API']

posterBot = Poster(token=BOT_TOKEN, target_chat=TARGET_CHAT, target_channel=TARGET_CHANNEL)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    # if there is a youtubeid then dl
    msg = update.message.text
    ytUrl = hasYtUrl(msg)
    if (ytUrl):
        id = idFromYtUrl(ytUrl)
        update.message.reply_text(f'Request for youtube video: {id} received. Processing..')
        posterBot.sendYoutubeVideo(id)
        update.message.reply_text(f'Video posted to #{id} @freetube')
    else:
        update.message.reply_text(msg)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # TODO add a separate message handler for yt
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
