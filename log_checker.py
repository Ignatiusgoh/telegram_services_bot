import re
from config import SERVICES
from telegram_alert import send_alert

THRESHOLD = 10  # Customize

for name, service in SERVICES.items():
    log_path = service["log"]
    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()[-1000:]  # Check recent logs only
            criticals = [line for line in lines if re.search(r'\b(CRITICAL|ERROR|Traceback)\b', line)]
            if len(criticals) > THRESHOLD:
                send_alert(f"⚠️ {name} has {len(criticals)} critical logs in last 1000 lines!")
    except Exception as e:
        send_alert(f"❌ Could not read log for {name}: {e}")