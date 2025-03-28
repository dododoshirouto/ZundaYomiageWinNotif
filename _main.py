import re
import sys
import os

from pywinauto import Desktop

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from systemtray import TrayApp
from voicevox_yomiage import VoicevoxYomiage, VV_Speaker
from eng_to_kana import EnglishToKana




vv = VoicevoxYomiage(speaker_id=VV_Speaker.ずんだもん.value)
e2k = EnglishToKana()
tray = None

def init():
    global tray
    tray = TrayApp(loop=loop, loop_async=True)
    tray.run()



async def loop():
    global tray
    if tray is None or tray.speaker is None:
        return
    
    # print("loop")
    if vv.speaker_id != tray.speaker.value:
        print("speaker change to: " + str(tray.speaker.name))
        vv.set_speaker(tray.speaker.value)

    texts = get_notifications()
    for text in texts:
        tray.is_talking = True
        tray.set_icon()
        await vv(text)
        tray.is_talking = False
        tray.set_icon()
    pass



readed_notifications = []

def get_notifications()->list[str]:
    global readed_notifications

    new_notifs = []

    try:
        # デスクトップのウィンドウ一覧を取得
        desktop = Desktop(backend="uia")

        # 通知のウィンドウを探す (アプリ名が "通知" のものを探す)
        notifications = [win for win in desktop.windows(title_re="新しい通知.*") if "新しい通知" in win.window_text()]

        for notification in notifications:
            notif_texts = []
            # 通知ウィンドウの全テキストを取得
            for child in notification.descendants():  # すべての子要素をチェック
                if not child.is_visible():
                    continue
                text = child.window_text().strip()
                if text:
                    # print(f"🔹 {text}")  # 通知の内容を出力
                    notif_texts.append(text)
            
            notif_text = "。\n".join(notif_texts[4:6])

            notif_text = text_processing(notif_text)

            if notif_text not in readed_notifications:
                readed_notifications.append(notif_text)
                new_notifs.append(notif_text)
                print(notif_text)
                print("\n")

    except Exception as e:
        print(f"通知取得エラー: {e}")
    
    return new_notifs

def text_processing(text:str):
    text = re.sub(r"\b[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9._%+-/…]*)?\b", " ", text) # URL
    text = re.sub(r"。{2,}", "。", text)
    text = re.sub(r"[\n\s。]{2,}", " ", text)
    text = vv.eng_to_kana(text)
    text = e2k.convertsZakkuri(text)
    # text = re.sub(r"[「」『』（）【】\(\)\[\]\{\}]+", "", text)
    return text


if __name__ == "__main__":
    init()