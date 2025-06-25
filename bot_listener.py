from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_TOKEN, SERVICES
import subprocess

def status(update, context):
    msg = ""
    for name, svc in SERVICES.items():
        search = f"{svc['folder']}/{svc['script']}"
        result = subprocess.getoutput(f"pgrep -af '{search}'")
        running = "✅ RUNNING" if svc['script'] in result else "❌ STOPPED"
        msg += f"{name}: {running}\n"
    update.message.reply_text(msg)

def logs(update, context):
    name = context.args[0] if context.args else None
    if name and name in SERVICES:
        try:
            log = subprocess.getoutput(f"tail -n 20 {SERVICES[name]['log']}")
            update.message.reply_text(f"{name} last logs:\n{log}")
        except Exception as e:
            update.message.reply_text(f"Error: {e}")
    else:
        update.message.reply_text(f"Usage: /logs Bollinger")

updater = Updater(TELEGRAM_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("status", status))
dp.add_handler(CommandHandler("logs", logs))

updater.start_polling()
updater.idle()