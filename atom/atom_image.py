"""
L4 原子层 - 图像操作
功能：提供图像相关的纯函数原子操作
文件：atom/atom_image.py
"""

from PIL import Image, ImageDraw
import os
from typing import Optional, Dict, Any


def atom_image_create_label(
    width: float,
    height: float,
    corner_radius: float,
    dpi: int = 300
) -> Image.Image:
    """创建标签图像

    Args:
        width: 标签宽度（mm）
        height: 标签高度（mm）
        corner_radius: 圆角半径（mm）
        dpi: 分辨率

    Returns:
        标签图像
    """
    width_px = int(width * dpi / 25.4)
    height_px = int(height * dpi / 25.4)
    img = Image.new('RGB', (width_px, height_px), color='white')
    return img


def atom_image_add_qr(
    label_img: Image.Image,
    qr_img: Image.Image,
    x: float,
    y: float,
    width: float,
    height: float,
    dpi: int = 300
) -> Image.Image:
    """将二维码添加到标签

    Args:
        label_img: 标签图像
        qr_img: 二维码图像
        x: X坐标（mm）
        y: Y坐标（mm）
        width: 宽度（mm）
        height: 高度（mm）
        dpi: 分辨率

    Returns:
        更新后的标签图像
    """
    x_px = int(x * dpi / 25.4)
    y_px = int(y * dpi / 25.4)
    width_px = int(width * dpi / 25.4)
    height_px = int(height * dpi / 25.4)

    qr_resized = qr_img.resize((width_px, height_px))
    
    if qr_resized.mode != label_img.mode:
        qr_resized = qr_resized.convert(label_img.mode)
    
    label_img.paste(qr_resized, (x_px, y_px))
    return label_img


def atom_image_add_text(
    label_img: Image.Image,
    text: str,
    x: float,
    y: float,
    width: float,
    height: float,
    font_name: str,
    font_size: float,
    font_style: list,
    color: str,
    dpi: int = 300,
    text_align: str = 'left',
    vertical_align: str = 'top'
) -> Image.Image:
    """将文本添加到标签

    Args:
        label_img: 标签图像
        text: 文本内容
        x: X坐标（mm）
        y: Y坐标（mm）
        width: 宽度（mm）
        height: 高度（mm）
        font_name: 字体名称
        font_size: 字体大小（mm）
        font_style: 字体样式
        color: 颜色
        dpi: 分辨率
        text_align: 水平对齐（left/center/right）
        vertical_align: 垂直对齐（top/middle/bottom）

    Returns:
        更新后的标签图像
    """
    x_px = int(x * dpi / 25.4)
    y_px = int(y * dpi / 25.4)
    width_px = int(width * dpi / 25.4)
    height_px = int(height * dpi / 25.4)
    font_size_px = int(font_size * dpi / 25.4 * 1.5)

    draw = ImageDraw.Draw(label_img)

    text = str(text)
    if text.startswith('\ufeff'):
        text = text[1:]

    font = _load_font(font_size_px)
    lines = _wrap_text(text, draw, font, width_px)

    line_height = font_size_px * 1.2
    total_text_height = len(lines) * line_height
    
    if vertical_align == 'middle':
        start_y = y_px + (height_px - total_text_height) // 2
    elif vertical_align == 'bottom':
        start_y = y_px + height_px - total_text_height
    else:
        start_y = y_px

    for i, line in enumerate(lines):
        line_y = start_y + i * line_height
        
        if text_align == 'center':
            line_width = draw.textbbox((0, 0), line, font=font)[2]
            line_x = x_px + (width_px - line_width) // 2
        elif text_align == 'right':
            line_width = draw.textbbox((0, 0), line, font=font)[2]
            line_x = x_px + width_px - line_width
        else:
            line_x = x_px
        
        draw.text((line_x, line_y), line, font=font, fill=color)

    return label_img


def atom_image_save(label_img: Image.Image, filename: str) -> str:
    """保存标签图像

    Args:
        label_img: 标签图像
        filename: 文件名

    Returns:
        保存的文件路径
    """
    label_img.save(filename)
    return filename


def atom_image_resize(img: Image.Image, width: int, height: int) -> Image.Image:
    """调整图像大小

    Args:
        img: 输入图像
        width: 目标宽度
        height: 目标高度

    Returns:
        调整大小后的图像
    """
    return img.resize((width, height))


def atom_image_paste(
    background: Image.Image,
    foreground: Image.Image,
    x: int,
    y: int
) -> Image.Image:
    """将前景图像粘贴到背景图像

    Args:
        background: 背景图像
        foreground: 前景图像
        x: X坐标
        y: Y坐标

    Returns:
        粘贴后的图像
    """
    background.paste(foreground, (x, y))
    return background


def atom_image_convert_rgb(img: Image.Image) -> Image.Image:
    """将图像转换为RGB模式

    Args:
        img: 输入图像

    Returns:
        RGB模式的图像
    """
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        return background
    elif img.mode != 'RGB':
        return img.convert('RGB')
    return img


def _load_font(font_size: int):
    """加载字体（内部函数）

    Args:
        font_size: 字体大小

    Returns:
        字体对象
    """
    from PIL import ImageFont

    font_paths = [
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/msyh.ttf',
        'C:/Windows/Fonts/msyhbd.ttf',
        'C:/Windows/Fonts/simsun.ttc',
    ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception:
            continue

    font_list = ['SimHei', 'Microsoft YaHei', 'Arial', 'Times New Roman']
    for font_name_try in font_list:
        try:
            return ImageFont.truetype(font_name_try, font_size)
        except Exception:
            continue

    return ImageFont.load_default()


def _wrap_text(text: str, draw: ImageDraw.ImageDraw, font, max_width: int) -> list:
    """文本自动换行（内部函数）

    Args:
        text: 文本内容
        draw: 绘图对象
        font: 字体对象
        max_width: 最大宽度

    Returns:
        换行后的文本行列表
    """
    if not text:
        return []
    
    lines = []
    current_line = ""

    for char in text:
        char_bbox = draw.textbbox((0, 0), char, font=font)
        char_width = char_bbox[2] - char_bbox[0]
        
        if char_width > max_width:
            if current_line:
                lines.append(current_line)
                current_line = ""
            continue
        
        test_line = current_line + char
        test_bbox = draw.textbbox((0, 0), test_line, font=font)
        test_width = test_bbox[2] - test_bbox[0]

        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char

    if current_line:
        lines.append(current_line)

    return lines
