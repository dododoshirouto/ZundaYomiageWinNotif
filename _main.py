import asyncio

from systemtray import TrayApp
from voicevox_yomiage import VoicevoxYomiage, VV_Speaker


vv = VoicevoxYomiage()

def main():
    TrayApp().run()


if __name__ == "__main__":
    main()