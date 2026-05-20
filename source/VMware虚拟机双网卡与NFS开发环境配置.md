# VMware 虚拟机双网卡与 NFS 开发环境配置

## 🛠️ 一、VMware 虚拟网络编辑器配置

### 1. 固定 NAT 网段 (用于宿主机连接与虚拟机上网)

1. 打开 VMware Workstation，点击顶部菜单栏的 `编辑` -> `虚拟网络编辑器`。
2. 点击右下角的 **“更改设置”**（获取管理员权限）。
3. 在列表中鼠标单击选中 **VMnet8 (NAT 模式)**。
4. 在下方修改以下参数：

- **子网 IP**：输入 `192.168.50.0`
- **子网掩码**：输入 `255.255.255.0`

1. 点击旁边的 **“NAT 设置”** 按钮：

- 查看并牢记里面的 **“网关 IP”**（默认通常是 `192.168.50.2`）。

1. 点击确定保存。

### 2. 手动绑定物理桥接网卡 (用于对接开发板)

1. 在同一个“虚拟网络编辑器”界面中，鼠标单击选中 **VMnet0 (桥接模式)**。
2. 在下方的“桥接至”下拉菜单中，**绝对不要选择“自动”**！请根据你的物理连线场景选择：

- **场景 A（网线直连板卡）**：明确选择你的**物理有线网卡**（通常带有 `Realtek PCIe`、`Intel Ethernet` 或 `Gigabit` 字样）。
- **场景 B（全部插在同一台路由器上）**：如果你的电脑是用无线网卡连 Wi-Fi，开发板插在路由器的 LAN 口，请明确选中你的**无线网卡**（通常带有 `Wireless`、`Wi-Fi` 或 `802.11` 字样）。

1. 点击右下角的“应用”，再点击“确定”退出。

***

## 第二、虚拟机硬件及 Ubuntu 内部网络配置

### 1. 给虚拟机添加双网卡

1. 确保虚拟机处于**关机**状态。
2. 点击 **“编辑虚拟机设置”**。
3. 检查现有的网卡，确保其网络连接设置为 **NAT 模式**。
4. 点击左下角的 **“添加”** 按钮 -> 选择 **“网络适配器”** -> 点击完成。
5. 选中新出现的“网络适配器 2”，将其网络连接设置为 **桥接模式**。
6. 点击确定保存。

### 2. Ubuntu 内部 Netplan 静态 IP 焊死

1. 开启虚拟机进入 Ubuntu，打开终端。
2. 输入以下命令查看当前系统识别到的真实网卡代号：

```bash
ip link

```

*在打印结果中看到两个以* *`e`* *开头的网卡（例如* *`ens33`* *和* *`ens34`，或者* *`enp0s3`* *等）。**下面以*** ***`ens33`****作为第一张网卡，*** ***`ens34`****作为第二张网卡进行配置。***&#x20;
3\. 打开 Netplan 配置文件（Ubuntu 20.04及以上版本的网络管理器）：

```bash
sudo nano /etc/netplan/01-network-manager-all.yaml

```

1. 将文件内的旧内容清空，完全替换为以下配置（**警告：YAML 格式对空格缩进极其严格，不能使用 Tab 键，请严格使用空格对齐**）：

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    # 网卡 1：NAT 模式，专职负责外网及 Windows 宿主机连接
    ens33:
      dhcp4: no
      addresses:
        - 192.168.50.100/24  # 虚拟机的雷打不动 IP
      routes:
        - to: default
          via: 192.168.50.2  # 第一阶段在 VMware 记录的 NAT 网关
      nameservers:
        addresses: [114.114.114.114, 8.8.8.8]

    # 网卡 2：桥接模式，专职负责与开发板高速通信
    ens40:
      dhcp4: no
      addresses:
        - 192.168.10.100/24  # 桥接专属网段

