---
name: decompose
description: 將 Large issue 的 implementation plan 細化為可執行 Phase／Task，或在新增核准與規格修訂後補齊映射；Small／Medium 使用原步驟即可。
---

> 本 skill 需要 `docs/AGENTS.md` **流程契約 2.0**；相容性依該檔「核心層齊備性檢查」。

## 輸入與位置

讀 README、implementation-plan.md、project.md、acceptance.md 與 verification.md。取得已核准的驗收條件、風險策略與相依；只拆可實作的已核准部分。Small／Medium 已有可執行步驟時直接沿用，明確要求進一步細化時在原檔完成。

在 implementation-plan.md 原地細化，保留高階決策、穩定 Task ID 與已完成證據。舊 issue 已由 README 指向獨立 Decomposition 時，沿用該檔作唯一任務來源；不複製第二份狀態。Superpowers writing-plans 可用時用於拆解，產物位置仍依本節。

## 拆解

1. 確認 README 風險策略仍成立，引用其判定與首要驗證；需要改變策略時先處理必要決策。
2. 依可驗證里程碑劃 Phase，再依可獨立驗證的輸出劃 Task；數量與耗時不設配額。相依可以指向其他 Task，執行前必須滿足。
3. 每個 Task 記：ID／目標、預期產出、最小範圍、相依、驗收編號、完成判準、驗證策略。只有多人／多 Task 共同支援時才另寫責任與整合邊界。
4. 每個已核准 Scenario、交付成果與風險證據指定一個責任 Task；其他 Task 可支援但不重複責任。各任務依 verification.md 定義測試層級或等價證據；同層不增加重複紅燈。
5. 新核准 Scenario 補拆到原計畫；修訂的 Scenario 檢查任務與舊證據，受影響者更新為未完成。其他已核准任務照常保留。未核准項只連結 README，不能產生可執行 Task。

## 最小格式

```markdown
## Phase 1 — 可驗證里程碑

### Task 1.1 — 目標
- 產出與範圍：...
- 相依：無／Task ID
- 驗收編號：...
- 完成判準：...
- 驗證：外部行為與底層測試策略，或單迴圈理由／等價證據
- 狀態：📝 待實作
- 證據：執行時填入命令紀錄或 artifact 連結
```

## 完成判準

已核准集合與責任 Task 覆蓋集合完全一致；無循環相依，首要驗證先於依賴它的實作，每個 Task 可判定完成。回報計畫位置、補拆／修訂 Task 與待核准編號；存在待核准內容時只宣稱已核准部分拆解完成。
