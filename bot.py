from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,CallbackContext
from pak_matches import main
from ip import get_public_ip
from weather import getWeather
from rp_temp import getTemp
from prayerapi import get_prayers_time_list
from subscribe import get_subscribe
from unsubscribe import get_unsubscribe
from chatid import get_all_chat_ids
from reminder import get_reminders

from result_bot import get_result_image, cleanup_file

import asyncio
import requests
import datetime 
import urllib.parse
import re
import os
import platform
import shutil

IP_CHECK_INTERVAL_SECONDS = 5 * 60
BOT_STARTED_AT = datetime.datetime.now()

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

async def subs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.full_name
    chat_id = update.message.chat_id
    reply =  get_subscribe(chat_id,name)
    await update.message.reply_text(reply)

async def unsubs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.full_name
    chat_id = update.message.chat_id
    reply =  get_unsubscribe(chat_id,name)
    await update.message.reply_text(reply)

async def chat_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(chat_id)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_status_message())
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    response = handle_response(text)
    if response:
        await update.message.reply_text(response)

async def ask_command(update: Update, context: CallbackContext):
    # Extract the question from the command
    question = ' '.join(context.args)
    
    # Make a request to the content generation endpoint
    try:
        response = requests.get(f"http://0.0.0.0:5000/generate_content/{update.message.text[5:].strip()}").text
        response = response[1:-2] 
    
        cleaned_output = clean_newlines(response)
        print(cleaned_output)
        await update.message.reply_text(cleaned_output)
    except requests.RequestException as e:
        print("Error fetching response:", e)
        await update.message.reply_text("Failed to fetch response.")

def handle_response(text: str):
    processed = text.lower()
    if 'hello' in processed:
        return "Hey there"
    return ''

async def send_push_message(message,chat_id):
    # Get the stored chat ID

    if chat_id:
        # Initialize the Telegram bot with your bot's token
        bot = Bot(token=TOKEN)
        # Send the message to the stored chat ID
        await bot.send_message(chat_id=chat_id, text=message)
        print("Push message sent successfully!")
    else:
        print("Chat ID not found!")

def tConvert(time):
    time = str(time)
    time_components = time.split(':')
    
    if len(time_components) > 1:  
        hours = int(time_components[0])
        minutes = int(time_components[1])
        hours = hours % 12 or 12  # Adjust hours
        return f"{hours}:{minutes:02d}"
    return time
def parse_datetime(datetime_str):
    # Assuming the datetime format in the string is "day-month-year hours:minutes"
    return datetime.datetime.strptime(datetime_str.strip(), '%d-%m-%Y %H:%M')

def clean_newlines(text):
    # Use regex to replace two or more newlines with a single newline
    return text.replace('\\n\\n', '\n')

def format_duration(total_seconds):
    total_seconds = int(total_seconds)
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)

def get_system_uptime():
    try:
        with open('/proc/uptime', 'r') as uptime_file:
            uptime_seconds = float(uptime_file.readline().split()[0])
        return format_duration(uptime_seconds)
    except Exception as e:
        print("Uptime error:", e)
        return "Unavailable"

def get_memory_usage():
    try:
        memory = {}
        with open('/proc/meminfo', 'r') as meminfo:
            for line in meminfo:
                key, value = line.split(':', 1)
                memory[key] = int(value.strip().split()[0])

        total_mb = memory['MemTotal'] / 1024
        available_mb = memory['MemAvailable'] / 1024
        used_mb = total_mb - available_mb
        used_percent = (used_mb / total_mb) * 100

        return f"{used_mb:.0f}/{total_mb:.0f} MB ({used_percent:.0f}%)"
    except Exception as e:
        print("Memory error:", e)
        return "Unavailable"

def get_cpu_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
            temp_c = int(temp_file.read().strip()) / 1000
        return f"{temp_c:.1f} C"
    except Exception as e:
        print("CPU temperature error:", e)
        return "Unavailable"

