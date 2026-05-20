# 技术文档中心

基于 **Sphinx** 构建的技术文档项目，支持 Markdown 格式编写，提供完整的文档管理和发布流程。

---

## 📁 项目结构

```
document/
├── source/             # 文档源文件目录
│   ├── _static/        # 静态资源（CSS、图片、图标等）
│   ├── _templates/     # 自定义模板文件
│   ├── img/            # 图片资源目录
│   ├── conf.py         # Sphinx 核心配置文件
│   ├── index.rst       # 文档首页（目录结构入口）
│   └── *.md            # Markdown 格式文档
├── build/              # 构建输出目录（自动生成）
├── Makefile            # Linux/Mac 构建脚本
├── make.bat            # Windows 构建脚本
└── README.md           # 项目说明文档
```

---

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.8+，然后安装依赖：

```bash
# 安装 Sphinx 及核心扩展
pip install sphinx sphinx-rtd-theme myst-parser

# 安装增强扩展（主题、图表、代码复制等）
pip install pydata-sphinx-theme sphinx-design sphinx-copybutton sphinxcontrib-mermaid
```

### 2. 构建文档

```bash
# Windows 系统
.\make.bat html

# Linux / macOS
make html

# 或直接使用 sphinx-build（推荐）
python -m sphinx.cmd.build -b html source build/html
```

### 3. 预览文档

```bash
# 启动本地预览服务器（端口 8080）
python -m http.server 8080 -d build/html

# 访问地址
# http://localhost:8080
```

---

## 🆕 从零创建新项目

### 方式一：使用官方脚手架（推荐）

```bash
# 创建项目目录
mkdir my-docs
cd my-docs

# 初始化 Sphinx 项目（交互式）
sphinx-quickstart

# 或一键初始化（自动回答）
sphinx-quickstart --quiet --project="我的文档" --author="姓名" --release="1.0.0" --language=zh_CN
```

### 方式二：手动创建项目结构

```bash
# 1. 创建目录结构
mkdir -p source/_static source/img source/_templates

# 2. 创建配置文件 conf.py
cat > source/conf.py << 'EOF'
project = '我的文档'
copyright = '2026, 作者名'
author = '作者名'
release = '1.0.0'
language = 'zh_CN'

extensions = [
    'myst_parser',
    'sphinx_copybutton',
]

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
EOF

# 3. 创建首页 index.rst
cat > source/index.rst << 'EOF'
.. 我的文档

欢迎使用文档系统
==========================================

.. toctree::
   :maxdepth: 2
   :caption: 目录:

   document1.md
EOF

# 4. 创建 Makefile
sphinx-build -M html source build

# 5. 创建 .md 文档
echo "# 第一个文档" > source/document1.md
```

### 方式三：从现有项目改造

```bash
# 1. 克隆现有项目
git clone https://github.com/username/docs-project.git
cd docs-project

# 2. 安装依赖
pip install -r requirements.txt

# 3. 直接构建
python -m sphinx.cmd.build -b html source build/html
```

---

## 📝 文档编写指南

### 添加新文档

1. **创建 Markdown 文件**：在 `source/` 目录下新建 `.md` 文件
2. **添加到目录树**：编辑 `source/index.rst`，将文档添加到对应分类

```rst
.. toctree::
   :maxdepth: 2
   :caption: 新分类名称:

   new_document.md
```

### 编写规范

- 使用 **Markdown** 格式编写
- 文件命名使用 **中文**，便于识别
- 图片放入 `source/img/` 目录
- 代码块指定语言标识以启用语法高亮

---

## ⚙️ 核心配置

### conf.py 关键配置

```python
# 项目信息
project = "我的文档"
author = "作者名"
release = "1.0.0"

# 启用扩展
extensions = [
    "myst_parser",           # Markdown 支持（必需）
    "sphinx_copybutton",     # 代码复制按钮
    "sphinxcontrib.mermaid", # Mermaid 图表
]

# 主题设置
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "navbar_align": "left",
    "show_nav_level": 2,
}
```

### index.rst 目录结构

使用 `toctree` 指令组织文档层级：

```rst
.. toctree::
   :maxdepth: 2
   :caption: 快速入门:

   getting_started.md

.. toctree::
   :maxdepth: 2
   :caption: 技术文档:

   ble_mesh.md
```

---

## 🔧 常用命令

| 命令 | 描述 |
|------|------|
| `python -m sphinx.cmd.build -b html source build/html` | 构建 HTML 文档 |
| `python -m http.server 8080 -d build/html` | 启动本地预览 |
| `make clean` | 清理构建文件 |
| `make html` | Linux/Mac 构建命令 |
| `.\make.bat html` | Windows 构建命令 |
| `sphinx-quickstart` | 创建新项目 |
| `sphinx-build -M html source build` | 多格式构建 |

---

## 🌐 部署发布

### 静态网站部署

编译生成的 `build/html` 目录是纯静态网站，可部署至：

- **GitHub Pages**
- **GitLab Pages**
- **Netlify**
- **Vercel**
- 自有服务器

### GitHub Pages 部署示例

```bash
# 创建 gh-pages 分支
git checkout -b gh-pages

# 构建文档
python -m sphinx.cmd.build -b html source build/html

# 复制到根目录
cp -r build/html/* .
git add .
git commit -m "Deploy documentation"
git push origin gh-pages
```

---

## 🛠️ 扩展功能

| 扩展 | 功能 |
|------|------|
| `myst-parser` | Markdown 格式支持 |
| `pydata-sphinx-theme` | 现代化主题 |
| `sphinx-copybutton` | 代码块复制按钮 |
| `sphinxcontrib-mermaid` | Mermaid 图表支持 |
| `sphinx-design` | 提示框、按钮组件 |

---

## ❓ 常见问题

### Q1: 构建失败 - sphinx-build 命令未找到

**解决方案**：使用 Python 模块方式运行

```bash
python -m sphinx.cmd.build -b html source build/html
```

### Q2: 图片不显示

**解决方案**：
- 确保图片路径正确
- 将图片放入 `source/img/` 目录
- 使用相对路径引用

### Q3: 编译警告/错误

- **警告**：通常不影响构建，建议修复以保持代码质量
- **错误**：会导致构建失败，需根据提示修复

---

## ✅ 最佳实践

1. **定期构建**：确保文档始终可编译通过
2. **版本控制**：源码纳入 Git，忽略 `build/` 目录
3. **格式统一**：保持一致的 Markdown 书写风格
4. **结构清晰**：按主题分类组织文档
5. **及时更新**：文档内容与代码同步更新

---

## 📄 许可证

MIT License

---

**文档版本**: 1.0.0
**最后更新**: 2026年5月
