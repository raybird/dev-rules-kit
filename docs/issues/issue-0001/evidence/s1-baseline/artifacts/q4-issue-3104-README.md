# Issue 3104 - todo 新增 export 指令匯出 CSV (Small)

## 概述
新增 `python3 todo.py export`，將 `todo.json` 的待辦以 CSV 印到標準輸出，欄位依序為 id、標題、完成狀態。

明說的假設（2026-10-18）：
- 以 Python 標準 `csv` 模組輸出：逗號分隔、`csv` 預設換行（CRLF）、UTF-8 不加 BOM；含逗號、引號或換行的標題依 CSV 規則加引號跳脫。
- 與 2026-09-20 已移除的分號版 `export-v1` 無相容關係，不恢復該指令。

## 涉及檔案
- `todo.py` - 新增 `export` 指令與 CSV 輸出
- `test_todo.py` - 新增 export 測試
- `README.md`（根目錄）- 使用說明補 `export` 一行（常青文件，依 project.md）

## 驗收條件

1. **AC-1**：`python3 todo.py export` 印到標準輸出，第一行為標題列 `id,title,done`，其後每筆待辦一列，依 `todo.json` 既有順序，欄位為 id、標題、完成狀態，完成狀態為 `true`／`false` — 檢查方式：以 `[{1, 買牛奶, 已完成}, {2, 寫週報, 未完成}]` 為輸入，輸出等於 `id,title,done`、`1,買牛奶,true`、`2,寫週報,false` 三列（unittest）
2. **AC-2**：沒有任何待辦時只輸出標題列 `id,title,done` — 檢查方式：以空清單為輸入的 unittest
3. **AC-3**：標題含逗號或雙引號時，輸出為合法 CSV，讀回後標題與原值相同 — 檢查方式：輸入標題 `寫, "週報"`，斷言該列字面值為 `3,"寫, ""週報""",false`（unittest）

- **核准日期**: 2026-10-18
- **核准來源**: 使用者原話「幫 todo 加一個 export 指令，把待辦匯出成 CSV。欄位已確定是 id、標題、完成狀態三欄，順序就這樣。」（AC-1～AC-3）；逐題確認：第 1 題「輸出到 stdout」（AC-1）、第 2 題「要標題列」（AC-1、AC-2）、第 2-1 題「照建議」＝欄名 `id,title,done`（AC-1、AC-2）、第 3 題「照建議」＝`true`／`false`（AC-1、AC-3）。AC-3 的跳脫行為屬「匯出成 CSV」的格式要求，已於同日首則回覆揭露為假設。

## 風險與首要驗證

**風險**: Low — 無明顯未知，依一般相依順序實作與驗證

## 實作與驗證步驟
1. 📝 **AC-1～AC-3：export 指令輸出 CSV** — 產出：`todo.py`、`test_todo.py`；相依：無 — 驗證方式：`python3 -m unittest -v`，先取得 AC-1～AC-3 因缺少 export 而失敗的紅燈，實作後全綠，既有 `test_render_marks_done` 維持通過
   - 完成證據：{執行時回寫紅綠燈命令與輸出}
2. 📝 **常青文件：根目錄 README 使用說明** — 產出：`README.md` 新增 `python3 todo.py export`：匯出 CSV 到標準輸出；相依：步驟 1 — 驗證方式：靜態檢查使用說明列出的指令與實作一致（純文件，不適用紅燈）
   - 完成證據：{執行時回寫}

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-10-18 | 建立；AC-1～AC-3 經逐題確認核准 | - |

---
**建立日期**: 2026-10-18  
**分級**: Small  
**風險**: Low\
**狀態**: 待實作
