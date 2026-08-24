# Figma MCP 调用手册

> 读取时机：AI 需要读取、截图、创建、修改、导出或同步 Figma 文件时。

本文只说明 Figma MCP 的工具调用方式，不定义产品需求、设计规范或项目流程。

## 1. 工具选择

Figma MCP 工具通常以 `mcp__figma__` 开头。按任务选择：

| 任务 | 工具 |
|---|---|
| 读取设计上下文 | `get_design_context` |
| 快速读取节点元数据 | `get_metadata` |
| 查看节点截图 | `get_screenshot` |
| 创建、修改、删除图层 | `use_figma` |
| 搜索组件、变量和样式 | `search_design_system` |
| 首次捕获网页页面 | `generate_figma_design` |
| 创建空白 Figma 文件 | `create_new_file` |
| 查询当前 Figma 用户和团队 | `whoami` |
| 导出图片、SVG 和原始图片 | `download_assets` |
| 上传图片或其他资源 | `upload_assets` |
| 读取 FigJam | `get_figjam` |
| 读取 Code Connect 映射 | `get_code_connect_map` |
| 写入 Code Connect 映射 | `add_code_connect_map` |

默认原则：读取优先使用 `get_design_context`；写入、修改和同步使用 `use_figma`。`generate_figma_design` 只用于首次捕获网页页面，不能替代后续编辑。

如果工具 schema 被延迟加载，先用一次 `ToolSearch` 批量加载所需工具，例如：

```text
ToolSearch query="select:get_design_context,get_metadata,get_screenshot,use_figma"
```

## 2. 调用前加载 Skill

| 工具或任务 | 调用前加载 |
|---|---|
| `use_figma` | `figma-use`，每次调用前都要加载 |
| `get_design_context` | `figma-design-to-code` |
| `create_new_file` | `figma-create-new-file` |
| 完整页面或多区块页面 | `figma-generate-design` |
| 组件、变量或设计系统 | `figma-generate-library` |
| FigJam | `figma-use-figjam` |
| Slides | `figma-use-slides` |

本地 Skill 优先读取对应的 `SKILL.md`；没有本地 Skill 时，读取 Figma MCP 提供的 `skill://figma/.../SKILL.md` 资源。

## 3. 从 URL 提取参数

Design URL：

```text
https://www.figma.com/design/ABC123/demo?node-id=123-456
```

转换为：

```json
{
  "fileKey": "ABC123",
  "nodeId": "123:456"
}
```

注意：`node-id` 中的 `-` 要转换成 `:`。

其他 URL 类型：

```text
/design/  -> Figma Design
/board/   -> FigJam，使用 get_figjam
/slides/  -> Figma Slides
/make/    -> Figma Make
```

`get_design_context`、`get_screenshot` 和写入目标节点都需要有效的 `nodeId`。如果 URL 没有 `node-id`，可以先调用不带 `nodeId` 的 `get_metadata` 了解页面；需要设计转代码时，应向用户索取具体节点 URL，不要猜节点 ID 或传空值。分支 URL 使用分支的 `branchKey` 作为 `fileKey`。

## 4. 常用调用模板

### 读取设计上下文

```js
mcp__figma__get_design_context({
  fileKey: "ABC123",
  nodeId: "123:456"
})
```

`get_design_context` 必须传入节点 ID。还不知道目标节点时，先列出页面：

```js
mcp__figma__get_metadata({
  fileKey: "ABC123"
})
```

### 读取元数据

```js
mcp__figma__get_metadata({
  fileKey: "ABC123",
  nodeId: "123:456"
})
```

### 获取截图

```js
mcp__figma__get_screenshot({
  fileKey: "ABC123",
  nodeId: "123:456"
})
```

### 使用 Plugin API 修改 Figma

`use_figma` 的 `code` 是在 Figma 文件上下文中执行的 JavaScript：

```js
mcp__figma__use_figma({
  fileKey: "ABC123",
  description: "读取并修改指定节点名称",
  skillNames: "figma-use",
  code: `
    const node = figma.getNodeById("123:456");

    if (!node) {
      throw new Error("Node not found");
    }

    node.name = "Updated Name";

    return {
      mutatedNodeIds: [node.id],
      name: node.name
    };
  `
})
```

