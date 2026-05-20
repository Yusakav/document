# VMware 虚拟机与主机共享文件夹设置指南

在 VMware 虚拟机中，使用共享文件夹是主机与虚拟机之间传递文件最快捷的方法，既不需要复制文件，也能节省硬盘空间。

## 一、 基础设置步骤

1.  **打开设置**：在 VMware 菜单栏选择 `设置` -> `选项` -> `共享文件夹`。
2.  **启用功能**：选择 **“总是启用”**。
3.  **添加文件夹**：
    * 点击“添加”，进入共享文件夹向导，点击“下一步”。
    * 点击“浏览”，选择主机上需要共享的文件夹，点击确定。
4.  **命名与完成**：
    * 设置在虚拟机中显示的“名称”，点击“下一步” -> “完成”。
    * 添加完成后，点击底部的“确定”保存设置。

---

## 二、 核心步骤：手动挂载（解决找不到文件夹问题）

很多时候完成上述设置后，在虚拟机的 `/mnt/hgfs` 目录下依然看不到文件夹。这时需要执行以下挂载命令：

### 1. 临时挂载命令
在虚拟机终端执行：
```bash
sudo mount -t fuse.vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other
```
* **注意**：挂载点通常为 `/mnt/hgfs`。如果提示目录不存在，请先创建：`sudo mkdir /mnt/hgfs`。
* **参数说明**：`-o allow_other` 表示允许普通用户访问共享目录。

### 2. 验证挂载
挂载完成后，需重新进入目录查看：
```bash
cd /mnt/hgfs
ls
```

---

## 三、 进阶配置：开机自动挂载

手动挂载在虚拟机重启后会失效。若要实现开机自动挂载，需编辑 `/etc/fstab` 文件：

1.  使用命令追加配置：
    ```bash
    echo '.host:/ /mnt/hgfs fuse.vmhgfs-fuse allow_other,defaults 0 0' | sudo tee -a /etc/fstab
    ```
2.  **风险提示**：如果配置错误，可能会导致系统进入修复模式（emergency mode）。请确保 `fuse.vmhgfs-fuse` 工具已安装。

---

## 四、 常见问题补充

* **无法拖拽文件**：如果是 Ubuntu 系统，可能与 Wayland 显示协议有关。可以尝试禁用 Wayland：
    * 编辑 `/etc/gdm3/custom.conf`。
    * 取消 `WaylandEnable=false` 的注释。
    * 重启显示管理器：`sudo systemctl restart gdm3`。
* **安装必要工具**：确保虚拟机内安装了 `open-vm-tools` 或 `open-vm-tools-desktop`。