def get_status_message():
    now = datetime.datetime.now()
    bot_uptime = format_duration((now - BOT_STARTED_AT).total_seconds())
    disk = shutil.disk_usage('/')
    disk_used_percent = (disk.used / disk.total) * 100
    public_ip, local_ip = get_public_ip()

    try:
        load_average = ", ".join(f"{load:.2f}" for load in os.getloadavg())
    except Exception:
        load_average = "Unavailable"

    return (
        "Server Status\n"
        f"Host: {platform.node() or 'Unknown'}\n"
        f"Bot uptime: {bot_uptime}\n"
        f"System uptime: {get_system_uptime()}\n"
        f"CPU temp: {get_cpu_temperature()}\n"
        f"Load avg: {load_average}\n"
        f"RAM: {get_memory_usage()}\n"
        f"Disk: {disk.used / (1024 ** 3):.1f}/{disk.total / (1024 ** 3):.1f} GB ({disk_used_percent:.0f}%)\n"
        f"Public IP: {public_ip or 'Unavailable'}\n"
        f"Local IP: {local_ip or 'Unavailable'}\n"
        f"Time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    )

async def check_public_ip_change(last_public_ip):
    public_ip, local_ip = get_public_ip()

    if not public_ip:
        print("Public IP check skipped: could not get current IP.")
        return last_public_ip

    if last_public_ip is None:
        print("Initial public IP:", public_ip)
        return public_ip

    if public_ip != last_public_ip:
        message = (
            "Public IP changed!\n"
            f"Old: {last_public_ip}\n"
            f"New: {public_ip}"
        )

        if local_ip:
            message += f"\nLocal: {local_ip}"

        for chat_id in get_all_chat_ids():
            await send_push_message(message, chat_id)

    return public_ip

async def main():

    print('In Main')
    last_public_ip = None
    next_ip_check = datetime.datetime.now()

    while True:
        if datetime.datetime.now() >= next_ip_check:
            last_public_ip = await check_public_ip_change(last_public_ip)
            next_ip_check = datetime.datetime.now() + datetime.timedelta(seconds=IP_CHECK_INTERVAL_SECONDS)

        chat_ids =  get_all_chat_ids()
        reminders = get_reminders()
        list = ['Fajr', 'Sunrise','Dhuhr', 'Asr', 'Maghrib', 'Isha']
        current_time = datetime.datetime.now().strftime('%H:%M')
        for prayer in list:
            response = requests.get('http://0.0.0.0:8080/db.json')
            data = response.json()
            print(' Current time: ', current_time,' Prayer: ',prayer,' prayer time',data[prayer]['time'])

            if data[prayer]['time'] == current_time:
                # Perform further actions if the current time matches
                print("Current time matches!!!! ",' Current time: ', current_time,' Prayer: ',prayer,' prayer time',data[prayer]['time'])
                if prayer == 'Sunrise':
                    for chat in chat_ids:
                        await send_push_message('☀️ Sunrise ☀️',chat)
                else:
                    for chat in chat_ids:
                        x = '🔔 '+prayer + ' Time 🔔'
                        await send_push_message(x, chat)
                        y = '🤲 *Dua after completion of Athan* \nاَللّٰهُمَّ رَبَّ هٰذِهِ الدَّعْوَةِ التَّامَّةِ وَالصَّلَاةِ الْقَائِمَةِ ، آتِ مُحَمَّدًا الْوَسِيْلَةَ  وَالْفَضِيْلَةَ ، وَابْعَثْهُ مَقَامًا مَّحْمُوْدًا الَّذِيْ وَعَدْتَّهُ\n🤲 *Dua between Adhan and Iqamah, x3*\nاللهم إني أسألك العفو والعافية في الدنيا والآخرة'
                        await send_push_message(y,chat)
        current_datetime = datetime.datetime.now()

        for reminder in reminders:
            reminder_datetime = parse_datetime(reminder['datetime'])
            if reminder_datetime.date() == current_datetime.date() and reminder_datetime.time().replace(second=0, microsecond=0) == current_datetime.time().replace(second=0, microsecond=0):
                x = '🚨 Reminder 🚨\n' + reminder['description']
                await send_push_message(x,reminder['phoneno'])
                print('Reminder sent to: ',reminder['phoneno'])
        # Sleep for 30 seconds
        await asyncio.sleep(60)

import subprocess
import os

from result_bot import get_result_image, cleanup_file

async def weight_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # Get name after command
    if context.args:
        name = ' '.join(context.args)
    else:
        await update.message.reply_text("Usage: /weight Osama")
        return

    await update.message.reply_text(f"Processing {name}...")

    try:
        image_path = get_result_image(name)

        await update.message.reply_photo(photo=open(image_path, 'rb'))

        cleanup_file(image_path)

    except Exception as e:
        print(e)
        await update.message.reply_text("Error processing request.")

from screenshot_bot import take_screenshot, cleanup_file

async def screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /screenshot google.com")
        return

    url = context.args[0]

    await update.message.reply_text(f"Capturing {url}... 📸")

    try:
        image_path = take_screenshot(url)

        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo)

        cleanup_file(image_path)

    except Exception as e:
        print(e)
        await update.message.reply_text("Failed to capture screenshot.")

# Add this with your other command handlers
async def reboot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('In Reboot')
    allowed_users = ['6348023188','5849884611']  # Replace with actual user ID(s)
    user_id = str(update.effective_user.id)
    
    if user_id not in allowed_users:
        await update.message.reply_text("You are not authorized to perform this action.")
        return

    try:
        # Send confirmation message
        await update.message.reply_text("Server reboot initiated. The bot will be offline temporarily.")
        
        # Using sudo reboot (similar to your rp_temp.py approach)
        sudo_password = 'O$ama@3099'  # Consider securing this better
        command = 'sudo -S reboot'
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=sudo_password + '\n')
        
        if process.returncode == 0:
            await update.message.reply_text("Reboot command executed successfully.")
        else:
            await update.message.reply_text(f"Error during reboot: {stderr.strip()}")
            
    except Exception as e:
        await update.message.reply_text(f"Failed to reboot: {str(e)}")


def run_bot():
    # Initialize the Application
    print('IN BOT')
    app = Application.builder().token(TOKEN).build()

    # Define command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('pakgames', pak_command))
    app.add_handler(CommandHandler('ip', ip_command))
    app.add_handler(CommandHandler('weather', weather_command))
    app.add_handler(CommandHandler('prayer', prayer_command))
    app.add_handler(CommandHandler('temp', temp_command))
    app.add_handler(CommandHandler('prayerSubscribe', subs_command))
    app.add_handler(CommandHandler('prayerUnsubscribe', unsubs_command))
    app.add_handler(CommandHandler('getchatid', chat_id_command))
    app.add_handler(CommandHandler('status', status_command))
    app.add_handler(CommandHandler('ask', ask_command))
    app.add_handler(CommandHandler('reboot', reboot_command))
    app.add_handler(CommandHandler('weight', weight_command))
    app.add_handler(CommandHandler('screenshot', screenshot_command))

    # Define message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Start the bot polling
    app.run_polling()



# The rest of the code remains unchanged
if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # Run the asynchronous main function concurrently
    loop.create_task(main())

    # Start the bot in the main thread
    run_bot()

    # Run the event loop indefinitely
    loop.run_forever()