如果 Skill 是通过 Figma MCP 资源而不是本地 Skill 加载，`skillNames` 使用 `resource:` 前缀，例如：

```js
skillNames: "resource:figma-use"
```

### 读取或修改指定页面

```js
const page = figma.root.children.find((item) => item.name === "My Page");

if (!page) {
  throw new Error("Page not found");
}

await figma.setCurrentPageAsync(page);
return { pageId: page.id, pageName: page.name };
```

## 5. `use_figma` JavaScript 约束

- 使用普通 JavaScript、顶层 `await` 和 `return`；不要自行包 async IIFE。
- 使用 `return` 返回结果；`console.log()` 不会作为工具结果返回。
- 每次创建或修改节点，都返回 `createdNodeIds` 和/或 `mutatedNodeIds`。
- 所有 Promise 都要 `await`。
- 切换页面必须使用 `await figma.setCurrentPageAsync(page)`；不要给 `figma.currentPage` 直接赋值。
- 每次 `use_figma` 调用开始时当前页面会重置；跨调用时要再次切换页面。
- 一次调用最多切换一次页面；多页面任务拆成多个调用，并行发出。
- 修改文字前先加载字体：

  ```js
  await figma.loadFontAsync({ family: "Inter", style: "Regular" });
  textNode.characters = "New text";
  ```

- Figma 颜色使用 `0` 到 `1` 的小数，不是 `0` 到 `255`：

  ```js
  { r: 1, g: 0, b: 0 }
  ```

- 不要调用 `figma.closePlugin()`、`figma.notify()`、`getPluginData()`、`setPluginData()` 或不受支持的 API。
- 大型操作拆成多个小调用，每次调用后用 `get_metadata` 或 `get_screenshot` 验证。
- `use_figma` 脚本失败时不会部分执行；先读错误并修正，再重试。

## 6. 推荐调用顺序

### 读取现有文件

```text
解析 URL
-> 没有 nodeId 时用 get_metadata 了解页面，必要时向用户索取具体节点 URL
-> 加载 figma-design-to-code
-> get_design_context
-> get_screenshot（需要视觉确认时）
```

### 修改现有文件

```text
解析 URL
-> 加载 figma-use
-> get_metadata 或 get_design_context
-> use_figma
-> get_metadata
-> get_screenshot
```

### 创建新文件

```text
加载 figma-create-new-file
-> 没有 planKey 时调用 whoami
-> create_new_file
-> 使用返回的 fileKey 调用 use_figma
```

### 首次捕获网页页面

```text
加载 figma-generate-design 和 figma-use
-> search_design_system
-> generate_figma_design 与 use_figma 并行调用
-> get_screenshot 验证
```

## 7. 可直接转发给其他 AI 的提示词

```text
你可以通过官方 Figma MCP 操作 Figma。

1. 从 Figma URL 提取 fileKey；有 node-id 时提取 nodeId，并把 node-id 中的横杠转换成冒号。get_design_context 和 get_screenshot 必须传入 nodeId；没有 node-id 时，可以用不带 nodeId 的 get_metadata 了解页面，但设计转代码时要向用户索取具体节点 URL，不要猜或传空值。
2. 读取设计优先调用 get_design_context；结构概览调用 get_metadata；截图调用 get_screenshot；创建或修改图层调用 use_figma。
3. 调用 use_figma 前必须加载 figma-use；调用 get_design_context 前必须加载 figma-design-to-code；创建新文件前必须加载 figma-create-new-file。Skill 通过 MCP 资源加载时，在 skillNames 中使用 resource: 前缀。
4. use_figma 的 code 使用普通 JavaScript、顶层 await 和 return。不要使用 async IIFE、figma.closePlugin() 或 figma.notify()。
5. 所有 Promise 都要 await；修改文字前先 loadFontAsync；切换页面使用 await figma.setCurrentPageAsync(page)。
6. 每次创建或修改节点，都用 return 返回 createdNodeIds 或 mutatedNodeIds。
7. 大操作拆成多次 use_figma 调用，每次调用后用 get_metadata 或 get_screenshot 验证。
8. 工具报错时先分析错误，不要盲目重试；失败的 use_figma 脚本不会产生部分修改。
```
