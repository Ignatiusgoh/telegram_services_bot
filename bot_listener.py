import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, SERVICES

# /status command
# async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     msg = ""
#     for name, svc in SERVICES.items():
#         search = f"{svc['folder']}/{svc['script']}"
#         result = subprocess.getoutput(f"pgrep -af '{search}'")
#         running = "✅ RUNNING" if svc['script'] in result else "❌ STOPPED"
#         msg += f"{name}: {running}\n" + result 
#     await update.message.reply_text(msg)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    msg = ""
    try:
        # Get all tmux windows
        windows = subprocess.getoutput("tmux list-windows -a").splitlines()
        for win in windows:
            
            session_win = win.split(":")[0] + ":" + win.split(":")[1].split()[0]
            name_split = win.split(":")[2]
            name = name_split.strip().split()[0]

            # Get the PID of the pane (the bash shell)
            pane_pid = subprocess.getoutput(f"tmux list-panes -t {session_win} -F '#{{pane_pid}}'").strip()

            # Find child processes of the pane (bash), if any
            children = subprocess.getoutput(f"pgrep -P {pane_pid}").splitlines()

            for child_pid in children:
                cmd = subprocess.getoutput(f"ps -p {child_pid} -o cmd=").strip()
                if "python" in cmd:
                    msg += f"{name}: ✅ RUNNING\n" # Python script is running inside tmux window
                else:
                    msg += f"{name}: ❌ STOPPED\n" # No Python process under that pane

    except Exception as e:
        await update.message.reply_text(f"Error checking window: {e}")
        
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
