import asyncio

from voicevox_yomiage import VoicevoxYomiage, VV_Speaker

vv = VoicevoxYomiage()

def main():
    print("Hello!")
    asyncio.run(vv("ハロー！"))


if __name__ == "__main__":
    main()