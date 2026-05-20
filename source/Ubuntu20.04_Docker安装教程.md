# Ubuntu 20.04 安装 Docker

本文档记录了在 Ubuntu 20.04 (Focal Fossa) 系统上，从解决网络连接失败到成功运行容器的全过程。

## 一、 环境清理

在安装新版本之前，建议清理系统可能存在的旧版本 Docker 组件，避免冲突。

```sh
sudo apt-get remove docker docker-engine docker.io containerd runc
```

## 二、 安装基础依赖

安装必要的软件包，以允许 `apt` 通过 HTTPS 使用存储库：

```sh
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
```

## 三、 配置软件源 (以清华源为例)

由于官方源在海外，国内安装建议使用清华大学（TUNA）镜像站，稳定性最高。

### 1. 添加 GPG 密钥

```sh
curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```

### 2. 写入软件源仓库

```sh
sudo add-apt-repository "deb [arch=amd64] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
```

## 四、 安装 Docker Engine

更新索引并安装 Docker 核心组件及最新的 Compose 插件。

```sh
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

**验证安装结果：**

```sh
docker --version
# 输出应类似：Docker version 28.1.1, build ...
```

## 五、 配置镜像加速器 (Registry Mirror)

安装后，如果直接 `docker pull` 镜像出现 `Timeout` 错误，说明无法连接 Docker Hub，必须配置国内加速器。

### 1. 创建/编辑配置文件

```sh
sudo mkdir -p /etc/docker
sudo nano /etc/docker/daemon.json
```

### 2. 写入以下内容

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://huecker.io",
    "https://dockerhub.timeweb.cloud",
    "https://noohub.net"
  ]
}
```

### 3. 重启服务使配置生效

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 六、 运行验证

使用 `hello-world` 镜像进行最后的跑通测试：

```sh
sudo docker run hello-world
```

**成功标志：** 看到终端输出 `Hello from Docker!`，这表示你的 Docker 已经具备从云端拉取镜像并本地运行的能力。

## 七、 进阶：免 sudo 操作 (可选)

如果你希望以普通用户身份直接运行 `docker` 命令，而不需要每次输入 `sudo`：

```sh
# 1. 将当前用户加入 docker 组
sudo usermod -aG docker $USER

# 2. 更新组信息（或重新连接 SSH 终端）
newgrp docker 

# 3. 测试
docker ps
```

---

### 常见问题排查 (Troubleshooting)

|现象|原因|对策|
|:--|:--|:--|
|`File has unexpected size`|镜像源正在同步中|执行 `sudo apt-get clean` 并换个源或等半小时|
|`Context deadline exceeded`|网络无法访问 Docker Hub|检查 `/etc/docker/daemon.json` 镜像加速配置|
|`Permission denied`|权限不足|使用 `sudo` 或执行本文第七章的免 sudo 配置|
