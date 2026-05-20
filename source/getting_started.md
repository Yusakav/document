# STM32H7 软件使用手册

## 1. 工程目录导航

**驱动层 (Drivers) → 中间件层 (Middlewares) → 应用层 (Projects)** 。

### 1.1 Drivers (驱动层)

- **BSP**: 核心层。对底层 HAL 库进行二次封装，提供 `UART`、`DI/DO`、`ADC/DAC`、`SDRAM` 等标准工控接口。

  - `Components`: 外部元器件驱动（如以太网 PHY `dp83848`、触摸屏 `ft5xxx` wifi 模块 `wifi` 等）。
  - `STM32H7XX`: 针对具体开发板的硬件层实现。

- **CMSIS**: ARM 官方提供的 Cortex-M 内核通用软件接口。
- **STM32H7xx_HAL_Driver**: ST 官方硬件抽象层库，提供外设最底层的控制接口。

### 1.2 Middlewares (中间件层)

- **ST/ST_USB_Library**: 负责 USB Host 通信协议。
- **Third_Party/FatFs**: 轻量级文件系统，用于管理 SD 卡、SPI Flash 中的数据文件。
- **Third_Party/LwIP**: 轻量级 TCP/IP 协议栈，支持 HTTP、MQTT、SNTP 等通信协议。

### 1.3 Projects (项目应用层)

- **AMKN86XX**: **不同板卡的 MDK 工程**。

- **config**: **工程配置中心**。

  - `AMKN86xx_Config.h`: 板卡引脚定义与功能开关。
  - `stm32h7xx_hal_conf.h`: HAL 库底层配置。

- **src / inc**: **应用逻辑区**。包含 `main.c` 及各功能应用逻辑（如 `io_app.c`）。
- **startup**: 芯片启动汇编文件。

---

## 2. 驱动层 API 手册

### 2.1 BSP IO 操作说明

#### 2.1.1 指示灯操作

##### 2.1.1.1 功能使能与参数配置

通过宏定义实现对指示灯功能的全局控制。用户可根据硬件资源开启 LED 驱动。

```c
#define LED_EN          1      // LED 总使能: 1-开启驱动, 0-关闭
#if (LED_EN > 0)
#define LED_NUM         1      // 配置 LED 的数量
#define LED_SCAN_T      1000   // 定时任务扫描间隔 (ms)，常用于控制闪烁频率
#endif
```

##### 2.1.1.2 枚举定义与硬件映射

使用枚举类型管理不同的 LED 通道。

**通道枚举：**

```c
typedef enum
{
    LED1 = 0,       // 物理通道 1
    LED_RUN = LED1  // 逻辑功能定义：系统运行指示灯
} Led_TypeDef;
```

**底层引脚定义：**
需配置对应的物理引脚、GPIO 端口及引脚时钟控制宏：

- **`LED1_PIN`**: 物理引脚号（如 `GPIO_PIN_2`）。
- **`LED1_GPIO_PORT`**: 所属端口（如 `GPIOB`）。
- **`LED1_GPIO_CLK_ENABLE()`**: 开启该引脚时钟的 HAL 库宏。

##### 2.1.1.3 通讯 API 接口

| 函数原型                                 | 功能描述                | 参数说明        | 返回值 |
| ---------------------------------------- | ----------------------- | --------------- | ------ |
| **void BSP_LED_Init(void)**              | **初始化 LED 硬件**     | 无              | 无     |
| **void BSP_LED_On(Led_TypeDef Led)**     | **点亮指定的 LED**      | `Led`: 通道枚举 | 无     |
| **void BSP_LED_Off(Led_TypeDef Led)**    | **熄灭指定的 LED**      | `Led`: 通道枚举 | 无     |
| **void BSP_LED_Toggle(Led_TypeDef Led)** | **翻转指定 LED 的状态** | `Led`: 通道枚举 | 无     |

---

#### 2.1.2 蜂鸣器操作

##### 2.1.2.1 功能使能与参数配置

通过宏定义控制蜂鸣器功能的全局控制。用户可根据实际硬件电路需求开启使能。

```c
#define BUZZER_EN          1      // 蜂鸣器总使能: 1-开启驱动, 0-关闭
#if (BUZZER_EN > 0)
#define BUZZER_NUM         1      // 蜂鸣器数量
#define BUZZer_SCAN_T      5000   // 定时任务扫描间隔 (ms)，用于周期性鸣叫或报警逻辑
#endif
```

##### 2.1.2.2 枚举定义与硬件映射

使用枚举类型管理不同的 BUZZER 通道。

**通道枚举：**

```c
typedef enum
{
    BUZZER = 0,             // 物理索引
    BUZZER_ALARM = BUZZER   // 逻辑功能定义：报警蜂鸣器
} Buzzer_TypeDef;
```

**底层引脚定义：**
需配置对应的物理引脚、GPIO 端口以及时钟使能控制宏:

- **`BUZZER_PIN`**: 驱动引脚号（如 `GPIO_PIN_14`）。
- **`BUZZER_GPIO_PORT`**: 所属端口（如 `GPIOB`）。
- **`BUZZER_GPIO_CLK_ENABLE()`**: 开启对应端口时钟。

##### 2.1.2.3 驱动 API 接口

| 函数原型                         | 功能描述             | 参数说明 | 返回值 |
| -------------------------------- | -------------------- | -------- | ------ |
| **void BSP_BUZZER_Init(void)**   | **初始化蜂鸣器硬件** | 无       | 无     |
| **void BSP_BUZZER_On(void)**     | **开启蜂鸣器**       | 无       | 无     |
| **void BSP_BUZZER_Off(void)**    | **关闭蜂鸣器**       | 无       | 无     |
| **void BSP_BUZZER_Toggle(void)** | **翻转状态**         | 无       | 无     |

---

#### 2.1.3 板载开关操作 (SW/拨码开关)

##### 2.1.3.1 功能使能与参数配置

通过宏定义配置开关的数量以及状态轮询的扫描周期。

```c
#define SW_EN            1      // SW 使能: 1-开启驱动, 0-关闭
#if (SW_EN > 0)
#define SW_NUM           9      // 开启的开关数量
#define SW_SCAN_T        1000   // 定时扫描时间间隔 (ms)
#endif
```

##### 2.1.3.2 枚举定义与硬件映射

使用枚举来标识不同的开关通道。每个枚举成员对应硬件原理图上的一个物理位置。

**通道枚举：**

```c
typedef enum
{
    SW1 = 0,
    SW2 = 1,
    // ...
    SW8 = 7
} SW_TypeDef;
```

**底层定义说明：**
需配置对应的物理引脚、GPIO 端口以及时钟使能控制宏。通常拨码开关会配置为上拉输入模式，以确保在开关断开时电平稳定。

- **`SWx_PIN`**: 物理引脚号（如 `GPIO_PIN_0`）。
- **`SWx_GPIO_PORT`**: 引脚所属的端口（如 `GPIOA`）。
- **`SWx_GPIO_CLK_ENABLE()`**: 开启该输入端口对应的外设时钟。

##### 2.1.3.3 驱动 API 接口

| 函数原型                                | 功能描述                 | 参数说明       | 返回值                   |
| --------------------------------------- | ------------------------ | -------------- | ------------------------ |
| **void BSP_SW_Init(void)**              | **初始化开关硬件**       | 无             | 无                       |
| **uint32_t BSP_SW_Read(SW_TypeDef Sw)** | **读取单个开关的状态**   | `Sw`: 通道枚举 | `1`-有效, `0`-无效       |
| **uint32_t BSP_SW_ReadAll(void)**       | **批量读取所有开关状态** | 无             | `uint32_t`: 组合状态掩码 |

---

#### 2.1.4 数字输入操作 (DI)

##### 2.1.4.1 功能使能与参数配置

通过宏定义实现对输入（DI）通道的全局使能控制。

```c
#define DI_EN            1      // DI使能: 1-打开, 0-关闭
#if (DI_EN > 0)
#define DI_NUM           4      // 开启的数字输入通道数量
#define DI_SCAN_T        10     // 定时扫描时间间隔 (ms)
#endif
```

##### 2.1.4.2 枚举定义与硬件映射

通过枚举方式定义 DI 通道。

**通道枚举：**

```c
typedef enum
{
    DI1 = 0,
    DI2 = 1,
    DI3 = 2,
    DI4 = 3,
    ...
} DI_TypeDef;
```

**底层引脚定义：**
需配置对应的物理引脚、GPIO 端口以及时钟使能控制宏:

- **`DIx_PIN`**: 物理引脚号（如 `GPIO_PIN_0`）。
- **`DIx_GPIO_PORT`**: 引脚所属的端口（如 `GPIOA`）。
- **`DIx_GPIO_CLK_ENABLE()`**: 开启该输入端口对应的外设时钟。

##### 2.1.4.3 驱动 API 接口

| 函数原型                                 | 功能描述                 | 参数说明               | 返回值                   |
| ---------------------------------------- | ------------------------ | ---------------------- | ------------------------ |
| **void BSP_DI_Init(void)**               | **初始化 DI 硬件**       | 无                     | 无                       |
| **uint32_t BSP_DI_Read(DI_TypeDef DIx)** | **读取单路数字输入状态** | `DIx`: DI 通道枚举索引 | `1`-高电平, `0`-低电平   |
| **uint32_t BSP_DI_ReadAll(void)**        | **批量读取所有 DI 状态** | 无                     | `uint32_t`: 各通道状态位 |

---

#### 2.1.5 数字输出操作 (DO)

##### 2.1.5.1 功能使能与参数配置

输出模块主要用于控制继电器、隔离 MOS 输出。

```c
#define DO_EN            1      // DO使能: 1-打开, 0-关闭
#if (DO_EN > 0)
#define DO_NUM           4      // 开启的数字输出通道数量
#define DO_SCAN_T        100    // 输出逻辑扫描间隔 (ms)
#endif
```

##### 2.1.5.2 枚举定义与硬件映射

通过枚举方式定义 DO 通道。

**通道枚举：**

```c
typedef enum
{
    DO1 = 0,
    DO2 = 1,
    DO3 = 2,
    DO4 = 3
} DO_TypeDef;
```

**底层引脚定义：**
需配置对应的物理引脚、GPIO 端口以及时钟使能控制宏:

- **`DOx_PIN`**: 驱动引脚号（如 `GPIO_PIN_1`）。
- **`DOx_GPIO_PORT`**: 所属端口（如 `GPIOC`）。
- **`DOx_GPIO_CLK_ENABLE()`**: 开启该输出端口对应的外设时钟。

##### 2.1.5.3 驱动 API 接口

| 函数原型                                           | 功能描述                   | 参数说明                                    | 返回值 |
| -------------------------------------------------- | -------------------------- | ------------------------------------------- | ------ |
| **void BSP_DO_Init(void)**                         | **初始化 DO 硬件引脚**     | 无                                          | 无     |
| **void BSP_DO_Write(DO_TypeDef DOx, uint8_t val)** | **设置单路输出电平状态**   | `DOx`: DO 枚举索引`val`: `1`-有效, `0`-无效 | 无     |
| **void BSP_DO_WriteAll(uint32_t val)**             | **批量设置所有 DO 状态**   | `val`: 按位组合的电平值 (Bit0 对应 DO1)     | 无     |
| **void BSP_DO_Toggle(DO_TypeDef DOx)**             | **翻转指定输出通道的状态** | `DOx`: DO 通道枚举索引                      | 无     |

---

### 2.2 BSP UART 操作说明

#### 2.2.1 功能使能与参数配置

通过宏定义实现对多个 UART 通道的灵活配置。用户可以根据实际硬件资源开启对应的串口，并设置波特率、接收模式以及 RS485 功能 (其他默认配置为 **`数据位:8`,`停止位:1`,`校验位:无**`) 。

```c
#define UART1_EN          1       // UART1使能, 1：打开， 0：关闭
#if (UART1_EN > 0)
#define UART1_RX_EN       1       // 接收使能: 1-打开; 0-关闭 (Modbus主机通讯须设为0)
#define UART1_BAUD        115200  // 设置波特率 (1200 ~ 115200)
#define UART1_RS485_EN    0       // RS485通信使能, 1：打开， 0：关闭
#define UART1_SCAN_T      10      // 设置定时扫描时间间隔, 单位：ms
#endif
```

#### 2.2.2 枚举定义与硬件映射

