# Sphinx 文档项目使用指南

本指南将详细介绍如何使用 Sphinx 来创建、编译和发布文档项目，基于当前的 STM32 HAL Docs 项目结构。

## 一、环境准备

### 1. 安装 Python

Sphinx 是基于 Python 的工具，首先需要安装 Python：

- **Windows**：从 [Python 官网](https://www.python.org/downloads/) 下载并安装
- **Ubuntu**：`sudo apt install python3 python3-pip`

### 2. 安装 Sphinx 及相关依赖

```bash
# 安装基础包
pip install sphinx sphinx-rtd-theme myst-parser

# 安装本项目使用的扩展
pip install pydata-sphinx-theme sphinx-design sphinx-copybutton sphinxcontrib-mermaid
```

## 二、项目结构

本项目的目录结构如下：

```
document/
├── source/            # 源码目录
│   ├── _static/       # 静态资源（CSS、图片等）
│   ├── _templates/    # 模板文件
│   ├── conf.py        # 配置文件
│   ├── index.rst      # 首页目录
│   └── *.md           # Markdown 文档
├── build/             # 构建输出目录
├── Makefile           # Linux 构建脚本
└── make.bat           # Windows 构建脚本
```

## 三、核心配置

### 1. conf.py 配置文件

`conf.py` 是 Sphinx 项目的核心配置文件，包含以下关键配置：

- **项目信息**：项目名称、作者、版本等
- **扩展**：启用的 Sphinx 扩展
- **主题**：HTML 输出主题
- **语言**：文档语言设置

### 2. index.rst 目录文件

`index.rst` 是文档的首页，定义了文档的目录结构：

```rst
.. toctree::
   :maxdepth: 2
   :caption: 快速入门:

   getting_started.md

.. toctree::
   :maxdepth: 2
   :caption: BLE Mesh 技术:

   ble_mesh.md
```

## 四、添加新文档

### 1. 创建 Markdown 文件

在 `source` 目录下创建新的 `.md` 文件，例如：

```bash
# 创建新文档
touch source/new_document.md
```

### 2. 添加到目录树

编辑 `source/index.rst`，将新文档添加到相应的分类下：

```rst
.. toctree::
   :maxdepth: 2
   :caption: 新分类:

   new_document.md
```

## 五、编译文档

### 1. Windows 系统

使用 `make.bat` 脚本：

```bash
# 查看帮助
.ake.bat help

# 构建 HTML 文档
.ake.bat html
```

### 2. Linux 系统

使用 `Makefile`：

```bash
# 查看帮助
make help

# 构建 HTML 文档
make html
```

### 3. 直接使用 sphinx-build

```bash
sphinx-build -M html source build
```

## 六、预览文档

### 1. 本地预览

编译完成后，文档会生成在 `build/html` 目录。可以使用任何 HTTP 服务器来预览：

```bash
# 使用 Python 内置服务器
python -m http.server 8080 -d build/html

# 或者使用 Node.js 的 serve
npx serve build/html -p 8080
```

然后在浏览器中访问：`http://localhost:8080`

### 2. 检查编译输出

编译过程中会显示警告和错误信息，例如：

- **警告**：通常是格式问题，不影响生成
- **错误**：会导致编译失败，需要修复

## 七、高级功能

### 1. Markdown 支持

本项目使用 `myst-parser` 扩展支持 Markdown 格式，支持以下功能：

- 标准 Markdown 语法
- 代码块高亮
- 表格
- 数学公式
- Mermaid 图表

### 2. 主题定制

本项目使用 `pydata-sphinx-theme`，可以在 `conf.py` 中定制：

```python
html_theme_options = {
    "navbar_align": "left",
    "show_nav_level": 1,
    "show_prev_next": True,
    "logo": {
        "text": "项目名称",
        "image_light": "_static/logo.jpg",
        "image_dark": "_static/logo.jpg",
    },
}
```

### 3. 扩展功能

- **sphinx-design**：提供提示框、按钮等组件
- **sphinx-copybutton**：为代码块添加复制按钮
- **sphinxcontrib-mermaid**：支持 Mermaid 流程图

## 八、发布文档

### 1. 静态网站部署

编译生成的 `build/html` 目录是纯静态网站，可以部署到任何静态网站托管服务：

- **GitHub Pages**
- **GitLab Pages**
- **Netlify**
- **Vercel**
- **自己的服务器**

### 2. GitHub Pages 部署示例

1. **创建 gh-pages 分支**

```bash
git checkout -b gh-pages
```

2. **构建文档**

```bash
sphinx-build -M html source build
```

3. **复制到根目录**

```bash
cp -r build/html/* .
git add .
git commit -m "Deploy documentation"
git push origin gh-pages
```

4. **配置 GitHub Pages**

在仓库设置中，将 GitHub Pages 源设置为 `gh-pages` 分支。

## 九、常见问题

### 1. 编译失败

- **文件路径错误**：检查 `index.rst` 中的文件路径是否正确
- **语法错误**：检查 Markdown 文件中的语法
- **依赖缺失**：确保所有必需的扩展都已安装

### 2. 预览问题

- **端口被占用**：尝试使用不同的端口
- **缓存问题**：清除浏览器缓存或使用隐私模式

### 3. 图片不显示

- 确保图片路径正确
- 将图片放在 `source/_static` 或 `source/img` 目录
- 使用相对路径引用

## 十、最佳实践

1. **文件命名**：使用小写字母和下划线，避免空格和特殊字符
2. **目录结构**：按主题分类组织文档
3. **内容格式**：保持一致的 Markdown 格式
4. **版本控制**：将源码纳入版本控制，忽略 `build` 目录
5. **定期编译**：确保文档始终可编译通过

## 十一、命令速查

| 命令 | 描述 |
|------|------|
| `sphinx-build -M html source build` | 构建 HTML 文档 |
| `python -m http.server 8080 -d build/html` | 启动本地预览服务器 |
| `pip install -r requirements.txt` | 安装依赖 |
| `make clean` | 清理构建文件 |

## 十二、总结

Sphinx 是一个强大的文档生成工具，通过本指南的步骤，你可以：

- ✅ 创建和组织文档结构
- ✅ 编写 Markdown 格式的内容
- ✅ 编译生成美观的 HTML 文档
- ✅ 本地预览和调试
- ✅ 部署到各种平台

遵循这些最佳实践，可以创建出专业、易维护的文档项目。