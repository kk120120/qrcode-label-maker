"""
L1 入口层 - 程序总入口
功能：只负责启动和清理，不写 UI、不写业务、不写控件、不写逻辑
文件：main.py
"""

import sys
import os
import logging
from pathlib import Path

# 设置运行路径
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """检查依赖版本"""
    required = {
        'PyQt5': '5.15.0',
        'Pillow': '8.0.0',
        'qrcode': '7.0.0',
    }

    for module, min_version in required.items():
        try:
            if module == 'PyQt5':
                from PyQt5.QtCore import PYQT_VERSION_STR
                version = PYQT_VERSION_STR
            elif module == 'Pillow':
                from PIL import Image
                version = Image.__version__
            elif module == 'qrcode':
                import qrcode
                try:
                    version = qrcode.__version__
                except AttributeError:
                    version = "unknown"
            logger.info(f"{module} version: {version}")
        except ImportError as e:
            logger.error(f"缺少依赖: {module} - {e}")
            return False
    return True


def load_config():
    """加载配置文件"""
    config_file = BASE_DIR / 'config.json'
    if config_file.exists():
        import json
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logger.info(f"已加载配置: {config_file}")
            return config
    return {}


def save_config(config):
    """保存配置文件"""
    config_file = BASE_DIR / 'config.json'
    import json
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        logger.info(f"已保存配置: {config_file}")


def main():
    """程序主入口"""
    logger.info("=" * 50)
    logger.info("QR Label Creator 启动")
    logger.info("=" * 50)

    # 检查依赖
    if not check_dependencies():
        print("错误：缺少必要的依赖库，请运行: pip install -r requirements.txt")
        sys.exit(1)

    # 加载配置
    config = load_config()

    # 创建应用程序
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("QR Label Creator")
    app.setOrganizationName("QR Label Creator")

    # 调用 L1 入口层，启动界面
    from entry.entry_main import EntryMain
    entry_main = EntryMain()
    window = entry_main.create_main_window()
    window.show()

    # 启动 UI 消息循环
    logger.info("启动消息循环...")
    exit_code = app.exec()

    # 程序退出时的清理
    logger.info("程序退出，清理资源...")

    # 保存配置
    save_config(config)

    logger.info(f"程序退出，退出码: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())