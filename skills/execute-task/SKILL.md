---
description: 根據 Implementation Plan Decomposition 執行指定的 Phase 或 Task 並實作程式碼
---

## Input

請先讀取以下內容：

- Implementation Plan
- Implementation Plan Decomposition
- 專案現有程式碼

## Execute Scope

請根據以下來源執行開發任務：

* 來源：**Implementation Plan Decomposition**
* 執行對象：指定的 **Phase / Task**
* 目標：實作對應功能並產出完整且可運行的程式碼

執行時應遵守以下原則：

* 僅實作當前指定的 Task
* 不應修改與任務無關的模組
* 必須遵守既有架構設計
* 產出的程式碼應可直接整合至專案

---

## Execute Tasks

1. **理解任務內容**

   * 讀取指定 Phase 與 Task
   * 確認任務目標與預期輸出
   * 確認相關模組與檔案

2. **分析現有程式碼**

   * 找出相關模組與既有邏輯
   * 確認現有設計模式
   * 避免破壞既有功能

3. **實作程式碼**

   * 根據 Task 實作必要功能
   * 遵守專案架構與命名規則
   * 確保程式邏輯清晰且可維護

4. **確保程式品質**

   * 程式碼需具備良好可讀性
   * 避免重複邏輯
   * 適當使用抽象與模組化

5. **基本驗證**

   * 確認程式可成功編譯
   * 確認沒有明顯錯誤
   * 確認未破壞既有功能

---

## Output

請輸出本次任務的實作結果，並遵循以下格式：

```markdown

# Task Implementation

## Phase

<Phase 名稱>

## Task

<Task 名稱>

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

```

---

## 注意事項

* 僅實作指定 Task
* 避免同時處理多個 Task
* 若任務依賴尚未完成的 Task，需明確指出
* 若發現架構問題或設計衝突，需在 Summary 中說明
* 結果輸出到與 Implementation Plan 相同資料夾檔案內