```

> ⚠️ **关于桥接网段（192.168.10.100）的重要适配原则**：
>
> - **如果你的电脑通过网线直接插在开发板上（无路由器介入）**：直接沿用上文的 `192.168.10.100`。
> - **如果你的电脑和开发板都插在同一个家用路由器上**：请先查看你家路由器的 IP。如果路由器后台是 `192.168.1.1`，则必须将此处的 `192.168.10.100/24` 修改为 `192.168.1.250/24`（注意不要和局域网内的手机或其它设备冲突）。

1. 编写完成后，按 `Ctrl + O` 保存，回车确认，再按 `Ctrl + X` 退出。
2. 让配置即刻生效：

```bash
sudo netplan apply

```

1. 验证外网：输入 `ping baidu.com`，能通说明 NAT 配置成功。

***

## 第三、Windows 通过Samba连接Ubuntu

### 1. SecureCRT / Xshell / Terminal SSH 连接

- **Protocol**: SSH2
- **Hostname / IP**: `192.168.50.100`
- **Port**: `22`
- **Username**: 你的 Ubuntu 用户名

### 2. VS Code 远程完美无缝协同

1. 打开 Windows 端的 VS Code，安装扩展：**Remote - SSH**。
2. 点击左侧小图标“远程资源管理器”，点击 `+` 号添加连接：

```text
ssh Ubuntu用户名@192.168.50.100

```

1. 选择保存配置文件，连接并输入 Ubuntu 密码。未来你的整个工作区直接映射进虚拟机内部。

### 3.  Samba 共享搭建

1. 在 Ubuntu 终端中部署 Samba：

```bash
sudo apt update
sudo apt install samba -y

```

1. 创建独立的共享开发目录：

```bash
mkdir -p ~/workspace
chmod 777 ~/workspace

```

1. 修改 Samba 权限配置文件：

```bash
sudo nano /etc/samba/smb.conf

```

滚动到文件最底部，追加以下内容：

```text
[workspace]
   comment = Embedded Linux Workspace
   path = /home/Ubuntu用户名/workspace
   browseable = yes
   writable = yes
   public = no
   valid users = Ubuntu用户名

```

1. 为 Samba 设置独立的访问密码（出于安全考虑，可以和系统登录密码不同）：

```bash
sudo smbpasswd -a Ubuntu用户名

```

1. 重启 Samba 守护进程：

```bash
sudo systemctl restart smbd

```

<br />

***

## 四、物理网卡与开发板交互

此阶段我们启用第二张桥接网卡（Ubuntu 端 IP：`192.168.10.100`）。以下以最经典的**电脑物理网口用网线直接开发板**为例。

### 1. Windows 物理有线网卡静态配置

因为网线直连时没有路由器分配 IP，必须手动给 Windows 物理有线网卡分配身份：

1. 进入 Windows 的 `控制面板` -> `网络和 Internet` -> `网络连接`。
2. 找到你的 **物理有线网卡**（即插着网线通往开发板的那个网口），右键 `属性`。
3. 双击 `Internet 协议版本 4 (TCP/IPv4)`。
4. 勾选“使用下面的 IP 地址”：

- **IP 地址**：`192.168.10.50`（必须在 10 网段，且不能和虚拟机或板卡冲突）
- **子网掩码**：`255.255.255.0`
- 默认网关和 DNS：**全部留空不填**。

1. 点击确定保存。

### 2. 开发板 U-Boot 与 Linux 环境变量配置

通过串口线（如 SecureCRT / Minicom 串口终端）连上板子，进入控制台。

#### 如果是在 U-Boot 阶段（准备通过 TFTP 下载内核镜像）：

在 U-Boot 命令行下执行以下环境变量配置，将其永久保存：

```bash
setenv ipaddr 192.168.10.20       # 设置板子自己的 IP 身份
setenv serverip 192.168.10.100    # 指向 Ubuntu 的桥接网卡 IP
setenv gatewayip 192.168.10.1     # 临时网关
saveenv                           # 必须执行此命令保存到 Flash

