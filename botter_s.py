import json
import logging
import json
import requests
from telegram import Update,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters,MessageHandler,ApplicationBuilder, ContextTypes, CommandHandler,InlineQueryHandler

from news import get_news_from_keyword

with open('auth.txt') as f:
    tok = f.readline()
    
base_url='https://api.telegram.org/' + str(tok)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    print(update.message.text)

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args)
    ret = get_news_from_keyword(text_caps)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ret[0])
    
    

async def inline_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    ret = get_news_from_keyword(query)
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='News',
            input_message_content=InputTextMessageContent(ret[0])
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)
    print(ret[0])

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(tok).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('news', news)
    inline_caps_handler = InlineQueryHandler(inline_news)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)

    #Last things to run(to handle mistakes at last)
    application.add_handler(unknown_handler)
    application.run_polling()