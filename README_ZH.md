# DDGS API

基于 FastAPI 的 DuckDuckGo 搜索 REST API 封装，支持 MCP（模型上下文协议）。

## 功能特性

- **REST API**：提供文本、图片、视频、新闻和书籍搜索端点
- **MCP 服务器**：可与 Claude Desktop 和其他 MCP 客户端集成
- **可配置默认值**：基于环境变量的搜索参数配置
- **API 密钥认证**：可选的身份验证支持

## 快速开始

### 安装

```bash
# 安装依赖
uv sync

# 复制环境配置文件
cp .env.example .env
```

### 运行服务

```bash
# 开发模式（自动重载）
fastapi dev app/main.py

# 生产模式
fastapi run app/main.py
```

服务地址：`http://localhost:8000`

## API 端点

### REST API

- `GET /search?query=<查询词>` - 快速文本搜索
- `POST /search/text` - 带参数的文本搜索
- `POST /search/images` - 图片搜索
- `POST /search/videos` - 视频搜索
- `POST /search/news` - 新闻搜索
- `POST /search/books` - 书籍搜索

API 文档：`http://localhost:8000/docs`

### MCP 服务器

MCP 端点：`http://localhost:8000/mcp`

可用工具：
- `search_text` - 搜索文本内容

## 配置说明

`.env` 文件中的主要环境变量：

```bash
# 代理设置（可选）
DDGS_PROXY=

# 默认搜索参数
DEFAULT_REGION=wt-wt
DEFAULT_SAFESEARCH=moderate
DEFAULT_MAX_RESULTS=10

# API 认证（可选）
API_KEYS=your-api-key

# MCP 启用的工具
MCP_ENABLE_TOOLS=text
```

## MCP 客户端配置

### Claude Desktop

在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "ddgs": {
      "url": "http://localhost:8000/mcp",
      "transport": {
        "type": "http"
      },
      "auth": {
        "type": "bearer",
        "token": "your-api-key"
      }
    }
  }
}
```

### Python 客户端

```python
from fastmcp.client import Client

async with Client("http://localhost:8000/mcp", auth="your-api-key") as client:
    tools = await client.list_tools()
    result = await client.call_tool("search_text", arguments={"query": "python"})
```

## Docker 部署

### 构建镜像

```bash
# 构建镜像
uv pip install -U ddgs # 先更新到最新的ddgs (可选)
docker build -t ddgs-api:latest .
```


### 运行Docker

```bash
# 基础运行
docker run -d -p 8000:8000 --name ddgs-api ddgs-api:latest

# 使用环境变量配置（推荐）
docker run -d -p 8000:8000 --name ddgs-api \
  -e DDGS_PROXY=socks5://127.0.0.1:1080 \
  -e DEFAULT_MAX_RESULTS=20 \
  -e API_KEYS=your-api-key \
  ddgs-api:latest

# 使用 .env 文件配置
docker run -d -p 8000:8000 --name ddgs-api \
  --env-file .env \
  ddgs-api:latest
```

可配置的环境变量包括：

**DDGS 初始化参数：**
- `DDGS_PROXY` - 代理地址
  - 支持协议：`http://`, `https://`, `socks5://`, `socks5h://`
  - 示例：`socks5://127.0.0.1:1080` 或 `http://user:pass@proxy:port`
  - 特殊值：`tb` (使用 Tor Browser)
- `DDGS_TIMEOUT` - 请求超时时间（秒，默认：5）

**默认搜索参数：**
- `DEFAULT_REGION` - 默认搜索区域
  - 示例：`wt-wt` (全球), `us-en` (美国), `cn-zh` (中国), `uk-en`, `jp-jp`, `ru-ru` 等
- `DEFAULT_SAFESEARCH` - 安全搜索级别
  - 可选值：`on` (严格), `moderate` (中等，默认), `off` (关闭)
- `DEFAULT_TIMELIMIT` - 时间限制
  - 可选值：`d` (最近一天), `w` (最近一周), `m` (最近一月), `y` (最近一年)
- `DEFAULT_MAX_RESULTS` - 默认最大结果数（默认：10）
- `DEFAULT_PAGE` - 默认页码（默认：1）
- `DEFAULT_BACKEND` - 搜索后端（默认：`auto`）
  - 文本搜索：`bing`, `brave`, `duckduckgo`, `google`, `mojeek`, `mullvad_brave`, `mullvad_google`, `yandex`, `yahoo`, `wikipedia`
  - 图片/视频：仅 `duckduckgo`
  - 新闻：`bing`, `duckduckgo`, `yahoo`
  - 书籍：仅 `annasarchive`

**API 配置：**
- `API_KEYS` - API 认证密钥（逗号分隔多个）
- `API_PREFIX` - API 路径前缀（如：`/api/v1`）

**MCP 配置：**
- `MCP_ENABLE_TOOLS` - 启用的 MCP 工具（逗号分隔，如：`text,news,books`）

**性能配置：**
- `EXECUTOR_MAX_WORKERS` - 线程池最大工作线程数（默认：100）
