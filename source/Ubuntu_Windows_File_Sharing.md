# Ubuntu Samba 服务器配置手册 (针对嵌入式开发优化)

本指南介绍如何在 Ubuntu 上配置 Samba 服务，以解决 VMware 共享文件夹 (HGFS) 不支持软链接、权限错乱等问题。特别适用于 **Luckfox Pico (RV1106)** 等需要跨平台协作的嵌入式 SDK 开发。

---

## 1. 为什么使用 Samba？

在嵌入式开发中，我们通常采用 **"Windows 编辑 + Linux 编译"** 的模式。

* **HGFS (VMware 共享)**：不支持 Linux 软链接（Symlinks），会导致编译 SDK 时报错。
* **Samba**：基于网络协议，完美支持软链接、原生 Linux 权限，且在 Windows 侧映射为磁盘后极其稳定。

---

## 2. 安装 Samba

在 Ubuntu 终端执行：

```bash
sudo apt update
sudo apt install samba samba-common-bin -y

```

---

## 3. 用户与权限配置

Samba 需要独立的密码数据库。

### 3.1 创建 Samba 用户密码

```bash
# 将 yusaka 替换为你的 Ubuntu 用户名
sudo smbpasswd -a yusaka

```

*提示：建议密码设置得与登录密码一致。*

### 3.2 确认目录权限

确保你的 SDK 目录所有者是当前用户：

```bash
sudo chown -R yusaka:yusaka /home/yusaka/Desktop/rv1106/luckfox-pico

```

---

## 4. 修改 Samba 配置文件

编辑配置文件：

```bash
sudo nano /etc/samba/smb.conf

```

### 4.1 开启软链接支持 (重要)

在 `[global]` 字段下（通常在文件开头），找到或添加以下内容，否则 Windows 无法识别 SDK 里的快捷方式：

```ini
[global]
   unix extensions = no

```

### 4.2 添加共享定义

在文件**最末尾**添加如下内容：

```ini
[rv1106_sdk]
   comment = Luckfox Pico SDK
   # 你的 SDK 实际路径
   path = /home/yusaka/Desktop/rv1106/luckfox-pico
   browseable = yes
   read only = no
   guest ok = no
   create mask = 0775
   directory mask = 0775
   valid users = yusaka
   
   # 支持软链接跳转
   follow symlinks = yes
   wide links = yes

```

---

## 5. 重启并验证服务

```bash
# 重启服务
sudo systemctl restart smbd

# 检查服务状态
sudo systemctl status smbd

```

---

## 6. 在 Windows 中访问

1. **获取 IP**：在 Ubuntu 输入 `ifconfig`。
2. **映射驱动器**：
* 打开 Windows “此电脑”。
* 点击上方菜单栏 “映射网络驱动器”。
* 文件夹填写：`\\<Ubuntu_IP>\rv1106_sdk`。
* 输入用户名 `yusaka` 和刚才设置的 Samba 密码。



---

## 7. 常见问题排查 (FAQ)

| 现象 | 解决方法 |
| --- | --- |
| **Windows 无法连接** | 检查防火墙：`sudo ufw allow samba` |
| **无法点击软链接** | 检查 `smb.conf` 中是否配置了 `unix extensions = no` |
| **文件无法写入** | 检查 Linux 目录权限：`chmod -R 775 <路径>` |
| **找不到 IP** | 确保虚拟机网络模式为 **NAT** 或 **桥接(Bridged)** |

---

## 8. 开发建议流程

1. **编译**：在 Ubuntu 终端输入 `./build.sh`。
2. **开发**：在 Windows 侧使用 VS Code 直接打开映射后的 `Z:` 盘目录进行代码编写。
3. **部署**：编译出的镜像文件会直接出现在 Windows 侧，直接使用 Luckfox 烧录工具即可。

---