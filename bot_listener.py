import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, SERVICES

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ""
    for name, svc in SERVICES.items():
        search = f"{svc['folder']}/{svc['script']}"
        result = subprocess.getoutput(f"pgrep -af '{search}'")
        running = "✅ RUNNING" if svc['script'] in result else "❌ STOPPED"
        msg += f"{name}: {running}\n" + result 
    await update.message.reply_text(msg)

# /logs command
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.args[0] if context.args else None
    if name and name in SERVICES:
        try:
            log = subprocess.getoutput(f"tail -n 20 {SERVICES[name]['log']}")
            await update.message.reply_text(f"{name} last logs:\n{log}")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
    else:
        await update.message.reply_text("Usage: /logs [ServiceName]\nExample: /logs Bollinger")

# Run the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("logs", logs))
    app.run_polling()
