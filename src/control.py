import threading

# -------------------------
# GLOBAL STATE
# -------------------------
_stop_flag = False
_lock = threading.Lock()


# -------------------------
# REQUEST STOP
# -------------------------
def request_stop():
    global _stop_flag
    with _lock:
        _stop_flag = True


# -------------------------
# RESET STOP (new session)
# -------------------------
def reset_stop():
    global _stop_flag
    with _lock:
        _stop_flag = False


# -------------------------
# CHECK STOP
# -------------------------
def should_stop():
    with _lock:
        return _stop_flag


# -------------------------
# KEYBOARD LISTENER (TERMUX SAFE)
# -------------------------
def start_keyboard_listener(trigger_key="q"):
    def _listener():
        while True:
            try:
                key = input().strip().lower()
                if key == trigger_key:
                    request_stop()
                    print("\n[CONTROL] Stop requested")
                    break
            except:
                break

    t = threading.Thread(target=_listener, daemon=True)
    t.start()
    return t
