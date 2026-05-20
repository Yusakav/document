# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- 项目信息 --
project = 'stm32_hal_docs'
copyright = '2026, nyarukov'
author = 'nyarukov'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# -- 通用配置 --
extensions = [
    'myst_parser',          # 开启 Markdown 支持
    'pydata_sphinx_theme',   # 当前选用的 PyData 主题
    'sphinx_design',         # 强烈建议添加：提供更强大的提示框和按钮支持
    'sphinx.ext.autodoc',    # 自动提取代码文档
    'sphinx.ext.napoleon',   # 支持 Google/NumPy 风格注释
    'sphinx.ext.viewcode',   # 在文档中直接查看源码
    'sphinx_copybutton',     # 为代码块添加复制按钮 (需 pip install sphinx-copybutton)
    'sphinx.ext.todo',       # 支持待办事项
    'sphinxcontrib.mermaid', # 用于渲染 Mermaid 流程图
    # 'sphinx_markdown_tables',
]

# 配置 MyST-Parser 以支持高级 Markdown 语法
myst_enable_extensions = [
    "colon_fence",           # 必须：支持 ::: 语法
    "deflist",
    "html_image",
    "substitution",
]

language = 'zh_CN'
templates_path = ['_templates']
exclude_patterns = []

myst_admonition_enable = True 

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# -- HTML 输出配置 --
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = [
    'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap',
    'custom.css',
]


# PyData 主题设置
html_theme_options = {
    
    "header_links_before_dropdown": 5,
    
    "navbar_align": "left",  # 靠左对齐，模仿谷歌云文档
    "navbar_end": ["theme-switcher", "navbar-icon-links"], # 保持简洁的右侧

    "show_nav_level": 1,
    "show_prev_next": True,

    "logo": {
        "text": "Nyarukov",
        "image_light": "_static/logo.jpg",
        "image_dark": "_static/logo.jpg",
    },
    
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/nyarukov",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "STM32 Cube",
            "url": "https://www.st.com",
            "icon": "https://www.st.com/favicon.ico",
            "type": "url",
        },
    ],
#    "announcement": "Here's a <a href='https://pydata.org'>PyData Announcement!</a>",
}

html_sidebars = {
    "**": ["sidebar-nav-bs", "sidebar-ethical-ads"], # 默认所有页面显示导航
    "index": [], # 首页不显示左侧边栏，获得全屏效果
}


