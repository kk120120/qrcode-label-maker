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

import qrcode
from PIL import Image

class QRGenerator:
    def __init__(self):
        pass
    
    def generate_qr(self, content, error_correction='M', qr_size="21x21"):
        """生成二维码图像"""
        # 映射纠错级别
        ec_mapping = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        
        # 根据尺寸计算version
        # QR码版本1是21x21模块，版本2是25x25模块，以此类推，每个版本增加4个模块
        try:
            size = int(qr_size.split('x')[0])
            version = (size - 21) // 4 + 1
            # 确保version在有效范围内（1-40）
            version = max(1, min(40, version))
        except:
            # 如果尺寸格式不正确，使用默认版本1
            version = 1
        
        qr = qrcode.QRCode(
            version=version,
            error_correction=ec_mapping.get(error_correction, qrcode.constants.ERROR_CORRECT_M),
            box_size=10,
            border=4,
        )
        
        qr.add_data(content)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    def save_qr(self, content, filename, error_correction='M', qr_size="21x21"):
        """保存二维码图像到文件"""
        img = self.generate_qr(content, error_correction, qr_size)
        img.save(filename)
        return filename
