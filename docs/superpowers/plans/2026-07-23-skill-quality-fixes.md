# Skill 品質修正實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修正六項會破壞 skill 契約安全、文件一致性、任務完成判定與輸出可信度的問題。

**Architecture:** 先修正 `docs/AGENTS.md` 的權威分級與時序規範，再讓 `new-issue`、`execute-task` 與 `decompose` 透過明確完成 gate 消費該規範；`code-simplify`、`git-squash` 與 `create-pr` 各自收斂為證據驅動的獨立契約。所有 workflow 都由 `scripts/sync-skills.py` 從 skill 單向產生。

**Tech Stack:** Markdown、YAML frontmatter、Python 3 同步腳本、Git、POSIX shell quoting

---

## 檔案配置

- `docs/AGENTS.md`：issue 文件分級、README 範本、Agent 工作時序的唯一權威來源。
- `skills/new-issue/SKILL.md`：驗證輸入、讀取權威規範、建立並核對分級文件集合。
- `skills/execute-task/SKILL.md`：執行單一任務、驗證完成條件並回寫權威任務狀態。
- `skills/decompose/SKILL.md`：產生具完成判準、驗證方式與完整覆蓋關係的 Task。
- `skills/code-simplify/SKILL.md`：只做可證明不改變公開行為與契約的簡化。
- `skills/git-squash/SKILL.md`：輸出經 POSIX shell 安全引用的 squash 指令。
- `skills/create-pr/SKILL.md`：以可追溯證據產生 PR 說明與測試狀態。
- `workflows/shared/*.md`：由同步腳本產生，不手動修改。

### Task 1：統一 issue 分級範本與 Agent 工作時序

**Files:**
- Modify: `docs/AGENTS.md:128-235`
- Modify: `docs/AGENTS.md:311-325`
- Modify: `docs/AGENTS.md:386-392`

- [ ] **Step 1：將 README 標準範本拆成 Medium 與 Large 文件清單**

保留共用 README 內容，但把「文件清單」改為明確分支：

```markdown
## 文件清單

<!-- Medium 僅列出實際建立的 implementation-plan.md；Large 才列出完整三份附屬文件。 -->

### Medium
1. **[implementation-plan.md](./implementation-plan.md)** 📋
   - 分析概要、實作步驟、測試策略與風險驗證

### Large
1. **[requirement-analysis.md](./requirement-analysis.md)** 🔍
   - 需求邊界與現況分析
2. **[technical-analysis.md](./technical-analysis.md)** 🔍
   - 技術方案與架構影響
3. **[implementation-plan.md](./implementation-plan.md)** 📋
   - 實作步驟、測試策略與風險驗證
```

在範本前明確要求產出時只保留對應分級的分支，不得把另一分支一併寫入 README。

- [ ] **Step 2：將 Agent 初建流程改成分級分支**

以以下順序取代固定四件套流程：

```markdown
1. **接收與理解**：閱讀 User Request，確認 issue ID 與核心目標；必要輸入不足時先詢問，不得猜測。
2. **探索與分級**：閱讀 workspace 現況，分別判定規模與風險，並決定文件集合與首要驗證。
3. **初步建立**：建立 `README.md`，填寫 metadata、已知資訊與初始 Timeline。
4. **依規模建立文件**：
   - Small：不建立其他文件，將需求、風險及可執行步驟寫入 README。
   - Medium：建立 `implementation-plan.md`，將分析概要、實作步驟與驗證寫入該檔。
   - Large：依序建立 `requirement-analysis.md`、`technical-analysis.md` 與 `implementation-plan.md`。
5. **完整性檢查**：確認實際文件集合、README 連結、metadata 與任務清單符合分級規範。
6. **執行與更新**：開始實作後依 Timeline 與 Changelog 規則保留時序。
```

- [ ] **Step 3：更新文件 metadata 與 Changelog**

使用系統日期 `2026-07-23`，將最後更新日期及版本更新為下一版，並新增一筆說明「README 文件清單與 Agent 工作時序依 Small／Medium／Large 分流」。

- [ ] **Step 4：人工核對權威規範沒有互斥指示**

逐項確認：Small 只要求 README、Medium 只要求 README 與 implementation plan、Large 才要求四件套；README 連結與 Agent 工作時序皆符合相同集合。

### Task 2：讓 new-issue 只協調權威規範

**Files:**
- Modify: `skills/new-issue/SKILL.md:7-79`

- [ ] **Step 1：重排必要輸入與停止條件**

明定 issue ID 與核心目標為必要輸入；任一缺漏時列出缺項並停止建立文件。保留自然語言與 `/new-issue` 兩種解析方式。