使用统一的 ID 枚举管理所有串口通道，方便在 API 调用时快速索引目标外设。

**通道枚举：**

```c
typedef enum
{
    UART1_ID = 0,
    UART2_ID,
    // ...
    UART10_ID,
} UART_ID_TypeDef;
```

**底层引脚与缓存定义：**
需配置对应的物理引脚、GPIO 端口、缓冲区大小、时钟使能控制宏:

- **`UARTx_TX/RX_PIN`**: 串行发送/接收引脚号（如 `GPIO_PIN_12`）。
- **`UARTx_TX/RX_GPIO_PORT`**: 引脚所属端口（如 `GPIOA`）。
- **`UARTx_TX/RX_GPIO_CLK_ENABLE()`**: 开启对应端口的时钟宏。
- **`UARTx_TX/RX_AF`**: 复用功能配置（如 `GPIO_AF6_UART4`）。
- **`UARTx_RXBUF_SIZE`**: 定义环形接收缓存长度（如 `256` 字节）。
- **`RS485_DIRx_PIN`**: 若使能 RS485，需定义方向控制引脚（DIR）及其端口。

#### 2.2.3 驱动 API 接口

| 函数原型                                                                                     | 功能描述                         | 参数说明                                  | 返回值                   |
| -------------------------------------------------------------------------------------------- | -------------------------------- | ----------------------------------------- | ------------------------ |
| **uint32_t BSP_UART_Init(UART_ID_TypeDef UART_ID)**                                          | **初始化指定串口硬件**           | `UART_ID`: 串口索引 ID                    | `0`-成功, `1`-失败       |
| **void BSP_UART_ClearRxBuffer(UART_ID_TypeDef UART_ID)**                                     | **清空接收缓存区**               | `UART_ID`: 串口索引 ID                    | 无                       |
| **uint16_t BSP_UART_GetRxLength(UART_ID_TypeDef UART_ID)**                                   | **获取当前接收缓存内的数据长度** | `UART_ID`: 串口索引 ID                    | `uint16_t`: 待读取字节数 |
| **uint32_t BSP_UART_Write(UART_ID_TypeDef UART_ID, uint8_t \*pBuffer, uint16_t BufferSize)** | **发送数据包**                   | `pBuffer`: 数据指针`BufferSize`: 发送长度 | `0`-成功, 其他-错误      |
| **uint32_t BSP_UART_Read(UART_ID_TypeDef UART_ID, uint8_t \*pBuffer, uint16_t BufferSize)**  | **接收数据**                     | `pBuffer`: 存放地址`BufferSize`: 读取长度 | 实际读取的字节数         |

#### 2.2.4 使用说明与注意事项

1. **Modbus 通讯冲突**：当 UART 接口用于 **Modbus 主机** 通讯或 **WIFI 模块** 交互时，必须将 `UARTx_RX_EN` 设置为 `0`。因为此类应用由轮询或专用状态机管理接收逻辑，关闭底层通用接收使能可避免数据丢失。
2. **RS485 方向控制**：若开启了 `UARTx_RS485_EN`，底层驱动会自动控制 `RS485_DIR` 引脚。在发送数据前，引脚切换为发送模式；数据发送彻底完成后，引脚会自动切换回接收模式。
3. **缓冲区配置**：`UARTx_RXBUF_SIZE` 应根据实际通讯频率 and 数据帧长度进行设置。设置过大会浪费 RAM 资源，过小则可能在高负载通讯中发生溢出。
4. **超时处理**：通过 `UARTx_SCAN_T` 定时扫描，配合 `BSP_UART_GetRxLength`，可以实现类似“帧超时”的判断，从而识别一包完整的数据帧。

---

### 2.3 BSP I2C 操作说明

#### 2.3.1 功能使能与参数配置

支持多路硬件 I2C 接口。通过宏定义可以灵活控制每一路总线的开关及其通讯速率。

```c
#define I2C1_EN             1          // 1: 开启 I2C1, 0: 关闭
#if (I2C1_EN > 0)
#define I2C1_SPEED          100000     // 设置时钟速度 (Hz)，标准模式为 100k
#define I2C1_ADDRESS        0x88       // 默认器件地址配置
#endif

#define I2C_TIMEOUT_MAX     3000       // 通讯超时阈值 (ms)，防止总线异常导致程序死锁
```

#### 2.3.2 枚举定义与硬件映射

使用 `I2C_ID_TypeDef` 枚举管理不同的硬件接口。在 BSP 层，每一路 I2C 都定义了严格的引脚复用和时钟配置。

**通道枚举：**

```c
typedef enum
{
    I2C1_ID = 0,    // 通常对应板载 EEPROM 总线
    I2C2_ID,
    I2C3_ID
} I2C_ID_TypeDef;
```

**底层引脚定义：**
配置如下：

- **`I2Cx_SCL/SDA_PIN`**: 物理引脚号（如 `GPIO_PIN_8`）。
- **`I2Cx_SCL/SDA_GPIO_PORT`**: 所属端口（如 `GPIOB`）。
- **`I2Cx_SCL/SDA_GPIO_CLK_ENABLE()`**: 开启对应端口的时钟。
- **`I2Cx_SCL/SDA_AF`**: 配置 I2C 专用的复用功能（如 `GPIO_AF4_I2C1`）。

#### 2.3.3 驱动 API 接口

| 函数原型                                                     | 功能描述             | 参数说明                                                     | 返回值                                                      |
| ------------------------------------------------------------ | -------------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| **void I2C_APPInit(void)**                                   | **全局初始化**       | 初始化所有 I2C 总线。                                        | 无                                                          |
| **HAL_StatusTypeDef BSP_I2C_Init(<br/>I2C_ID_TypeDef I2C_ID)** | **硬件底层初始化**   | `I2C_ID`: 目标 I2C 索引<br/>`I2C1_ID` ~ `I2C3_ID`。          | `HAL_OK`: 设备已就绪`HAL_BUSY`: 总线忙`HAL_TIMEOUT`: 无响应 |
| **HAL_StatusTypeDef BSP_I2C_WriteData(<br/>I2C_ID_TypeDef I2C_ID, uint16_t Addr, uint16_t Reg, uint8_t Value)** | **单字节写入**       | `I2C_ID`: 索引<br/> ID`Addr`: 从机设备地址<br/>`Reg`: 目标寄存器地址<br/>`Value`: 待写入的 8 位数据 | `HAL_OK`: 设备已就绪`HAL_BUSY`: 总线忙`HAL_TIMEOUT`: 无响应 |
| **uint8_t BSP_I2C_ReadData(<br/>I2C_ID_TypeDef I2C_ID, uint16_t Addr, uint16_t Reg)** | **单字节读取**       | `I2C_ID`: 索引<br/> ID`Addr`: 从机设备地址<br/>`Reg`: 目标寄存器地址 | `uint8_t`: 读取到的 8 位数据                                |
| **HAL_StatusTypeDef BSP_I2C_WriteBuffer(<br/>I2C_ID_TypeDef I2C_ID, uint16_t Addr, uint16_t Reg, uint16_t RegSize, uint8_t \*pBuffer, uint16_t Length)** | **连续缓冲区写入**   | `I2C_ID`: 索引 <br/>ID`Addr`: 从机设备地址<br/>`Reg`: 起始寄存器地址<br/>`RegSize`: 寄存器地址宽度（如 `I2C_MEMADD_SIZE_8BIT`）<br/>`*pBuffer`: 发送数据缓冲区首地址<br/>`Length`: 待发送字节数 | `HAL_OK`: 设备已就绪`HAL_BUSY`: 总线忙`HAL_TIMEOUT`: 无响应 |
| **HAL_StatusTypeDef BSP_I2C_ReadBuffer(<br/>I2C_ID_TypeDef I2C_ID, uint16_t Addr, uint16_t Reg, uint16_t RegSize, uint8_t \*pBuffer, uint16_t Length)** | **连续缓冲区读取**   | `I2C_ID`: 索引<br/> ID`Addr`: 从机设备地址<br/>`Reg`: 起机寄存器地址<br/>`RegSize`: 寄存器地址宽度<br/>`*pBuffer`: 接收数据存放缓冲区首地址<br/>`Length`: 待读取字节数 | `HAL_OK`: 设备已就绪`HAL_BUSY`: 总线忙`HAL_TIMEOUT`: 无响应 |
| **HAL_StatusTypeDef BSP_I2C_ReadMultiple(<br/>I2C_ID_TypeDef I2C_ID, uint8_t Addr, uint16_t Reg, uint16_t MemAddress, uint8_t \*Buffer, uint16_t Length)** | **多重寻址高级读取** | `Addr`: 设备地址<br/>`Reg`: 内部偏移<br/>`MemAddress`: 内存起始地址长度<br/>`*Buffer`: 存储指针<br/>`Length`: 长度 | `HAL_OK`: 设备已就绪`HAL_BUSY`: 总线忙`HAL_TIMEOUT`: 无响应 |
| **HAL_StatusTypeDef BSP_I2C_IsDeviceReady(<br/>I2C_ID_TypeDef I2C_ID, uint16_t DevAddress, uint32_t Trials)** | **设备在线检测**     | `I2C_ID`: 索引 <br/>ID`DevAddress`: 待检测的从机地址<br/>`Trials`: 尝试通信的次数（握手次数） | `HAL_OK`: 设备已就绪`HAL_BUSY`: 总线忙`HAL_TIMEOUT`: 无响应 |

#### 2.3.4 使用说明与注意事项

1. **地址格式说明**：API 中的 `Addr` 参数通常采用 **8 位地址格式**。
2. **超时机制**：内置的 `I2C_TIMEOUT_MAX` 能够确保在总线被拉低（如从机死机或物理短路）时，应用层能够跳出等待循环，避免看门狗复位。
3. **上拉电阻**：硬件设计上，SCL 和 SDA 必须外接上拉电阻（通常为 4.7kΩ）。若通讯不稳定，请检查引脚配置中的 `I2Cx_AF` 是否与硬件实际引脚对应。

---

### 2.4 BSP SPI 操作说明

#### 2.4.1 功能使能与参数配置

支持多路串行外设接口（SPI1、SPI2、SPI3）。

```c
#define SPI1_EN             1          // SPI1使能, 1：打开， 0：关闭
#if (SPI1_EN > 0)
#define SPI1_DMA_EN         0          // DMA使能: 1-开启 (需配置流与通道), 0-轮询模式
#define SPI1_TIMEOUT_MAX    1000       // 最大通讯超时阈值 (ms)
#endif

#define SPI_EN              (SPI1_EN|SPI2_EN|SPI3_EN)
#define SPI_NUM             3          // 当前 SPI 实例数量
```

#### 2.4.2 枚举定义与硬件映射

通过 ID 枚举区分物理 SPI 控制器，用户在调用 API 时只需传入对应的枚举值。

**通道枚举：**

```c
typedef enum
{
    SPI1_ID = 0,
    SPI2_ID,
    SPI3_ID,
} SPI_ID_TypeDef;
```

**底层引脚与配置：**
资源定义：

- **`SPIx_SCK_PIN`**: 串行时钟引脚（如 `GPIO_PIN_3`）。
- **`SPIx_MISO_PIN`**: 主机输入/从机输出引脚（Master In Slave Out）。
- **`SPIx_MOSI_PIN`**: 主机输出/从机输入引脚（Master Out Slave In）。
- **`SPIx_SCK/MISO/MOSI_GPIO_PORT`**: 对应的 GPIO 端口（如 `GPIOB`）。
- **`SPIx_SCK/MISO/MOSI_AF`**: 硬件复用功能（如 `GPIO_AF5_SPI1`）。

#### 2.4.3 驱动 API 接口

