# TALYS Visualizer GUI 重构计划 - 分栏设计

## 概述
将当前的左右分栏布局（左侧参数面板 + 右侧大可视化区域）改为类似XFresco的标签页分栏设计，提高空间利用率和用户体验。

## 设计原则
- 遵循开发规则中的"分层界面设计"原则
- 基于XFresco的成功设计模式
- 保持所有现有功能完整性
- 提高参数设置的效率和直观性

## 新布局设计

### 1. 标签页结构
```
┌─────────────────────────────────────────────────────────────┐
│ File  Edit  Calculate  View  Help                          │
├─────────────────────────────────────────────────────────────┤
│ [基础参数] [高级参数] [输出选项] [可视化] [专家模式]        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  当前标签页内容区域（充分利用整个窗口空间）                │
│                                                             │
│                                                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ 状态栏: 就绪 | 进度条 | TALYS状态                          │
└─────────────────────────────────────────────────────────────┘
```

### 2. 标签页分类

#### 标签页1: 基础参数 (Basic Parameters)
**对应开发规则中的"基础模式"**
- 目标核设置 (Z, A, 元素符号)
- 入射粒子选择
- 入射能量设置
- 快速计算按钮

#### 标签页2: 高级参数 (Advanced Parameters)  
**对应开发规则中的"高级模式"**
- 物理模型选择 (按模块分组)
  - 能级密度模型
  - 伽马强度函数
  - 光学模型参数
  - 预平衡模型
- 数值计算参数
- 特殊计算模式

#### 标签页3: 输出选项 (Output Options)
- 输出文件控制
- 可视化选项
- 数据导出设置
- 文件管理

#### 标签页4: 可视化 (Visualization)
- 实时图表显示
- 多图表对比
- 交互式数据探索
- 图表导出功能

#### 标签页5: 专家模式 (Expert Mode)
**对应开发规则中的"专家模式"**
- 原始输入文件编辑器
- 高级TALYS选项
- 自定义脚本
- 调试信息

## 实施计划

### Phase 1: 设计新的标签页组件 (1-2天)
1. 创建 `TabbedMainWindow` 类
2. 设计各标签页的布局结构
3. 定义标签页间的数据传递接口

### Phase 2: 重构现有组件 (2-3天)
1. 将 `BasicParameterPanel` 拆分为多个专门的标签页面板
2. 创建 `BasicParametersTab`
3. 创建 `AdvancedParametersTab`
4. 创建 `OutputOptionsTab`

### Phase 3: 集成可视化功能 (1-2天)
1. 创建 `VisualizationTab`
2. 将现有的可视化功能集成到标签页中
3. 实现标签页间的数据同步

### Phase 4: 专家模式实现 (1-2天)
1. 创建 `ExpertModeTab`
2. 实现原始输入文件编辑器
3. 添加高级调试功能

### Phase 5: 测试和优化 (1天)
1. 功能完整性测试
2. 用户体验优化
3. 性能测试

## 技术实现细节

### 1. 主窗口结构
```python
class TabbedMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # 创建中央标签页组件
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # 添加各个标签页
        self.add_basic_tab()
        self.add_advanced_tab()
        self.add_output_tab()
        self.add_visualization_tab()
        self.add_expert_tab()
```

### 2. 标签页基类
```python
class BaseParameterTab(QWidget):
    """标签页基类"""
    parameters_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.connect_signals()
    
    def get_parameters(self) -> dict:
        """获取当前标签页的参数"""
        raise NotImplementedError
    
    def set_parameters(self, params: dict):
        """设置标签页参数"""
        raise NotImplementedError
```

### 3. 参数同步机制
```python
class ParameterSynchronizer(QObject):
    """参数同步器 - 管理各标签页间的参数同步"""
    
    def __init__(self):
        super().__init__()
        self.parameters = {}
        self.tabs = []
    
    def register_tab(self, tab: BaseParameterTab):
        """注册标签页"""
        self.tabs.append(tab)
        tab.parameters_changed.connect(self.on_parameters_changed)
    
    def on_parameters_changed(self, params: dict):
        """处理参数变化"""
        self.parameters.update(params)
        # 通知其他标签页更新
        for tab in self.tabs:
            if tab != self.sender():
                tab.update_from_global_parameters(self.parameters)
```

## 布局优化

### 1. 空间利用
- 每个标签页充分利用整个窗口空间
- 使用网格布局和分组框优化参数排列
- 动态调整组件大小适应窗口变化

### 2. 用户体验
- 标签页图标和工具提示
- 参数验证和实时反馈
- 快捷键支持
- 上下文帮助

### 3. 响应式设计
- 支持不同屏幕分辨率
- 最小窗口尺寸限制
- 组件自适应缩放

## 兼容性保证

### 1. 现有功能保持
- 所有现有的参数设置功能
- TALYS接口调用机制
- 计算结果处理流程

### 2. 数据格式兼容
- 参数字典格式保持不变
- 配置文件格式兼容
- 项目文件向后兼容

## 测试计划

### 1. 功能测试
- 各标签页参数设置功能
- 标签页间参数同步
- TALYS计算流程完整性

### 2. 用户体验测试
- 界面响应速度
- 操作流畅性
- 错误处理友好性

### 3. 兼容性测试
- 不同操作系统
- 不同屏幕分辨率
- 现有项目文件加载

## 文档更新计划

根据开发规则，完成每个阶段后立即更新：

1. **TALYS_Visualizer_Development_Plan.md**
   - 更新Phase 4进度
   - 标记GUI重构任务完成

2. **Phase1_Implementation_Guide.md**
   - 添加新的GUI架构说明
   - 更新代码示例

3. **用户文档**
   - 更新界面使用说明
   - 添加新功能介绍

## 预期效果

### 1. 空间利用率提升
- 消除大片空白的可视化区域
- 参数设置区域扩大3-4倍
- 更好的信息密度

### 2. 用户体验改善
- 更直观的功能分类
- 减少滚动和切换操作
- 更专业的界面外观

### 3. 功能扩展性
- 为未来新功能预留空间
- 模块化设计便于维护
- 符合专业科学软件标准
