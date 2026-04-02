# mcp-server-mongodb 運作規範

## 指令處理規則
- 在查詢 publish 資料時，**必須**由使用者提供以下資訊：專案名稱 (Project Name), 資產名稱 (Asset Name) 或鏡頭名稱 (Shot Name)。嚴禁直接執行全域查詢或由 Agent 自行假設查詢對象。