| 函数原型                                                                                                          | 功能描述           | 参数说明                                                                                       | 返回值                    |
| ----------------------------------------------------------------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------- | ------------------------- |
| **void SPI_APPInit(void)**                                                                                        | **全局初始化**     | 遍历所有使能（`SPIx_EN > 0`）的 SPI 通道并完成初始化。                                         | 无                        |
| **uint32_t BSP_SPI_Init(SPI_ID_TypeDef SPI_ID)**                                                                  | **硬件底层初始化** | `SPI_ID`: 目标 SPI 索引。配置引脚、时钟频率及模式。                                            | `0`: 成功`1`: 失败        |
| **uint32_t BSP_SPI_SetSpeed(SPI_ID_TypeDef SPI_ID, uint8_t val)**                                                 | **动态修改速率**   | `SPI_ID`: 索引 ID`val`: 预分频值（对应 `SPI_BAUDRATEPRESCALER_x`）                             | `0`: 成功                 |
| **uint32_t BSP_SPI_WriteReadData(SPI_ID_TypeDef SPI_ID, uint8_t *DataIn, uint8_t *DataOut, uint16_t DataLength)** | **全双工同步交换** | `SPI_ID`: 索引 ID`*DataIn`: 接收缓冲区指针`*DataOut`: 发送数据指针`DataLength`: 交换的字节总数 | `0`: 成功`其他`: 错误状态 |
| **uint32_t BSP_SPI_WriteData(SPI_ID_TypeDef SPI_ID, uint8_t \*Data, uint16_t DataLength)**                        | **高速单向发送**   | `SPI_ID`: 索引 ID`*Data`: 发送数据首地址`DataLength`: 发送长度                                 | `0`: 成功                 |
| **uint32_t BSP_SPI_ReadData(SPI_ID_TypeDef SPI_ID, uint8_t \*Data, uint16_t DataLength)**                         | **高速单向读取**   | `SPI_ID`: 索引 ID`*Data`: 存放接收数据的地址`DataLength`: 读取长度                             | `0`: 成功                 |

---

### 2.5 BSP QSPI 操作说明

#### 2.5.1 功能使能与参数配置

QSPI 模块主要用于驱动外部 SPI Flash (如 W25Qxx 或 GD25Qxx 系列)。

```c
#define QSPI_EN                1                // QSPI模块使能, 1：打开， 0：关闭
#if (QSPI_EN > 0)
#define QSPI_DIVCLK            QSPI_DIVCLK_4    // 设置分频系数, 决定通讯频率
#define QSPI_IOMODE            QSPI_IOMODE_4_LINES // 设置线数: 1线, 2线, 或 4线(Quad)
#define QSPI_CKMODE            QSPI_CLK_MODE0   // 设置时钟极性, Mode 0 或 Mode 3
#define QSPI_FLASH_SIZE        QSPI_FLASH_SIZE_8MB // 设置外接Flash容量 (2^23 = 8MB)
#endif
```

#### 2.5.2 枚举定义与硬件映射

通过宏定义，确保驱动能匹配不同厂商的 Flash 芯片特性。

**核心模式定义：**

- **`QSPI_DIVCLK_x`**: 通讯频率分频。
- **`QSPI_IOMODE_x`**: 通讯模式。
- **`QSPI_FLASH_SIZE_x`**: 外接 Flash 容量定义采用 字节的幂次格式（如 8MB 对应系数 23）。

**底层引脚与时钟定义：**

- **`QSPI_CLK_PIN`**: 串行同步时钟引脚。
- **`QSPI_BK1_NCS_PIN`**: 第一组 Flash 的片选引脚。
- **`QSPI_BK1_IO0~IO3_PIN`**: 四根双向数据线。
- **`QSPI_CLK_ENABLE()`**: 开启 QSPI 外设内核时钟。

#### 2.5.3 驱动 API 接口

| 函数原型                                                                                      | 功能描述               | 参数说明                                  | 返回值              |
| --------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------- | ------------------- |
| **void QSPI_AppInit(void)**                                                                   | **初始化 QSPI 硬件**   | 无                                        | 无                  |
| **int QSPI_SendCommand(QSPI_CommandTypeDef \*cmd, int timeout)**                              | **发送指令**           | `cmd`: 指令结构体指针`timeout`: 超时时间  | `0`-成功, 其他-错误 |
| **int QSPI_WriteBlocking(uint8_t \*data, int timeout)**                                       | **以阻塞方式发送数据** | `data`: 待发送数据指针`timeout`: 超时时间 | `0`-成功, 其他-错误 |
| **int QSPI_ReadBlocking(uint8_t \*data, int timeout)**                                        | **以阻塞方式读取数据** | `data`: 存放数据指针`timeout`: 超时时间   | `0`-成功, 其他-错误 |
| **int QSPI_AutoPolling(QSPI_CommandTypeDef *cmd, QSPI_AutoPollingTypeDef *cfg, int timeout)** | **自动轮询**           | `cmd`: 指令指针`cfg`: 掩码配置            | `0`-成功, 其他-错误 |

---

### 2.6 BSP CAN 通讯操作说明

#### 2.6.1 功能使能与参数配置

支持多路 FDCAN 控制器配置。

```c
#define CAN1_EN             1          // CAN1使能, 1：打开， 0：关闭
#if (CAN1_EN > 0)
#define CAN1_BAUD           1000000    // CAN1波特率 (支持最高 1Mbps)
#define CAN1_SCAN_T         10         // 定时接收扫描间隔 (ms)
#define CAN1_TX_T           1000       // 发送数据时间间隔 (ms)
#endif

#define CAN_EN              (CAN1_EN|CAN2_EN)
#define CAN_NUM             2          // 系统开启的 CAN 控制器总数量
```

#### 2.6.2 枚举与数据结构定义

定义统一的 ID 枚举和消息结构体，涵盖了 FDCAN 的头部信息与 8 字节数据载荷。

**通道枚举：**

```c
typedef enum
{
    CAN1_ID = 0,
    CAN2_ID,
} CAN_ID_TypeDef;
```

**报文结构体：**

```c
typedef struct {
    FDCAN_TxHeaderTypeDef TxHeader;    // 发送报文头 (含 ID、长度、帧类型等)
    uint8_t               Data[8];     // 数据载荷
} CAN_TX_MSG;

typedef struct {
    FDCAN_RxHeaderTypeDef RxHeader;    // 接收报文头
    uint8_t               Data[8];     // 接收到的数据
} CAN_RX_MSG;
```

#### 2.6.3 硬件引脚映射

每一路 CAN 通道在 BSP 层均定义了具体的物理引脚和复用功能：

- **`CANx_TX/RX_PIN`**: 物理引脚号（如 `GPIO_PIN_13`）。
- **`CANx_TX/RX_GPIO_PORT`**: 引脚所属端口（如 `GPIOH`）。
- **`CANx_TX/RX_GPIO_CLK_ENABLE()`**: 开启对应端口的外设时钟。
- **`CANx_TX/RX_AF`**: FDCAN 专用复用功能（如 `GPIO_AF9_FDCAN1`）。

#### 2.6.4 驱动 API 接口

| 函数原型                                                                            | 功能描述            | 参数说明                                                         | 返回值                       |
| ----------------------------------------------------------------------------------- | ------------------- | ---------------------------------------------------------------- | ---------------------------- |
| **uint8_t BSP_CAN_Init(CAN_ID_TypeDef CAN_ID)**                                     | **初始化 CAN 硬件** | `CAN_ID`: CAN 通道索引 ID                                        | `0`: 成功, `1`: 失败         |
| **uint32_t BSP_CAN_Write(CAN_ID_TypeDef CAN_ID, CAN_TX_MSG \*pTxMsg, uint8_t num)** | **发送 CAN 报文**   | `CAN_ID`: 索引 ID`pTxMsg`: 发送结构体指针`num`: 待发送的消息数量 | 实际发送的消息个数           |
| **uint32_t BSP_CAN_GetRxMsgNum(CAN_ID_TypeDef CAN_ID)**                             | **获取缓存消息数**  | `CAN_ID`: 索引 ID                                                | 接收 FIFO 中待读取的消息数量 |
| **uint32_t BSP_CAN_Read(CAN_ID_TypeDef CAN_ID, CAN_RX_MSG \*pRxMsg, uint16_t num)** | **读取接收报文**    | `CAN_ID`: 索引 ID`pRxMsg`: 存储指针`num`: 准备读取的数量         | 实际成功读取的消息个数       |

---

### 2.7 BSP ADC 操作说明

#### 2.7.1 BSP ADC 操作说明

框架集成了多通道 ADC 采集功能，根据硬件支持对电压、电流等模拟信号的量化处理。用户可通过宏定义配置采样精度、平均值计算次数以及硬件采样模式。

```c
#define ADC_EN           1      // ADC总使能
#if (ADC_EN > 0)
#define AI_NUM           8      // 实际使用的模拟输入通道数
#define AI_SCAN_T        1000   // 采集扫描周期 (ms)
#define ADC_AVGNUM       4      // 采样平均值次数 (1~64)，用于平滑滤波
#define ADC_SAMPLE_TIME  ADC_SAMPLETIME_1CYCLE_5  // 采样保持时间配置
#endif
```

#### 2.7.2 量程与模式定义

系统支持对每一路通道独立设置物理量程转换逻辑，并将原始采样值（0~4095）映射为实际物理单位。

- **输入模式**：
- `ADC_MODE_SINGLE` (0)：单端输入，参考地为 GND。
- `ADC_MODE_DIFFERENTIAL` (1)：差分输入，提高抗干扰能力。

- **量程配置 (`AIx_RANGE`)**：
- `0`: `0~4095` 原始采样值。
- `1`: `0~+10V` 电压量程。
- `2`: `-10V~+10V` 电压量程。
- `3`: `0~5V` 电压量程。
- `4`: `-5V~+5V` 电压量程。
- `5`: `0~+20mA` 电流量程。
- `6`: `-20mA~+20mA` 电流量程。

#### 2.7.3 枚举定义与硬件映射

**通道枚举：**

```c
typedef enum
{
    AI1_ID = 0,
    AI2_ID,
    // ...
} AIx_TypeDef;
```

**底层引脚与资源定义：**
每一路 AI 通道映射到特定的 ADC 硬件通道，并可能涉及特定的模拟开关配置：

