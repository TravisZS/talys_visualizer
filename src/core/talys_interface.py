"""
TALYS接口模块
负责与TALYS可执行文件的交互，包括输入文件生成、计算执行和输出解析
"""

import subprocess
import tempfile
import os
import shutil
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import Settings
from utils.logger import LoggerMixin

class TalysInterface(LoggerMixin):
    """TALYS计算接口类"""
    
    def __init__(self, executable_path: Optional[str] = None):
        """
        初始化TALYS接口
        
        Args:
            executable_path: TALYS可执行文件路径，默认使用配置中的路径
        """
        self.executable = executable_path or Settings.TALYS_EXECUTABLE
        self.temp_dir: Optional[Path] = None
        self.current_calculation = None
        
        # 验证TALYS可执行文件
        self._verify_talys_executable()
        
    def _verify_talys_executable(self) -> bool:
        """
        验证TALYS可执行文件是否可用

        Returns:
            bool: 如果TALYS可执行文件可用返回True
        """
        try:
            # 使用which命令检查可执行文件是否在PATH中
            result = subprocess.run(
                ['which', self.executable],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                talys_path = result.stdout.strip()
                self.logger.info(f"TALYS可执行文件找到: {talys_path}")
                return True
            else:
                # 如果which失败，尝试直接运行TALYS（无参数会显示帮助信息）
                try:
                    result = subprocess.run(
                        [self.executable],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        input="\n"  # 发送空行，让TALYS快速退出
                    )
                    # TALYS通常在没有输入时会退出，这是正常的
                    self.logger.info(f"TALYS可执行文件验证成功: {self.executable}")
                    return True
                except subprocess.TimeoutExpired:
                    # 超时也可能表示TALYS在等待输入，这是正常的
                    self.logger.info(f"TALYS可执行文件响应（超时但正常）: {self.executable}")
                    return True

        except FileNotFoundError:
            self.logger.error(f"找不到TALYS可执行文件: {self.executable}")
            return False
        except Exception as e:
            self.logger.error(f"验证TALYS可执行文件时出错: {e}")
            return False

    def validate_parameters(self, parameters: Dict[str, Any]) -> tuple[bool, str]:
        """
        验证计算参数

        Args:
            parameters: 参数字典

        Returns:
            tuple: (是否有效, 错误信息)
        """
        try:
            # 检查基础必需参数
            basic_required_params = ['projectile', 'element', 'mass']
            for param in basic_required_params:
                if param not in parameters:
                    return False, f"缺少必需参数: {param}"
                if parameters[param] is None or parameters[param] == '':
                    return False, f"参数 {param} 不能为空"

            # 验证入射粒子
            valid_projectiles = ['n', 'p', 'd', 't', 'h', 'a', 'g']
            if parameters['projectile'] not in valid_projectiles:
                return False, f"无效的入射粒子: {parameters['projectile']}"

            # 验证原子序数和质量数
            try:
                mass = int(parameters['mass'])
                if mass < 1 or mass > 300:
                    return False, "质量数必须在1-300之间"
            except (ValueError, TypeError):
                return False, "质量数必须是整数"

            # 验证能量
            if 'energy' in parameters:
                # 单一能量模式
                try:
                    energy = float(parameters['energy'])
                    if energy <= 0 or energy > 1000:
                        return False, "能量必须在0-1000 MeV之间"
                except (ValueError, TypeError):
                    return False, "能量必须是数字"
            elif 'energy_mode' in parameters and parameters['energy_mode'] == 'range':
                # 能量范围模式
                try:
                    energy_min = float(parameters.get('energy_min', 0))
                    energy_max = float(parameters.get('energy_max', 0))
                    energy_step = float(parameters.get('energy_step', 1))

                    if energy_min <= 0 or energy_min > 1000:
                        return False, "最小能量必须在0-1000 MeV之间"
                    if energy_max <= 0 or energy_max > 1000:
                        return False, "最大能量必须在0-1000 MeV之间"
                    if energy_min >= energy_max:
                        return False, "最小能量必须小于最大能量"
                    if energy_step <= 0 or energy_step > (energy_max - energy_min):
                        return False, "能量步长必须大于0且小于能量范围"
                except (ValueError, TypeError):
                    return False, "能量参数必须是数字"
            else:
                return False, "缺少能量参数"

            # 验证元素符号
            element = parameters['element']
            if not element or not element.isalpha():
                return False, "元素符号必须是字母"

            return True, "参数验证通过"

        except Exception as e:
            return False, f"参数验证出错: {e}"
    
    def create_temp_directory(self) -> Path:
        """
        创建临时工作目录
        
        Returns:
            Path: 临时目录路径
        """
        if self.temp_dir and self.temp_dir.exists():
            return self.temp_dir
            
        self.temp_dir = Path(tempfile.mkdtemp(prefix="talys_calc_"))
        self.logger.info(f"创建临时工作目录: {self.temp_dir}")
        return self.temp_dir
    
    def cleanup_temp_directory(self):
        """清理临时工作目录"""
        if self.temp_dir and self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
                self.logger.info(f"清理临时目录: {self.temp_dir}")
                self.temp_dir = None
            except Exception as e:
                self.logger.error(f"清理临时目录失败: {e}")
    
    def generate_input_file(self, parameters: Dict[str, Any]) -> Path:
        """
        生成TALYS输入文件
        
        Args:
            parameters: 计算参数字典
            
        Returns:
            Path: 生成的输入文件路径
        """
        if not self.temp_dir:
            self.create_temp_directory()
            
        input_file = self.temp_dir / "talys.inp"
        
        try:
            with open(input_file, 'w', encoding='utf-8') as f:
                # 文件头部注释
                f.write("# TALYS input file generated by TALYS Visualizer\n")
                f.write(f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("#\n\n")
                
                # 必需参数
                f.write("# Required parameters\n")
                basic_required_params = ['projectile', 'element', 'mass']
                for param in basic_required_params:
                    if param in parameters:
                        f.write(f"{param} {parameters[param]}\n")
                    else:
                        raise ValueError(f"缺少必需参数: {param}")

                # 能量参数处理
                if 'energy' in parameters:
                    # 单一能量模式
                    f.write(f"energy {parameters['energy']}\n")
                elif 'energy_mode' in parameters and parameters['energy_mode'] == 'range':
                    # 能量范围模式
                    f.write(f"energy {parameters['energy_min']} {parameters['energy_max']} {parameters['energy_step']}\n")
                else:
                    raise ValueError("缺少能量参数")
                
                f.write("\n")
                
                # 可选参数
                f.write("# Optional parameters\n")
                excluded_params = ['projectile', 'element', 'mass', 'energy', 'energy_min', 'energy_max', 'energy_step', 'energy_mode']
                for key, value in parameters.items():
                    if key not in excluded_params:
                        # 处理布尔值
                        if isinstance(value, bool):
                            value = 'y' if value else 'n'
                        f.write(f"{key} {value}\n")
                
                f.write("\n# End of input file\n")
            
            self.logger.info(f"生成TALYS输入文件: {input_file}")
            return input_file
            
        except Exception as e:
            self.logger.error(f"生成输入文件失败: {e}")
            raise TalysInterfaceError(f"生成输入文件失败: {e}")
    
    def run_calculation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行TALYS计算
        
        Args:
            parameters: 计算参数
            
        Returns:
            Dict: 计算结果数据
        """
        try:
            # 生成输入文件
            input_file = self.generate_input_file(parameters)
            
            # 切换到工作目录
            original_dir = os.getcwd()
            os.chdir(self.temp_dir)
            
            self.logger.info("开始TALYS计算...")
            start_time = time.time()
            
            # 运行TALYS，通过重定向输入文件
            # TALYS通常使用: talys < input_file
            with open(input_file, 'r') as f:
                input_content = f.read()

            self.current_calculation = subprocess.Popen(
                [self.executable],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # 等待计算完成
            stdout, stderr = self.current_calculation.communicate(
                input=input_content,
                timeout=Settings.TALYS_TIMEOUT
            )
            
            calculation_time = time.time() - start_time
            
            if self.current_calculation.returncode == 0:
                self.logger.info(f"TALYS计算完成，耗时: {calculation_time:.2f}秒")
                
                # 解析输出文件
                results = self.parse_output_files()
                results['calculation_time'] = calculation_time
                results['stdout'] = stdout
                
                return results
            else:
                error_msg = f"TALYS计算失败 (返回码: {self.current_calculation.returncode})"
                if stderr:
                    error_msg += f"\n错误信息: {stderr}"
                self.logger.error(error_msg)
                raise TalysCalculationError(error_msg)
                
        except subprocess.TimeoutExpired:
            self.logger.error("TALYS计算超时")
            if self.current_calculation:
                self.current_calculation.kill()
            raise TalysCalculationError("TALYS计算超时")
        except Exception as e:
            self.logger.error(f"TALYS计算过程中出错: {e}")
            raise TalysCalculationError(f"计算失败: {e}")
        finally:
            os.chdir(original_dir)
            self.current_calculation = None
    
    def parse_output_files(self) -> Dict[str, Any]:
        """
        解析TALYS输出文件
        
        Returns:
            Dict: 解析后的数据
        """
        if not self.temp_dir:
            raise TalysInterfaceError("没有可用的工作目录")
        
        results = {}
        
        # 解析总截面文件
        total_file = self.temp_dir / "total.tot"
        if total_file.exists():
            results['total_cross_section'] = self._parse_cross_section_file(total_file)
            self.logger.debug("解析总截面文件完成")
        
        # 解析能谱文件
        spectra_files = list(self.temp_dir.glob("*.spe"))
        if spectra_files:
            results['spectra'] = {}
            for file in spectra_files:
                particle = file.stem
                results['spectra'][particle] = self._parse_spectrum_file(file)
            self.logger.debug(f"解析{len(spectra_files)}个能谱文件完成")
        
        # 解析角分布文件
        angular_files = list(self.temp_dir.glob("*.ang"))
        if angular_files:
            results['angular'] = {}
            for file in angular_files:
                energy = file.stem
                results['angular'][energy] = self._parse_angular_file(file)
            self.logger.debug(f"解析{len(angular_files)}个角分布文件完成")

        # 解析残余核产生文件
        residual_files = list(self.temp_dir.glob("rp*.tot"))
        if residual_files:
            results['residual_production'] = {}
            for file in residual_files:
                nucleus = file.stem
                results['residual_production'][nucleus] = self._parse_cross_section_file(file)
            self.logger.debug(f"解析{len(residual_files)}个残余核产生文件完成")

        # 解析反应道截面文件
        channel_files = list(self.temp_dir.glob("*.L*"))
        if channel_files:
            results['reaction_channels'] = {}
            for file in channel_files:
                channel = file.name
                results['reaction_channels'][channel] = self._parse_cross_section_file(file)
            self.logger.debug(f"解析{len(channel_files)}个反应道文件完成")

        # 解析gamma射线产生文件
        gamma_files = list(self.temp_dir.glob("*.gam"))
        if gamma_files:
            results['gamma_production'] = {}
            for file in gamma_files:
                transition = file.stem
                results['gamma_production'][transition] = self._parse_spectrum_file(file)
            self.logger.debug(f"解析{len(gamma_files)}个gamma产生文件完成")

        # 列出所有输出文件
        output_files = list(self.temp_dir.glob("*"))
        results['output_files'] = [f.name for f in output_files if f.is_file()]

        self.logger.info(f"解析完成，共找到{len(results['output_files'])}个输出文件")
        return results
    
    def _parse_cross_section_file(self, file_path: Path) -> Dict[str, List[float]]:
        """解析截面文件"""
        energies = []
        cross_sections = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 跳过头部注释
            data_start = 0
            for i, line in enumerate(lines):
                if not line.strip().startswith('#') and line.strip():
                    data_start = i
                    break
            
            # 解析数据
            for line in lines[data_start:]:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            energy = float(parts[0])
                            xs = float(parts[1])
                            energies.append(energy)
                            cross_sections.append(xs)
                        except ValueError:
                            continue
            
            return {
                'energy': energies,
                'cross_section': cross_sections
            }
            
        except Exception as e:
            self.logger.error(f"解析截面文件失败 {file_path}: {e}")
            return {'energy': [], 'cross_section': []}
    
    def _parse_spectrum_file(self, file_path: Path) -> Dict[str, List[float]]:
        """解析能谱文件"""
        try:
            energies = []
            intensities = []

            with open(file_path, 'r') as f:
                lines = f.readlines()

            # 跳过注释行和头部信息
            data_started = False
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 检查是否是数据行（通常包含两列数字）
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        energy = float(parts[0])
                        intensity = float(parts[1])
                        energies.append(energy)
                        intensities.append(intensity)
                        data_started = True
                    except ValueError:
                        if data_started:
                            break  # 数据部分结束
                        continue

            self.logger.debug(f"解析能谱文件 {file_path.name}: {len(energies)} 个数据点")
            return {'energy': energies, 'intensity': intensities}

        except Exception as e:
            self.logger.error(f"解析能谱文件失败 {file_path}: {e}")
            return {'energy': [], 'intensity': []}

    def _parse_angular_file(self, file_path: Path) -> Dict[str, List[float]]:
        """解析角分布文件"""
        try:
            angles = []
            cross_sections = []

            with open(file_path, 'r') as f:
                lines = f.readlines()

            # 跳过注释行和头部信息
            data_started = False
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 检查是否是数据行
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        angle = float(parts[0])
                        cross_section = float(parts[1])
                        angles.append(angle)
                        cross_sections.append(cross_section)
                        data_started = True
                    except ValueError:
                        if data_started:
                            break
                        continue

            self.logger.debug(f"解析角分布文件 {file_path.name}: {len(angles)} 个数据点")
            return {'angle': angles, 'cross_section': cross_sections}

        except Exception as e:
            self.logger.error(f"解析角分布文件失败 {file_path}: {e}")
            return {'angle': [], 'cross_section': []}
    
    def stop_calculation(self):
        """停止当前计算"""
        if self.current_calculation and self.current_calculation.poll() is None:
            self.logger.info("停止TALYS计算")
            self.current_calculation.terminate()
            try:
                self.current_calculation.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.current_calculation.kill()
            self.current_calculation = None

class TalysInterfaceError(Exception):
    """TALYS接口错误"""
    pass

class TalysCalculationError(Exception):
    """TALYS计算错误"""
    pass
