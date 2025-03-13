import asyncio

from systemtray import TrayApp
from voicevox_yomiage import VoicevoxYomiage, VV_Speaker


vv = VoicevoxYomiage()

def init():
    TrayApp(loop=loop).run()



def loop():
    print("loop")
    pass


if __name__ == "__main__":
    init()