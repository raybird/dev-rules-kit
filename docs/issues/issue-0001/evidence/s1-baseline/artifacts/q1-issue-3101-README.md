# Issue 3101 - 新增 export 指令匯出 CSV (Small)

## 概述
在 `todo.py` 新增 `export` 子指令，將待辦以 CSV 格式輸出到 stdout，欄位依序為 id、標題、完成狀態。根目錄 `README.md` 記載 2026-09-20 已移除舊的分號分隔 `export-v1` 且無相容層；本指令為新的逗號分隔 CSV，不沿用舊格式。

## 涉及檔案
- `todo.py` - 新增 `export` 子指令與 CSV 輸出
- `test_todo.py` - 新增 AC-1、AC-2 測試
- `README.md` - 使用說明補上 `export`（常青文件，依 project.md 觸發）

## 驗收條件

1. **AC-1**：`python3 todo.py export` 將 CSV 輸出到 stdout；第一行為標題列 `id,title,done`，之後依 `todo.json` 儲存順序每筆一行，`done` 欄為 `true`／`false`。沒有待辦時只輸出標題列。不寫入任何檔案、不修改 `todo.json`。 — 檢查方式：`python3 -m unittest -v`，以已知字面值資料（例如 `1,買牛奶,true`、`2,寫週報,false`）比對輸出
2. **AC-2**：標題含逗號、雙引號或換行時，依標準 CSV 規則加引號與跳脫，以 Python `csv` 模組讀回可得到原標題。 — 檢查方式：`python3 -m unittest -v`，標題如 `買"牛奶", 兩瓶` 讀回後與原字串相等
3. **AC-3**：根目錄 `README.md` 使用說明列出 `python3 todo.py export` 及其輸出到 stdout 的用法。 — 檢查方式：人工檢視 `README.md` 的「使用說明」

- **核准日期**: 2026-10-18
- **核准來源**:
  - 2026-10-18 對話原話：「幫 todo 加一個 export 指令，把待辦匯出成 CSV。欄位已確定是 id、標題、完成狀態三欄，順序就這樣。」（AC-1、AC-2、AC-3）
  - Q1「輸出到 stdout」（AC-1 輸出位置）
  - Q2「要標題列」；Q2-1「照建議」＝標題列名稱 `id,title,done`（AC-1）
  - Q3「照建議」＝`done` 欄值 `true`／`false`（AC-1）
  - AC-2 的引號跳脫屬於「CSV」本身的標準規則，是原話所要求格式的必要部分，不是新增行為

## 風險與首要驗證

**風險**: Low — 無明顯未知，依一般相依順序實作與驗證

## 實作與驗證步驟
1. 📝 **AC-1：export 輸出標題列與資料列到 stdout** — 產出：`todo.py`、`test_todo.py`；相依：無；驗證方式：`python3 -m unittest -v`，先紅燈（缺 export 行為）再綠燈，期望值使用字面值
   - 完成證據：（execute-task 回寫紅綠燈命令與輸出）
2. 📝 **AC-2：特殊字元依 CSV 規則跳脫** — 產出：`todo.py`、`test_todo.py`；相依：步驟 1；驗證方式：`python3 -m unittest -v`，以 `csv` 模組讀回比對原字面標題
   - 完成證據：（execute-task 回寫）
3. 📝 **AC-3：更新使用說明** — 產出：`README.md`；相依：步驟 1；驗證方式：人工檢視使用說明含 `export`（純文件，不適用紅燈）
   - 完成證據：（execute-task 回寫）

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-10-18 | 建立；AC-1～AC-3 依對話原話與 Q1～Q3 答覆核准 | - |

---
**建立日期**: 2026-10-18  
**分級**: Small  
**風險**: Low\
**狀態**: 待實作