- **`AIx_PIN/PORT`**: 对应的模拟输入引脚及端口（如 `PC2`）。
- **`AIx_CHANNEL`**: 映射的硬件 ADC 通道（如 `ADC_CHANNEL_12`）。
- **`AIx_ANALOG_SWITCH()**: 针对特定引脚（如 `PA0_C`, `PA1_C`）需要调用的模拟开关使能宏，以连接内部 ADC 模块。

#### 2.7.4 驱动 API 接口

| 函数原型                                                | 功能描述            | 参数说明                                           | 返回值         |
| ------------------------------------------------------- | ------------------- | -------------------------------------------------- | -------------- |
| **uint32_t BSP_ADC_Init(void)**                         | **初始化 ADC 硬件** | 初始化引脚、时钟、DMA 及转换参数。                 | `0`: 成功      |
| **uint32_t BSP_ADC_DMA_Start(void)**                    | **启动自动采集**    | 开启 DMA 模式下的连续扫描采样。                    | `0`: 成功      |
| **uint32_t BSP_ADC_DMA_Abort(void)**                    | **停止采集**        | 强行终止当前的 DMA 传输与转换。                    | `0`: 成功      |
| **uint32_t BSP_ADC_Read(uint16_t \*pBuf, uint8_t len)** | **获取转换数据**    | `*pBuf`: 存储数据的缓冲区`len`: 准备读取的通道长度 | 成功读取的状态 |

#### 2.7.5 使用说明与注意事项

1. **模拟开关配置**：对于带有 \_C 后缀的引脚（如 PA0_C），必须定义 AIX_ANALOG_SWITCH() 开启硬件模拟路径。
2. **采样稳定性**：若信号波动较大，建议增大 ADC_AVGNUM 进行软件滤波。
3. **量程转换逻辑**：`BSP_ADC_Read` 获取的是经过平均处理后的 **原始 12 位数值**。应用层需根据 `AIx_RANGE` 的定义，应用层需自行根据公式进行工程单位换算。

---

### 2.8 BSP DAC 操作说明

#### 2.8.1 功能使能与参数配置

支持双通道数模转换（DAC）功能。

```c
#define DAC1_EN            1        // DAC1使能: 1-开启, 0-关闭
#if (DAC1_EN > 0)
#define DAC1_MODE          0        // 输出模式: 0-手动输出; 1-连续N次停止; 2-循环持续输出
#define DAC1_FREQ          1000     // 自动输出频率 (Hz)
#define DAC1_SCAN_T        1000     // 定时任务扫描间隔 (ms)
#define DAC1_TXBUF_SIZE    256      // 发送缓存长度 (仅在模式 1 或 2 时生效)
#endif
```

#### 2.8.2 枚举定义与硬件映射

**通道枚举：**

```c
typedef enum
{
    AO1_ID = 0,
    AO2_ID
} DACx_TypeDef;
```

**底层引脚与资源定义：**
DAC 通道直接映射至特定的 GPIO 引脚及硬件控制器：

- **`AOx_PIN/PORT`**: 模拟输出物理引脚（如 `PA4`, `PA5`）。
- **`AOx_CHANNEL`**: 硬件 DAC 内部通道（Channel 1 或 Channel 2）。
- **时钟控制**: 通过 ` DAC_CLK_ENABLE()`` 和  `AO_GPIO_CLK_ENABLE()`` 管理时钟。

#### 2.8.3 驱动 API 接口

| 函数原型                                                                        | 功能描述              | 参数说明                                                                                                                                                                               | 返回值    |
| ------------------------------------------------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| **uint32_t BSP_DAC_Init(uint8_t id)**                                           | **初始化 DAC 硬件**   | `id`: `DAC1_ID` 或 `DAC2_ID`                                                                                                                                                           | `0`: 成功 |
| **uint32_t BSP_DAC_SetValue(uint8_t id, uint32_t Value)**                       | **手动设置输出值**    | `Value`: 0~4095 (12 位对应 0~Vref)                                                                                                                                                     | `0`: 成功 |
| **uint32_t BSP_DAC_SetWave(uint8_t id, uint32_t \*pData, uint32_t Length)**     | **配置输出波形数据**  | `*pData`: 波形数据指针`Length`: 数据点数                                                                                                                                               | `0`: 成功 |
| **uint32_t BSP_DAC_DMA_Config(uint8_t id, uint32_t \*Buffer, uint16_t Length)** | **配置 DMA 传输参数** | `*Buffer`: 数据源地址`Length`: 缓冲区长度                                                                                                                                              | `0`: 成功 |
| **uint32_t BSP_DAC_Start(uint8_t id)**                                          | **启动 DAC 转换输出** | `id`: 目标 DAC 通道 ID                                                                                                                                                                 | `0`: 成功 |
| **uint32_t BSP_DAC_Ctrl(uint8_t id, DAC_CMD_TYPE Cmd, uint32_t Parg)**          | **高级功能控制**      | `Cmd`: <br /> `CMD_DAC_ENA / DIS`: 动态使能或关闭 DAC 通道。<br> `CMD_DAC_FREQ`: 修改输出频率。<br> `CMD_DAC_RESET`: 重置 DAC 模块状态。<br> `Parg`: <br /> `CMD_DAC_FREQ`模式下的频率 | `0`: 成功 |

---

### 2.9 BSP TIM 定时器操作说明

#### 2.9.1 功能使能与参数配置

支持多个硬件定时器的配置。定时器通常用于精确的时间基准生成、周期性任务触发或外部事件计数。**注意：** 定时器资源在硬件上与 PWM 输出和 FCLK 功能共用，使能前需确保无功能冲突。

```c
#define TIM1_EN        1         // TIM1使能: 1-打开, 0-关闭
#if (TIM1_EN > 0)
#define TIM1_MODE      0         // 工作模式: 0-TIM_WKMODE_INT (定时中断);
                                 //           1-TIM_WKMODE_COUNT (外部/内部定时计数)
#define TIM1_T         1000000   // 定时周期, 单位: us (此处为 1s)
#define TIM1_PSC       1         // 计数分频系数 (仅在 TIM_WKMODE_COUNT 模式下手动设置)
#endif
```

#### 2.9.2 中断逻辑

驱动层提供了统一的中断回调机制。当定时器溢出或匹配时，会自动触发中断服务程序（ISR）：

- **中断处理 (`TIMx_UP_IRQHandler`)**: 自动清除中断标志位，并根据模式执行不同逻辑。
- **定时中断模式**: 调用 `TIM_ISRHook` 函数，用户可在此处理业务逻辑（如设置 `UserVars.TimIntFlag`）。
- **定时计数模式**: 系统自动累加 `TimConnt[TIMx_ID]` 变量，记录事件发生的总次数。

#### 2.9.3 驱动 API 接口

| 函数原型                                                           | 功能描述             | 参数说明                                              | 返回值                        |
| ------------------------------------------------------------------ | -------------------- | ----------------------------------------------------- | ----------------------------- |
| **uint32_t BSP_TIM_Init(uint8_t id, uint8_t mode, uint32_t para)** | **初始化定时器硬件** | `id`: 定时器 ID。`mode`: 工作模式 。`para`: 预设参数  | `0`: 成功                     |
| **uint32_t BSP_TIM_Start(uint8_t id, uint32_t para)**              | **开启定时器**       | `id`: 定时器 ID 。`para`: 初始计数值或配置项          | `0`: 成功                     |
| **uint32_t BSP_TIM_Stop(uint8_t id, uint32_t para)**               | **停止定时器**       | `id`: 定时器 ID                                       | `0`: 成功                     |
| **uint32_t BSP_TIM_ReadCount(uint8_t id)**                         | **读取当前计数值**   | `id`: 定时器 ID                                       | `uint32_t`: 当前 CNT 寄存器值 |

#### 2.9.4 使用说明与注意事项

1. **时间单位**：`TIMx_T` 宏默认以微秒（**us**）为单位。驱动内部会根据外设总线时钟自动计算 `Prescaler` 和 `Period` 值。
2. **中断安全**：由于 `TIM_ISRHook` 是在中断上下文中运行的，**严禁**在该函数内调用 `Delay`、串行打印（printf）或其他耗时较长的阻塞操作，否则会导致系统死机或实时性崩溃。
3. **资源冲突排查**：

- 如果使能了 `PWM` 输出，请对照引脚定义表确认是否占用了相同的 `TIM` 编号。
- 高级定时器（如 TIM1, TIM8）通常具有死区控制等功能，配置时需额外注意安全属性。

---

### 2.10 BSP PWM 输出操作说明

#### 2.10.1 功能描述与应用

支持多路 PWM 输出通道，用于**步进电机控制**（脉冲+方向+使能模式）。每路 PWM 配有独立的“方向 (DIR)”和“使能 (ENA)”控制引脚。

#### 2.10.2 配置参数详述

用户可以通过以下宏定义灵活调整 PWM 的初始状态：

```c
#define PWM1_EN        1        // PWM1总使能
#if (PWM1_EN > 0)
#define PWM1_FREQ      1000     // 初始频率: 1000Hz
#define PWM1_RATE      500      // 初始占空比: 50.0%
#define PWM1CH1_EN     1        // 通道1使能
#endif

#define PWM_SCAN_T     3000     // 定时扫描/更新任务间隔 (ms)
```

#### 2.10.3 驱动 API 接口

| 函数原型                                                                                   | 功能描述               | 参数说明                                                          | 返回值    |
| ------------------------------------------------------------------------------------------ | ---------------------- | ----------------------------------------------------------------- | --------- |
| **uint32_t BSP_PWM_Init(uint8_t pwm_id, uint32_t PWM_Freq, uint16_t PWM_Rate)**            | **初始化 PWM 硬件**    | `id`: `PWMx_ID` 。`Freq`: 频率 。`Rate`: 占空比                   | `0`: 成功 |
| **uint32_t BSP_PWM_ConfigFreq(uint8_t pwm_id, uint32_t PWM_Freq)**                         | **动态修改频率**       | `id`: `PWMx_ID` 。`Freq`: 目标频率                                | `0`: 成功 |
| **uint32_t BSP_PWM_ConfigDutyCycle(uint8_t pwm_id, uint8_t Channel, uint32_t Duty_Cycle)** | **修改指定通道占空比** | `pwm_id`: `PWMx_ID` 。`Channel`: `PWM_CHx` 。`Duty_Cycle`: 0~1000 | `0`: 成功 |
| **void BSP_PWM_Start(uint8_t pwm_id, uint8_t pwm_ch)**                                     | **开启脉冲输出**       | `id`: `PWMx_ID` 。`ch`: 物理通道索引                              | 无        |
| **void BSP_PWM_Stop(uint8_t pwm_id, uint8_t pwm_ch)**                                      | **停止脉冲输出**       | `id`: `PWMx_ID` 。`ch`: 物理通道索引                              | 无        |

#### 2.10.4 使用说明与注意事项

1. **电机控制逻辑**：

- **PUL (PWM)**: 负责控制电机的速度（频率越高，转速越快）。
- **DIR (方向)**: 调用 `BSP_GPIO_Write` 操作对应的 `PWMx_DIR_PIN` 以控制正反转。
- **ENA (使能)**: 逻辑高电平或低电平（视驱动器而定）使电机进入脱机或锁死状态。

2. **定时器冲突**：

- PWM1 使用了 **TIM1**（高级定时器），PWM4 使用了 **TIM17**。
- 在使用这些通道时，必须确保 `3.1.8` 章节中的通用定时器宏（如 `TIM1_EN`）处于关闭状态，否则会导致硬件初始化冲突。

3. **动态调速**：在电机运行过程中，可以直接调用 `BSP_PWM_ConfigFreq` 实现平滑调速。建议配合加速度算法（斜坡升降速）使用，以防止步进电机丢步。

---

### 2.11 BSP FCLK 捕获操作说明

#### 2.11.1 功能概述

支持多路 FCLK 脉冲输入接口。

#### 2.11.2 工作模式定义

通过 `FCLKx_MODE` 宏，用户可以将 FCLK 配置为四种不同的物理模式：

| 模式宏定义                  | 功能说明           | 输入通道要求                      |
| --------------------------- | ------------------ | --------------------------------- |
| **`FCLK_MODE_COUNT`** (0)   | **脉冲计数**       | 仅 CH1 输入有效                   |
| **`FCLK_MODE_DECODE`** (1)  | **正交编码器接口** | CH1 接 A 相，CH2 接 B 相          |
| **`FCLK_MODE_FREQ`** (2)    | **多路测频模式**   | CH1 ~ CH4 四路独立输入            |
| **`FCLK_MODE_PWMRATE`** (3) | **PWM 占空比测量** | 仅 CH1 输入有效（捕获周期与脉宽） |

#### 2.11.3 驱动 API 接口

| 函数原型                                                                                                        | 功能描述              | 参数说明                                                                                              | 返回值                         |
| --------------------------------------------------------------------------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------ |
| **uint32_t BSP_FCLK_Init(uint8_t id, uint8_t mode, uint8_t ch)**                                                | **初始化 FCLK 硬件**  | `id`: 控制器 ID (FCLK0/FCLK1)`mode`: 模式 (0:频率, 1:PWM, 2:计数, 3:编码器)`ch`: 硬件通道号 (CH1/CH2) | `0`: 成功`1`: 参数错误         |
| **uint32_t BSP_FCLK_Start(uint8_t id, uint8_t mode, uint8_t ch)**                                               | **开启捕获/计数任务** | `id`: 控制器 ID`mode`: 工作模式`ch`: 指定通道                                                         | `0`: 开启成功`1`: 开启失败     |
| **uint32_t BSP_FCLK_ReadFreq(uint8_t FCLK_ID, uint8_t ch, uint32_t \*pbuf, uint16_t Length, uint32_t Timeout)** | **读取输入频率**      | `FCLK_ID`: 控制器 ID`ch`: 采样通道`pbuf`: 结果存储指针`Length`: 读取数量`Timeout`: 超时时间           | **实际频率值 (Hz)**            |
| **uint32_t BSP_FCLK_ReadPWMRate(uint8_t id, uint32_t \*pbuf, uint16_t len, uint32_t Timeout)**                  | **读取 PWM 占空比**   | `id`: 控制器 ID`pbuf`: 结果存储指针`len`: 读取长度`Timeout`: 超时时间                                 | `0`: 读取成功`非0`: 超时或错误 |
| **uint32_t BSP_FCLK_ReadCount(uint8_t id)**                                                                     | **读取累计脉冲数**    | `id`: 指定定时器/计数器 ID                                                                            | **32 位无符号脉冲计数值**      |
| **int16_t BSP_FCLK_ReadEncoder(uint8_t id)**                                                                    | **读取编码器计数值**  | `id`: 正交编码器定时器 ID                                                                             | **16 位有符号增量值**          |

---

### 2.12 BSP SD 卡存储操作说明

#### 2.12.1 功能使能与参数配置

通过宏定义实现对 SDMMC 接口的配置。用户可以开启 SD 卡支持，并选择工作模式（SD 卡或 NAND Flash）以及设置相关的维护功能。

```c
#define SDCARD_EN                1       // SD卡使能：1, 使能;  0, 关闭;
#if (SDCARD_EN > 0)
#define SD_SCAN_T                10      // 设置定时扫描时间间隔, 单位：ms
#define SD_MODE_SDCARD           0       // SD卡工作模式定义
#define SD_MODE_NAND_FLASH       1       // NAND_FLASH工作模式定义

