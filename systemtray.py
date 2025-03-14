import sys
import os
from PIL import Image, ImageWin

import time
import threading
import asyncio

from voicevox_yomiage import VV_Speaker as VV

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
icons_prefix = {
    VV.ずんだもん: "zundamon_",
    VV.四国めたん: "metan_",
    VV.春日部つむぎ: "tsumugi_",
    VV.雨晴はう: "hau_",
    VV.中国うさぎ: "usagi_",
    VV.九州そら: "sora_",
    VV.栗田まろん: "maron_",
    VV.WhiteCUL: "CUL_",
    VV.No_7: "no_7_",
}

class TrayApp:
    def __init__(self, active=True, loop=lambda: None, loop_async=False, speaker=VV.ずんだもん):
        self.active = active
        self.is_talking = False
        self.loop = loop
        self.loop_async = loop_async
        self.speaker = speaker

        self.icons_current_name = None
        self.icons_current = None


        # import json
        # print(json.dumps(icons_dict, indent=4, ensure_ascii=False))  # ensure_ascii=Falseで日本語をそのまま出力

        self.icon = pystray.Icon(
            "Zunda Yomiage Win Notif",
            menu=self.build_menu()
        )

        self.load_icons()
        # self.set_icon("standby")
        self.icon_anim_start()
        self.start()
    
    def load_icons(self, force=False):
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
                icon_path = os.path.join(base_path, "assets", f"{icons_prefix.get(self.speaker)}{value}.png")
                icon_size = self.get_tray_icon_size()
                self.icons[key].append(Image.open(icon_path).convert("RGBA").resize(icon_size, Image.NEAREST))
        
        self.set_icon(force=force)

    def build_menu(self):
        return Menu(
            MenuItem("ずんだ通知読み上げもん", lambda :None, enabled=False),
            MenuItem("無効にする", self.stop) if self.active else MenuItem("有効にする", self.start),
            MenuItem(
                self.speaker.name,
                Menu(*[
                    MenuItem(sp.name, lambda _, sp=sp: self.set_speaker(VV[sp.text]), checked=lambda _, sp=sp: self.speaker == sp)
                    for sp in VV
                ])
            ),
            MenuItem("終了", self.on_quit)
        )
    
    def set_icon(self, icon_name=None, force=False):
        if icon_name is None:
            if self.active:
                if self.is_talking:
                    icon_name = "talking"
                else:
                    icon_name = "standby"
            else:
                icon_name = "sleep"

        if self.icons_current_name == icon_name and not force:
            return

        self.icons_current_name = icon_name
        self.icons_current = self.icons.get(self.icons_current_name)
        self.icon.icon = self.icons_current[0]
    
    def set_speaker(self, speaker:VV):
        self.speaker = speaker
        self.load_icons(True)
        self._update_menu()
        return self

    def run(self):
        self.icon.run()
    
    def loop_call(self):
        while self.active:
            if self.loop_async:
                asyncio.run(self.loop())
            else:
                self.loop()
            time.sleep(0.1)

    def start(self):
        self.active = True
        self.is_talking = False
        self.thread = threading.Thread(target=self.loop_call, daemon=True)
        self.thread.start()
        self._update_menu()
    
    def stop(self):
        self.active = False
        self._update_menu()

    def on_quit(self, _):
        self.icon.stop()
        sys.exit(0)

    def _update_menu(self):
        """メニューを最新状態に更新する"""
        self.icon.menu = self.build_menu()
        self.icon.update_menu()
        self.set_icon()
    

    def icon_anim_loop(self):
        now_icon = 0
        # for img in itertools.cycle(self.icons_current):  # 無限ループで画像を切り替え
        while True:
            img = self.icons_current[now_icon % len(self.icons_current)]
            self.icon.icon = img  # アイコンを変更


            status = "sleep"
            if self.active:
                if self.is_talking:
                    status = "talking"
                else:
                    status = "standby"

            time.sleep(icons_interval.get(status, 0.2))
            now_icon = (now_icon + 1) % len(self.icons_current)
    
    def icon_anim_start(self):
        self.icon_anim_thread = threading.Thread(target=self.icon_anim_loop, daemon=True)
        self.icon_anim_thread.start()
    
    def get_tray_icon_size(self):
        # hdc = ImageWin.HDC(0)
        # dpi = hdc.GetDeviceCaps(88)  # LOGPIXELSX
        # if dpi >= 192:  # 200% スケール
        #     return 32, 32
        # elif dpi >= 144:  # 150% スケール
        #     return 24, 24
        # else:  # 標準 (100%)
        #     return 16, 16
        import ctypes
        size = ctypes.windll.user32.GetSystemMetrics(49)  # SM_CXSMICON
        return size, size




if __name__ == "__main__":
    tray = TrayApp()
    tray.set_speaker(VV.四国めたん)
    tray.run()

