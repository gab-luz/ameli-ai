import sys
sys.path.append('ext/')
from ext.console import intro_header
import time
from common import wish_me, notify_ameli


#assistant directly works without giving introduction or any other shit.
def start_from_hibernation():
    print(intro_header)
    from common import wish_me
    notify_ameli('Ameli-AI has just started...')
    wish_me()
    time.sleep(1)
    from app_finder import showmagic
    showmagic()

if __name__ == '__main__':
    start_from_hibernation()