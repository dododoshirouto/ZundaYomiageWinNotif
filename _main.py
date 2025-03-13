from pywinauto import Desktop


from systemtray import TrayApp
from voicevox_yomiage import VoicevoxYomiage, VV_Speaker


vv = VoicevoxYomiage()
tray = None

def init():
    global tray
    tray = TrayApp(loop=loop, loop_async=True)
    tray.run()



async def loop():
    print("loop")
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
        notifications = [win for win in desktop.windows() if "新しい通知" in win.window_text()]

        for notification in notifications:
            notif_texts = []
            # 通知ウィンドウの全テキストを取得
            for child in notification.descendants():  # すべての子要素をチェック
                text = child.window_text().strip()
                if text:
                    # print(f"🔹 {text}")  # 通知の内容を出力
                    notif_texts.append(text)
            
            notif_text = ", ".join(notif_texts)

            if notif_text not in readed_notifications:
                readed_notifications.append(notif_text)
                new_notifs.append(notif_text)
                print(notif_text)

    except Exception as e:
        print(f"通知取得エラー: {e}")
    
    return new_notifs


if __name__ == "__main__":
    init()