from telegram.constants import PARSEMODE_MARKDOWN
from telegram.ext import Updater, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from urllib.parse import quote
import os
import logging

from telegram.ext.filters import Filters

base_url = 'https://twitter.com/intent/tweet?text='

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def generate_button(text: str) -> InlineKeyboardMarkup:
    encoded_text = quote(text, safe='', encoding='utf-8')
    keyboard = [[
        InlineKeyboardButton('Click Me to Tweet this!',
                             url=f'{base_url}{encoded_text}')
    ]]
    markup = InlineKeyboardMarkup(keyboard)
    return markup


def click2tweet(update, context):
    text = update.effective_message.text
    reply_markup = generate_button(text)
    message = '*Tweet*:\n' + text
    update.effective_message.reply_text(message,
                                        parse_mode=PARSEMODE_MARKDOWN,
                                        reply_markup=reply_markup)


if __name__ == '__main__':
    bot_api: str = os.environ.get('BOT_API', "")
    PORT: int = int(os.environ.get('PORT', 5000))
    heroku: str = os.environ.get("heroku", "None")

    updater = Updater(token=bot_api)
    dispatcher = updater.dispatcher
    click2tweet_handler = MessageHandler(filters=Filters.text
                                         & ~Filters.command,
                                         callback=click2tweet)
    dispatcher.add_handler(click2tweet_handler)
    dispatcher.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=bot_api)
    updater.bot.setWebhook(heroku + bot_api)
