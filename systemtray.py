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
    def __init__(self, active=True, loop=lambda: None):
        self.active = active
        self.is_talking = False
        self.loop = loop

        self.icons_current_name = None
        self.icons_current = None

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

        self.icon = pystray.Icon(
            "Zunda Yomiage Win Notif",
            self.icons.get("standby")[0],
            menu=self.build_menu()
        )

        self.icon_anim_start()
        self.set_icon("standby")
        self.start()

    def build_menu(self):
        return Menu(
            MenuItem("standby", lambda: self.set_icon("standby")),
            MenuItem("talking", lambda: self.set_icon("talking")),
            MenuItem("sleep", lambda: self.set_icon("sleep")),
            MenuItem("終了", self.on_quit)
        )
    
    def set_icon(self, icon_name=None):
        if icon_name is None:
            if self.active:
                if self.is_talking:
                    icon_name = "talking"
                else:
                    icon_name = "standby"
            else:
                icon_name = "sleep"

        if self.icons_current_name == icon_name:
            return

        self.icons_current_name = icon_name
        self.icons_current = self.icons.get(self.icons_current_name)
        self.icon.icon = self.icons_current[0]
        self._update_menu()

    def run(self):
        self.icon.run()
    
    def loop_call(self):
        while self.active:
            self.loop()
            time.sleep(0.2)

    def start(self):
        self.active = True
        self.thread = threading.Thread(target=self.loop_call, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.active = False

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
    tray.run()

