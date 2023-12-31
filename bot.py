from telegram import Bot,Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,Updater
from pak_matches import main
from ip import get_public_ip
from weather import getWeather
from rp_temp import getTemp
from prayerapi import get_prayers_time_list
import asyncio
import aiohttp


###########################################################################################################
#Telegram bot processing starts
###########################################################################################################
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

TOKEN = '6539729053:AAESRPhDqn3yiqSz_pBYfgNTkjnehFSQvBA'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me!')

async def pak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = await main()
    await update.message.reply_text(reply)

async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply =  get_public_ip()
    await update.message.reply_text(reply)

async def temp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply =  getTemp()
    await update.message.reply_text(reply)

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply =  getWeather()
    await update.message.reply_text(reply)

async def prayer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply =  get_prayers_time_list()

    await update.message.reply_text(reply)


# Example usage
# output = await create_output_string()
# print(output)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = handle_response(text)
    print(response)
    if response:
        await update.message.reply_text(response)


def handle_response(text: str):
    processed = text.lower()
    print(processed)
    if 'hello' in processed:
        return "Hey there"
    return ''


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
#    app.add_handler(MessageHandler(filters.Text & ~filters.command, handle_message))
 #   app.add_handler(MessageHandler(filters.Text, handle_message))
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('pakgames', pak_command))
    app.add_handler(CommandHandler('ip', ip_command))
    app.add_handler(CommandHandler('weather', weather_command))
    app.add_handler(CommandHandler('prayer', prayer_command))
    app.add_handler(CommandHandler('temp', temp_command))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.run_polling()

