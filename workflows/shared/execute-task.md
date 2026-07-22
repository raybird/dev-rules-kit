---
description: 根據 issue 的任務清單執行指定的實作步驟或 Phase / Task 並實作程式碼
---

## Input

請先讀取以下內容：

- issue 的 `README.md`（取得 `**分級**` 與 `**風險**` 欄位）
- 該分級對應的任務清單（見下方 Execute Scope）
- 任務文件「風險與首要驗證」或「Risk Decision」中的完成證據
- 專案現有程式碼

## Execute Scope

任務清單來源依 issue 分級而定（分級規則的權威定義見 `docs/AGENTS.md`「文件動態分級規範」，下表為摘要）：

| 分級 | 任務清單來源 | 執行對象 |
|---|---|---|
| Small | `README.md` 的「實作與驗證步驟」 | 指定的**步驟** |
| Medium | `implementation-plan.md` 的「實作步驟」 | 指定的**步驟** |
| Large | Implementation Plan Decomposition | 指定的 **Phase / Task** |

目標：實作對應功能並產出完整且可運行的程式碼。

風險已在規劃階段決定任務順序。執行時不得自行重排或改寫已核准的風險策略，只執行目前指定的步驟 / Task；若必要風險資訊缺漏，先回到規劃階段補齊。

執行時應遵守以下原則：

* 僅實作當前指定的 Task
* 不應修改與任務無關的模組
* 必須遵守既有架構設計
* 產出的程式碼應可直接整合至專案

---

## Execute Tasks

1. **確認工作分支**

   * 檢查當前分支：若位於 main / master 等主幹分支，先建立並切換至 issue 分支再開始實作
   * 分支命名：以 `issue-{ID}` 開頭，可加簡短描述後綴（如 `issue-101-oauth-login`）
   * 分支名稱必須包含 issue ID，供 `dev-cycle` 狀態偵測使用

2. **理解任務內容**

   * 讀取指定的步驟（Small / Medium）或 Phase 與 Task（Large）
   * 確認任務目標與預期輸出
   * 確認相關模組與檔案
   * 若當前任務是首要驗證，確認預定的完成證據

3. **分析現有程式碼**

   * 找出相關模組與既有邏輯
   * 確認現有設計模式
   * 避免破壞既有功能

4. **實作程式碼**

   * 根據 Task 實作必要功能
   * 遵守專案架構與命名規則
   * 確保程式邏輯清晰且可維護

5. **確保程式品質**

   * 程式碼需具備良好可讀性
   * 避免重複邏輯
   * 適當使用抽象與模組化

6. **基本驗證**

   * 確認程式可成功編譯
   * 確認沒有明顯錯誤
   * 確認未破壞既有功能
   * 若當前任務是首要驗證，記錄實際觀察結果、執行方式及是否符合預定完成證據
   * 不得只寫「已驗證」；證據必須包含可重複確認的命令結果、測試輸出、樣本觀察或等效資訊

---

## Output

請輸出本次任務的實作結果，並遵循以下格式：

```markdown

# Task Implementation

## Phase

<Phase 名稱；Small / Medium 可省略此區塊>

## Task

<Task 名稱，或 Small / Medium 的步驟名稱>

## Summary

（簡要說明本次實作內容）

## Implemented Changes

* 說明新增或修改的功能
* 說明關鍵設計決策

## Modified Files

* path/to/file1
* path/to/file2

## Code

（輸出新增或修改的程式碼）

## Risk Validation Evidence

（若本 Task 是首要驗證，記錄實際觀察結果、執行方式與是否符合預定完成證據；否則省略此區塊。）

```

---

## 注意事項

* 僅實作指定的步驟 / Task
* 避免同時處理多個步驟 / Task
* 若任務依賴尚未完成的步驟 / Task，需明確指出
* 若發現架構問題或設計衝突，需在 Summary 中說明
* 結果輸出到該 issue 的 `docs/issues/issue-{ID}/` 資料夾內
