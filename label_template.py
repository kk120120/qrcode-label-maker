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

import json
import os
import uuid

class LabelTemplate:
    def __init__(self):
        self.template = {
            "label_size": {
                "width": 50,
                "height": 30,
                "corner_radius": 2
            },
            "dpi": 300,
            "objects": []
        }
    
    def set_label_size(self, width, height, corner_radius):
        """设置标签尺寸"""
        self.template['label_size']['width'] = width
        self.template['label_size']['height'] = height
        self.template['label_size']['corner_radius'] = corner_radius
    
    def set_dpi(self, dpi):
        """设置DPI"""
        if 96 <= dpi <= 600:
            self.template['dpi'] = dpi
        else:
            self.template['dpi'] = 300
    
    def add_qr_object(self, x, y, width=10, height=10, qr_version="21x21", error_correction="Q", content="", batch=False, csv_column=""):
        """添加二维码对象"""
        obj = {
            "type": "qr",
            "id": str(uuid.uuid4()),
            "position": {
                "x": x,
                "y": y
            },
            "size": {
                "width": width,
                "height": height
            },
            "properties": {
                "qr_version": qr_version,
                "error_correction": error_correction,
                "content": content,
                "batch": batch,
                "csv_column": csv_column
            }
        }
        self.template['objects'].append(obj)
        return obj['id']
    
    def add_text_object(self, x, y, width=30, height=10, font="Arial", font_size=3, font_style=["normal"], color="#000000", content="", batch=False, csv_column=""):
        """添加文本对象"""
        obj = {
            "type": "text",
            "id": str(uuid.uuid4()),
            "position": {
                "x": x,
                "y": y
            },
            "size": {
                "width": width,
                "height": height
            },
            "properties": {
                "font": font,
                "font_size": font_size,
                "font_style": font_style,
                "color": color,
                "content": content,
                "batch": batch,
                "csv_column": csv_column
            }
        }
        self.template['objects'].append(obj)
        return obj['id']
    
    def update_object(self, obj_id, **kwargs):
        """更新对象属性"""
        for obj in self.template['objects']:
            if obj['id'] == obj_id:
                # 更新位置
                if 'x' in kwargs and 'y' in kwargs:
                    obj['position']['x'] = kwargs['x']
                    obj['position']['y'] = kwargs['y']
                # 更新大小
                if 'width' in kwargs and 'height' in kwargs:
                    obj['size']['width'] = kwargs['width']
                    obj['size']['height'] = kwargs['height']
                # 更新属性
                if 'properties' in kwargs:
                    obj['properties'].update(kwargs['properties'])
                return True
        return False
    
    def remove_object(self, obj_id):
        """删除对象"""
        self.template['objects'] = [obj for obj in self.template['objects'] if obj['id'] != obj_id]
    
    def get_object(self, obj_id):
        """获取对象"""
        for obj in self.template['objects']:
            if obj['id'] == obj_id:
                return obj
        return None
    
    def get_objects(self):
        """获取所有对象"""
        return self.template['objects']
    
    def save_template(self, file_path):
        """保存模板到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.template, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存模板失败: {e}")
            return False
    
    def load_template(self, file_path):
        """从文件加载模板"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.template = json.load(f)
            return True
        except Exception as e:
            print(f"加载模板失败: {e}")
            return False
    
    def get_template(self):
        """获取模板数据"""
        return self.template
    
    def check_boundaries(self):
        """检查对象是否超出标签边界"""
        label_width = self.template['label_size']['width']
        label_height = self.template['label_size']['height']
        
        out_of_bounds = []
        for obj in self.template['objects']:
            x = obj['position']['x']
            y = obj['position']['y']
            width = obj['size']['width']
            height = obj['size']['height']
            
            if x < 0 or y < 0 or x + width > label_width or y + height > label_height:
                out_of_bounds.append(obj['id'])
        
        return out_of_bounds
