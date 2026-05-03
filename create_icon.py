from PIL import Image
import os

# 选择一个二维码图片作为源文件
source_image = "icon_path/sw-icon.png"
target_icon = "icon_path/sw-icon.ico"

# 打开图片
img = Image.open(source_image)

# 调整大小为 256x256
img = img.resize((256, 256), Image.Resampling.LANCZOS)

# 保存为 ICO 格式
img.save(target_icon, format='ICO')

print(f"图标已创建: {target_icon}")
