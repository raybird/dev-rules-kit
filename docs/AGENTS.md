# 文件資料夾說明（AGENTS）

本文件為 `docs/` 資料夾的規範說明，協助 AI Agent 理解文件結構、命名規範與撰寫標準。

## 資料夾用途

`docs/` 資料夾用於存放專案的技術文件、議題分析、實作計劃與相關文件。每個議題（Issue）通常會有獨立的資料夾，包含完整的分析、計劃與實作記錄。

## 資料夾結構規範

### 總體架構

```
docs/
├── _templates/              # 文件模板
│   ├── architecture-template.md
│   ├── domain-template.md
│   └── changelog-template.md
├── architecture/            # 系統架構文件
│   ├── system-overview.md   # 系統總覽
│   ├── shared-services.md   # 共用服務
│   └── projects/            # 各子專案架構
│       ├── angular.md
│       ├── member.md
│       └── site-ssr.md
├── domain/                  # 業務領域文件
│   └── auth.md              # 認證領域
├── operations/              # 維運文件
│   ├── environment-setup.md
│   ├── release-process.md
│   ├── incident-handling.md
│   └── monitoring-logging.md
├── changelog/               # 發布紀錄
│   └── YYYY-MM-DD-release.md
├── issues/                  # Issue 文件目錄
│   └── issue-XXXX/          # 各 Issue 的文件
└── AGENTS.md                # 本說明文件
```

### Issue 資料夾命名

- **格式**：`issues/issue-{編號}/`
- **範例**：
  - `issues/issue-3240/` - Issue #3240 的相關文件
  - `issues/issue-3238/` - Issue #3238 的相關文件
  - `issues/issue-3221/` - Issue #3221 的相關文件

### 標準文件結構

每個 issue 資料夾建議包含以下文件：

1. **README.md** ⭐（必備）
   - 議題概述與快速導覽
   - 文件清單與用途說明
   - 關鍵差異對照表
   - 涉及檔案清單
   - 重構步驟概要
   - 維護紀錄

2. **requirement-analysis.md** ⭐（建議）
   - 需求描述
   - 現況分析
   - 問題點總結
   - 目標與涉及檔案

3. **implementation-plan.md** 📋（建議）
   - 設計方案
   - 實作步驟（分階段）
   - 使用方式對照
   - 測試策略
   - 風險評估
   - 檢查清單

4. **其他專項文件**（視需要）
   - `refactoring-notes.md` - 檔案重構說明
   - `migration-plan.md` - 遷移計劃
   - `technical-analysis.md` - 技術分析
   - `test-cases.md` - 測試案例
   - 等等

## 文件撰寫規範

### README.md 標準格式

```markdown
# Issue {編號} - {標題}

## 概述
{簡要說明議題目標}

## 文件清單
### 主要文件
1. **[requirement-analysis.md](./requirement-analysis.md)** ⭐
   - {說明}

2. **[technical-analysis.md](./technical-analysis.md)** 🔍
   - {說明}

3. **[implementation-plan.md](./implementation-plan.md)** 📋
   - {說明}

## 快速導覽
### 當前流程
{流程說明}

### 重構後流程
{流程說明}

## 關鍵差異
| 項目 | 變更前 | 變更後 |
|------|--------|--------|

## 涉及檔案
### {模組名稱}
- `{檔案路徑}` - {說明}

## 重構步驟概要
1. ✅ **步驟 1** - {狀態}
2. ⏳ **步驟 2** - {狀態}

## 維護紀錄
| 日期 | 異動 | 負責人 |
|------|------|--------|
| YYYY-MM-DD | {說明} | - |

---
**建立日期**: YYYY-MM-DD  
**最後更新**: YYYY-MM-DD  
**文件版本**: X.X  
**狀態**: {狀態}
```

### 日期規範

- **日期格式**：使用 `YYYY-MM-DD` 格式（例如：2026-12-19）
- **時間來源**：**使用系統當時的時間為準**
  - 建立文件時，使用系統當天的日期
  - 更新文件時，使用系統當天的日期
  - 維護紀錄中的日期，應反映實際變更發生的系統日期
- **建立日期**：文件初次建立的日期（系統當時日期）
- **最後更新**：文件最後修改的日期（系統當時日期）
- **維護紀錄**：依實際變更時間記錄，不要全部統一為同一天
  - 例如：系統日期 12-18 建立文件，系統日期 12-19 進行檔案重構，應分別記錄為 2026-12-18 和 2026-12-19
  - 每次異動都應使用該次異動發生時的系統日期

### 狀態標記

- ✅ 已完成
- ⏳ 進行中
- 📝 設計完成，待實作
- 🔄 重構中

### Emoji 使用規範

