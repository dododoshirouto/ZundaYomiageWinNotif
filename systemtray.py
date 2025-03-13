import sys
import os
from PIL import Image

import time
import threading
import itertools

# システムトレイ
import pystray
from pystray import Menu, MenuItem



icons_dict = {
    "standby": ["standby"],
    "talking": ["talking", "talking_2", "talking_3"],
    "sleep": ["sleep", "sleep_2"],
}
icons_interval = {
    "standby": 0.2,
    "talking": 0.2,
    "sleep": 0.6,
}

class TrayApp:
    def __init__(self):
        # PyInstallerでパスを解決するときの対応:
        if hasattr(sys, '_MEIPASS'):
            # PyInstallerで固めたexeから実行されている場合
            base_path = sys._MEIPASS
        else:
            # 普通にPythonで実行している場合
            base_path = os.path.dirname(__file__)

        self.icons = {}
        for key, values in icons_dict.items():
            self.icons[key] = []
            for value in values:
                icon_path = os.path.join(base_path, "assets", f"{value}.png")
                self.icons[key].append(Image.open(icon_path))

        # import json
        # print(json.dumps(icons_dict, indent=4, ensure_ascii=False))  # ensure_ascii=Falseで日本語をそのまま出力

        # アイコンは初期オフ状態で
        self.icons_current = self.icons.get("standby")

        self.icon = pystray.Icon(
            "Zunda Yomiage Win Notif",
            self.icons_current[0],
            menu=self.build_menu()
        )

        self.icon_anim_thread = None
        self.icon_anim_stop_event = threading.Event()
        self.icon_anim_start()

    def build_menu(self):
        return Menu(
            MenuItem("standby", lambda: self.set_icon("standby")),
            MenuItem("talking", lambda: self.set_icon("talking")),
            MenuItem("sleep", lambda: self.set_icon("sleep")),
            MenuItem("終了", self.on_quit)
        )
    
    def set_icon(self, icon_name="standby"):
        self.icons_current = self.icons.get(icon_name)
        self.icon.icon = self.icons_current[0]
        # self.icon_anim_start()
        self._update_menu()

    def run(self):
        self.icon.run()

    def on_quit(self, _):
        self.icon.stop()
        sys.exit(0)

    def _update_menu(self):
        """メニューを最新状態に更新する"""
        self.icon.menu = self.build_menu()
        self.icon.update_menu()
    

    def icon_anim_loop(self):
        now_icon = 0
        # for img in itertools.cycle(self.icons_current):  # 無限ループで画像を切り替え
        while True:
            img = self.icons_current[now_icon % len(self.icons_current)]
            self.icon.icon = img  # アイコンを変更
            time.sleep(icons_interval.get(list(self.icons.keys())[list(self.icons.values()).index(self.icons_current)], 0.2))  # 0.5秒ごとに切り替え
            now_icon = (now_icon + 1) % len(self.icons_current)
    
    def icon_anim_start(self):
        self.icon_anim_thread = threading.Thread(target=self.icon_anim_loop, daemon=True)
        self.icon_anim_thread.start()



if __name__ == "__main__":
    tray = TrayApp()
    tray.set_icon("talking")
    tray.run()