- [ ] **Step 2：移除重複的完整分級表與風險手段清單**

以單一權威指示取代 `### 規模`、`### 風險` 的重述內容：

```markdown
## 規劃與建檔

1. 完整讀取 `docs/AGENTS.md` 的「文件動態分級規範」、「文件類型與內容規範」、「README.md 範本」與「Agent 工作流程與時序保留」。
2. 分別判定規模與風險；兩者不得互相推導。
3. 只建立該規模要求的文件，並依權威規範填寫 metadata、任務清單、首要驗證與完成證據。
4. 若核心需求、變更邊界或必要驗證仍有阻塞未知，先詢問使用者，不得以「待確認」取代必要決策後繼續建檔。
```

- [ ] **Step 3：加入 exhaustive 完成 gate**

要求結束前逐項核對：文件集合精確符合分級、README 沒有不存在的連結、metadata 完整、任務清單有產出與完成判準、所有阻塞未知已處理或明確停止。

- [ ] **Step 4：保留最小對話輸出契約**

對話僅輸出分析摘要、規模與風險、已建立／更新檔案、阻塞問題及待確認事項，不重複完整文件。

### Task 3：建立 Task 完成與文件回寫閉環

**Files:**
- Modify: `skills/execute-task/SKILL.md:5-128`

- [ ] **Step 1：明定 required inputs 與阻塞分支**

要求 issue ID、分級、風險、指定步驟／Task、該項完成判準與驗證方式全部可取得；缺少任一必要資訊時停止實作並回到規劃階段。

- [ ] **Step 2：把基本驗證改為證據 gate**

要求先找出專案可用的 build、test、lint、typecheck 或等效檢查，再執行所有與本 Task 相關的驗證。每項記錄命令、結果；不適用或無法執行時記錄原因與殘餘風險。所有 Task 完成判準與必要驗證都通過後才能進入文件更新。

- [ ] **Step 3：新增權威狀態回寫步驟**

成功後必須：

```markdown
1. 在原任務清單將指定步驟／Task 標記為已完成。
2. 在同一任務項目記錄驗證方式與實際證據。
3. 以系統日期更新 README Timeline。
4. 依 `docs/AGENTS.md` 更新受影響文件的 Changelog；若現況與舊描述不同，以帶日期的 NOTE 補充，不覆寫歷史描述。
```

任一回寫未完成時，本次 Task 不得宣稱完整完成。

- [ ] **Step 4：移除獨立報告與程式碼副本**

刪除要求輸出 `# Task Implementation` 到 issue 資料夾及 `## Code` 區塊，改為對話摘要：Task、Summary、Modified Files、Verification Evidence、Document Updates、Residual Risks。

### Task 4：補齊 decompose 的可執行完成契約

**Files:**
- Modify: `skills/decompose/SKILL.md:90-201`

- [ ] **Step 1：擴充每個 Task 的必要欄位**

將 Task schema 統一為：

```markdown
#### Task 1.1

* 任務說明：<單一、明確的工程責任>
* 預期產出：<可檢查的檔案或行為>
* 涉及模組或檔案：<repo-relative paths>
* 完成判準：<可觀察且全部必須成立的條件>
* 驗證方式：<可重複執行的命令、測試或觀察程序>
* 覆蓋項目：<對應的需求、交付成果或風險證據識別>
```

- [ ] **Step 2：新增完整覆蓋 gate**

輸出前建立覆蓋核對：Implementation Plan 中每項需求、交付成果與風險證據都必須指定唯一的責任 Task；沒有未映射項目，也沒有責任重複。其他支援 Task 可以引用同一項目，但必須寫清楚支援邊界與整合點，不得成為第二個責任歸屬。

- [ ] **Step 3：強化完成條件用語**

將主觀的「應具備」「盡量」保留給粒度啟發式；將 Task 欄位、覆蓋檢查、Phase 1 風險證據統一改為「必須」與「完成 gate」。

### Task 5：保護 code-simplify 的公開契約

**Files:**
- Modify: `skills/code-simplify/SKILL.md:9-45`
- Modify: `skills/code-simplify/SKILL.md:53-64`

- [ ] **Step 1：新增最高優先安全 gate**

在所有簡化規則前明定：行為、公開 API、跨模組契約、DI token、反射／序列化 metadata、override 與 callback 簽章不得改變；與其他簡化規則衝突時，以此 gate 為準。

- [ ] **Step 2：將強制刪除改為證據條件**