#define SD_MODE      SD_MODE_NAND_FLASH  // 选择当前工作模式
#endif
```

#### 2.12.2 状态与硬件映射

**底层引脚定义：**
SDMMC 接口通常使用 4 位数据线模式，需定义数据线、时钟线及命令线的详细物理映射：

- **`SDMMC1_Dx_PIN/PORT`**: 数据线 D0~D3 引脚及端口配置。
- **`SDMMC1_CK/CMD_PIN`**: 时钟线与命令线引脚配置。
- **`SDMMC1_CLK_ENABLE()`**: 开启 SDMMC1 外设时钟宏。
- **`SDMMC1_GPIO_AF`**: GPIO 复用功能设置（如 `GPIO_AF12_SDIO1`）。
- **电源/检测引脚 (可选)**: 包含 `SD_DETECT`（插入检测）、`SD_PWR`（电源控制）、`SD_WP`（保护）。

#### 2.12.3 驱动 API 接口

| 函数原型                                                                                                    | 功能描述                 | 参数说明                                                                                                                                                                                                         | 返回值                   |
| ----------------------------------------------------------------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| **HAL_StatusTypeDef BSP_SD_Init(void)**                                                                     | 初始化 SD 卡硬件         | 无                                                                                                                                                                                                               | `HAL_OK`-成功, 其他-失败 |
| **uint8_t BSP_SD_ReadBlocks(uint8_t \*pData, uint32_t ReadAddr, uint32_t NumOfBlocks, uint32_t Timeout)**   | 从指定地址读取块数据     | `pData`: 数据缓冲区`ReadAddr`: 块地址`NumOfBlocks`: 块数                                                                                                                                                         | `MSD_OK`-成功, 其他-错误 |
| **uint8_t BSP_SD_WriteBlocks(uint8_t \*pData, uint32_t WriteAddr, uint32_t NumOfBlocks, uint32_t Timeout)** | 向指定地址写入块数据     | `pData`: 源数据指针`WriteAddr`: 块地址`NumOfBlocks`: 块数                                                                                                                                                        | `MSD_OK`-成功, 其他-错误 |
| **uint8_t BSP_SD_Erase(uint32_t StartAddr, uint32_t EndAddr)**                                              | 擦除指定范围的扇区       | `StartAddr`: 起始地址`EndAddr`: 结束地址                                                                                                                                                                         | `MSD_OK`-成功, 其他-错误 |
| **uint8_t BSP_SD_GetCardInfo(HAL_SD_CardInfoTypeDef \*CardInfo)**                                           | 获取卡容量、块大小等信息 | `CardInfo`: 信息结构体指针                                                                                                                                                                                       | `MSD_OK`-成功, 其他-错误 |
| **uint32_t BSP_SD_Ctrl(uint8_t Cmd, uint32_t Para)**                                                        | 磁盘控制与状态查询接口   | `Cmd`: 控制指令 ID`Para`: <br>`CMD_SD_SYNC`检测 SD 是否插入<br>`CMD_SD_STATUS`读取 SD 卡状态<br>`CMD_SD_SECTOR_COUNT`读取 SD 卡扇区数量<br>`CMD_SD_SECTOR_SIZE`读取 SD 卡扇区大小<br>`CMD_SD_TYPE`读取 SD 卡类型 | 根据指令返回对应数值     |

---

### 2.13 BSP USBH 操作说明

#### 2.13.1 功能使能与参数配置

通过宏定义实现对 USB Host (主机) 功能的使能控制。USBH 模块基于 ST 的 HAL 库实现，主要用于连接 U 盘或其他 USB 从设备，并提供基础的供电与物理层连接配置。

```c
#define USBH_EN          1       // USBH主机使能, 1：打开， 0：关闭
#if (USBH_EN > 0)
// USB主机引脚相关配置
#endif
```

#### 2.13.2 枚举定义与硬件映射

**底层引脚与时钟定义：**

- **`USB_VBUS_PIN`**: VBUS 供电检测/触发引脚号（如 `GPIO_PIN_13`）。
- **`USB_PWR_PIN`**: USB 接口外部电源开关控制引脚（如 `GPIO_PIN_12`）。
- **`USB_DM_PIN` / `USB_DP_PIN**`: USB 差分信号负 (Data Minus) / 正 (Data Plus) 引脚。
- **`USB_x_GPIO_PORT`**: 引脚所属端口（如 `GPIOB`）。
- **`USB_x_GPIO_CLK_ENABLE()`**: 开启对应端口的时钟宏。
- **`USB_AF`**: USB OTG 外设的复用功能配置（如 `GPIO_AF12_OTG2_FS`）。

### 2.14 BSP SDRAM 外扩存储器操作说明

#### 2.14.1 功能使能与参数配置

框架通过 FMC 接口实现对外部 SDRAM 的驱动控制。用户可以通过宏定义开启 SDRAM 支持，并灵活规划存储空间，如分配 LCD 显存及应用程序缓冲区。

```c
#define SDRAM_EN                     1           // SDRAM使能, 1：打开， 0：关闭
#if (SDRAM_EN > 0)
#define SDRAM_ADDR                  ((uint32_t)(0XC0000000))     /* SDRAM硬件起始地址 */
#define SDRAM_SIZE                  (32 * 1024 * 1024)           /* SDRAM总容量: 32MB */

/* 显存空间规划 */
#define SDRAM_LCD_SIZE              (4 * 1024 * 1024)            /* 单层显存大小: 4MB */
#define SDRAM_LCD_LAYER             2                            /* 显存层数: 2层 */
#define SDRAM_LCD_BUF1              ((uint16_t*)SDRAM_ADDR)      /* 图层1地址 */
#define SDRAM_LCD_BUF2              (SDRAM_ADDR + SDRAM_LCD_SIZE)/* 图层2地址 */

/* 剩余空间规划为应用缓冲区 */
#define SDRAM_APP_BUF               (SDRAM_ADDR + SDRAM_LCD_SIZE * SDRAM_LCD_LAYER)
#define SDRAM_APP_SIZE              (SDRAM_SIZE - SDRAM_LCD_SIZE * SDRAM_LCD_LAYER)
#endif
```

#### 2.14.2 硬件映射与引脚定义

**底层引脚与功能定义：**

- **`SDRAM_Ax_PIN`**: 地址总线引脚 A0 ~ A12（如 `GPIO_PIN_0` 至 `GPIO_PIN_2`）。
- **`SDRAM_Dx_PIN`**: 数据总线引脚 D0 ~ D15（支持 16 位带宽）。
- **`SDRAM_CLK/CKE_PIN`**: 同步时钟及使能信号线。
- **`SDRAM_RAS/CAS/WE_PIN`**: 行/列地址选通及写使能控制线。
- **`SDRAM_BS0/BS1_PIN`**: Bank 选择信号线。
- **`SDRAM_LDQM/UDQM_PIN`**: 数据输入/输出掩码控制（低字节/高字节）。
- **`SDRAM_x_GPIO_AF`**: 全局统一使用 `GPIO_AF12_FMC` 复用功能。

#### 2.14.3 驱动 API 接口

| 函数原型                                                               | 功能描述              | 参数说明                                       | 返回值 |
| ---------------------------------------------------------------------- | --------------------- | ---------------------------------------------- | ------ |
| **void SDRAM_APPInit(void)**                                           | 初始化 SDRAM 硬件     | 无                                             | 无     |
| **void BSP_Sdram_Clear(uint32_t addr, uint32_t size, uint32_t data)**  | 快速清除/填充指定区域 | `addr`: 起始地址`size`: 字节数`data`: 填充值   | 无     |
| **void BSP_Sdram_Write(uint32_t addr, uint8_t \*pbuf, uint32_t size)** | 向 SDRAM 写入数据     | `addr`: 目标地址`pbuf`: 源数据指针`size`: 长度 | 无     |
| **void BSP_Sdram_Read(uint32_t addr, uint8_t \*pbuf, uint32_t size)**  | 从 SDRAM 读取数据     | `addr`: 源地址`pbuf`: 存放地址`size`: 长度     | 无     |

---

### 2.15 BSP RTC 实时时钟操作说明

#### 2.15.1 功能使能与参数配置

框架通过宏定义实现对 RTC 模块的使能控制与扫描周期配置。用户可开启 RTC 功能以实现系统时间的维护，并设置定时读取或同步的时间间隔。

```c
#define RTC_EN          1         // RTC使能, 1：打开使能， 0：关闭
#if (RTC_EN > 0)
#define RTC_SCAN_T      1000      // 设置定时扫描时间间隔, 单位：ms
#endif
```

#### 2.15.2 结构体定义与备份寄存器映射

系统使用统一的结构体管理日期和时间信息，并利用 RTC 备份寄存器保存系统状态标志，确保在 Vbat 供电下数据不丢失。

**时间结构体定义：**

```c
typedef struct
{
    uint8_t year;     // 年 (0-99)
    uint8_t month;    // 月 (1-12)
    uint8_t day;      // 日 (1-31)
    uint8_t hour;     // 时 (0-23)
    uint8_t minute;   // 分 (0-59)
    uint8_t second;   // 秒 (0-59)
    uint8_t weekday;  // 星期 (1-7)
} RTC_TIME;
```

**备份寄存器与宏映射：**
RTC 备份寄存器用于存储初始化标志位或其他关键掉电保存数据：

- **`RTC_BACKUP_FLAG`**: 自定义备份域有效标志（如 `0x5AA5`）。
- **`RTC_BKP_REG0`**: 备份寄存器起始地址（映射至 `RTC_BKP_DR0`）。
- **`RTC_BKP_REG(n)**: 备份寄存器索引宏，用于访问第 n 个数据槽。

#### 2.15.3 驱动 API 接口

| 函数原型                                                                  | 功能描述                 | 参数说明                                        | 返回值                   |
| ------------------------------------------------------------------------- | ------------------------ | ----------------------------------------------- | ------------------------ |
| **HAL_StatusTypeDef BSP_RTC_Init(void)**                                  | 初始化 RTC 硬件及备份域  | 无                                              | `HAL_OK`-成功, 其他-失败 |
| **void BSP_RTC_WriteBackUpFlag(uint32_t BackUpReg, uint32_t BackUpFlag)** | 向指定备份寄存器写入标志 | `BackUpReg`: 寄存器索引`BackUpFlag`: 写入的数值 | 无                       |
| **HAL_StatusTypeDef BSP_RTC_ReadBackUpFlag(uint32_t BackUpReg)**          | 检查备份寄存器标志位     | `BackUpReg`: 待读取寄存器                       | `HAL_OK`-有效, 其他-无效 |
| **HAL_StatusTypeDef BSP_RTCSetDateTime(RTC_TIME \*rtc)**                  | 设置当前系统日期与时间   | `rtc`: 时间结构体指针                           | `HAL_OK`-成功, 其他-失败 |
| **HAL_StatusTypeDef BSP_RTCGetDateTime(RTC_TIME \*rtc)**                  | 获取当前系统日期与时间   | `rtc`: 存储地址指针                             | `HAL_OK`-成功, 其他-失败 |

---

### 2.16 BSP LTDC 液晶显示操作说明

#### 2.16.1 功能使能与参数配置

通过宏定义实现对 LTDC 的灵活配置。用户可根据实际连接的 LCD 面板型号设置分辨率、时序参数、极性以及显存布局。

```c
#define LTDC_EN                                 1       // LTDC使能, 1：打开， 0：关闭
#if (LTDC_EN > 0)
#define LTDC_SCAN_T                             100     // 设置定时扫描时间间隔, 单位：ms
#define LCD_PRODUCT                             0       // LCD型号: 0-800X480; 1-1024X600
#define LCD_DISP_TYPE                           0       // 显示方式: 0-横屏; 1-横屏180; 2-竖屏; 3-竖屏180

// 时序参数配置 (以 800x480 为例)
#define LCD_WIDTH                               800     // LCD分辨率宽
#define LCD_HEIGH                               480     // LCD分辨率高
#define LCD_HSYNC_WIDTH                         20      // HSYNC信号宽度
#define LCD_HBP_WIDTH                           46      // HBP信号宽度
#define LCD_HFP_WIDTH                           210     // HFP信号宽度

// 信号极性配置
#define LCD_HSYNC_POLARIRY                      0       // HSYNC极性: 0-低电平; 1-高电平
#define LCD_VSYNC_POLARIRY                      0       // VSYNC极性: 0-低电平; 1-高电平
#define LCD_DE_POLARIRY                         0       // DE极性: 0-低电平; 1-高电平
#define LCD_CLK_POLARIRY                        0       // Pixel Clock极性: 0-低电平; 1-高电平
#endif

```

