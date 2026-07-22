# Issue 規模與風險雙軸 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 issue 評估改為「規模決定文件、風險決定驗證順序」雙軸模型，並防止 Agent 將風險優先誤讀為一律採用垂直切片。

**Architecture:** `docs/AGENTS.md` 維持唯一權威來源，定義雙軸、風險判準與決策流程；`new-issue` 負責評估並寫入 metadata，`decompose` 負責依最大未知選擇 Phase 1，`execute-task` 負責保存驗證證據。只修改 `skills/` 來源，再用 `scripts/sync-skills.py` 逐位元組同步至 `workflows/shared/`。

**Tech Stack:** Markdown、YAML frontmatter、Python 3 同步檢查腳本

---

## 檔案配置

- 修改 `docs/AGENTS.md`：雙軸唯一權威定義、README 範本、檢查清單與修訂紀錄。
- 修改 `skills/new-issue/SKILL.md`：分開評估規模與風險，產生風險決策紀錄。
- 修改 `skills/decompose/SKILL.md`：用風險來源選擇 Phase 1，加入垂直切片防誤用問題。
- 修改 `skills/execute-task/SKILL.md`：讀取風險資訊並記錄首要驗證的完成證據。
- 修改 `skills/dev-cycle/SKILL.md`：明訂風險不影響流程分支，舊 issue 不自動推測風險。
- 修改 `docs/usage.md`：更新 OAuth 示例並加入雙軸反例。
- 修改 `CHANGELOG.md`：記錄下游需要重新複製的行為變更。
- 修改 `docs/superpowers/specs/2026-07-22-issue-size-risk-design.md`：完成後將狀態更新為「已實作」。
- 由腳本更新 `workflows/shared/new-issue.md`、`workflows/shared/decompose.md`、`workflows/shared/execute-task.md`、`workflows/shared/dev-cycle.md`。

### Task 1: 建立雙軸權威規範

**Files:**
- Modify: `docs/AGENTS.md:16-39`
- Modify: `docs/AGENTS.md:108-117`
- Modify: `docs/AGENTS.md:151-211`
- Modify: `docs/AGENTS.md:300-322`

- [ ] **Step 1: 將單一分級規範改成雙軸定義**

在既有「文件動態分級規範」保留 Small／Medium／Large 表格，明訂：

```markdown
Issue 必須分別評估兩個互不推導的軸：

- **規模（`**分級**`）**：只決定文件數量、任務清單來源及是否需要 `decompose`。
- **風險（`**風險**`）**：只決定實作順序、首要驗證手段及必要證據，不改變文件數量。
```

加入 Low／Medium／High 表格；High 至少涵蓋資料損失、安全／權限、不可逆操作、廣泛影響及核心外部行為未知。明訂任一高風險條件成立即採 High，不使用加總分數。

- [ ] **Step 2: 加入風險決策流程與手段表**

以「最大未知或後果 → 風險等級與理由 → 首要驗證 → 完成證據 → 排後續步驟」作為強制順序，並加入下列候選手段：

```markdown
| 風險來源 | 優先手段範例 |
|---|---|
| 外部契約未知 | 契約驗證、最小真實請求、相容性探測 |
| 資料樣態未知 | 資料盤點、分布查詢、小樣本 dry run |
| 效能未知 | 基準測試、壓力測試、最小技術實驗 |
| 既有行為可能被破壞 | Characterization test、快照、對比腳本、回歸測試網 |
| 端到端整合或使用者行為未知 | 垂直切片 |
| 無明顯未知 | 一般技術相依順序 |
```

- [ ] **Step 3: 加入垂直切片防誤用規則**

加入設計規格中的強制提示，並要求選擇垂直切片時回答三件事：驗證哪個端到端假設、為何其他手段不更直接、完成後需要什麼證據。

- [ ] **Step 4: 更新 README 範本與檢查清單**

在 Standard 與 Small metadata 的 `**分級**` 下一行加入：

```markdown
**風險**: Low | Medium | High
```

在兩種文件的規劃內容要求記錄「最大風險、首要驗證、選擇理由、完成證據」。快速檢查清單加入 `**風險**` 欄位及首要驗證是否排在主要實作前。

- [ ] **Step 5: 更新文件版本與修訂紀錄**

