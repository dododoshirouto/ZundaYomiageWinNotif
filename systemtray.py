import sys
import os
from PIL import Image

# システムトレイ
import pystray
from pystray import Menu, MenuItem



class TrayApp:
    def __init__(self):
        # PyInstallerでパスを解決するときの対応:
        if hasattr(sys, '_MEIPASS'):
            # PyInstallerで固めたexeから実行されている場合
            base_path = sys._MEIPASS
        else:
            # 普通にPythonで実行している場合
            base_path = os.path.dirname(__file__)
            
        off_icon_path = os.path.join(base_path, "icons", "off.png")
        on_icon_path  = os.path.join(base_path, "icons", "on.png")
        mosaic_icon_path = os.path.join(base_path, "icons", "mosaic.png")
        black_icon_path  = os.path.join(base_path, "icons", "black.png")

        self.icon_off = Image.open(off_icon_path)
        self.icon_on = Image.open(on_icon_path)
        self.icon_mosaic = Image.open(mosaic_icon_path)
        self.icon_black = Image.open(black_icon_path)

        # アイコンは初期オフ状態で
        self.icon = pystray.Icon(
            "Zunda Yomiage Win Notif",
            self.icon_off,
            menu=self.build_menu()
        )

    def build_menu(self):
        """現在のモードを見てメニューのラベルを動的に変える"""
        # ラベル生成用のヘルパ
        def mode_label(mode_value, text):
            return ("● " if self.streamer.mode == mode_value else "　") + text

        return Menu(
            MenuItem("配信開始", self.on_start),
            MenuItem("配信停止", self.on_stop),
            MenuItem("ストリームキー変更", self.on_change_key),
            MenuItem(
                "モード",
                Menu(
                    MenuItem(mode_label("normal", "普通"), self.on_mode_normal),
                    MenuItem(mode_label("mosaic", "モザイク"), self.on_mode_mosaic),
                    MenuItem(mode_label("black", "暗転"), self.on_mode_black),
                )
            ),
            MenuItem("終了", self.on_quit)
        )
    
    def set_icon(self):
        self.icon.icon = self.icon_off
        self.icon.update_menu()

    def run(self):
        self.icon.run()

    def on_start(self, _):
        self.streamer.start_stream()
        self.set_icon(stream=self.streamer.process is not None)

    def on_stop(self, _):
        self.streamer.stop_stream()
        self.set_icon(stream=self.streamer.process is not None)

    def on_quit(self, _):
        self.icon.stop()
        sys.exit(0)

    def _update_menu(self):
        """メニューを最新状態に更新する"""
        self.icon.menu = self.build_menu()
        self.icon.update_menu()