#### 2.16.2 颜色定义与硬件映射

系统预定义了标准 RGB565 颜色常量，并映射了 LTDC 接口所需的全部物理引脚，包括时钟、同步信号及数据通道。

**颜色常量定义：**
使用 `RGB565(r, g, b)` 宏生成 16 位颜色编码，方便在 API 调用时直接指定色彩。

- **`LCD_WHITE` / `LCD_BLACK**`: 纯白 / 纯黑。
- **`LCD_RED` / `LCD_GREEN` / `LCD_BLUE**`: 标准三原色。
- **`LCD_YELLOW` / `LCD_ORANGE**`: 常用功能色。

**底层引脚与时钟定义：**

- **`LCD_CLK/HSYNC/VSYNC/DE_PIN`**: 关键控制引脚号（如 `GPIO_PIN_14`）。
- **`LCD_Rx/Gx/Bx_PIN`**: RGB 各分量数据引脚。
- **`LCD_x_GPIO_PORT`**: 引脚所属端口（如 `GPIOI`, `GPIOK`, `GPIOJ`）。
- **`LCD_x_GPIO_CLK_ENABLE()`**: 开启对应端口的时钟宏。
- **`LCD_x_GPIO_AF`**: 复用功能配置（通常为 `GPIO_AF14_LTDC`）。
- **`LTDC_L1_START_ADDRESS`**: 定义图层 1 的显存起始地址（通常位于外部 SDRAM）。

#### 2.16.3 驱动 API 接口

| 函数原型                                                     | 功能描述           | 参数说明                                                     | 返回值    |
| ------------------------------------------------------------ | ------------------ | ------------------------------------------------------------ | --------- |
| **void BSP_LTDC_Init(void)**                                 | **初始化硬件**     | 初始化 LTDC 控制器、时钟及硬件引脚复用                       | 无        |
| **void LCD_DrawPixel(uint16_t x, uint16_t y, uint16_t color)** | **指定坐标打点**   | `x, y`: 像素坐标<br>`color`: 颜色值                          | 无        |
| **uint16_t LCD_ReadPixel(uint16_t x, uint16_t y)**           | **读取像素颜色**   | `x, y`: 目标像素坐标                                         | 16 位颜色 |
| **void LCD_ClearScreen(uint16_t color)**                     | **清空全屏**       | `color`: 填充全屏的背景颜色                                  | 无        |
| **void LCD_FillRect(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, uint16_t color)** | **填充实心矩形**   | `x0, y0`: 左上角坐标<br>`x1, y1`: 右下角坐标<br>             |           |
| `color`: 填充颜色                                            | 无                 |                                                              |           |
| **void LCD_DrawLine(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint32_t color)** | **绘制直线**       | `x1, y1`: 起点坐标<br>`x2, y2`: 终点坐标<br>`color`: 线条颜色 | 无        |
| **void LCD_DrawRect(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint32_t color)** | **绘制空心矩形**   | `x1, y1`: 左上角坐标<br>`x2, y2`: 右下角坐标<br>`color`: 边框颜色 | 无        |
| **void LCD_DrawCircle(uint16_t x0, uint16_t y0, uint16_t r, uint32_t color)** | **绘制空心圆**     | `x0, y0`: 圆心坐标<br>`r`: 半径<br>`color`: 边框颜色         | 无        |
| **void LCD_DispChar(uint16_t x, uint16_t y, uint8_t num, uint8_t size, uint32_t color)** | **显示单个字符**   | `x, y`: 起始坐标<br>`num`: 字符 ASCII 码<br>`size`: 字体大小 (12/16/24)<br>`color`: 颜色 | 无        |
| **void LCD_DispString(uint16_t x, uint16_t y, uint16_t width, uint16_t height, uint8_t size, char \*p, uint32_t color)** | **显示字符串**     | `x, y`: 起始坐标<br>`width, height`: 限制显示区域<br>`size`: 字体大小<br>`*p`: 字符串首地址 | 无        |
| **void LCD_DispNum(uint16_t x, uint16_t y, uint32_t num, uint8_t len, uint8_t size, uint32_t color)** | **显示数字**       | `x, y`: 坐标<br>`num`: 数值<br>`len`: 数字长度<br>`size`: 字体大小 | 无        |
| **void LCD_DispBmp(uint16_t \_usX, uint16_t \_usY, uint16_t \_usHeight, uint16_t \_usWidth, uint16_t \*\_ptr)** | **绘制位图(图片)** | `_usX, _usY`: 绘制起始位置`_usWidth, _usHeight`: 图片宽高<br>`*_ptr`: 图片颜色数组指针 | 无        |

---

### 2.17 BSP 以太网操作说明

#### 2.17.1 功能使能与参数配置

以太网模块基于官方 LwIP 协议栈进行移植，支持 TCP 服务器/客户端、UDP 及 HTTP 模式。用户可通过宏定义配置静态 IP 或启用 DHCP 动态获取地址。

```c
#define LWIP_EN                     1       // TCPIP(LWIP)协议栈使能：1, 使能;  0, 关闭
#if (LWIP_EN > 0)
#define LWIP_SCAN_T                 1       // 设置定时扫描时间间隔, 单位：ms
#define LWIP_WKMODE                 LWIP_WKMODE_SERVER  // 工作模式: SERVER(服务端), CLIENT(客户端), HTTP
#define LWIP_NETYPE                 LWIP_NETYPE_TCP     // 通信类型: TCP 或 UDP
#define LWIP_CONFIG_EN              1       // 配置来源: 1-按如下宏定义设置; 0-按EEPROM存储信息设置

/* 默认静态IP配置 (LWIP_CONFIG_EN == 1 时生效) */
#define LOCAL_IP              "192.168.1.105"   // 本地IP地址
#define LOCAL_PORT            5000              // 本地监听端口号
#define LOCAL_SUBNET_MASK     "255.255.255.0"   // 本地子网掩码
#define LOCAL_GATEWAY         "192.168.1.1"     // 本地网关
#define DSC_IP                "192.168.1.248"   // 远端目的服务器IP (客户端模式用)
#define DSC_PORT              5001              // 远端目的端口号
#endif

```

#### 2.17.2 文件位置与硬件映射

**关键文件位置：**

- **底层驱动接口**：`ethernetif.c` (负责 HAL 库与 LwIP 数据包的互转，含零拷贝配置)。
- **应用初始化**：`lwip_app.c` (负责协议栈初始化、DHCP 状态机及各模式调度)。
- **协议栈核心**：`Middlewares/Third_Party/LwIP` (官方协议栈源码)。
- **配置头文件**：`lwipopts.h` (LwIP 剪裁配置) 及 `config.h` (用户业务配置)。

**底层引脚定义：**

- **`ETH_RMII_REF_CLK`**: 50MHz 参考时钟 (PA1)。
- **`ETH_RMII_MDIO/MDC`**: PHY 寄存器配置接口 (PA2/PC1)。
- **`ETH_RMII_TXD0/TXD1/TX_EN`**: 发送数据线及使能 (PG13/PG12/PG11)。
- **`ETH_RMII_RXD0/RXD1/CRS_DV`**: 接收数据线及有效信号 (PC4/PC5/PA7)。
- **`ETH_RESET_PIN`**: PHY 芯片硬件复位引脚 (PI10)。

---

## 3. 应用层 手册

---

### 3.1 APP_IO 端口操作说明（DI/DO/继电器/按键/拨码）

**位置:** `Projects/STM32H7XX/src/io_app.c`

#### 3.1.1 功能概述与测试逻辑

IO 模块包含数字输入（DI）、数字输出（DO）、继电器控制、拨码开关读取、系统状态指示灯（RUN LED）及蜂鸣器功能。

**测试程序实现的功能：**

- **RUN LED**：以 **1 秒** 为周期翻转状态，表示系统运行正常。
- **蜂鸣器**：每隔 **3 秒** 触发一次 **50ms** 的短促鸣叫。
- **DO 输出**：每隔 **3 秒** 对所有 DO 端口进行状态翻转。
- **DI 输入**：实时监测输入电平。通过串口打印当前所有 DI 的二进制状态。
- **拨码开关与按键**：定时读取物理拨码状态。

#### 3.1.2 IO 位映射定义

系统使用 `INT32U` 变量位图（Bitmap）来管理多路 IO，每一位对应一个物理端口：

| 功能模块      | 位标志定义示例                      | 说明                            |
| ------------- | ----------------------------------- | ------------------------------- |
| **DI 输入**   | `DI1FLAG (0x00000001)` ~ `DI32FLAG` | 32 路数字量输入监测             |
| **DO 输出**   | `DO1FLAG (0x00000001)` ~ `DO32FLAG` | 32 路数字量输出控制             |
| **继电器**    | `JDQ1FLAG` ~ `JDQ6FLAG`             | 控制继电器吸合/断开             |
| **按键/拨码** | `K1FLAG` / `K1VAL`                  | 对应板载物理按键或 8 位拨码开关 |

#### 3.1.3 驱动 API 接口

| 函数原型                  | 功能描述                              | 参数说明 | 返回值 |
| ------------------------- | ------------------------------------- | -------- | ------ |
| **void IO_APPInit(void)** | 初始化 LED、蜂鸣器、DI/DO 等硬件      | 无       | 无     |
| **void IO_Proc(void)**    | IO 处理主循环（含自动翻转与变化上报） | 无       | 无     |

---

### 3.2 APP_UART 异步通讯操作说明

**位置:** `Projects/STM32H7XX/src/uart_app.c`

#### 3.2.1 功能概述与测试逻辑

UART 通讯模块（支持 RS232/RS485）采用**非阻塞式分包接收**机制。测试程序主要实现“回环测试”功能：接收外部发来的数据包，并原样发送回去。

#### 3.2.2 驱动 API 接口

| 函数原型                    | 功能描述             | 参数说明 | 返回值 |
| --------------------------- | -------------------- | -------- | ------ |
| **void Uart_APPInit(void)** | 初始化 UART 硬件配置 | 无       | 无     |
| **void Uart_Proc(void)**    | 串口通讯处理         | 无       | 无     |

---

### 3.3 APP_TIM 通用定时器操作说明

**位置:** `Projects/STM32H7XX/src/tim_app.c`

#### 3.3.1 功能概述与测试逻辑

TIM 程序支持两种工作模式：**定时中断模式**和**外部计数模式**。

**测试工作流程：**

1. **定时中断模式 (`TIM_WKMODE_INT`)**：

- 定时器达到设定的溢出时间（如 ）时触发中断。
- 在 `TIM_ISRHook` 中断回调中设置对应的 `TimIntFlag`。
- 异步处理函数 `TIM_Proc` 监测到标志位后，通过串口打印 `AT+TIMx=INT` 并清除标志。

2. **外部计数模式 (`TIM_WKMODE_COUNT`)**：

- 定时器记录外部引脚输入的脉冲个数。
- `TIM_Proc` 以 `TIM_SCAN_T` 为周期轮询读取计数器的当前值。
- 通过串口打印当前计数值 `AT+TIMx=xx`。

#### 3.3.2 驱动 API 接口

| 函数原型                    | 功能描述         | 参数说明                                          |
| --------------------------- | ---------------- | ------------------------------------------------- |
| **void TIM_APPInit(void)**  | 初始化定时器模块 | 根据配置宏初始化各定时器的模式（中断/计数）与参数 |
| **void TIM_APPStart(void)** | 启动定时器运行   | 使能定时器计数器，开始计时或计数                  |
| **void TIM_ISRHook(id)**    | 中断钩子函数     | 由底层硬件中断调用，用于标记中断事件发生          |
| **void TIM_Proc(void)**     | 定时器事件处理   | 处理中断标志打印及轮询计数输出                    |

---

### 3.4 APP_PWM 输出操作说明

**位置:** `Projects/STM32H7XX/src/pwm_app.c`

