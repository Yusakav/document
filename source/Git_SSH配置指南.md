# Git 基础配置与 SSH 密钥生成

## Git 基础配置

### 1. 安装 Git

#### Windows 系统
从 [Git 官方网站](https://git-scm.com/download/win) 下载并安装 Git。

#### macOS 系统
使用 Homebrew 安装：
```bash
brew install git
```

#### Linux 系统
```bash
# Debian/Ubuntu
sudo apt update && sudo apt install git

# CentOS/RHEL
sudo yum install git
```

### 2. 配置用户信息

首次使用 Git 时，需要配置用户名和邮箱：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. 查看配置信息

```bash
git config --list
```

### 4. 配置默认编辑器

```bash
# 使用 VS Code 作为默认编辑器
git config --global core.editor "code --wait"

# 使用 Vim 作为默认编辑器
git config --global core.editor "vim"
```

### 5. 配置行尾符

```bash
# Windows 系统
git config --global core.autocrlf true

# macOS/Linux 系统
git config --global core.autocrlf input
```

---

## SSH 密钥生成

### 1. 检查是否已存在 SSH 密钥

```bash
ls -la ~/.ssh/
```

如果存在 `id_rsa` 和 `id_rsa.pub` 文件，说明已经生成过密钥。

### 2. 生成新的 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

**参数说明：**
- `-t ed25519`: 指定密钥类型为 Ed25519（推荐使用）
- `-C`: 添加注释（通常使用邮箱地址）

### 3. 保存密钥

按回车键使用默认路径 `~/.ssh/id_ed25519`，然后设置密码（可选）。

### 4. 启动 SSH 代理

```bash
# 启动 SSH 代理
eval "$(ssh-agent -s)"

# 将私钥添加到代理
ssh-add ~/.ssh/id_ed25519
```

### 5. 查看公钥内容

```bash
cat ~/.ssh/id_ed25519.pub
```

### 6. 将公钥添加到 GitHub

1. 登录 GitHub 账号
2. 进入 Settings → SSH and GPG keys
3. 点击 "New SSH key"
4. 粘贴公钥内容并保存

### 7. 测试连接

```bash
ssh -T git@github.com
```

如果成功，会显示类似以下内容：
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## 配置 SSH 配置文件

创建或编辑 `~/.ssh/config` 文件：

```bash
touch ~/.ssh/config
```

添加以下内容：

```config
# GitHub
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

### 配置多个 SSH 密钥

如果需要管理多个 GitHub 账号，可以添加多个 Host 配置：

```config
# GitHub - 个人账号
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes

# GitHub - 工作账号
Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_work
  IdentitiesOnly yes
```

使用时：
```bash
# 克隆个人仓库
git clone git@github.com:username/repo.git

# 克隆工作仓库
git clone git@github-work:workusername/workrepo.git
```

---

## Troubleshooting

### 权限问题

确保密钥文件权限正确：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### 连接超时

检查网络连接或尝试使用 HTTPS 协议：

```bash
git clone https://github.com/username/repo.git
```

### 代理问题

如果在代理环境下，需要配置 SSH 代理：

```bash
# 在 ~/.ssh/config 中添加
ProxyCommand connect -H proxy.example.com:8080 %h %p
```