使用日期 `2026-07-22` 更新「最後更新」、提升文件版本，並新增雙軸規範的修訂紀錄；不得覆蓋 2026-07-21 的既有紀錄。

- [ ] **Step 6: 人工檢查規模與風險沒有互相推導**

確認規則可同時容納：

```text
Small + High：文件仍只有 README，但第一步先建立權限回歸證據。
Large + Low：文件仍是完整四件套，但 Phase 可依一般相依順序排列。
```

### Task 2: 讓 new-issue 分別評估規模與風險

**Files:**
- Modify: `skills/new-issue/SKILL.md:29-48`

- [ ] **Step 1: 保留規模分級但移除「未知大就升級 Large」的耦合**

刪除「Medium 出現重大未知就升級 Large」規則，改為規模只看修改範圍、結構複雜度與工作量。若範圍本身擴大才調整規模，不能只因風險高而升級。

- [ ] **Step 2: 加入獨立風險評估**

要求依 `docs/AGENTS.md` 判定 Low／Medium／High，將結果寫入 README：

```markdown
**分級**: Small | Medium | Large\
**風險**: Low | Medium | High
```

舊 issue 沒有風險欄位時，不得從分級或檔案數量猜測。

- [ ] **Step 3: 強制產生風險決策紀錄**

Small 的 README 與 Medium／Large 的 Implementation Plan 都必須包含：

```markdown
## 風險與首要驗證

- **最大風險**：...
- **風險等級與理由**：...
- **首要驗證**：...
- **選擇理由**：...
- **完成證據**：...
```

Low risk 若無特殊前置驗證，仍需明確寫「無明顯未知，依一般相依順序實作」及一般驗證條件。

- [ ] **Step 4: 檢查輸出要求沒有增加額外文件**

確認 Small、Medium、Large 的文件數量與既有規則完全相同，高風險不會建立額外分析文件。

### Task 3: 讓 decompose 先選驗證手段，再決定 Phase 1

**Files:**
- Modify: `skills/decompose/SKILL.md:11-17`
- Modify: `skills/decompose/SKILL.md:36-60`
- Modify: `skills/decompose/SKILL.md:111-157`

- [ ] **Step 1: 將 README 與風險紀錄加入輸入**

要求先讀 README 的 `**風險**`，以及 Implementation Plan 的「風險與首要驗證」段落；若新 issue 缺少任一項，回到規劃階段補齊，不自行從分級推測。

- [ ] **Step 2: 將 Phase 切分原則改成決策樹**

先要求指出最大未知，再從契約驗證、資料盤點、效能實驗、回歸保護網、垂直切片或一般相依順序中選擇手段。將現有「外部整合或使用者行為都採垂直切片」拆開：外部契約本身未知優先契約探測，跨層互動未知才考慮垂直切片。

- [ ] **Step 3: 加入不可先選垂直切片的強制提示**

逐字加入設計規格的防誤用提示與三個必答問題。若無法回答，規則要求重新選擇首要驗證手段。

- [ ] **Step 4: 更新正反例**

保留 OAuth 垂直切片作為「端到端 callback 行為未知」的適用案例，另加入資料遷移先盤點與 dry run 的案例，避免整節只有垂直切片成功範例。

- [ ] **Step 5: 更新 decomposition 輸出格式**

在 Phase 1 前加入：

```markdown
## Risk Decision

* 最大風險：...
* 首要驗證：...
* 選擇理由：...
* 完成證據：...
```

Phase 1 的 Goal 與 Deliverables 必須能對應這份決策及證據。

### Task 4: 保存驗證證據並維持 dev-cycle 分流單純

**Files:**
- Modify: `skills/execute-task/SKILL.md:5-23`
- Modify: `skills/execute-task/SKILL.md:42-70`
- Modify: `skills/execute-task/SKILL.md:74-108`
- Modify: `skills/dev-cycle/SKILL.md:20-38`

- [ ] **Step 1: execute-task 讀取風險與完成證據**

在 Input 加入 README 的 `**風險**` 與任務文件中的「完成證據」。明訂 execute-task 不重新排列已核准的步驟，只執行目前指定項目。

- [ ] **Step 2: 首要驗證任務必須輸出實際證據**

在基本驗證及 Output 增加：

