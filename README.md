# TALYS Visualizer

一个用于TALYS核反应计算的可视化桌面应用程序。

## 项目状态

🚧 **开发中** - 当前处于 Phase 1: 基础架构开发阶段

## 技术栈

- **GUI框架**: PyQt6
- **绘图库**: Matplotlib, PyQtGraph  
- **数据处理**: NumPy, Pandas
- **编译工具**: Nuitka
- **Python版本**: 3.8+

## 开发环境设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd talys_visualizer
```

### 2. 创建虚拟环境
```bash
python -m venv talys_visualizer_env
source talys_visualizer_env/bin/activate  # Linux/Mac
# 或
talys_visualizer_env\Scripts\activate     # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 运行程序
```bash
python main.py
```

## 项目结构

```
talys_visualizer/
├── main.py                     # 程序入口
├── requirements.txt            # Python依赖
├── config/                     # 配置文件
├── src/                        # 源代码
│   ├── core/                   # 核心逻辑
│   ├── gui/                    # GUI组件
│   ├── visualization/          # 可视化组件
│   └── utils/                  # 工具函数
├── tests/                      # 测试文件
├── build/                      # 构建脚本
├── installer/                  # 安装包制作
├── docs/                       # 文档
└── resources/                  # 资源文件
```

## 开发文档

- [开发计划](TALYS_Visualizer_Development_Plan.md)
- [Phase 1 实施指南](Phase1_Implementation_Guide.md)
- [参数提取计划](TALYS_Default_Parameters.md)
- [构建分发指南](Build_and_Distribution_Guide.md)
- [开发规则](talys-visualizer-development-rules.md)

## 许可证

[待定]

## 贡献

请参阅开发文档了解贡献指南。
