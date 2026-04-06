# Python 批量二维码标签生成器
# Copyright (C) 2026
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PIL import Image, ImageDraw, ImageFont
import os

class ImageProcessor:
    def __init__(self):
        pass
    
    def create_label(self, width, height, corner_radius, dpi=300):
        """创建标签图像"""
        # 转换mm为像素
        width_px = int(width * dpi / 25.4)
        height_px = int(height * dpi / 25.4)
        
        # 创建白色背景图像
        img = Image.new('RGB', (width_px, height_px), color='white')
        return img
    
    def add_qr_to_label(self, label_img, qr_img, x, y, width, height, dpi=300):
        """将二维码添加到标签"""
        # 转换mm为像素
        x_px = int(x * dpi / 25.4)
        y_px = int(y * dpi / 25.4)
        width_px = int(width * dpi / 25.4)
        height_px = int(height * dpi / 25.4)
        
        # 调整二维码大小
        qr_resized = qr_img.resize((width_px, height_px))
        
        # 添加到标签
        label_img.paste(qr_resized, (x_px, y_px))
        return label_img
    
    def add_text_to_label(self, label_img, text, x, y, width, height, font_name, font_size, font_style, color, dpi=300):
        """将文本添加到标签"""
        # 转换mm为像素
        x_px = int(x * dpi / 25.4)
        y_px = int(y * dpi / 25.4)
        width_px = int(width * dpi / 25.4)
        height_px = int(height * dpi / 25.4)
        
        # 增大字体大小，确保文字清晰可见
        font_size_px = int(font_size * dpi / 25.4 * 1.5)
        
        # 创建绘图对象
        draw = ImageDraw.Draw(label_img)
        
        # 确保文本是字符串类型，并处理utf8with bom格式
        text = str(text)
        # 移除可能存在的BOM标记
        if text.startswith('\ufeff'):
            text = text[1:]
        
        # 尝试加载字体，确保支持utf-8
        font = None
        
        # 1. 尝试使用系统中可能存在的中文字体路径
        # 常见的中文字体路径
        font_paths = [
            'C:/Windows/Fonts/simhei.ttf',  # SimHei
            'C:/Windows/Fonts/msyh.ttf',    # Microsoft YaHei
            'C:/Windows/Fonts/msyhbd.ttf',  # Microsoft YaHei Bold
            'C:/Windows/Fonts/simsun.ttc',   # SimSun
        ]
        
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size_px)
                break
            except:
                continue
        
        # 2. 如果找不到系统字体，尝试使用字体名称
        if font is None:
            font_list = ['SimHei', 'Microsoft YaHei', 'Arial', 'Times New Roman']
            for font_name_try in font_list:
                try:
                    font = ImageFont.truetype(font_name_try, font_size_px)
                    break
                except:
                    continue
        
        # 3. 如果所有字体都加载失败，使用默认字体
        if font is None:
            font = ImageFont.load_default()
        
        # 处理文本自动换行
        import textwrap
        
        # 处理文本自动换行，考虑中英文混合
        lines = []
        current_line = ""
        
        for char in text:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = bbox[2] - bbox[0]
            
            if test_width <= width_px:
                current_line = test_line
            else:
                # 如果当前行不为空，添加到行列表
                if current_line:
                    lines.append(current_line)
                # 开始新行
                current_line = char
        
        # 添加最后一行
        if current_line:
            lines.append(current_line)
        
        # 计算文本高度
        # 行距为1.2倍字高
        line_height = font_size_px * 1.2
        total_text_height = len(lines) * line_height
        
        # 靠上对齐
        start_y = y_px
        
        # 绘制文本
        for i, line in enumerate(lines):
            line_y = start_y + i * line_height
            # 靠左对齐
            line_x = x_px
            draw.text((line_x, line_y), line, font=font, fill=color)
        
        return label_img
    
    def save_label(self, label_img, filename):
        """保存标签图像"""
        label_img.save(filename)
        return filename
    
    def batch_process(self, template, csv_data, output_dir):
        """批量处理生成标签"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        results = []
        for i, row in csv_data.iterrows():
            # 创建标签
            label_img = self.create_label(
                template['label_size']['width'],
                template['label_size']['height'],
                template['label_size']['corner_radius'],
                template['dpi']
            )
            
            # 添加对象
            qr_content = ""
            for obj in template['objects']:
                if obj['type'] == 'qr' and obj['properties']['batch']:
                    # 批量二维码
                    content = str(row[obj['properties']['csv_column']])
                    qr_content = content
                    qr_gen = QRGenerator()
                    qr_img = qr_gen.generate_qr(
                        content,
                        obj['properties']['error_correction'],
                        obj['properties']['qr_version']
                    )
                    label_img = self.add_qr_to_label(
                        label_img, qr_img,
                        obj['position']['x'], obj['position']['y'],
                        obj['size']['width'], obj['size']['height'],
                        template['dpi']
                    )
                elif obj['type'] == 'text' and obj['properties']['batch']:
                    # 批量文本
                    content = str(row[obj['properties']['csv_column']])
                    label_img = self.add_text_to_label(
                        label_img, content,
                        obj['position']['x'], obj['position']['y'],
                        obj['size']['width'], obj['size']['height'],
                        obj['properties']['font'],
                        obj['properties']['font_size'],
                        obj['properties']['font_style'],
                        obj['properties']['color'],
                        template['dpi']
                    )
                elif obj['type'] == 'qr' and not obj['properties']['batch']:
                    # 固定二维码
                    qr_gen = QRGenerator()
                    qr_img = qr_gen.generate_qr(
                        obj['properties']['content'],
                        obj['properties']['error_correction'],
                        obj['properties']['qr_version']
                    )
                    label_img = self.add_qr_to_label(
                        label_img, qr_img,
                        obj['position']['x'], obj['position']['y'],
                        obj['size']['width'], obj['size']['height'],
                        template['dpi']
                    )
                elif obj['type'] == 'text' and not obj['properties']['batch']:
                    # 固定文本
                    label_img = self.add_text_to_label(
                        label_img, obj['properties']['content'],
                        obj['position']['x'], obj['position']['y'],
                        obj['size']['width'], obj['size']['height'],
                        obj['properties']['font'],
                        obj['properties']['font_size'],
                        obj['properties']['font_style'],
                        obj['properties']['color'],
                        template['dpi']
                    )
            
            # 保存文件
            # 使用二维码内容前12个字符作为文件名
            if qr_content:
                filename = qr_content[:12] + '.png'
            else:
                filename = 'noQR_{}.png'.format(i)
            
            filepath = os.path.join(output_dir, filename)
            self.save_label(label_img, filepath)
            results.append(filepath)
        
        return results

# 避免循环导入
from qr_generator import QRGenerator
