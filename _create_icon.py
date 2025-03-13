from PIL import Image

# 入力画像のパス
input_path = "icons/on.png"

# 出力アイコンのパス
output_path = "icon.ico"

# 作成するアイコンサイズのリスト
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256), (512, 512)]

# 画像を開く
img = Image.open(input_path)

# `.ico` ファイルを作成（バイリニア補間でリサイズ）
img.save(output_path, format="ICO", sizes=sizes, resample=Image.NEAREST)

print(f"アイコンを作成しました: {output_path}")