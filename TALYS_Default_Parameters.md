# TALYS 默认参数提取计划

## 目标
从TALYS源代码中提取所有输入参数的默认值，确保GUI界面使用与TALYS完全一致的默认设置。

## 参数分类

### 1. 必需参数 (4个)
```
projectile    # 入射粒子类型
element       # 目标元素符号  
mass          # 目标核质量数
energy        # 入射能量
```

### 2. 物理模型参数

#### 能级密度模型
```fortran
! 从 input3.f 提取
ldmodel = 1        ! 默认: CTM模型
ldmodelCN = 0      ! 复合核特殊模型
```

#### 伽马强度函数
```fortran
! 从 input4.f 提取  
strength = 9       ! E1伽马强度函数模型
strengthM1 = 3     ! M1伽马强度函数模型
```

#### 光学模型
```fortran
! 从 input3.f 提取
alphaomp = 1       ! α粒子光学模型
deuteronomp = 1    ! 氘核光学模型
localomp = .true.  ! 局域光学模型
```

#### 裂变模型
```fortran
! 从 input4.f 提取
fismodel = 1       ! 裂变模型选择
fymodel = 1        ! 裂变产物模型
```

### 3. 输出控制参数

#### 基础输出
```fortran
! 从 input4.f 提取
flagmain = .true.     ! 主要输出
flagbasic = .true.    ! 基础信息输出
flagpop = .false.     ! 布居输出
flagcheck = .false.   ! 数值检查输出
```

#### 详细输出
```fortran
flagspec = .false.    ! 能谱输出
flagang = .false.     ! 角分布输出
flagddx = .false.     ! 双微分截面
flagdisc = .false.    ! 离散能级
flagchannels = .false. ! 反应道
flagrecoil = .false.  ! 反冲
```

### 4. 数值计算参数

#### 网格设置
```fortran
! 从 input2.f 提取
bins = 40             ! 能量分格数
maxlevelstar = 30     ! 最大激发能级数
maxrot = 2            ! 最大转动量子数
```

#### 预平衡参数
```fortran
! 从 input3.f 提取
flagpecomp = .true.   ! 预平衡复合
flagsurface = .true.  ! 表面效应
multipreeq = 40.      ! 多步预平衡开关
```

## 提取方法

### 1. 源代码分析
需要分析的关键文件：
- `source/input1.f` - 基础参数默认值
- `source/input2.f` - 第二组参数默认值  
- `source/input3.f` - 第三组参数默认值
- `source/input4.f` - 第四组参数默认值
- `source/input5.f` - 第五组参数默认值
- `source/input6.f` - 第六组参数默认值

### 2. 自动提取脚本
```python
def extract_defaults_from_source():
    """从TALYS源代码自动提取默认值"""
    
    default_params = {}
    
    # 解析input*.f文件
    for i in range(1, 7):
        filename = f"source/input{i}.f"
        defaults = parse_input_file(filename)
        default_params.update(defaults)
    
    return default_params

def parse_input_file(filename):
    """解析单个input文件中的默认值设置"""
    defaults = {}
    
    with open(filename, 'r') as f:
        content = f.read()
        
    # 查找默认值设置模式
    # 例如: flagspec=.false.
    # 例如: ldmodel=1
    
    return defaults
```

### 3. 验证方法
```python
def verify_defaults():
    """通过运行TALYS验证提取的默认值"""
    
    # 创建最小输入文件
    minimal_input = """
projectile n
element H
mass 1  
energy 1.0
"""
    
    # 运行TALYS并解析输出中的"USER INPUT FILE + DEFAULTS"部分
    # 与提取的默认值进行对比
```

## 参数数据库结构

### 数据库设计
```python
class TalysParameter:
    def __init__(self, name, default_value, param_type, description, 
                 valid_range=None, depends_on=None):
        self.name = name
        self.default_value = default_value
        self.param_type = param_type  # 'bool', 'int', 'float', 'string'
        self.description = description
        self.valid_range = valid_range
        self.depends_on = depends_on  # 依赖的其他参数

# 参数数据库
TALYS_PARAMETERS = {
    'ldmodel': TalysParameter(
        name='ldmodel',
        default_value=1,
        param_type='int',
        description='Level density model',
        valid_range=(1, 6),
        depends_on=None
    ),
    'strength': TalysParameter(
        name='strength', 
        default_value=9,
        param_type='int',
        description='E1 gamma-ray strength function model',
        valid_range=(1, 10),
        depends_on=None
    ),
    # ... 更多参数
}
```

### 参数分组
```python
PARAMETER_GROUPS = {
    'required': ['projectile', 'element', 'mass', 'energy'],
    'level_density': ['ldmodel', 'ldmodelCN', 'ctable', 'ptable'],
    'gamma_strength': ['strength', 'strengthM1', 'gamgam'],
    'optical_model': ['alphaomp', 'deuteronomp', 'localomp'],
    'fission': ['fismodel', 'fymodel', 'fispartdamp'],
    'output_basic': ['flagmain', 'flagbasic', 'flagspec'],
    'output_detailed': ['flagang', 'flagddx', 'flagchannels'],
    'numerical': ['bins', 'maxlevelstar', 'maxrot']
}
```

## 实施计划

### Week 1: 手动提取核心参数
- [ ] 分析input1.f到input6.f
- [ ] 手动提取前50个最重要参数的默认值
- [ ] 创建初始参数数据库

### Week 2: 自动提取脚本
- [ ] 开发源代码解析脚本
- [ ] 自动提取所有参数默认值
- [ ] 验证提取结果的准确性

### Week 3: 参数数据库完善
- [ ] 完善参数描述和分组
- [ ] 添加参数依赖关系
- [ ] 创建参数验证规则

### Week 4: 集成测试
- [ ] 与GUI界面集成
- [ ] 验证默认值的正确性
- [ ] 性能优化

## 质量保证

### 验证方法
1. **源代码对比**: 直接对比源代码中的默认值设置
2. **TALYS输出验证**: 运行TALYS并检查输出的默认值
3. **回归测试**: 确保提取的参数能产生与原TALYS相同的结果

### 文档要求
- 每个参数的来源文件和行号
- 参数的物理意义说明
- 参数之间的依赖关系
- 有效值范围和约束条件