#### 3.4.1 功能概述与测试逻辑

PWM 程序主要用于验证模块生成可变频率和可变占空比波形的能力。该程序通过定时轮询机制，动态改变 PWM 的输出参数，从而实现对步进电机驱动器或其他外设的控制。

**测试动作描述：**
程序以 `PWM_SCAN_T` 为周期循环执行以下操作：

1. **频率切换**：在 1KHz 与 2KHz 之间步进切换。
2. **占空比变化**：在 100 到 900 范围内循环增加。
3. **IO 控制联动**：同步翻转 `DIR`（方向）和 `ENA`（使能）引脚的高低电平。

#### 3.4.2 驱动 API 接口

| 函数原型                    | 功能描述          | 参数说明                                        |
| --------------------------- | ----------------- | ----------------------------------------------- |
| **void PWM_APPInit(void)**  | 初始化 PWM 模块   | 根据配置文件初始化 PWM1~PWM8 的默认频率与占空比 |
| **void PWM_APPStart(void)** | 开启 PWM 通道输出 | 启动指定通道（CH1~CH4）的波形输出               |
| **void PWM_Proc(void)**     | PWM 轮询处理      | 执行频率、占空比的动态调整逻辑及 IO 翻转        |

---

### 3.5 APP_FCLK 脉冲输入操作说明

**位置:** `Projects/STM32H7XX/src/fcllk_app.c`

#### 3.5.1 功能概述与测试逻辑

FCLK 程序主要用于对外部脉冲信号进行捕捉与分析。

**测试工作模式：**

1. **计数模式 (`FCLK_MODE_COUNT`)**：

- 统计指定通道（通常为 CH1）输入的脉冲个数。

2. **正交解码模式 (`FCLK_MODE_DECODE`)**：

- 专为旋转编码器设计，通过 CH1 (A 相) 和 CH2 (B 相) 的相位差判断旋转方向并增减计数值。

3. **测频模式 (`FCLK_MODE_FREQ`)**：

- 测量输入信号的频率（单位：Hz）。

4. **PWM 占空比模式 (`FCLK_MODE_PWMRATE`)**：

- 测量 PWM 信号的占空比。

#### 3.5.2 驱动 API 接口

| 函数原型                     | 功能描述         | 参数说明                                        |
| ---------------------------- | ---------------- | ----------------------------------------------- |
| **void FCLK_APPInit(void)**  | 初始化 FCLK 模块 | 根据配置文件中的宏定义（MODE, CH_EN）初始化硬件 |
| **void FCLK_APPStart(void)** | 启动脉冲输入     | 使能捕获通道及相关计数器                        |
| **void FCLK_Proc(void)**     | FCLK 轮询处理    | 定时轮询硬件数据并通过串口异步打印结果          |

---

### 3.6 APP_ADC 模拟量采集操作说明

**位置:** `Projects/STM32H7XX/src/adc_app.c`

#### 3.6.1 功能使能与参数配置

通过宏定义实现对多路模拟输入 (AI) 通道的配置，支持多种量程切换（如 0~10V、4~20mA 等）。用户需在配置头文件中开启对应的 ADC 通道并设定采样频率。

```c
#define ADC_EN              1       // ADC模块使能: 1-打开, 0-关闭
#if (ADC_EN > 0)
#define AI_SCAN_T           100     // 自动扫描时间间隔, 单位: ms
#define AI1_EN              1       // 通道1使能
#define AI1_RANGE           1       // 量程设置: 1(0~10V), 5(0~20mA) 等
#define AI_NUM              10      // 启用的总通道数
#endif
```

#### 3.6.2 枚举定义与硬件映射

**量程命令定义：**

- **`0`**: `0~4095` 原始采样值。
- **`1`**: `0~+10V` 电压量程。
- **`2`**: `-10V~+10V` 电压量程。
- **`3`**: `0~5V` 电压量程。
- **`4`**: `-5V~+5V` 电压量程。
- **`5`**: `0~+20mA` 电流量程。
- **`6`**: `-20mA~+20mA` 电流量程。

#### 3.6.3 驱动 API 接口

| 函数原型                                   | 功能描述                     | 参数说明                           | 返回值                   |
| ------------------------------------------ | ---------------------------- | ---------------------------------- | ------------------------ |
| **void ADC_APPInit(void)**                 | 初始化 ADC 模块              | 无                                 | 无                       |
| **INT16S ADC_Conv(INT8U Cmd, INT16S val)** | 将原始 AD 值转换为工程实际值 | `Cmd`: 量程类型, `val`: 原始 AD 值 | `INT16S`: 计算后的实际值 |
| **void ADC_Proc(void)**                    | ADC 轮询处理                 | 无                                 | 无                       |

---

### 3.7 APP_DAC 模拟量输出操作说明

**位置:** `Projects/STM32H7XX/src/dac_app.c`

#### 3.7.1 功能使能与输出模式

```c
#define DAC1_EN             1       // DAC1 模块使能
#define DAC1_MODE           2       // 0: 手动直流输出; 1: 输出N个周期波形后停止; 2: 持续循环输出波形
#define DAC1_TXBUF_SIZE     128     // 波形数据点数（缓冲区大小）
```

#### 3.7.2 驱动 API 接口

| 函数原型                                   | 功能描述                       | 参数说明                                                 | 返回值 |
| ------------------------------------------ | ------------------------------ | -------------------------------------------------------- | ------ |
| **void DAC_APPInit(void)**                 | 初始化 DAC 模块                | 无                                                       | 无     |
| **void DAC_APPStart(void)**                | 配置 DMA 缓冲区并启动 DAC 输出 | 无                                                       | 无     |
| **void DAC_SetWave(id, type, size, rate)** | 填充指定类型的波形数据到缓存   | `id`: 通道号, `type`: 波形, `size`: 点数, `rate`: 占空比 | 无     |

---

### 3.8 APP_CAN 总线通讯操作说明

**位置:** `Projects/STM32H7XX/src/can_app.c`

#### 3.8.1 功能使能与测试模式

提供双机通讯测试逻辑，通过宏定义切换 **测试板 A (发送方)** 或 **测试板 B (回环方)** 角色，以验证链路完整性。

```c
#define CAN1_EN             1           // CAN1 模块使能
#define CAN2_EN             1           // CAN2 模块使能

// 测试角色定义（二选一）
// #define CAN_TEST_A       // A板：主动发送 4 组 ID (1-4) 并等待接收
#define CAN_TEST_B          // B板：接收 A 板数据并原样“回弹”发送
```

#### 3.8.2 消息结构与通讯流程

采用 `CAN_TX_MSG` 和 `CAN_RX_MSG` 结构体管理报文。

**通讯机制说明：**

- **A 板逻辑**：每隔 `CANx_TX_T` 时间，循环发送 4 帧数据包，报文 ID 分别为 1, 2, 3, 4，数据载荷为 `0x00~0x07`。
- **B 板逻辑**：实时轮询接收缓存，一旦检测到数据包，立即提取其 ID 和 Data，重新组装后通过 `BSP_CAN_Write` 发回给 A 板。

#### 3.8.3 驱动 API 接口

| 函数原型                   | 功能描述         | 参数说明 | 返回值 |
| -------------------------- | ---------------- | -------- | ------ |
| **void CAN_APPInit(void)** | 初始化 CAN1/CAN2 | 无       | 无     |
| **void CAN_Proc(void)**    | CAN 轮询处理     | 无       | 无     |

---

### 3.9 APP_Flash 存储操作说明 (QSPI/SPI)

**位置:** `Drivers/BSP/STM32H7XX/w25qxx.c`

#### 3.9.1 模块概述

本模块用于驱动外部串行 NOR Flash 存储器（如 **W25Qxx** 或 **GD25Q64** 系列）。系统支持通过 **QSPI**（四线串行外设接口）或标准 **SPI** 进行连接。

- **硬件兼容性**：虽然底层硬件控制器（QSPI 或 SPI）因 MCU 型号而异，但本框架通过封装，使应用层调用 **W25QXX** 系列 API 时保持完全一致。
- **性能优势**：QSPI 模式下，数据吞吐量是传统 SPI 的 4 倍，且支持内存映射模式，适合存储大容量的图形素材或执行代码。

#### 3.9.2 驱动 API 接口 (W25QXX)

| 函数原型                                                | 功能详细描述     | 应用场景与注意事项                                                                           |
| ------------------------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------- |
| **void BSP_W25QXX_Init(void)**                          | **初始化 Flash** | 配置底层 GPIO 引脚                                                                           |
| **void BSP_W25QXX_Reset(void)**                         | **复位 Flash**   | 向芯片发送复位指令。                                                                         |
| **uint16_t BSP_W25QXX_ReadID(void)**                    | **读取器 ID**    | 返回 16 位 ID（包含厂家 ID 和设备 ID）。                                                     |
| **void BSP_W25QXX_SectorErase(uint32_t SectorAddress)** | **扇区擦除**     | Flash 最小擦除单位。写入前必须确保目标区域为 0xFF。此操作将指定地址所在的 4KB 区域全部置 1。 |
| **void BSP_W25QXX_ChipErase(void)**                     | **全片擦除**     | 擦除整颗 Flash 芯片的所有数据。                                                              |
| **void BSP_W25QXX_Read(Addr, Len, pBuffer)**            | **读取数据**     | 从任意物理地址读取指定长度的数据。                                                           |
| **void BSP_W25QXX_WritePage(Addr, Len, pBuffer)**       | **页写入 **      | 向 Flash 写入数据。                                                                          |
| **void BSP_W25QXX_Write_NoCheck(Addr, Len, pBuffer)**   | **页写入**       | 向 Flash 写入数据`支持跨页`。                                                                |

---

### 3.10 APP_EEPROM 操作说明 (I2C)

**位置:** `Drivers/BSP/STM32H7XX/eeprom.c`

#### 3.10.1 模块架构说明

驱动外部 **EEPROM**（如 AT24C64）。

- **总线**：EEPROM 依赖于 `EEPROM_ID` 所指向的 I2C 硬件接口（如 I2C2）。在使用前，需确保对应的 I2C 接口已正确初始化。

#### 3.10.2 参数配置定义

| 宏定义                   | 示例值    | 说明                      |
| ------------------------ | --------- | ------------------------- |
| **`EEPROM_EN`**          | `1`       | 总使能开关。              |
| **`EEPROM_ID`**          | `I2C2_ID` | 指定使用的硬件 I2C 端口。 |
| **`EEPROM_I2C_ADDRESS`** | `0xA0`    | 设备从机地址。            |
| **`EEPROM_PAGESIZE`**    | `32`      | **物理页大小**。          |
| **`EEPROM_MAX_SIZE`**    | `0x2000`  | 总容量。                  |
| **`EEPROM_MAX_TRIALS`**  | `3000`    | 忙检测最大尝试次数。      |

#### 3.10.3 核心 API 接口详述

| 函数原型                                                                                            | 功能详细描述       | 应用场景与细节                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **uint32_t BSP_EEPROM_Init(void)**                                                                  | **初始化 EEPROM ** | 1. 初始化所关联的 I2C 硬件外设时钟及引脚。2. 通过发送从机地址并等待应答，检测 EEPROM 芯片是否在位。3. 返回 `EEPROM_OK` 表示硬件连接正常。                                   |
| **uint32_t BSP_EEPROM_ReadBuffer(uint8_t \*pBuffer, uint16_t ReadAddr, uint16_t NumByteToRead)**    | **读取数据**       | 1. 从指定的 `ReadAddr` 开始，连续读取 `NumByteToRead` 长度的数据到 `pBuffer`。2. 内部处理了起始地址发送和数据流接收。3. `EEPROM_READ_TIMEOUT` 超时时间，防止 I2C 总线死锁。 |
| **uint32_t BSP_EEPROM_WriteBuffer(uint8_t \*pBuffer, uint16_t WriteAddr, uint16_t NumByteToWrite)** | **写入数据**       | 1. 将 `pBuffer` 中长度为 `NumByteToWrite` 的数据写入 `WriteAddr`。                                                                                                          |

### 3.11 RTC、EEPROM 与 SPI FLASH 综合测试操作说明

**位置:** `Projects/STM32H7XX/src/rtc_eeprom_spiflash_app.c`

#### 3.11.1 功能概述与测试逻辑