```

*测试网络*：在 U-Boot 命令行下输入 `ping 192.168.10.100`，看到 `host 192.168.10.100 is alive` 即代表硬件链路彻底打通。

#### 如果是在板载 Linux 系统跑起来后：

在板子的 Linux 终端执行：

```bash
ifconfig eth0 192.168.10.20 netmask 255.255.255.0 up

```

***

## 五、嵌入式调试服务搭建 (TFTP & NFS)

### 1. TFTP 固件极速下载服务配置

1. 在 Ubuntu 中安装官方 TFTP 服务器组件：

```bash
sudo apt install tftpd-hpa -y

```

1. 打开并修改其配置文件：

```bash
sudo nano /etc/default/tftpd-hpa

```

将内容精准修改为：

```text
TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/home/Ubuntu用户名/tftpboot"
TFTP_ADDRESS=":69"
TFTP_OPTIONS="--secure"

```

1. 创建对应的物理目录，并彻底放开文件系统权限（防止 U-Boot 抓取时报权限错误）：

```bash
mkdir -p ~/tftpboot
chmod 777 ~/tftpboot

```

1. 重启 TFTP 服务使其生效：

```bash
sudo systemctl restart tftpd-hpa

```

*应用*：编译出来的 `zImage`、`uImage` 或设备树 `.dtb`，直接丢进 Ubuntu 的 `~/tftpboot` 目录。在板子 U-Boot 下直接输入 `tftp 80800000 zImage` 即可秒速下载入板载内存。

### 2. NFS 远程根文件系统挂载服务配置

1. 在 Ubuntu 中部署 NFS 内核服务器：

```bash
sudo apt install nfs-kernel-server -y

```

1. 创建用于存放 Buildroot 或 根文件系统（rootfs）的导出目录：

```bash
mkdir -p ~/nfsroot
chmod 777 ~/nfsroot

```

1. 赋予 NFS 目录远程导出白名单权限：

```bash
sudo nano /etc/exports

```

在文件的最后一行，另起一行追加：

```text
/home/Ubuntu用户名/nfsroot *(rw,sync,no_root_squash,no_subtree_check)

```

1. 强制刷新并重启 NFS 核心服务：

```bash
sudo exportfs -arv
sudo systemctl restart nfs-kernel-server

```

*应用*：本地将根文件系统解压至 `~/nfsroot` 后，板子进入 Linux 终端，直接执行以下命令，即可将 Ubuntu 的目录挂载到板子的 `/mnt` 下，实现不用烧录、直接在 Windows 下改动代码，板子上立刻同步运行：

```bash
mount -t nfs -o nolock,v3 192.168.10.100:/home/Ubuntu用户名/nfsroot /mnt

```

***

<br />

完成以上所有配置，网络拓扑状态如下：

| 设备/软件           | 接入网卡模式         | 达到的最终 IP 状态         | 承载的业务功能                                            |
| --------------- | -------------- | ------------------- | -------------------------------------------------- |
| **Ubuntu 虚拟机**  | **网卡 1 (NAT)** | `192.168.50.100`    | 访问互联网、承载 Windows 的 SSH / VS Code / Samba 访问**。**   |
| **Ubuntu 虚拟机**  | **网卡 2 (桥接)**  | `192.168.10.100`    | 充当 TFTP 服务器、NFS 服务器。                               |
| **Windows 宿主机** | 虚拟网卡 VMnet8    | `192.168.50.1` (自动) | 顺畅高频访问虚拟机的 `192.168.50.100`。                       |
| **Windows 宿主机** | 物理有线网卡         | `192.168.10.50`     | 物理上网线直连板卡，保证物理链路属于 10 网段。                          |
| **嵌入式开发板**      | 物理网口 (直连)      | `192.168.10.20`     | U-Boot / Linux 状态下，精准找 `192.168.10.100` 抓取固件和文件系统。 |

