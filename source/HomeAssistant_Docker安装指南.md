# 🐳 使用 Docker 在 Ubuntu 上安装 Home Assistant

如果你已经完成了 Docker 的安装，并配置好了镜像加速器，那么部署 Home Assistant 其实只需要几步即可完成。本教程将从**基础安装 → 推荐方式 → 进阶扩展 → 米家集成**，一步步带你搭建一个可扩展的智能家居平台。

***

# 一、为什么选择 Docker 安装？

使用 Docker 部署 Home Assistant 有几个明显优势：

- ✅ **无需关心 Python 版本**（系统自带 Python 3.8 也没问题）
- ✅ **环境隔离，干净稳定**
- ✅ **方便迁移和备份**
- ✅ **支持快速扩展（ESPHome / MQTT 等）**

***

# 二、快速安装（Docker 命令方式）

## 1. 拉取 Home Assistant 镜像

首先下载官方稳定版镜像：

```bash
sudo docker pull homeassistant/home-assistant:stable
```

如果你看到 `Pulled`，说明镜像已经成功下载。

***

## 2. 创建并运行容器

执行以下命令启动 Home Assistant：

```bash
sudo docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v /home/yusaka/hass_config:/config \
  --network=host \
  homeassistant/home-assistant:stable
```

### 参数详解

- `-d`：后台运行容器
- `--name homeassistant`：容器名称
- `--privileged`：允许访问 USB（Zigbee / 蓝牙设备必需）
- `--restart=unless-stopped`：开机自动启动
- `-e TZ=Asia/Shanghai`：设置时区
- `-v /home/yusaka/hass_config:/config`：配置目录挂载（非常重要）
- `--network=host`：使用宿主机网络（自动发现设备关键）

***

## 3. 访问 Home Assistant

首次启动需要初始化，大约等待 1\~2 分钟。

在浏览器输入：

```
http://你的服务器IP:8123
```

例如：

```
http://192.168.1.100:8123
```

***

# 三、更推荐的方式：Docker Compose

相比 `docker run`，使用 Compose 更易管理、更适合长期使用。

***

## 1. 创建目录

```bash
mkdir -p ~/homeassistant/config
cd ~/homeassistant
```

***

## 2. 创建配置文件

```bash
nano docker-compose.yml
```

写入以下内容：

```yaml
services:
  homeassistant:
    container_name: homeassistant
    image: "homeassistant/home-assistant:stable"
    volumes:
      - ./config:/config
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
    privileged: true
    network_mode: host
```

保存并退出：

```
Ctrl + O → Enter → Ctrl + X
```

***

## 3. 启动服务

```bash
sudo docker compose up -d
```

***

## 4. 检查运行状态

```bash
sudo docker ps
```

如果看到：

```
homeassistant   Up ...
```

说明运行成功。

***

# 四、首次使用与初始化

访问：

```
http://你的IP:8123
```

首次进入你会完成以下配置：

1. 👤 创建管理员账号
2. 🏠 设置家庭名称
3. 📍 配置地理位置（用于日出日落自动化）
4. 🔍 自动扫描智能设备

***

# 五、开发者进阶玩法（强烈推荐）

如果你有嵌入式开发背景（ESP32 / STM32），Home Assistant 会非常强大。

***

## 1. 添加 ESPHome（开发神器）

编辑 `docker-compose.yml`：

```yaml
services:
  homeassistant:
    ...
  esphome:
    container_name: esphome
    image: ghcr.io/esphome/esphome
    volumes:
      - ./esphome-config:/config
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
    privileged: true
    network_mode: host
```

启动：

```bash
sudo docker compose up -d
```

访问：

- Home Assistant → `8123`
- ESPHome → `6052`

👉 你可以直接用 YAML 配置生成 ESP32 固件并无线烧录。

***

## 2. MQTT 集成（适合自定义设备）

建议再部署一个：

- eclipse-mosquitto（MQTT Broker）

用于设备之间通信。

***

# 六、防火墙设置

如果网页打不开，可能是端口被拦截：

```bash
sudo ufw allow 8123/tcp
```

***

# 七、故障排查

## 查看容器日志

```bash
sudo docker logs -f homeassistant
```

***

## 查看 IP 地址

```bash
hostname -I
```

***

## 常见问题

| 问题    | 解决方法        |
| ----- | ----------- |
| 无法访问  | 检查端口 / 防火墙  |
| 容器未启动 | `docker ps` |
| 启动报错  | 查看 logs     |

***

# 八、小米米家（Xiaomi Home）集成

如果你使用小米设备，可以接入官方集成。

***

## 1. 进入配置目录

```bash
cd ~/homeassistant/config
```

***

## 2. 下载插件

```bash
git clone https://github.com/XiaoMi/ha_xiaomi_home.git
```

***

## 3. 安装组件

```bash
cd ha_xiaomi_home
chmod +x install.sh
./install.sh /home/yusaka/homeassistant/config
```

***

## 4. 重启 Home Assistant

```bash
sudo docker restart homeassistant
```

***

## 5. Web 页面添加

进入：

```
Settings → Devices & Services → Add Integration
```

步骤：

1. 搜索 `Xiaomi Home`
2. 登录米家账号
3. 选择设备
4. 完成接入

***

# 九、进阶建议（非常重要）

## 本地控制（低延迟）

- 有小米网关 → 局域网直连（更快）
- 无网关 → 云端控制（略慢）

***

## 调试模式

开启：

- Action Debug 模式
  👉 可直接发送 MIoT 指令（适合开发）

***

<br />

