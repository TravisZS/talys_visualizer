"""
国际化(i18n)支持模块
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from PyQt6.QtCore import QObject, pyqtSignal

class LanguageManager(QObject):
    """语言管理器"""
    
    # 信号定义
    language_changed = pyqtSignal(str)  # 语言改变时发出
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.current_language = 'en'  # 默认英文
        self.translations = {}
        self.available_languages = {}
        self.load_available_languages()
        self.load_translations()
        
    def load_available_languages(self):
        """加载可用语言列表"""
        self.available_languages = {
            'en': {
                'name': 'English',
                'native_name': 'English',
                'flag': '🇺🇸',
                'file': 'en.json'
            },
            'zh': {
                'name': 'Chinese',
                'native_name': '中文',
                'flag': '🇨🇳',
                'file': 'zh.json'
            }
        }
        
    def load_translations(self):
        """加载翻译文件"""
        translations_dir = Path(__file__).parent.parent.parent / "resources" / "translations"
        
        for lang_code, lang_info in self.available_languages.items():
            translation_file = translations_dir / lang_info['file']
            
            if translation_file.exists():
                try:
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                    self.logger.debug(f"已加载语言文件: {lang_code}")
                except Exception as e:
                    self.logger.error(f"加载语言文件失败 {lang_code}: {e}")
                    self.translations[lang_code] = {}
            else:
                self.logger.warning(f"语言文件不存在: {translation_file}")
                self.translations[lang_code] = {}
                
        # 如果没有加载到任何翻译，创建默认的英文翻译
        if not self.translations:
            self.create_default_translations()
            
    def create_default_translations(self):
        """创建默认翻译（英文）"""
        self.translations['en'] = {
            # 主窗口
            "app_title": "TALYS Visualizer",
            "ready": "Ready",
            
            # 菜单
            "menu_file": "&File",
            "menu_edit": "&Edit", 
            "menu_calculate": "&Calculate",
            "menu_view": "&View",
            "menu_help": "&Help",
            
            "action_new": "&New Project",
            "action_open": "&Open Project",
            "action_save": "&Save Project",
            "action_import": "&Import Parameters",
            "action_export": "&Export Parameters",
            "action_exit": "E&xit",
            
            "action_run": "&Run TALYS",
            "action_stop": "&Stop Calculation",
            "action_validate": "&Validate Parameters",
            
            "action_fullscreen": "&Fullscreen",
            "action_help": "&User Manual",
            "action_about": "&About",
            
            # 标签页
            "tab_basic": "🎯 Basic Parameters",
            "tab_advanced": "⚙️ Advanced Parameters", 
            "tab_output": "📄 Output Options",
            "tab_visualization": "📊 Visualization",
            "tab_expert": "🔧 Expert Mode",
            
            # 基础参数
            "basic_title": "Basic Parameter Settings",
            "basic_description": "Set basic parameters for TALYS nuclear reaction calculations. These are the essential parameters required for calculations.",
            
            "group_target": "Target Nucleus",
            "label_atomic_number": "Atomic Number (Z):",
            "label_mass_number": "Mass Number (A):",
            "label_element": "Element Symbol:",
            "label_nuclide": "Nuclide:",
            
            "group_projectile": "Incident Particle",
            "label_particle_type": "Particle Type:",
            "projectile_neutron": "Neutron (n)",
            "projectile_proton": "Proton (p)",
            "projectile_deuteron": "Deuteron (d)",
            "projectile_triton": "Triton (t)",
            "projectile_helium3": "Helium-3 (h)",
            "projectile_alpha": "Alpha particle (a)",
            "projectile_gamma": "Gamma ray (g)",
            
            "group_energy": "Incident Energy",
            "label_energy_mode": "Energy Mode:",
            "radio_single_energy": "Single Energy",
            "radio_energy_range": "Energy Range",
            "label_energy": "Energy:",
            "label_energy_min": "Minimum:",
            "label_energy_max": "Maximum:",
            
            "group_calculation": "Calculation Control",
            "button_run": "🚀 Run TALYS Calculation",
            "button_validate": "✅ Validate Parameters",
            "label_summary": "Current Parameter Summary:",
            
            # 高级参数
            "advanced_title": "Advanced Parameter Settings",
            "advanced_description": "Configure TALYS physics models and advanced calculation options. These parameters affect calculation accuracy and physics model selection.",
            
            "group_level_density": "Level Density Models",
            "label_ldmodel": "Main Model (ldmodel):",
            "label_ldmodelcn": "Compound Nucleus Model (ldmodelcn):",
            
            "group_gamma_strength": "Gamma Strength Functions",
            "label_strength": "E1 Strength Function (strength):",
            "label_strengthm1": "M1 Strength Function (strengthm1):",
            
            "group_optical": "Optical Model Parameters",
            "label_alphaomp": "Alpha Particle Model (alphaomp):",
            "label_deuteronomp": "Deuteron Model (deuteronomp):",
            "label_localomp": "Local Optical Model (localomp):",
            
            "group_numerical": "Numerical Calculation Parameters",
            "label_bins": "Energy Bins (bins):",
            "label_maxlevelstar": "Max Excited Levels (maxlevelstar):",
            "label_maxrot": "Max Rotational Quantum Number (maxrot):",
            
            # 输出选项
            "output_title": "Output Options Settings",
            "output_description": "Control TALYS calculation output files and data formats. Select the required output types to obtain corresponding calculation results.",
            
            "group_basic_output": "Basic Output Options",
            "group_detailed_output": "Detailed Output Options", 
            "group_special_output": "Special Output Options",
            
            "output_flagmain": "Main Output (flagmain)",
            "output_flagbasic": "Basic Information (flagbasic)",
            "output_channels": "Channel Information (channels)",
            "output_flagpop": "Population Information (flagpop)",
            
            "output_outspectra": "Particle Emission Spectra (outspectra)",
            "output_outangle": "Angular Distribution (outangle)",
            "output_flagddx": "Double Differential Cross Section (flagddx)",
            "output_outlevels": "Discrete Level Information (outlevels)",
            "output_flaggamma": "Gamma Cascade (flaggamma)",
            
            "output_flagrecoil": "Recoil Information (flagrecoil)",
            "output_flagfission": "Fission Information (flagfission)",
            "output_flagcheck": "Numerical Check (flagcheck)",
            "output_flagastro": "Astrophysics (flagastro)",
            
            "label_expected_files": "Expected Output Files:",
            
            # 可视化
            "viz_title": "Calculation Results Visualization",
            "viz_description": "View and analyze TALYS calculation results. Results will be displayed here after running calculations.",
            
            "viz_tab_cross_section": "📈 Cross Sections",
            "viz_tab_spectra": "📊 Spectra",
            "viz_tab_angular": "🎯 Angular Distribution",
            "viz_tab_files": "📁 File Viewer",
            
            "label_plot_type": "Chart Type:",
            "label_log_scale": "Logarithmic Scale",
            "button_export_chart": "Export Chart",
            
            # 专家模式
            "expert_title": "Expert Mode",
            "expert_warning": "⚠️ Expert mode allows direct editing of TALYS input files. Please ensure you understand the meaning of TALYS parameters.",
            
            "expert_tab_input": "📝 Input File Editor",
            "expert_tab_advanced": "⚙️ Advanced Options",
            "expert_tab_debug": "🐛 Debug Information",
            
            "button_load_file": "Load File",
            "button_save_file": "Save File", 
            "button_generate": "Generate Input",
            "button_validate_input": "Validate Input",
            
            "label_talys_path": "TALYS Path:",
            "label_timeout": "Timeout:",
            "label_work_dir": "Working Directory:",
            "label_keep_files": "Keep Temporary Files",
            
            # 通用
            "button_ok": "OK",
            "button_cancel": "Cancel",
            "button_apply": "Apply",
            "button_close": "Close",
            "button_browse": "Browse...",
            
            # 状态消息
            "status_ready": "Ready",
            "status_calculating": "Calculating...",
            "status_completed": "Calculation completed",
            "status_error": "Error occurred",
            
            # 工具提示
            "tooltip_atomic_number": "Target nucleus atomic number (1-118)",
            "tooltip_mass_number": "Target nucleus mass number (1-300)",
            "tooltip_energy": "Incident particle energy (MeV)",
            "tooltip_run_calculation": "Start TALYS calculation",
            "tooltip_validate_params": "Validate current parameter settings",
        }
        
        # 创建中文翻译
        self.translations['zh'] = {
            "app_title": "TALYS 可视化工具",
            "ready": "就绪",
            
            "menu_file": "文件(&F)",
            "menu_edit": "编辑(&E)",
            "menu_calculate": "计算(&C)", 
            "menu_view": "视图(&V)",
            "menu_help": "帮助(&H)",
            
            "action_new": "新建项目(&N)",
            "action_open": "打开项目(&O)",
            "action_save": "保存项目(&S)",
            "action_import": "导入参数(&I)",
            "action_export": "导出参数(&E)",
            "action_exit": "退出(&X)",
            
            "action_run": "运行TALYS(&R)",
            "action_stop": "停止计算(&T)",
            "action_validate": "验证参数(&V)",
            
            "action_fullscreen": "全屏模式(&F)",
            "action_help": "用户手册(&H)",
            "action_about": "关于(&A)",
            
            "tab_basic": "🎯 基础参数",
            "tab_advanced": "⚙️ 高级参数",
            "tab_output": "📄 输出选项", 
            "tab_visualization": "📊 可视化",
            "tab_expert": "🔧 专家模式",
            
            "basic_title": "基础参数设置",
            "basic_description": "设置TALYS计算的基本参数。这些是进行核反应计算所必需的参数。",
            
            "group_target": "目标核",
            "label_atomic_number": "原子序数 (Z):",
            "label_mass_number": "质量数 (A):",
            "label_element": "元素符号:",
            "label_nuclide": "核素:",
            
            "group_projectile": "入射粒子",
            "label_particle_type": "粒子类型:",
            "projectile_neutron": "中子 (n)",
            "projectile_proton": "质子 (p)",
            "projectile_deuteron": "氘核 (d)",
            "projectile_triton": "氚核 (t)",
            "projectile_helium3": "氦-3 (h)",
            "projectile_alpha": "α粒子 (a)",
            "projectile_gamma": "伽马射线 (g)",
            
            "group_energy": "入射能量",
            "label_energy_mode": "能量模式:",
            "radio_single_energy": "单一能量",
            "radio_energy_range": "能量范围",
            "label_energy": "能量:",
            "label_energy_min": "最小:",
            "label_energy_max": "最大:",
            
            "group_calculation": "计算控制",
            "button_run": "🚀 运行TALYS计算",
            "button_validate": "✅ 验证参数",
            "label_summary": "当前参数摘要:",
        }
        
    def get_available_languages(self) -> Dict[str, Dict[str, str]]:
        """获取可用语言列表"""
        return self.available_languages.copy()
    
    def get_current_language(self) -> str:
        """获取当前语言"""
        return self.current_language
    
    def set_language(self, language_code: str) -> bool:
        """设置当前语言"""
        if language_code not in self.available_languages:
            self.logger.warning(f"不支持的语言代码: {language_code}")
            return False
            
        if language_code != self.current_language:
            self.current_language = language_code
            self.language_changed.emit(language_code)
            self.logger.info(f"语言已切换到: {language_code}")
            
        return True
    
    def translate(self, key: str, default: Optional[str] = None) -> str:
        """翻译文本"""
        # 尝试获取当前语言的翻译
        current_translations = self.translations.get(self.current_language, {})
        
        if key in current_translations:
            return current_translations[key]
        
        # 如果当前语言没有翻译，尝试英文
        if self.current_language != 'en':
            english_translations = self.translations.get('en', {})
            if key in english_translations:
                return english_translations[key]
        
        # 如果都没有，返回默认值或键名
        return default if default is not None else key
    
    def tr(self, key: str, default: Optional[str] = None) -> str:
        """翻译文本的简写方法"""
        return self.translate(key, default)

# 全局语言管理器实例
_language_manager = None

def get_language_manager() -> LanguageManager:
    """获取全局语言管理器实例"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager

def tr(key: str, default: Optional[str] = None) -> str:
    """全局翻译函数"""
    return get_language_manager().translate(key, default)
