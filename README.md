# mcp-server-mongodb

這是一個基於 Model Context Protocol (MCP) 的 MongoDB 查詢伺服器，特別針對 Avalon/OpenPype 架構的管線資料庫進行了優化。它允許 LLM 透過標準化介面與生產追蹤數據進行互動。

## 功能特點

- **動態專案查詢**：根據專案名稱自動處理集合（Collections）。
- **層級化檢索**：支援從專案到資產/鏡頭、子集（Subsets）、版本（Versions）及表現形式（Representations）的導航。
- **異步操作**：採用 `motor` 驅動程式提供高效的 MongoDB 互動。
- **FastMCP 整合**：利用最新的 MCP 標準實現無縫工具發現。

## 工具清單 (Tools)

| 工具名稱 | 功能說明 | 參數 (粗體為必填) |
| :--- | :--- | :--- |
| `get_projects` | 取得資料庫中所有的專案定義 | `name`, `full` |
| `get_assets` | 從特定專案中取得資產 (Assets) | **`project_name`**, `name`, `limit`, `skip`, `full` |
| `get_sequences` | 取得專案中的序列 (Sequences) 資訊 | **`project_name`**, `name`, `limit`, `full` |
| `get_shots` | 取得專案中的鏡頭 (Shots) | **`project_name`**, `name`, `limit`, `full` |
| `get_subsets` | 取得指定父層下的子集 (Subsets) | **`project_name`**, **`parent_id`**, `name`, `limit`, `full` |
| `get_versions` | 取得子集下的版本 (Versions) 列表 | **`project_name`**, **`subset_id`**, `limit`, `full` |
| `get_representations` | 取得版本下的表現形式 (Representations) | **`project_name`**, **`version_id`**, `limit`, `full` |

## 安裝與執行

請確保您的環境中已安裝 Python 3.11+ 以及 `uv`。

```bash
uv sync
```

使用 stdio 傳輸方式執行伺服器：

```bash
uv run main.py -host "您的_MONGODB_主機" -db "資料庫名稱"
```

### 啟動參數

| 參數 | 別名 | 說明 | 必填 |
|-----------|-------|-------------|----------|
| `--host`  | `-host`| MongoDB 主機地址 (例如 `127.0.0.1:27017`) | 是 |
| `--database` | `-db` | MongoDB 資料庫名稱 (預設: `avalon`) | 否 |

## 使用規範 (重要)

在查詢專案資料時，必須遵守以下規範：
1. **明確識別**：Agent **必須**由使用者提供專案名稱 (Project Name)、資產名稱 (Asset Name) 或鏡頭名稱 (Shot Name)。
2. **禁止盲目查詢**：嚴禁執行全域查詢或由 Agent 自行假設查詢對象。

## 依賴項目

- `mcp`: Model Context Protocol SDK
- `motor`: MongoDB 的異步 Python 驅動程式
- `pydantic-settings`: 使用 Pydantic 進行設定管理

## 授權

MIT