```markdown
## Risk Validation Evidence

（若本 Task 是首要驗證，記錄實際觀察結果、執行方式與是否符合原訂完成證據；否則省略。）
```

禁止只寫「已驗證」而沒有命令結果、樣本觀察、測試輸出或其他可重複確認資訊。

- [ ] **Step 3: dev-cycle 明訂風險不形成流程分支**

在分級判定後補充：`**風險**` 只影響任務順序與驗證方式，不影響 `decompose` 或狀態偵測；舊 issue 缺少風險時不自動推測，只有重新規劃或新增步驟時才補評估。

### Task 5: 更新使用說明與發布紀錄

**Files:**
- Modify: `docs/usage.md:9-58`
- Modify: `docs/usage.md:154-205`
- Modify: `docs/usage.md:272-284`
- Modify: `CHANGELOG.md:13`
- Modify: `docs/superpowers/specs/2026-07-22-issue-size-risk-design.md:4`

- [ ] **Step 1: OAuth 範例標示兩軸**

將範例明確標示為 `Large + High`，說明 Large 來自跨模組與架構整合，High 來自真實 callback 與帳號綁定行為尚未確認，兩者是獨立判斷。

- [ ] **Step 2: 修正垂直切片說明**

說明 OAuth 採垂直切片是因為最大未知位於端到端登入行為；加入「若未知只在 Google API 契約，應先做最小真實請求，不必先串完整登入流程」。

- [ ] **Step 3: 加入雙軸對照例**

至少加入：

```text
Small + High：單行權限條件修正；只產出 README，但先建立權限回歸案例。
Large + Low：規格已凍結的跨模組搬移；仍建立完整文件並 decompose，但可按技術相依順序執行。
```

- [ ] **Step 4: 更新快速參考與文件 metadata**

`new-issue` 注意事項加入 `**風險**`；`decompose` 注意事項加入「先選驗證手段，不預設垂直切片」；使用日期 `2026-07-22` 更新維護紀錄、最後更新與版本。

- [ ] **Step 5: 新增 Changelog 條目**

在最新條目前新增一筆 Minor 行為變更，列出 `docs/`、`skills/`、`workflows/shared/` 的下游更新影響；不要修改既有歷史條目。

- [ ] **Step 6: 更新設計規格狀態**

所有修改及驗證完成後，將設計規格的 `**狀態**` 從「待實作」改為「已實作」。

### Task 6: 同步並驗證全部規則

**Files:**
- Generate: `workflows/shared/new-issue.md`
- Generate: `workflows/shared/decompose.md`
- Generate: `workflows/shared/execute-task.md`
- Generate: `workflows/shared/dev-cycle.md`

- [ ] **Step 1: 執行 skill/workflow 同步**

Run:

```bash
python3 scripts/sync-skills.py
```

Expected: 列出四個已更新的 workflow，不手動編輯 `workflows/shared/`。

- [ ] **Step 2: 執行同步與文件一致性檢查**

Run:

```bash
python3 scripts/sync-skills.py --check
```

Expected:

```text
OK: 所有 skill/workflow 配對已同步，workflows/README.md 描述一致，雙語規則章節數一致。
```

- [ ] **Step 3: 檢查 Markdown whitespace**

Run:

```bash
git diff --check
```

Expected: 無輸出，exit code 0。

- [ ] **Step 4: 情境乾跑**

逐一用規則判定以下六種案例，確認得到預期的文件與首要活動：

```text
Small + Low 文案修正 → README；一般相依順序
Small + High 權限修正 → README；回歸保護網
Medium + Medium 套件整合 → README + plan；契約探測
Large + High 資料遷移 → 四件套 + decompose；資料盤點與 dry run
Large + High OAuth → 四件套 + decompose；端到端未知時採垂直切片
Large + Low 機械式搬移 → 四件套 + decompose；一般技術相依順序
```

- [ ] **Step 5: 檢查變更範圍**

Run:

```bash
git status --short
```

Expected: 只包含本計畫列出的規範、skill、同步 workflow、使用說明、Changelog、spec 與 plan；不得出現無關檔案。

> 本計畫不自動建立 commit。若使用者明確要求提交，再依專案規範檢查 status、diff 與近期 log 後提交。
