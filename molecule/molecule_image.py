"""
L3 分子层 - 图像管理
功能：编排原子操作，实现完整业务动作
文件：molecule/molecule_image.py
"""

import os
import pandas as pd
from typing import List, Optional, Dict, Any
from PIL import Image
from atom.atom_image import (
    atom_image_create_label,
    atom_image_add_qr,
    atom_image_add_text,
    atom_image_save,
    atom_image_convert_rgb
)
from atom.atom_qr import atom_qr_generate


class ImageManager:
    """图像管理器"""

    def molecule_image_create_label(
        self,
        width: float,
        height: float,
        corner_radius: float,
        dpi: int = 300
    ) -> Image.Image:
        """创建标签图像"""
        return atom_image_create_label(width, height, corner_radius, dpi)

    def molecule_image_add_qr(
        self,
        label_img: Image.Image,
        qr_img: Image.Image,
        x: float,
        y: float,
        width: float,
        height: float,
        dpi: int = 300
    ) -> Image.Image:
        """将二维码添加到标签"""
        return atom_image_add_qr(label_img, qr_img, x, y, width, height, dpi)

    def molecule_image_add_text(
        self,
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
        """将文本添加到标签"""
        return atom_image_add_text(
            label_img, text, x, y, width, height,
            font_name, font_size, font_style, color, dpi,
            text_align, vertical_align
        )

    def molecule_image_save(self, label_img: Image.Image, filename: str) -> str:
        """保存标签图像"""
        return atom_image_save(label_img, filename)

    def molecule_image_qr_generate(
        self,
        content: str,
        error_correction: str,
        qr_version: str
    ) -> Optional[Image.Image]:
        """生成二维码图像"""
        return atom_qr_generate(content, error_correction, qr_version)

    def molecule_image_export_current(
        self,
        template: Dict[str, Any],
        file_path: str,
        csv_handler: Any = None,
        row_index: Optional[int] = None
    ) -> bool:
        """导出当前标签图像

        Args:
            template: 模板数据
            file_path: 保存文件路径
            csv_handler: CSV处理器
            row_index: 指定行索引（从0开始），None表示使用第一行

        Returns:
            是否导出成功
        """
        try:
            objects = template.get('objects', [])
            img = self.molecule_image_create_label(
                template['label_size']['width'],
                template['label_size']['height'],
                template['label_size']['corner_radius'],
                template['dpi']
            )

            csv_data = None
            if csv_handler:
                csv_data = csv_handler.molecule_csv_get_data()
            
            # 获取指定行数据
            row = None
            if csv_data is not None and not csv_data.empty:
                if row_index is None or row_index < 0 or row_index >= len(csv_data):
                    row_index = 0
                row = csv_data.iloc[row_index]

            for obj in objects:
                if obj['type'] == 'qr':
                    content = obj['content']
                    if obj.get('batch', False) and row is not None:
                        csv_column = obj.get('csv_column', '')
                        if csv_column:
                            content = str(row[csv_column])
                    
                    qr_img = atom_qr_generate(
                        content,
                        obj['error_correction'],
                        obj['qr_version']
                    )
                    if qr_img:
                        img = self.molecule_image_add_qr(
                            img, qr_img,
                            obj['position']['x'], obj['position']['y'],
                            obj['size']['width'], obj['size']['height'],
                            template['dpi']
                        )
                elif obj['type'] == 'text':
                    content = obj['content']
                    if obj.get('batch', False) and row is not None:
                        csv_column = obj.get('csv_column', '')
                        if csv_column:
                            content = str(row[csv_column])
                    
                    img = self.molecule_image_add_text(
                        img, content,
                        obj['position']['x'], obj['position']['y'],
                        obj['size']['width'], obj['size']['height'],
                        obj['font'],
                        obj['font_size'],
                        obj['font_style'],
                        obj['color'],
                        template['dpi'],
                        obj.get('text_align', 'left'),
                        obj.get('vertical_align', 'top')
                    )

            self.molecule_image_save(img, file_path)
            return True
        except Exception:
            return False

    def molecule_image_batch_export(
        self,
        template: Dict[str, Any],
        csv_manager: Any,
        output_dir: str,
        export_format: str,
        progress_callback=None
    ) -> tuple[bool, str]:
        """批量导出标签图像

        Args:
            template: 模板数据
            csv_manager: CSV管理器实例
            output_dir: 输出目录
            export_format: 导出格式 (png/pdf)
            progress_callback: 进度回调函数 (current, total)

        Returns:
            (是否导出成功, 错误原因)
        """
        try:
            csv_data = None
            if csv_manager:
                csv_data = csv_manager.molecule_csv_get_data()
                
            if csv_data is None or csv_data.empty:
                return False, "未导入CSV或Excel数据，请先导入数据文件"

            label_size = template.get('label_size', {})
            if label_size.get('width', 0) <= 0 or label_size.get('height', 0) <= 0:
                return False, "标签尺寸无效，请检查标签设置"

            objects = template.get('objects', [])
            if not objects:
                return False, "标签中没有对象，请先添加二维码或文本对象"

            batch_enabled_objects = [obj for obj in objects if obj.get('batch', False)]
            if batch_enabled_objects:
                csv_columns = list(csv_data.columns)
                for obj in batch_enabled_objects:
                    csv_column = obj.get('csv_column', '')
                    if csv_column and csv_column not in csv_columns:
                        return False, f"对象 '{obj.get('id', 'unknown')}' 关联的数据列 '{csv_column}' 不存在于CSV中"

            results = self._batch_process(
                template, csv_data, output_dir, export_format,
                progress_callback
            )

            if len(results) == 0:
                return False, "批量导出失败，未生成任何文件"

            return True, ""
        except PermissionError:
            return False, "文件权限错误，请关闭已生成的文件后重试"
        except OSError as e:
            return False, f"系统错误：{str(e)}"
        except Exception as e:
            return False, f"导出过程中发生错误：{str(e)}"

    def _batch_process(
        self,
        template: Dict[str, Any],
        csv_data: pd.DataFrame,
        output_dir: str,
        export_format: str,
        progress_callback=None
    ) -> List[str]:
        """批量处理生成标签（内部方法）

        Args:
            template: 模板数据
            csv_data: CSV数据
            output_dir: 输出目录
            export_format: 导出格式
            progress_callback: 进度回调函数 (current, total)

        Returns:
            生成的文件路径列表
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        results = []
        images = []
        total = len(csv_data)

        for i, row in csv_data.iterrows():
            if progress_callback:
                progress_callback(i + 1, total)
            label_img = self.molecule_image_create_label(
                template['label_size']['width'],
                template['label_size']['height'],
                template['label_size']['corner_radius'],
                template['dpi']
            )

            qr_content = ""
            for obj in template['objects']:
                processed_img = self._process_single_object(
                    label_img, obj, row, template['dpi']
                )
                if processed_img is not None:
                    label_img = processed_img
                    if obj['type'] == 'qr' and obj['batch']:
                        qr_content = str(row.get(obj['csv_column'], ''))

            if export_format == "png":
                if qr_content:
                    filename = qr_content[:20] + '.png'
                else:
                    filename = f'noQR_{i}.png'

                filepath = os.path.join(output_dir, filename)
                self.molecule_image_save(label_img, filepath)
                results.append(filepath)
            else:
                images.append(label_img)

        if export_format == "pdf" and images:
            pdf_path = self._save_as_pdf(
                images, output_dir, template['dpi']
            )
            if pdf_path:
                results.append(pdf_path)

        return results

    def _process_single_object(
        self,
        label_img: Image.Image,
        obj: Dict[str, Any],
        row: pd.Series,
        dpi: int
    ) -> Optional[Image.Image]:
        """处理单个对象

        Args:
            label_img: 标签图像
            obj: 对象数据
            row: CSV行数据
            dpi: 分辨率

        Returns:
            处理后的标签图像
        """
        if obj['type'] == 'qr':
            if obj['batch']:
                content = str(row[obj['csv_column']])
            else:
                content = obj['content']

            qr_img = atom_qr_generate(
                content,
                obj['error_correction']
            )
            if qr_img:
                return self.molecule_image_add_qr(
                    label_img, qr_img,
                    obj['position']['x'], obj['position']['y'],
                    obj['size']['width'], obj['size']['height'],
                    dpi
                )

        elif obj['type'] == 'text':
            if obj['batch']:
                content = str(row[obj['csv_column']])
            else:
                content = obj['content']

            return self.molecule_image_add_text(
                label_img, content,
                obj['position']['x'], obj['position']['y'],
                obj['size']['width'], obj['size']['height'],
                obj['font'],
                obj['font_size'],
                obj['font_style'],
                obj['color'],
                dpi,
                obj.get('text_align', 'left'),
                obj.get('vertical_align', 'top')
            )

        return None

    def _save_as_pdf(
        self,
        images: List[Image.Image],
        output_dir: str,
        dpi: int
    ) -> Optional[str]:
        """保存为PDF文件

        Args:
            images: 图像列表
            output_dir: 输出目录
            dpi: 分辨率

        Returns:
            PDF文件路径
        """
        if not images:
            return None

        pdf_filename = "labels.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        pdf_dpi = min(dpi * 2, 800)

        rgb_images = []
        for img in images:
            rgb_img = atom_image_convert_rgb(img)
            if rgb_img.mode != 'RGB':
                rgb_img = rgb_img.convert('RGB')
            rgb_images.append(rgb_img)

        rgb_images[0].save(
            pdf_path,
            save_all=True,
            append_images=rgb_images[1:],
            resolution=pdf_dpi,
            format='PDF'
        )

        return pdf_path
