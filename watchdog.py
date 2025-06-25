import subprocess
from config import SERVICES
from telegram_alert import send_alert

# Checks whether services are running 

for name, service in SERVICES.items():
    script = service["script"]
    folder = service["folder"]
    search_term = f"{folder}/{script}"
    result = subprocess.getoutput(f"pgrep -af '{search_term}'")

    if script not in result:
        send_alert(f"🚨 {name} service is NOT running!\nMissing: {script}")