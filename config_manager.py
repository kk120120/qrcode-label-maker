import json
import os

class ConfigManager:
    """配置文件管理类"""
    
    def __init__(self):
        """初始化配置管理器"""
        # 配置文件路径
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        # 配置数据
        self.config = {
            "last_open_dir": "d:/",
            "last_import_dir": "d:/"
        }
        # 加载配置
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
    
    def save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_last_open_dir(self):
        """获取上一次打开文件的目录"""
        return self.config.get("last_open_dir", "d:/")
    
    def set_last_open_dir(self, directory):
        """设置上一次打开文件的目录"""
        self.config["last_open_dir"] = directory
        self.save_config()
    
    def get_last_import_dir(self):
        """获取上一次导入文件的目录"""
        return self.config.get("last_import_dir", "d:/")
    
    def set_last_import_dir(self, directory):
        """设置上一次导入文件的目录"""
        self.config["last_import_dir"] = directory
        self.save_config()
    
    def get_qr_sizes(self):
        """获取二维码尺寸列表"""
        return ["17x17", "21x21", "25x25", "29x29", "33x33", "37x37", "41x41", "45x45", "49x49", "53x53"]
    
    def get_capacity(self, version, error_level):
        """获取二维码容量信息"""
        # 简单的容量映射，实际应用中可能需要更复杂的计算
        capacity_map = {
            "17x17": {"L": (41, 25, 17, 10), "M": (34, 20, 14, 8), "Q": (27, 16, 11, 7), "H": (17, 12, 8, 5)},
            "21x21": {"L": (77, 47, 32, 19), "M": (63, 38, 26, 15), "Q": (48, 31, 22, 12), "H": (34, 27, 19, 11)},
            "25x25": {"L": (127, 77, 53, 32), "M": (101, 63, 43, 26), "Q": (77, 52, 37, 22), "H": (58, 43, 31, 18)},
            "29x29": {"L": (187, 114, 78, 47), "M": (155, 98, 67, 40), "Q": (122, 82, 57, 32), "H": (86, 68, 48, 27)},
            "33x33": {"L": (267, 154, 106, 64), "M": (221, 122, 84, 50), "Q": (177, 102, 71, 42), "H": (122, 86, 60, 35)},
            "37x37": {"L": (357, 202, 139, 83), "M": (296, 152, 104, 62), "Q": (242, 127, 88, 52), "H": (173, 109, 75, 44)},
            "41x41": {"L": (467, 255, 177, 106), "M": (382, 194, 133, 79), "Q": (311, 155, 107, 64), "H": (233, 133, 92, 55)},
            "45x45": {"L": (587, 313, 218, 131), "M": (482, 232, 160, 95), "Q": (382, 187, 130, 78), "H": (287, 158, 110, 65)},
            "49x49": {"L": (717, 377, 262, 157), "M": (582, 273, 188, 112), "Q": (462, 219, 152, 91), "H": (357, 182, 127, 75)},
            "53x53": {"L": (857, 448, 310, 187), "M": (682, 321, 221, 133), "Q": (532, 255, 176, 105), "H": (427, 213, 148, 88)}
        }
        
        if version in capacity_map and error_level in capacity_map[version]:
            return capacity_map[version][error_level]
        return None