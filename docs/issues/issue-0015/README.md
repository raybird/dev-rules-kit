# Issue 15 - 下游試用候選版的方式

## 文件清單
- [implementation-plan.md](./implementation-plan.md)

## 概述

來源：[GitHub #15](https://github.com/raybird/dev-rules-kit/issues/15)，由 #11 待確認事項 TBD-7 另開。#11 發布前在兩個下游專案的實際 issue 試用候選版（2026-11-20～23，結果見 [issue-0011 的 S8 證據](../issue-0011/evidence/s8-downstream.md)），試用方式本身出了三個問題：

1. **候選版 docs 會隨交付分支帶進主幹**：verify-artifact 從被審查提交讀流程契約，所以下游的候選版 docs 必須提交在交付分支上。一個下游專案在合併前 revert，revert 後 HEAD 回到舊契約，下一輪只能完整審查；另一個專案（squash 合併）接受候選版 docs 併進主幹。根目錄 AGENTS.md 只寫「以隔離設定載入未發布的版本」，沒寫 docs 怎麼放。
2. **verify-artifact 的用法錯誤也回 INVALID**：`--issue` 寫成編號、artifact 路徑與被審查 SHA 不符、SHA 不存在，都和「需重新審查」一樣回 exit 1 與 `INVALID：`，看起來像有效性判定失敗。
3. **試用 session 的設定只存在維護者本機**：設定目錄放在 /tmp 時，重開機後同一個 issue 改由全域技能接手且沒有提示；只裝 kit 技能時缺少全域指示、記憶、其他技能與 MCP；`CLAUDE_CONFIG_DIR` 不同的 session 不在 session 清單，只能用檔案回報。修正後的腳本在 `~/.cache`，寫死了 kit 路徑與 #11 的檢查字串。

另外，根目錄 AGENTS.md 要求試用結果「記在該 kit issue 的 `## 現況`」，但 `## 現況` 只能有 `**現行 review**` 與外部狀態表；#11 照這句寫被 verify-artifact 判需重審，最後改記在 evidence 檔。

收錄依據（AGENTS.md「範圍」）：三個問題都在 #11 的下游試用實際發生，最後一點是 kit 規則互相矛盾；試用是維護者的流程，下游 project.md 解決不了。本 issue 定案的做法用於接下來 #12 的下游試用。

## 現況

**現行 review**: review-fbaac77.md

## 快速導覽

### 當前流程

維護者自己準備隔離設定、轉告下游 session 怎麼更新 docs；docs 放法到合併前才由下游審查提出；verify-artifact 參數打錯時回 INVALID，agent 可能誤以為 PASS 失效；試用結果記在 `## 現況` 會讓 PASS 失效。

### 重構後流程

維護者以 `scripts/trial-session.sh <候選版 SHA>` 在下游 worktree 開試用 session，技能固定取自該 SHA；試用開始時先請下游使用者選 docs 放法（隨交付分支合併，或合併前 revert），各附代價；結果記在 kit issue 的 evidence 檔。verify-artifact 的用法錯誤回 exit 2 與 `用法錯誤：`。

## 關鍵差異

| 項目 | 變更前 | 變更後 |
|------|--------|--------|
| 下游候選版 docs | 沒有規定，合併前才發現問題 | 試用開始時由下游使用者在兩種做法中選一種，代價寫在維護文件 |
| 試用結果 | 規定記在 `## 現況`（與格式規定矛盾） | 記在該 kit issue 的 evidence 檔 |
| verify-artifact 參數錯誤 | exit 1、`INVALID：` | exit 2、`用法錯誤：`，並說明這不是有效性判定 |
| 試用 session | 本機腳本，寫死路徑與版本檢查 | `scripts/trial-session.sh`，技能取自指定 SHA，設定目錄在 `~/.cache` |

## 涉及檔案

### 維護文件

- `AGENTS.md` - 試用那一段：結果改記在 evidence 檔，指向 workflow-regression 的下游試用一節
- `docs/workflow-regression.md` - 新增「下游試用」一節：開 session、docs 放法的選擇與代價、回報方式、結果紀錄

### 腳本

- `scripts/trial-session.sh` - 新增：以指定 SHA 的 kit 技能開 Claude Code 試用 session
- `scripts/test-install.py` - 試用腳本的測試（暫存 HOME 與替身 `claude`）
- `skills/review/scripts/verify-artifact.py` - 用法錯誤改 exit 2 與 `用法錯誤：`
- `scripts/test-evidence.py` - 用法錯誤與有效性失敗的結束碼測試

### 技能與紀錄

- `skills/review/SKILL.md` - verify-artifact 那一句補上 exit 2 的意思
- 技能歷代雜湊（`scripts/build-skill-hashes.py` 產生的清單）、`CHANGELOG.md`、`docs/rule-verification-status.md`

## Gherkin 驗收劇本

```gherkin
Feature: 下游試用候選版有固定、可重現的做法

  @SCN-001
  Scenario: verify-artifact 的用法錯誤與有效性判定分開
    Given 一個有本機審查報告的 issue
    When 執行 verify-artifact 時參數有誤：--issue 不是 docs/issues/issue-{ID} 形式、--artifact 的檔名與 --reviewed 不符、--reviewed 或 --head 不是存在的提交、--artifact 與 --issue 指向不同 issue，或兩者都沒給
    Then exit code 是 2，stderr 以「用法錯誤：」開頭，並說明修正參數後重跑、這不是有效性判定
    And 不輸出「INVALID」

  @SCN-002
  Scenario: 有效性判定的結果不變
    Given 參數正確
    When 被審查提交之後有不屬記帳區段的變更、歷史被改寫，或其他現有的無效情況
    Then 照舊 exit 1、stderr 以「INVALID：」開頭
    And 只動記帳區段時照舊 exit 0、輸出 OK
    And test-evidence 既有的判定測試全部通過

  @SCN-003
  Scenario: 以指定 SHA 開試用 session
    Given 維護者在下游 issue 的 worktree，傳入 kit 候選版的 SHA
    When 執行 scripts/trial-session.sh
    Then 設定目錄建立在 ~/.cache/dev-rules-kit/ 底下，kit 技能的內容與該 SHA 的 skills/ 相同，與 kit 工作區狀態無關
    And 其他全域技能、全域指示、settings、記憶（projects）與 MCP 設定照常可用，原本的 ~/.claude 與 ~/.claude.json 沒有被修改
    And 啟動前印出候選版 SHA 與設定目錄
    And SHA 不存在時不建立設定目錄、exit 非 0

  @SCN-004
  Scenario: 試用開始時決定下游 docs 的放法
    Given 維護者照 workflow-regression「下游試用」開始一次試用
    When 下游 session 要把 docs 更新到候選版
    Then 文件要求先請下游使用者在兩種做法中選一種，並列出代價：隨交付分支合併（未發版的流程契約進主幹、其他 issue 同步主幹時跟著換版；kit 發版內容不同時在主幹以 init-project.py --update 同步一次，不改寫歷史），或合併前 revert（revert 後的 HEAD 是舊流程契約，下一輪審查依舊契約判定，可能只能完整審查）
    And 更新 docs 的指令寫明 init-project.py --update 的專案路徑參數
    And 選擇與理由記在該 kit issue 的 evidence 檔

  @SCN-005
  Scenario: 試用結果記在 evidence 檔
    Given 下游試用結束
    When 維護者記錄結果
    Then 根目錄 AGENTS.md 與 workflow-regression 都寫明結果記在該 kit issue 的 evidence 檔，由實作步驟與 rule-verification-status 引用
    And 兩處都沒有要求把結果寫進 `## 現況`
    And 試用 session 不在 session 清單時，文件寫明改用檔案回報
```

## Gherkin 核准紀錄
- **核准 commit**: 70f176a
- **核准來源**: 2026-11-24 使用者選「核准 SCN-001～005（建議）」；範圍與做法依同日逐題確認的選擇：docs 放法選「試用開始時問下游使用者，列兩種做法與代價（建議）」；用法錯誤選「exit 2，前綴「用法錯誤：」（建議）」；試用設定選「腳本進 scripts/，維護文件寫做法（建議）」；AGENTS.md 的矛盾與試用選「改成記在 evidence 檔；本 issue 不另試用（建議）」

全部 Scenario 於 2026-11-24 核准。

## 風險與首要驗證

- **最大風險**：trial-session.sh 為了只覆蓋 kit 技能而暫時改 HOME 執行 install.sh；路徑寫錯時會把候選版技能裝進維護者真正的 `~/.claude`，或改到 `~/.claude.json`，之後所有 session 都在跑未發版的技能且沒有提示
- **風險等級與理由**：Medium。只影響維護者本機，可以重裝復原，但發生時不會報錯，而且會污染之後所有下游 session 的試用與一般工作
- **首要驗證**：先寫腳本與測試：以暫存目錄當 HOME、PATH 放替身 `claude`，比對執行前後 HOME 底下 `.claude/` 與 `.claude.json` 的雜湊不變，設定目錄裡的 kit 技能與 `git archive <SHA>` 相同
- **選擇理由**：直接量測最嚴重的失敗（改到真正的設定）；替身 `claude` 讓測試不必真的啟動 session
- **完成證據**：test-install 的試用腳本測試通過；另以 kit 工作區有未提交修改的狀態執行一次，設定目錄的技能仍與指定 SHA 相同

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | 本 issue 是否需要下游試用 | 已解決：2026-11-24 使用者選「改成記在 evidence 檔；本 issue 不另試用（建議）」；verify-artifact 只區分用法錯誤、判定邏輯不變，以 test-evidence 驗證；試用腳本與文件在 #12 的下游試用實際使用，結果記在 #12 | 決定發版前是否需要下游試用；SCN-001～005 |

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-24 | 建立；使用者決定 docs 放法、用法錯誤、試用設定與試用需求 | 使用者／Claude Code |
| 2026-11-24 | 使用者核准 SCN-001～005 | 使用者 |
| 2026-11-24 | 審查 review-fbaac77：RETURN，MUST FIX 2 項（試用腳本遇到 symlink 會寫到原處、相對連結的技能斷掉） | Claude Code |

---
**建立日期**: 2026-11-24  
**分級**: Medium — 維護文件、一支新腳本與 verify-artifact 的錯誤分類，不改 docs/AGENTS.md 與流程契約；不需 Phase／Task 拆解  
**風險**: Medium\
**狀態**: 修正中
