# 使用說明文件設計規格

**日期**：2026-05-28  
**狀態**：待實作

## 背景

`dev-rules-kit` 目前缺少一份說明「用起來是什麼感覺」的文件。現有 README 解釋了裝什麼，setup 文件說明了怎麼安裝，但沒有端對端的使用示範。目標是新增一份 `docs/usage.md`，同時服務新手（完整情境 walkthrough）與老手（各 skill 快速參考）。

## 目標讀者

- **新手**：第一次接觸 skill/workflow 概念，需要情境式引導
- **老手**：已熟悉工具，需要快速查找觸發語法與輸入格式

## 文件位置

`docs/usage.md`（單一檔案，從 README.md 的使用方式章節補充連結）

## 文件結構

### 1. 快速開始

一段話說明這套 kit 解決什麼問題，以及前置條件（已按平台 setup 文件安裝完成）。

### 2. 完整閉環示範

情境：為現有 web app 新增 OAuth 登入功能（issue-101）

情境選擇理由：
- 夠具體，有明確需求邊界
- 通用，不綁定特定語言或框架
- 複雜度適中，能自然觸發 review 後修正的循環

包含以下步驟：
- Step 1 — `new-issue`
- Step 2 — `decompose`
- Step 3 — `execute-task`（含 code-simplify + create-commit 子步驟）
- Step 4 — `create-pr`
- Step 5 — `review`（含 MUST FIX 後回到 execute-task 的循環示範）
- Step 6 — `dev-cycle`（用同一情境示範查詢模式與推進模式）

### 3. 各 Skill 快速參考

每個 skill 一個快查表，欄位：觸發方式、產出、注意事項。
排列順序按開發閉環：`new-issue` → `decompose` → `execute-task` → `code-simplify` → `create-commit` → `create-pr` → `review` → `dev-cycle`

## 每個 Step 的呈現格式

```
### Step N — {skill-name}

**觸發**：使用者實際輸入的文字

**AI 產出**：產出的檔案或內容的關鍵片段（非完整輸出）

**關鍵行為**：一兩句說明這個 skill 的核心設計邏輯
```

review 後修正循環以 callout 框強調：

```
> **循環示範**：review 發現問題，AI 標記 MUST FIX，
> 回到 execute-task 修正後重新走一次 commit → PR → review。
```

## 各 Skill 快速參考格式

```
### `{skill-name}`

| | |
|---|---|
| **觸發** | 觸發語法或自然語言範例 |
| **產出** | 預期產出摘要 |
| **注意** | 重要行為或限制 |
```

## 連結更新

- `README.md` 的「使用方式」章節補上 `docs/usage.md` 連結

## 不在本次範圍內

- 修改任何現有 skill/workflow 內容
- 新增多個文件或子目錄
- 影片腳本或互動式教學