只有確認沒有外部引用或契約用途，且適用驗證通過時，才能移除 Interface、Abstract Class、參數或泛型。無法證明時保留原狀，不以「目前只有單一實作」或「函式內未讀取」作為充分理由。

- [ ] **Step 3：增加合法 no-op 與驗證輸出**

若沒有安全且實質提升清晰度的變更，保持原狀並回報原因。若有修改，列出執行的驗證與結果；驗證失敗時還原本次簡化，不宣稱完成。

### Task 6：安全引用 git-squash 的動態 Shell 參數

**Files:**
- Modify: `skills/git-squash/SKILL.md:21-48`

- [ ] **Step 1：定義 POSIX shell 單引號規則**

要求 branch、subject、body 等所有動態參數以單引號包住。內容中的每個 `'` 必須用結束引用、`\'`、重新開始引用的方式表示，例如：

```bash
git commit -m '#3403 fix(member): 修正 O'\''Brien 帳號' -m '- fix: 避免 $(command) 與 `command` 被 Shell 展開'
```

- [ ] **Step 2：修正三步驟範例與完成 gate**

Step 1 的基準分支、Step 2 的功能分支及 Step 3 的 subject/body 都使用同一引用規則。輸出前逐一檢查動態參數；任一值未安全引用時不得輸出可執行命令。

- [ ] **Step 3：修正兩個 `-m` 的說明**

只說明第一個 `-m` 是 subject、第二個是 body；移除「為了保留 `#`」的錯誤因果。

### Task 7：讓 create-pr 的每項聲明都可追溯

**Files:**
- Modify: `skills/create-pr/SKILL.md:5-46`

- [ ] **Step 1：建立輸入證據順序**

要求依序取得指定 commit 範圍、commit 訊息、淨 diff、檔案清單、可取得的 issue／需求文件及實際驗證紀錄。commit 範圍不明時先詢問，不得自行任選。

- [ ] **Step 2：加入事實追溯 gate**

Why 必須來自需求或 commit 意圖；How 與變更清單必須來自淨 diff 與相關文件；測試驗證必須來自實際執行紀錄。無法證實的內容標示未知或不輸出，不得從程式碼反向捏造動機。

- [ ] **Step 3：重寫測試與選用區塊規則**

有證據時列出實際命令／案例與結果；沒有證據時固定輸出：

```markdown
### 測試驗證

- **未執行**：<未執行的檢查>
- **原因**：<可證實的原因>
- **殘餘風險**：<合併前仍需確認的事項>
```

截圖、補充說明與相關連結沒有內容時整段省略。所有範例 placeholder 必須在最終輸出移除。

### Task 8：同步 workflows 並驗證六項契約

**Files:**
- Generate: `workflows/shared/code-simplify.md`
- Generate: `workflows/shared/new-issue.md`
- Generate: `workflows/shared/execute-task.md`
- Generate: `workflows/shared/decompose.md`
- Generate: `workflows/shared/git-squash.md`
- Generate: `workflows/shared/create-pr.md`
- Modify: `docs/superpowers/specs/2026-07-23-skill-quality-fixes-design.md`

- [ ] **Step 1：執行同步腳本**

Run: `python3 scripts/sync-skills.py`

Expected: 顯示 9 組 `Synced:`，最後顯示 `Successfully synced 9 skills to workflows/shared.`

- [ ] **Step 2：執行完整同步檢查**

Run: `python3 scripts/sync-skills.py --check`

Expected: `OK: 所有 skill/workflow 配對已同步，workflows/README.md 描述一致，雙語規則章節數一致。`

- [ ] **Step 3：檢查 Markdown 空白錯誤**

Run: `git diff --check`

Expected: 無輸出，exit code 0。

- [ ] **Step 4：逐項人工驗收**

確認：

- `code-simplify` 無法僅因單一實作或未讀參數就修改契約。
- Small／Medium／Large 的文件集合、README 連結與 Agent 時序一致。
- `execute-task` 未更新原任務狀態與驗證證據時不能完成。
- 每個 decomposition Task 都有完成判準、驗證方式與覆蓋項目。
- `git-squash` 對 branch、subject、body 使用安全單引號引用並處理內含單引號。
- `create-pr` 沒有證據時明列未執行、原因與殘餘風險，不產生虛構測試。

- [ ] **Step 5：更新設計規格狀態**

將 `docs/superpowers/specs/2026-07-23-skill-quality-fixes-design.md` 的狀態由「待實作」改為「已實作」，並確認工作區原有 `.serena/project.yml` 異動未被修改。

> 本計畫不包含 commit 步驟；只有使用者明確要求時才建立 commit。
