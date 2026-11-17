# Issue 8 - 下游 repo 不再部署常青文件範本，document-types 的【應客製】改為範例

## 文件清單
- [implementation-plan.md](./implementation-plan.md)

## 概述

來源：[GitHub #8](https://github.com/raybird/dev-rules-kit/issues/8)。2026-11-17 檢視 `init-project.py` 部署到下游 repo 的內容時發現兩處不合理：

1. **`docs/_templates/` 部署到下游，但沒有人讀。** 三份常青文件範本（architecture、domain、changelog，共 157 行）沒有任何技能引用。全 kit 只有 `docs/agents/document-types.md` 的一句「順序與互動類的圖沿用 `docs/_templates/` 既有的 Mermaid」提到它，卻每次初始化與更新都部署到下游，也列入部署基線的雜湊追蹤。
2. **核心檔要求下游客製，與雜湊保護矛盾。** `docs/agents/document-types.md`「常見文件類型範例」標示【應客製】，請專案換成自己的組合。但這份是受部署基線保護的核心檔，下游照做之後，`--update` 會判為衝突並整批停止。這與 `docs/AGENTS.md`「專案內容集中於 project.md」的客製邊界矛盾。

2026-11-17 唯讀檢查本機 7 個已初始化的下游專案：7 個都部署了 `docs/_templates/`，沒有一個改過任何核心檔（部署基線的 10 個檔案雜湊全部相符），所以第 2 點的矛盾還沒有實際觸發。另有 1 個專案在自己的開發文件目錄樹裡列了 `_templates/`。

收錄依據（AGENTS.md「範圍」）：第 2 點屬 kit 規則互相矛盾。第 1 點下游沒有回報問題，屬清理；2026-11-17 維護者討論後決定一併處理。

**不在範圍**：`docs/agents/readme-templates.md` 留在 repo（2026-11-17 決定）。它屬於流程契約：v2.9 修訂紀錄把它列為契約材料，記帳判定也依「照範本寫成的表格」逐列判斷，必須跟著 commit 走。

## 現況

**現行 review**: review-151871c.md

| 外部狀態 | 查證命令 | 上次結果 | 查證日期 |
|---|---|---|---|
| GitHub #8 | gh issue view 8 --json state -q .state | OPEN | 2026-11-17 |

## 快速導覽

### 當前流程

`init-project.py` 部署 `docs/AGENTS.md`、`docs/agents/*.md` 與 `docs/_templates/*.md`，並在 `docs/.dev-rules-kit.json` 記錄它們的雜湊。document-types.md 的【應客製】一節請下游直接改寫核心檔。

### 重構後流程

`init-project.py` 只部署 `docs/AGENTS.md` 與 `docs/agents/*.md`。三份範本隨 execute-task 技能安裝在 `skills/execute-task/references/`。document-types.md 的範例只當參考，專案常用的文件組合登記在 project.md。

## 關鍵差異

| 項目 | 變更前 | 變更後 |
|------|--------|--------|
| 下游 repo 的 kit 檔案 | 11 份（另加部署基線） | 8 份（另加部署基線） |
| 常青文件範本位置 | `docs/_templates/`（每個下游 repo 一份） | `skills/execute-task/references/`（隨技能安裝） |
| 已部署的 `docs/_templates/` | 列入部署基線 | 留在原處、不再列入部署基線；CHANGELOG 說明可以手動刪除 |
| 【應客製】一節 | 請下游改寫核心檔 | 一般範例；專案常用的組合登記在 project.md |

## 涉及檔案

### 部署

- `scripts/init-project.py` - 部署清單移除 `_templates`
- `scripts/test-install.py` - 初始化清單更新；新增從舊部署基線升級的案例

### 範本與規範

- `docs/_templates/*.md` → `skills/execute-task/references/*.md` - 搬移，內容不變
- `skills/execute-task/SKILL.md` - 回寫步驟指向 references 的範本
- `docs/AGENTS.md` - 部署說明、常青文件段落補範本位置、文件版本與修訂紀錄
- `docs/agents/document-types.md` - 第 106 行不再引用 `docs/_templates/`；【應客製】改為範例說明

### 發布文件

- `CHANGELOG.md`；`docs/rule-verification-status.md`、README.md、docs/usage.md 只檢查有無需要跟著改的引用

## Gherkin 驗收劇本

```gherkin
Feature: 下游 repo 只保存流程契約，範本隨技能安裝

  @SCN-001
  Scenario: 新初始化不再部署常青文件範本
    Given 一個沒有 kit 檔案的暫存專案
    When 執行 init-project.py 初始化
    Then 專案內沒有 docs/_templates/ 目錄
    And docs/.dev-rules-kit.json 不含 docs/_templates/ 的條目
    And init-project.py --check 輸出 OK

  @SCN-002
  Scenario: 從舊版部署基線升級
    Given 一個以 v4.12.0 初始化、含 docs/_templates/ 三份範本與其基線條目的暫存專案
    When 先執行 init-project.py --update --dry-run，再執行 init-project.py --update
    Then dry-run 不寫入任何檔案
    And 更新成功，docs/_templates/ 的三份檔案保持原樣、沒有被刪除
    And docs/.dev-rules-kit.json 不再列出 docs/_templates/ 的條目
    And init-project.py --check 輸出 OK

  @SCN-003
  Scenario: 範本可從 execute-task 技能取得
    Given 本 issue 的分支
    When 檢視 skills/execute-task/references/ 與 docs/AGENTS.md「常青文件更新責任」
    Then references/ 裡有三份範本，內容與搬移前的 docs/_templates/ 相同
    And docs/AGENTS.md「常青文件更新責任」有一句：新建常青文件時，可參考 execute-task 技能 references/ 的範本
    And kit 內除了 CHANGELOG 與 issue 歷史文件，沒有文件再引用 docs/_templates/

  @SCN-004
  Scenario: 【應客製】一節改為範例
    Given 本 issue 的分支
    When 檢視 docs/agents/document-types.md「常見文件類型範例」
    Then 該節不再含「應客製」字樣
    And 說明下方組合是範例，專案常用的組合登記在 project.md
    And docs/agents/project.md 範本內容不變，PAST_TEMPLATES 不需要新增雜湊

  @SCN-005
  Scenario: CHANGELOG 說明已部署舊檔的處理
    Given 本版的 CHANGELOG 條目
    When 下游依條目更新
    Then 條目寫明 docs/_templates/ 不再部署，舊檔不會自動刪除，可以手動刪除
    And 寫明刪除前先檢查專案自己的文件有沒有引用 docs/_templates/

  @SCN-006
  Scenario: execute-task 回寫常青文件時指向範本
    Given 本 issue 的分支
    When 檢視 skills/execute-task/SKILL.md 的回寫步驟
    Then 步驟寫明新建常青文件時，可參考本技能 references/ 的範本
```

## Gherkin 核准紀錄
- **核准 commit**: c0c7e9f
- **核准來源**: 使用者於 2026-11-17 對話逐題確認的答案：「`docs/_templates/` 的去處」選「搬進 execute-task 技能」（SCN-001～003）、「readme-templates.md」選「留在 repo，不納入本 issue」（不在範圍）、「【應客製】」選「改成範例，指向 project.md」（SCN-004）、「已部署舊檔」選「CHANGELOG 說明可以手動刪除」（SCN-002 的「保持原樣」、SCN-005），並回覆「好，開 issue 處理這兩點」。SCN-006：同日逐題確認 TBD-1 選「要，兩處都寫」

| Scenario | 核准日期 | 狀態 |
|----------|---------|------|
| SCN-001 | 2026-11-17 | 已核准 |
| SCN-002 | 2026-11-17 | 已核准 |
| SCN-003 | 2026-11-17 | 已核准 |
| SCN-004 | 2026-11-17 | 已核准 |
| SCN-005 | 2026-11-17 | 已核准 |
| SCN-006 | 2026-11-17 | 已核准 |

## 重構步驟概要

任務與證據見 [implementation-plan.md](implementation-plan.md#實作步驟)。

## 風險與首要驗證

- **最大風險**：已初始化的下游專案升級時，舊部署基線裡的 `docs/_templates/` 條目讓 `--update` 或 `--check` 失敗，或者舊檔被誤刪
- **風險等級與理由**：Low。部署清單只少一個目錄，`init-project.py` 本來就以目前清單重寫基線、不刪除檔案；容易回復
- **首要驗證**：S1 先在 test-install.py 加入以舊基線升級的案例，再改 init-project.py
- **選擇理由**：直接在暫存專案重現下游的升級路徑；依維護指引，改部署行為要以暫存專案驗證
- **完成證據**：SCN-001、SCN-002 的案例先紅後綠，既有 test-install 案例（衝突時不部分寫入、dry-run、symlink）照常通過

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | SCN-006：execute-task SKILL.md 的回寫步驟要不要也指向 references/ 的範本 | 已解決：2026-11-17 使用者選「要，兩處都寫」；docs/AGENTS.md 是下游文件，不知道技能安裝在哪裡，技能本身知道自己的目錄 | SCN-006、S2 |
| TBD-2 | 版本號 | 已解決：2026-11-17 使用者選 Minor（v4.13.0）；沒有技能或規則依賴 `docs/_templates/`，舊檔留在下游不會壞 | S4 |
| TBD-3 | 發布前的下游試用 | 已解決：2026-11-17 使用者選「試用後再發布」；視為改變 agent 行為，先在一個下游專案實際跑 `--update` 並在一個實際 issue 使用，新建常青文件沒有觸發時照實記為未觸發 | 發布 |
| TBD-4 | [review-ee77c12](review-ee77c12.md) PASS，SHOULD FIX 2 項要不要在分支上修：CHANGELOG 4.13.0「下游更新」第二點的「換回上一版 kit 的原文」只在基線剛好是 v4.12.0 時可行，應改為換成本版原文；docs/usage.md 第 13 行的「範本」指的是 `docs/_templates/`，已不正確。修正會讓 PASS 失效、需要重審 | 已解決：2026-11-17 使用者選「兩項都修並差異覆審」；CHANGELOG 改為換成本版 kit 的原文，usage.md 刪掉「範本」 | SCN-005、發布 |

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-17 | 建立 GitHub #8 與本 issue；使用者逐題確認範圍，SCN-001～005 核准 | 使用者／Claude Code |
| 2026-11-17 | 使用者逐題確認 TBD-1～3：SCN-006 核准、版本 v4.13.0、發布前下游試用；規劃文件直接提交到 main（`c0c7e9f`） | 使用者／Claude Code |
| 2026-11-17 | S1～S4 完成，待獨立審查 | Claude Code |
| 2026-11-17 | 獨立審查 [review-ee77c12](review-ee77c12.md) PASS，沒有 MUST FIX；SHOULD FIX 2 項待使用者決定（TBD-4） | Claude Code |
| 2026-11-17 | 使用者決定 SHOULD FIX 兩項都修並差異覆審（TBD-4），PASS 失效 | 使用者／Claude Code |
| 2026-11-17 | 差異覆審 [review-151871c](review-151871c.md) PASS，沒有 MUST FIX、SHOULD FIX 與 NICE TO HAVE；下一步依 TBD-3 下游試用 | Claude Code |

---
**建立日期**: 2026-11-17  
**分級**: Medium — 部署腳本、測試、範本搬移與兩份規範多檔修改，邏輯直接，不需 Phase／Task 拆解  
**風險**: Low\
**狀態**: 審查通過，待下游試用