模块包含了嵌入式系统中常见的三种存储与时钟外设测试：**RTC**、**EEPROM** 以及 **SPI FLASH**。

**核心测试逻辑：**

1. **EEPROM/FLASH 读写校验**：

- **写入**：将 `0` 至 `LEN-1` 的递增序列写入指定地址。
- **读取**：从相同地址回读数据到缓存。
- **对比**：逐字节比对回读值与原始值，若不一致则立即报错。

3. **RTC 断电保持**：

- 利用备份寄存器（BKP）存储标志位。若标志位存在，说明 RTC 已被校准且由电池维持，无需重复初始化时间。

#### 3.11.2 串口输出示例

- **EEPROM**: `AT+EEPROM=读写测试 OK!`
- **SPI FLASH**: `AT+W25QXX=写256字节到0页!`
- **RTC**: `AT+RTC=2025.7.2,16:8:10`

---

### 3.12 SD 卡文件系统测试操作说明

**位置:** `Projects/STM32H7XX/src/sd_app.c`

#### 3.12.1 功能概述与测试逻辑

本模块基于 **FatFs 文件系统** 实现了对 SD 卡的读写测试。测试程序模拟了嵌入式设备中常见的数据存储流程：挂载文件系统、创建文件、循环写入数据、关闭并重新打开文件进行回读校验。

**核心测试流程：**

1. **硬件检测**：通过 `BSP_SD_Ctrl` 轮询 SD 卡的物理插入状态及初始化状态。
2. **驱动注册**：利用 `FATFS_LinkDriver` 将底层 SDIO 驱动与 FatFs 逻辑盘符绑定。
3. **文件操作循环**：

- **写测试**：创建名为 `embedarm.dat` 的文件，按 `FBUF_SIZE` 为一页，循环写入 `SD_PAGE_NUM` 次。
- **读校验**：重新打开文件，将读取的数据与原始递增序列（`0` 至 `255`）进行逐字节对比。

4. **资源释放**：测试结束后卸载文件系统并注销驱动，确保数据完整写入物理介质。

#### 3.12.2 驱动与系统 API 接口详解

| 功能描述                               | 函数原型       | 功能详述                                                        |
| -------------------------------------- | -------------- | --------------------------------------------------------------- |
| `BSP_SD_Init()`                        | **底层初始化** | 初始化 SDIO 外设、配置 DMA 及 GPIO，完成 SD 卡上电握手。        |
| `BSP_SD_Ctrl(CMD_SD_STATUS, 0)`        | **底层控制**   | 获取 SD 卡状态位，用于判断盘片是否在线（`SD_NODISK`）。         |
| `FATFS_LinkDriver(&SD_Driver, SDPath)` | **FS 注册**    | 建立 FatFs 逻辑驱动器与物理 SDIO 驱动的链接映射。               |
| `f_mount(&fs, SDPath, 0)`              | **FS 挂载**    | 挂载文件系统。参数 `0` 表示不立即挂载，而在首次文件操作时执行。 |
| `f_open(&fsrc, path, mode)`            | **文件打开**   | 打开或创建文件。模式 `FA_CREATE_ALWAYS` 会覆盖同名文件。        |
| `f_read` / `f_write`                   | **文件读写**   | 执行扇区级的缓冲区读写，返回实际操作的字节数。                  |

#### 3.12.3 串口输出示例

- `AT+FILE=SD卡: 测试读写文件`
- `AT+FILE=SD卡: 写1页` ... `写10页`
- `AT+FILE=SD卡: 读1页`
- `AT+FILE=SD卡: 数据对比正确`
- `AT+FILE=SD卡: 文件读写测试成功!`
- `AT+SD=OK`

---

### 3.13 USB Host (U 盘) MSC 类测试操作说明

**位置:** `Projects/STM32H7XX/src/usbh_app.c`

#### 3.13.1 功能概述与测试逻辑

本模块实现了 **USB Host (高速模式)** 协议栈下的 **MSC (Mass Storage Class)** 大容量存储设备测试。

**核心测试流程：**

1. **USB 库初始化**：调用 `USBH_Init` 和 `USBH_RegisterClass` 注册 MSC 类。
2. **状态机驱动**：通过 `USBH_UserProcess` 回调函数捕获 U 盘的 **连接 (CONNECTION)**、**枚举完成 (CLASS_ACTIVE)** 和 **断开 (DISCONNECT)** 状态。
3. **应用触发**：仅当 `Appli_state == APPLICATION_READY` 时，表示 U 盘已就绪，触发文件读写测试。
4. **文件读写循环**：

- 逻辑与 SD 卡测试一致，创建 `embedarm.dat` 并进行 `FBUF_SIZE * UDISK_PAGE_NUM` 字节的完整写入与回读比对。

#### 3.13.2 驱动 API 接口详述

| 接口名称                                                                                                                           | 参数/标志                                                              | 功能详述                 | 返回值                           |
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------ | -------------------------------- |
| **USBH_StatusTypeDef USBH_Init(USBH_HandleTypeDef *phost, void (*pUsrFunc)(USBH_HandleTypeDef \*phost, uint8_t id), uint8_t id)** | `phost`: 句柄指针`pUsrFunc`: 用户回调函数`id`: 主机 ID (如 0:FS, 1:HS) | **初始化 USB 主机栈**。  | `USBH_OK`: 成功`USBH_FAIL`: 失败 |
| **USBH_StatusTypeDef USBH_Process(USBH_HandleTypeDef \*phost)**                                                                   | `phost`: 主机句柄指针                                                  | **USB 核心状态机驱动**。 | `USBH_StatusTypeDef`             |

#### 3.13.3 串口输出示例

- `AT+FILE=UDISK: 测试读写文件`
- `AT+FILE=UDISK: 写1页` ... `写10页`
- `AT+FILE=UDISK: 读1页`
- `AT+FILE=UDISK: 数据对比正确`
- `AT+FILE=UDISK: 文件读写测试成功!`
- `AT+UDISK=OK`

---

### 3.14 APP_LTDC 液晶显示测试操作说明

**位置:** `Projects/STM32H7XX/src/ltdc_app.c`

#### 3.14.1 功能概述与测试逻辑

本模块实现了基于 **LTDC ** 的屏幕显示测试。

**核心测试流程：**

1. **硬件初始化**：调用 `BSP_LTDC_Init()` 配置像素时钟、同步信号（HSYNC/VSYNC）及显存地址。
2. **分步演示逻辑**：

- **刷屏测试**：测试全屏填充（黑/白），验证显存写入速度。
- **文字显示**：测试字符 `LCD_DispChar` 与字符串 `LCD_DispString` 的渲染。
- **几何绘图**：依次测试打点、画线、画矩形，验证坐标系的准确性。
- **色块填充**：遍历 `colors[]` 数组绘制彩条，验证色彩深度（RGB565 或 RGB888）和显示驱动的颜色还原度。

3. **时间片轮询**：通过 `APP_GetSubTick` 配合 `LTDC_SCAN_T` 实现非阻塞式刷新，防止阻塞主循环。

#### 3.14.2 显示效果

1. **全屏白色**。
2. 左上角出现蓝色字符 **'A'** 和绿色 **"Hello, LCD!"**。
3. 下方出现红色数字 **12345**。
4. 屏幕中下方出现一条青色斜线和一个品红色矩形框。
5. 底部出现一排由 25 种颜色组成的彩色条带。
6. **全屏变黑**，随即重新开始循环。

---

### 3.15 APP_TCP/IP 网络通讯操作说明

**位置:** `Projects/STM32H7XX/src/lwip_app.c`

#### 3.15.1 功能概述与通讯模式

| 函数原型                                             | 功能描述                  | 参数说明                          | 返回值               |
| ---------------------------------------------------- | ------------------------- | --------------------------------- | -------------------- |
| **void LWIP_APPInit(void)**                          | 初始化 LwIP 协议栈及网卡  | 无                                | 无                   |
| **void LWIP_Proc(uint32_t cnt)**                     | 协议栈任务轮询处理        | `cnt`: 扫描计数器                 | 无                   |
| **uint32_t TCP_Server_Read(uint32_t \*p)**           | 从 TCP 服务器缓存读取数据 | `p`: 指向接收数据指针的地址       | 返回接收到的数据长度 |
| **void TCP_Server_Write(uint8_t \*p, uint16_t len)** | 向已连接的客户端发送数据  | `p`: 数据指针, `len`: 发送长度    | 无                   |
| **uint32_t TCP_Client_Read(uint32_t **pBuffer)\*\*   | 从 TCP 客户端缓存读取数据 | `pBuffer`: 指向接收数据指针的地址 | 返回接收到的数据长度 |
| **void TCP_Client_Write(uint8_t \*p, uint16_t len)** | 向远端服务器发送数据      | `p`: 数据指针, `len`: 发送长度    | 无                   |
| **uint32_t UDP_Server_Read(uint32_t \*p)**           | 从 UDP 缓存读取数据       | `p`: 指向接收数据指针的地址       | 返回接收到的数据长度 |
| **void UDP_Server_Write(uint8_t \*p, uint16_t len)** | UDP 原始数据回发          | `p`: 数据指针, `len`: 发送长度    | 无                   |

#### 3.15.2 驱动 API 接口

在协议栈底层初始化完成后，系统根据 `LWIP_WKMODE`（工作模式）和 `LWIP_NETYPE` 调用具体的应用层初始化函数。这些函数负责建立控制块、绑定端口并进入监听或连接状态。

**关键初始化函数映射：**

```c
#if ((LWIP_WKMODE == LWIP_WKMODE_SERVER) && (LWIP_NETYPE == LWIP_NETYPE_TCP))
    tcp_echoserver_init();      // 初始化TCP服务器，开始监听 LOCAL_PORT
#endif

#if ((LWIP_WKMODE == LWIP_WKMODE_CLIENT) && (LWIP_NETYPE == LWIP_NETYPE_TCP))
    tcp_echoclient_connect();   // 初始化TCP客户端，尝试连接 DSC_IP:DSC_PORT
#endif

#if (LWIP_NETYPE == LWIP_NETYPE_UDP)
    udp_echoserver_init();      // 初始化UDP服务端/客户端通讯
#endif
```

#### 3.15.3 文件位置说明

- **应用调度层**：`Projects/STM32H7XX/src/lwip_app.c`

- **TCP 通讯实现**：
- **服务器模式**：`Drivers/BSP/STM32H7XX/tcp_echoserver.c / .h`
- **客户端模式**：`Drivers/BSP/STM32H7XX/tcp_echoclient.c / .h`

- **UDP 通讯实现**：
- **服务器模式**：`Drivers/BSP/STM32H7XX/udp_echoserver.c / .h`
- **客户端模式**：`Drivers/BSP/STM32H7XX/udp_echoclient.c / .h`

- **底层适配层**：`Drivers/BSP/STM32H7XX/ethernetif.c`
- 处理 HAL 库与 LwIP 之间的数据搬运。

---

### 3.16 WIFI 数据处理操作说明

**位置:** `Projects/STM32H7XX/src/wifiapp.c`

#### 3.16.1 功能概述与测试逻辑

本模块是用户层的 WIFI 处理数据中心。

**核心处理逻辑：**

1. **数据分发**：所有的接收事件通过 `WIFI_DataProcess`。
2. **Modbus TCP 解析**：专门针对 `00 00 00 00 00 06` 标准报文头进行解析，通过 `Modbus_Proc` 函数处理寄存器读写。
3. **非阻塞发送**：提供 `WIFI_UserTxProc` 。

#### 3.16.2 关键 API 接口详解

| 接口名称                  | 参数/标志                                                         | 功能详述                  | 返回值                       |
| ------------------------- | ----------------------------------------------------------------- | ------------------------- | ---------------------------- |
| **`WIFI_ModbusTCP_Proc`** | `id`: 连接 ID,`pRxBuf`: 接收缓冲区,`len`: 报文长度                | **Modbus TCP 数据处理**。 | `INT32S`: 处理状态或响应长度 |
| **`WIFI_DataProcess`**    | `id`: 连接 ID,`pbuf`: 数据指针,`len`: 长度,`pWifiSta`: 状态结构体 | **WIFI 数据处理**。       | `void`                       |

#### 3.16.3 串口输出示例

- `AT+WIFI=[ID=0:192.168.1.10,8080]:CONNECT`
- `AT+WIFI=RX[ID=0:192.168.1.10,8080,12]:00 01 00 00 00 06 01 03 ...`
