import subprocess
from config import SERVICES
from telegram_alert import send_alert

# Checks whether services are running 

# for name, service in SERVICES.items():
#     script = service["script"]
#     folder = service["folder"]
#     search_term = f"{folder}/{script}"
#     result = subprocess.getoutput(f"pgrep -af '{search_term}'")

#     if script not in result:
#         send_alert(f"🚨 {name} service is NOT running!\nMissing: {script}")

windows = subprocess.getoutput("tmux list-windows -a").splitlines()

for win in windows:
            
    session_win = win.split(":")[0] + ":" + win.split(":")[1].split()[0]
    name_split = win.split(":")[2]
    name = name_split.strip().split()[0]

    # Get the PID of the pane (the bash shell)
    pane_pid = subprocess.getoutput(f"tmux list-panes -t {session_win} -F '#{{pane_pid}}'").strip()

    # Find child processes of the pane (bash), if any
    children = subprocess.getoutput(f"pgrep -P {pane_pid}").splitlines()
    
    if children:
        # for child_pid in children:
        cmd = subprocess.getoutput(f"ps -p {children[0]} -o cmd=").strip()
        if "python" in cmd:
            continue 
    else:
        send_alert(f"❌ {name} script STOPPED")