在文件清單中使用 emoji 標記文件類型：
- ⭐ 重要文件（必讀）
- 📋 計劃文件
- 🔧 實作指南
- 🔍 分析文件
- 📊 圖表/視覺化
- 🧪 測試相關
- 💡 簡化說明
- 🔄 重構說明

## 文件內容撰寫指南

### requirement-analysis.md

應包含：
- 需求描述
- 現況分析（詳細說明現有程式碼邏輯）
- 問題點總結
- 目標
- 涉及檔案清單

### implementation-plan.md

應包含：
- 設計方案（函式簽名、流程設計）
- 實作步驟（分階段，標記完成狀態）
- 使用方式對照（變更前後）
- 測試策略
- 風險評估
- 檢查清單

### refactoring-notes.md（如適用）

應包含：
- 重構時間
- 重構內容
- 重構緣由（詳細說明）
- 檔案結構變更
- 程式碼變更細節
- 驗證結果
- 影響範圍

## Agent 工作流程與時序保留 (Workflow & Timeline Tracking)

在開發或是逐步推進的 Issue 中，經常會發生「文件建立時間」與「逐步實作時間」產生落差的情況。為避免後續接手人員因為「描繪舊狀態的設計文件」對比「已經開發的程式碼」而產生誤會，Agent 必須遵守以下時序保留原則：

1. **接收與理解**：閱讀 User Request，建立 `docs/issues/issue-{ID}/` 目錄。
2. **初步建立**：建立 `README.md` (填寫已知資訊與初始 Timeline)。
3. **需求分析**：撰寫 `requirement-analysis.md`，確認需求邊界。結尾附上 `## 修訂紀錄 (Changelog)`。
4. **技術分析**：閱讀程式碼，撰寫 `technical-analysis.md`。結尾附上 `## 修訂紀錄 (Changelog)`。
5. **規劃實作**：根據分析結果，撰寫 `implementation-plan.md`。結尾附上 `## 修訂紀錄 (Changelog)`。
6. **執行與更新 (重要)**：開始 Coding 後，若發現原始分析與現狀不符，**不應直接抹除舊文件的歷史描述**，而是：
   - 在 `README.md` 的 `Timeline` 區塊加上開發進度與日期。
   - 在 `implementation-plan.md` 或其他文件的對應段落，使用 Github Alert 語法 (如 `> [!NOTE]`) 加上標有日期的補充說明，指出何時的 commit 已經改變了先前的 As-Is 狀態。
   - 將異動簡述更新於各文件的 `Changelog` 中。

## 文件維護原則

1. **即時更新**：實作完成後應立即更新文件狀態
2. **日期準確**：維護紀錄應反映實際變更時間
3. **狀態追蹤**：使用清晰的狀態標記（✅ ⏳ 📝）
4. **完整性**：確保文件涵蓋所有重要資訊
5. **可讀性**：使用清晰的標題、列表和表格

## 常見文件類型範例

### 重構類議題（如 issue-3240）

- README.md - 概述與快速導覽
- requirement-analysis.md - 現況分析
- implementation-plan.md - 實作計劃
- refactoring-notes.md - 重構說明

### 遷移類議題（如 issue-3238）

- README.md - 概述與流程對照
- requirement-analysis.md - 需求分析
- migration-plan.md - 遷移策略
- implementation-guide.md - 實作指南

### 分析類議題（如 issue-3221）

- README.md - 文件索引
- {topic}-flow-analysis.md - 流程分析
- {topic}-blocking-factors.md - 阻擋因素
- flow-diagram.md - 流程圖
- simplified-guide.md - 簡化說明

## 注意事項

1. **語言**：所有文件使用繁體中文（台灣）
2. **日期格式**：使用 `YYYY-MM-DD` 格式（例如：2026-12-19）
3. **日期來源**：**必須使用系統當時的時間為準**，不要手動指定或統一日期
4. **檔案路徑**：使用相對路徑（例如：`./requirement-analysis.md`）
5. **程式碼區塊**：標註語言類型（例如：`typescript`、`bash`）
6. **連結**：使用 Markdown 連結格式，確保相對路徑正確

## 快速檢查清單

建立新 issue 文件時，確認：
- [ ] 已建立 `issue-{編號}/` 資料夾
- [ ] 已建立 `README.md` 並包含標準格式
- [ ] 已建立 `requirement-analysis.md`（如適用）
- [ ] 已建立 `technical-analysis.md`（如適用）
- [ ] 已建立 `implementation-plan.md`（如適用）
- [ ] 日期格式正確（YYYY-MM-DD）
- [ ] **日期使用系統當時的時間為準**
- [ ] 維護紀錄反映實際變更時間（使用各次變更時的系統日期）
- [ ] 文件連結路徑正確
- [ ] 狀態標記清晰

---

**建立日期**: 2026-04-27  
**最後更新**: 2026-06-20  
**文件版本**: 1.0  
**適用範圍**: `docs/` 資料夾所有文件
