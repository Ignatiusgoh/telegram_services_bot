SERVICES = {
    "trade_execution": {
        "script": "main.py",
        "folder": "/root/rv_trailing_stop_entry",
        "log": "/root/rv_trailing_stop_entry/execution.log"
    },
    "event_listener": {
        "script": "main.py",
        "folder": "/root/binance-event-listener/src",
        "log": "/root/binance-event-listener/src/binance_event_listener.log"
    },
    "adjuster": {
        "script": "main.py",
        "folder": " /root/adjuster/src",
        "log": "/root/adjuster/src/breakeven_adjuster.log"
    }
}

TELEGRAM_TOKEN = "7518373336:AAGIfxUfLQJ40t5rsfEVSbkMqjvgFxpz5tc"
CHAT_ID = "205666825"
